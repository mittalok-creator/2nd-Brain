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
  schema     entity field contracts hold, taxonomy references resolve, and every
             entity is owned by exactly one page

Usage:
    python3 scripts/validate_repository.py [--only CHECK] [--quiet]

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
    "core/schema/_catalogue.yaml",
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
SNAKE_CASE = re.compile(r"^[a-z][a-z0-9_]*$")

# The complete set of abstract field types (core/README.md). A provider adapter maps
# each to its vendor equivalent; nothing outside this list may be used.
ABSTRACT_TYPES = {
    "text",
    "rich_text",
    "number",
    "select",
    "multi_select",
    "status",
    "date",
    "checkbox",
    "url",
    "email",
    "phone",
    "relation",
    "rollup",
    "formula",
    "person",
    "file",
    "created_time",
    "last_edited_time",
}

# Relations and rollups are declared in core/relations/, never in an entity schema,
# so that cardinality is stated once rather than twice. See core/schema/README.md.
TYPES_FORBIDDEN_IN_SCHEMA = {"relation", "rollup"}

ENUM_TYPES = {"select", "multi_select", "status"}
NUMBER_FORMATS = {"integer", "decimal", "currency", "percent"}
VALIDATION_KEYS = {"min", "max", "pattern", "max_length"}


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


def load_yaml(report: Report, path: Path):
    """Parse a YAML file, reporting rather than raising on malformed input.

    The `yaml` check reports syntax errors in detail; downstream checks only need to
    skip the file without taking the whole run down with a traceback.
    """
    import yaml  # local import: callers have already confirmed it is available

    try:
        return yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except yaml.YAMLError as exc:
        report.error(f"{rel(path)} could not be parsed — {str(exc).splitlines()[0]}")
        return None


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

    document = load_yaml(report, hierarchy_path)
    if document is None:
        return
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
        blueprint = load_yaml(report, path)
        if blueprint is None:
            continue
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


def _load_taxonomies(report: Report, yaml) -> dict[str, dict]:
    """Index core/taxonomy/ by id so schema references can be resolved."""
    taxonomies: dict[str, dict] = {}
    for path in sorted((REPO_ROOT / "core/taxonomy").glob("*.yaml")):
        if path.name.startswith("_"):
            continue
        document = load_yaml(report, path)
        if document is None:
            continue
        taxonomy_id = document.get("id")
        if not taxonomy_id:
            report.error(f"schema: {rel(path)} has no id")
            continue
        taxonomies[taxonomy_id] = document
    return taxonomies


def _taxonomy_values(taxonomy: dict, set_name: str | None) -> set[str] | None:
    """Allowed value ids for a taxonomy, or for one named set within it."""
    if set_name is not None:
        sets = taxonomy.get("sets") or {}
        if set_name not in sets:
            return None
        entries = (sets[set_name] or {}).get("values") or []
    else:
        entries = taxonomy.get("values") or []
    return {entry["id"] for entry in entries if isinstance(entry, dict) and "id" in entry}


