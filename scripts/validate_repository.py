#!/usr/bin/env python3
"""Validate the 2nd Brain repository specification.

Three independent checks, all offline and deterministic:

  structure  required files and directories exist, and every top-level
             directory documents itself with a README.md
  yaml       every .yaml/.yml file parses, and every spec file under core/,
             workspace/, agents/ and automation/ carries the header contract
  links      every relative Markdown link resolves to a real path

Usage:
    python3 scripts/validate_repository.py [--only structure|yaml|links] [--quiet]

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


# ── Entrypoint ───────────────────────────────────────────────────────────────


CHECKS = {"structure": check_structure, "yaml": check_yaml, "links": check_links}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the 2nd Brain specification.")
    parser.add_argument("--only", choices=sorted(CHECKS), help="run a single check")
    parser.add_argument("--quiet", action="store_true", help="suppress progress output")
    args = parser.parse_args()

    report = Report(quiet=args.quiet)
    selected = [args.only] if args.only else ["structure", "yaml", "links"]

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
