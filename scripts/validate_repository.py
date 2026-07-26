#!/usr/bin/env python3
"""Validate the 2nd Brain repository specification.

Three independent checks, all offline and deterministic:

  structure  required files and directories exist, and every top-level
             directory documents itself with a README.md
  yaml       every .yaml/.yml file parses, and every spec file under core/,
             workspace/, agents/ and automation/ carries the header contract
  links      every relative Markdown link resolves to a real path
  hierarchy  the workspace page tree satisfies its navigation constraints, and
             composed pages have blueprints while generated pages do not

Usage:
    python3 scripts/validate_repository.py [--only structure|yaml|links|hierarchy] [--quiet]

Exit code 0 when clean, 1 when any check fails.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# ── Contract ─────────────────────────────────────────────────────────────────

REQUIRED_FILES = [
    "workspace/pages/_hierarchy.yaml",
    "workspace/capture-routing.yaml",
    "README.md",
    "LICENSE",
    "CHANGELOG.md",
    "ROADMAP.md",
    "CONTRIBUTING.md",
    "CODE_OF_CONDUCT.md",
    "SECURITY.md",
    "Makefile",
    ".gitignore",
    ".editorconfig",
    ".env.example",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/labels.yml",
    ".github/dependabot.yml",
    "docs/README.md",
    "docs/adr/_template.md",
]

REQUIRED_DIRS = [
    "core/schema",
    "core/relations",
    "core/taxonomy",
    "core/design",
    "workspace/pages",
    "workspace/dashboards",
    "workspace/views",
    "workspace/templates",
    "agents",
    "prompts",
    "automation",
    "scripts",
    "config",
    "docs",
    "assets",
    "tests",
]

# Top-level directories that must explain themselves.
SELF_DOCUMENTING_DIRS = [
    "core",
    "workspace",
    "agents",
    "prompts",
    "automation",
    "scripts",
    "config",
    "docs",
    "assets",
    "tests",
]

# Directories whose YAML files must carry the spec header (see CONTRIBUTING.md).
SPEC_ROOTS = ["core", "workspace", "agents", "automation"]
SPEC_HEADER_FIELDS = ["id", "name", "version", "status", "description"]
VALID_STATUSES = {"draft", "active", "deprecated"}

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build"}

# Files exempt from the spec-header contract (indexes, registries, workflow exports).
HEADER_EXEMPT = re.compile(r"(^|/)(_|\.)|/n8n/|/actions/")

LINK_PATTERN = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")


# ── Reporting ────────────────────────────────────────────────────────────────


class Report:
    def __init__(self, quiet: bool = False) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []
        self.quiet = quiet

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def info(self, message: str) -> None:
        if not self.quiet:
            print(message)


# ── Helpers ──────────────────────────────────────────────────────────────────


def walk(root: Path):
    """Yield files under root, skipping ignored directories."""
    for path in sorted(root.rglob("*")):
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.is_file():
            yield path


def rel(path: Path) -> str:
    return path.relative_to(REPO_ROOT).as_posix()


# ── Checks ───────────────────────────────────────────────────────────────────


def check_structure(report: Report) -> None:
    report.info("→ structure")

    for name in REQUIRED_FILES:
        if not (REPO_ROOT / name).is_file():
            report.error(f"structure: missing required file '{name}'")

    for name in REQUIRED_DIRS:
        if not (REPO_ROOT / name).is_dir():
            report.error(f"structure: missing required directory '{name}/'")

    for name in SELF_DOCUMENTING_DIRS:
        directory = REPO_ROOT / name
        if directory.is_dir() and not (directory / "README.md").is_file():
            report.error(f"structure: '{name}/' has no README.md describing its purpose")

    issue_templates = REPO_ROOT / ".github/ISSUE_TEMPLATE"
    if not issue_templates.is_dir() or not any(issue_templates.glob("*.yml")):
        report.error("structure: .github/ISSUE_TEMPLATE contains no issue forms")

    workflows = REPO_ROOT / ".github/workflows"
    if not workflows.is_dir() or not any(workflows.glob("*.yml")):
        report.error("structure: .github/workflows contains no workflows")

    adrs = sorted((REPO_ROOT / "docs/adr").glob("[0-9][0-9][0-9][0-9]-*.md"))
    if not adrs:
        report.error("structure: docs/adr contains no numbered decision records")
    seen: dict[str, str] = {}
    for adr in adrs:
        number = adr.name[:4]
        if number in seen:
            report.error(f"structure: duplicate ADR number {number} ({seen[number]}, {adr.name})")
        seen[number] = adr.name


def check_yaml(report: Report) -> None:
    report.info("→ yaml")

    try:
        import yaml  # type: ignore
    except ImportError:
        report.warn("yaml: PyYAML not installed — syntax check skipped (pip install pyyaml)")
        return

    for path in walk(REPO_ROOT):
        if path.suffix not in (".yaml", ".yml"):
            continue

        try:
            documents = list(yaml.safe_load_all(path.read_text(encoding="utf-8")))
        except yaml.YAMLError as exc:
            report.error(f"yaml: {rel(path)} failed to parse — {str(exc).splitlines()[0]}")
            continue

        if not documents or documents[0] is None:
            report.warn(f"yaml: {rel(path)} is empty")
            continue

        relative = rel(path)
        if relative.split("/")[0] not in SPEC_ROOTS or HEADER_EXEMPT.search("/" + relative):
            continue

        document = documents[0]
        if not isinstance(document, dict):
            report.error(f"yaml: {relative} must be a mapping at the top level")
            continue

        for field in SPEC_HEADER_FIELDS:
            if field not in document:
                report.error(f"yaml: {relative} spec header is missing '{field}'")

        version = document.get("version")
        if version is not None and not SEMVER.match(str(version)):
            report.error(f"yaml: {relative} version '{version}' is not semantic (x.y.z)")

        status = document.get("status")
        if status is not None and status not in VALID_STATUSES:
            report.error(
                f"yaml: {relative} status '{status}' must be one of {sorted(VALID_STATUSES)}"
            )


def check_links(report: Report) -> None:
    report.info("→ links")

    for path in walk(REPO_ROOT):
        if path.suffix != ".md":
            continue

        text = path.read_text(encoding="utf-8")
        for match in LINK_PATTERN.finditer(text):
            target = match.group(1).strip()

            if target.startswith(("http://", "https://", "mailto:", "#", "<")):
                continue
            if target.startswith("{{") or "${" in target:
                continue

            target = target.split("#", 1)[0]
            if not target:
                continue

            resolved = (path.parent / target).resolve()
            if not resolved.exists():
                line = text[: match.start()].count("\n") + 1
                report.error(f"links: {rel(path)}:{line} broken link → '{match.group(1)}'")


def check_hierarchy(report: Report) -> None:
    """Validate the workspace page tree against the constraints in ADR-0005."""
    report.info("→ hierarchy")

    try:
        import yaml  # type: ignore
    except ImportError:
        report.warn("hierarchy: PyYAML not installed — check skipped")
        return

    hierarchy_path = REPO_ROOT / "workspace/pages/_hierarchy.yaml"
    if not hierarchy_path.is_file():
        report.error("hierarchy: workspace/pages/_hierarchy.yaml is missing")
        return

    document = yaml.safe_load(hierarchy_path.read_text(encoding="utf-8")) or {}
    pages = document.get("pages") or []
    constraints = document.get("constraints") or {}
    max_depth = constraints.get("max_depth", 3)

    if not pages:
        report.error("hierarchy: no pages declared")
        return

    by_id: dict[str, dict] = {}
    for page in pages:
        page_id = page.get("id")
        if not page_id:
            report.error("hierarchy: a page entry has no id")
            continue
        if page_id in by_id:
            report.error(f"hierarchy: duplicate page id '{page_id}'")
        by_id[page_id] = page

    # Exactly one root.
    roots = [p for p in by_id.values() if p.get("parent") in (None, "null")]
    if len(roots) != 1:
        names = sorted(p["id"] for p in roots)
        report.error(f"hierarchy: expected exactly one root page, found {len(roots)} {names}")

    # Parents resolve, and depth is bounded.
    for page in by_id.values():
        parent = page.get("parent")
        if parent and parent not in by_id:
            report.error(f"hierarchy: '{page['id']}' has unknown parent '{parent}'")

        depth, cursor, seen = 1, page, {page["id"]}
        while cursor.get("parent"):
            parent_id = cursor["parent"]
            if parent_id in seen or parent_id not in by_id:
                report.error(f"hierarchy: cycle or broken chain above '{page['id']}'")
                break
            seen.add(parent_id)
            cursor = by_id[parent_id]
            depth += 1
        else:
            if depth > max_depth:
                report.error(
                    f"hierarchy: '{page['id']}' is at depth {depth}, exceeding max {max_depth} "
                    f"({depth - 1} clicks from root)"
                )

    # Sibling order is explicit and unique.
    siblings: dict[str, dict[int, str]] = {}
    for page in by_id.values():
        parent = page.get("parent") or "__root__"
        order = page.get("order")
        if order is None:
            report.error(f"hierarchy: '{page['id']}' has no explicit order")
            continue
        taken = siblings.setdefault(parent, {})
        if order in taken:
            report.error(
                f"hierarchy: '{page['id']}' and '{taken[order]}' share order {order} "
                f"under '{parent}'"
            )
        else:
            taken[order] = page["id"]

    # Blueprints: composed pages have one, generated pages do not.
    blueprints: dict[str, str] = {}
    for path in sorted((REPO_ROOT / "workspace/pages").glob("*.yaml")):
        if path.name.startswith("_"):
            continue
        blueprint = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        blueprint_id = blueprint.get("id")
        if not blueprint_id:
            report.error(f"hierarchy: {rel(path)} has no id")
            continue
        if blueprint_id in blueprints:
            report.error(f"hierarchy: page id '{blueprint_id}' declared by two blueprints")
        blueprints[blueprint_id] = path.name

        if blueprint_id not in by_id:
            report.error(
                f"hierarchy: {rel(path)} declares '{blueprint_id}', which is absent from "
                f"_hierarchy.yaml"
            )
            continue

        page = by_id[blueprint_id]
        for key in ("class", "question", "owns_entities"):
            if key not in blueprint:
                report.error(f"hierarchy: {rel(path)} is missing required key '{key}'")
        for key in ("class", "parent", "order"):
            if key in blueprint and blueprint.get(key) != page.get(key):
                report.error(
                    f"hierarchy: {rel(path)} {key}='{blueprint.get(key)}' contradicts "
                    f"_hierarchy.yaml '{page.get(key)}'"
                )

    for page in by_id.values():
        kind = page.get("kind")
        if kind == "composed" and page["id"] not in blueprints:
            report.error(f"hierarchy: composed page '{page['id']}' has no blueprint file")
        if kind == "generated":
            if page["id"] in blueprints:
                report.error(
                    f"hierarchy: generated page '{page['id']}' must not have a blueprint "
                    f"({blueprints[page['id']]})"
                )
            if not page.get("entity"):
                report.error(f"hierarchy: generated page '{page['id']}' declares no entity")
        if kind not in ("composed", "generated"):
            report.error(f"hierarchy: '{page['id']}' has invalid kind '{kind}'")


# ── Entrypoint ───────────────────────────────────────────────────────────────


CHECKS = {
    "structure": check_structure,
    "yaml": check_yaml,
    "links": check_links,
    "hierarchy": check_hierarchy,
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the 2nd Brain specification.")
    parser.add_argument("--only", choices=sorted(CHECKS), help="run a single check")
    parser.add_argument("--quiet", action="store_true", help="suppress progress output")
    args = parser.parse_args()

    report = Report(quiet=args.quiet)
    selected = [args.only] if args.only else ["structure", "yaml", "links", "hierarchy"]

    report.info("2nd Brain — specification validation")
    for name in selected:
        CHECKS[name](report)

    for warning in report.warnings:
        print(f"  warn  {warning}")
    for error in report.errors:
        print(f"  FAIL  {error}")

    if report.errors:
        print(f"\n✗ {len(report.errors)} error(s), {len(report.warnings)} warning(s)")
        return 1

    print(f"\n✓ specification valid ({len(report.warnings)} warning(s))")
    return 0


if __name__ == "__main__":
    sys.exit(main())