def _check_field(report: Report, where: str, field: dict, taxonomies: dict) -> None:
    field_id = field.get("id")
    if not field_id:
        report.error(f"schema: {where} has a field with no id")
        return
    label = f"{where}.{field_id}"

    if not SNAKE_CASE.match(str(field_id)):
        report.error(f"schema: {label} field id is not snake_case")
    if "name" not in field:
        report.error(f"schema: {label} has no display name")

    field_type = field.get("type")
    if field_type not in ABSTRACT_TYPES:
        report.error(
            f"schema: {label} type '{field_type}' is not an abstract field type "
            f"(see core/README.md)"
        )
        return
    if field_type in TYPES_FORBIDDEN_IN_SCHEMA:
        report.error(
            f"schema: {label} declares type '{field_type}' — relations and rollups belong in "
            f"core/relations/, not in an entity schema"
        )
        return

    # Enum fields draw from a shared taxonomy or an explicit local option list.
    allowed: set[str] | None = None
    if field_type in ENUM_TYPES:
        taxonomy_id = field.get("taxonomy")
        if taxonomy_id:
            taxonomy = taxonomies.get(taxonomy_id)
            if taxonomy is None:
                report.error(f"schema: {label} references unknown taxonomy '{taxonomy_id}'")
            else:
                set_name = field.get("set")
                if field_type == "status" and not set_name:
                    report.error(f"schema: {label} is a status field but names no taxonomy set")
                allowed = _taxonomy_values(taxonomy, set_name)
                if allowed is None:
                    report.error(
                        f"schema: {label} references set '{set_name}', absent from "
                        f"taxonomy '{taxonomy_id}'"
                    )
        elif "options" in field:
            options = field.get("options") or []
            allowed = set(options)
            for option in options:
                if not SNAKE_CASE.match(str(option)):
                    report.error(f"schema: {label} option '{option}' is not snake_case")
        else:
            report.error(
                f"schema: {label} is a {field_type} field with neither 'taxonomy' nor 'options'"
            )
    elif "options" in field:
        report.error(f"schema: {label} declares options but is type '{field_type}'")

    default = field.get("default")
    if default is not None and allowed and field_type in ENUM_TYPES:
        values = default if isinstance(default, list) else [default]
        for value in values:
            if value not in allowed:
                report.error(f"schema: {label} default '{value}' is not an allowed value")

    if field_type == "number":
        number_format = field.get("format")
        if number_format is not None and number_format not in NUMBER_FORMATS:
            report.error(
                f"schema: {label} format '{number_format}' must be one of "
                f"{sorted(NUMBER_FORMATS)}"
            )
    elif "format" in field:
        report.error(f"schema: {label} declares format but is type '{field_type}'")

    for key in field.get("validation") or {}:
        if key not in VALIDATION_KEYS:
            report.error(
                f"schema: {label} validation key '{key}' must be one of {sorted(VALIDATION_KEYS)}"
            )


def check_schema(report: Report) -> None:
    """Validate entity field contracts, taxonomy references, and entity ownership."""
    report.info("→ schema")

    try:
        import yaml  # type: ignore
    except ImportError:
        report.warn("schema: PyYAML not installed — check skipped")
        return

    catalogue_path = REPO_ROOT / "core/schema/_catalogue.yaml"
    if not catalogue_path.is_file():
        report.error("schema: core/schema/_catalogue.yaml is missing")
        return

    catalogue = load_yaml(report, catalogue_path)
    if catalogue is None:
        return
    listed = {
        entry["id"]: entry
        for entry in (catalogue.get("entities") or [])
        if isinstance(entry, dict) and "id" in entry
    }
    rejected = {
        entry["id"]
        for entry in (catalogue.get("rejected") or [])
        if isinstance(entry, dict) and "id" in entry
    }

    declared_count = catalogue.get("entity_count")
    if declared_count is not None and declared_count != len(listed):
        report.error(
            f"schema: _catalogue.yaml declares entity_count {declared_count} but lists "
            f"{len(listed)} entities"
        )

    taxonomies = _load_taxonomies(report, yaml)

    # ── Entity schemas ─────────────────────────────────────────────────────────
    defined: dict[str, str] = {}
    for path in sorted((REPO_ROOT / "core/schema").glob("*.yaml")):
        if path.name.startswith("_"):
            continue
        document = load_yaml(report, path)
        if document is None:
            continue
        entity_id = document.get("id")
        if not entity_id:
            report.error(f"schema: {rel(path)} has no id")
            continue

        if not SNAKE_CASE.match(str(entity_id)):
            report.error(f"schema: {rel(path)} entity id '{entity_id}' is not snake_case")
        if entity_id in defined:
            report.error(f"schema: entity id '{entity_id}' defined twice")
        defined[entity_id] = path.name

        if entity_id not in listed:
            report.error(f"schema: '{entity_id}' is not listed in _catalogue.yaml")
        elif listed[entity_id].get("file") != path.name:
            report.error(
                f"schema: _catalogue.yaml points '{entity_id}' at "
                f"'{listed[entity_id].get('file')}', but it is defined in {path.name}"
            )

        fields = document.get("fields")
        if not fields:
            report.error(f"schema: {rel(path)} declares no fields")
            continue

        seen: set[str] = set()
        for field in fields:
            if not isinstance(field, dict):
                report.error(f"schema: {rel(path)} has a field that is not a mapping")
                continue
            field_id = field.get("id")
            if field_id in seen:
                report.error(f"schema: {entity_id}.{field_id} is declared twice")
            seen.add(field_id)
            _check_field(report, entity_id, field, taxonomies)

        identity = document.get("identity") or {}
        primary = identity.get("primary")
        if not primary:
            report.error(f"schema: {rel(path)} declares no identity.primary")
        elif primary not in seen:
            report.error(f"schema: {entity_id} identity.primary '{primary}' is not a field")
        for source in identity.get("slug_from") or []:
            if source not in seen:
                report.error(f"schema: {entity_id} identity.slug_from '{source}' is not a field")

        for rule in (document.get("defaults") or {}).get("sort") or []:
            if isinstance(rule, dict) and rule.get("field") not in seen:
                report.error(
                    f"schema: {entity_id} default sort field '{rule.get('field')}' is not a field"
                )

    for entity_id, entry in listed.items():
        if entity_id not in defined:
            report.error(
                f"schema: _catalogue.yaml lists '{entity_id}' ({entry.get('file')}), "
                f"but no schema defines it"
            )
        if entity_id in rejected:
            report.error(f"schema: '{entity_id}' is both listed and rejected in _catalogue.yaml")

    # ── Ownership: every entity owned by exactly one page ──────────────────────
    hierarchy_path = REPO_ROOT / "workspace/pages/_hierarchy.yaml"
    if not hierarchy_path.is_file():
        return

    hierarchy = load_yaml(report, hierarchy_path)
    if hierarchy is None:
        return
    owners: dict[str, list[str]] = {}

    for page in hierarchy.get("pages") or []:
        entity_id = page.get("entity")
        if entity_id:
            owners.setdefault(entity_id, []).append(f"{page['id']} (generated)")
            if entity_id not in defined:
                report.error(
                    f"schema: generated page '{page['id']}' names entity '{entity_id}', "
                    f"which no schema defines"
                )

    for path in sorted((REPO_ROOT / "workspace/pages").glob("*.yaml")):
        if path.name.startswith("_"):
            continue
        document = load_yaml(report, path)
        if document is None:
            continue
        page_id = document.get("id", path.name)
        for entity_id in document.get("owns_entities") or []:
            owners.setdefault(entity_id, []).append(str(page_id))
            if entity_id not in defined:
                report.error(
                    f"schema: page '{page_id}' claims to own '{entity_id}', "
                    f"which no schema defines"
                )

    for entity_id in defined:
        claims = owners.get(entity_id, [])
        if not claims:
            report.error(
                f"schema: entity '{entity_id}' is owned by no page — add it to a composed "
                f"page's owns_entities, or to a generated page's entity"
            )
            continue
        if len(claims) > 1:
            report.error(f"schema: entity '{entity_id}' is owned by {len(claims)} pages {claims}")
            continue

        # The catalogue's `owned_by` is documentation, so it must agree with reality.
        actual = claims[0].split(" ")[0]
        recorded = (listed.get(entity_id) or {}).get("owned_by")
        if recorded and recorded != actual:
            report.error(
                f"schema: _catalogue.yaml records '{entity_id}' as owned by '{recorded}', "
                f"but page '{actual}' owns it"
            )


# ── Entrypoint ───────────────────────────────────────────────────────────────


CHECKS = {
    "structure": check_structure,
    "yaml": check_yaml,
    "links": check_links,
    "hierarchy": check_hierarchy,
    "schema": check_schema,
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate the 2nd Brain specification.")
    parser.add_argument("--only", choices=sorted(CHECKS), help="run a single check")
    parser.add_argument("--quiet", action="store_true", help="suppress progress output")
    args = parser.parse_args()

    report = Report(quiet=args.quiet)
    selected = (
        [args.only] if args.only else ["structure", "yaml", "links", "hierarchy", "schema"]
    )

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
