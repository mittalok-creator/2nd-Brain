# Changelog

All notable changes to **2nd Brain** are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

Versioning is applied to the **specification**, not to any single tool:

- **MAJOR** — a breaking change to the data model or page hierarchy that requires migration.
- **MINOR** — new databases, agents, dashboards, or automations added backwards-compatibly.
- **PATCH** — documentation, copy, tuning, and fixes with no structural impact.

---

## [Unreleased]

### Planned
- Phase 3 — Databases (entity catalogue, field schemas, taxonomies)

---

## [0.2.0] — 2026-07-26

**Phase 2 — Workspace Architecture**

### Added
- `workspace/pages/_hierarchy.yaml` — the authoritative page tree: 15 top-level pages,
  one root, maximum depth 3, every surface within 2 clicks of Home.
- Page classes (`root`, `rhythm`, `direction`, `domain`, `system`) grouping surfaces by the
  role they play rather than by life area.
- Sixteen composed page blueprints: Home, Inbox, Today, Planner, Reviews, Goals, Projects,
  Knowledge, Learning, Career, Finance, Health, Relationships, Command Center, Agents,
  System, Taxonomy.
- `workspace/capture-routing.yaml` — the capture model: 7 entry points, one inbox,
  16 ordered routing rules, and a boundary-enforced completeness gate.
- `docs/01-architecture/information-architecture.md` — page tree, navigation constraints,
  ownership model, and capture flow.
- ADR-0005 (workspace information architecture), ADR-0006 (single-inbox capture with
  deferred routing).
- Page contract keys: `class`, `question`, and `owns_entities` on every blueprint.
- `hierarchy` check in `scripts/validate_repository.py`, wired into CI and `make hierarchy`:
  enforces one root, depth ≤ 3, unique sibling order, composed-versus-generated correctness,
  and agreement between each blueprint and `_hierarchy.yaml`.

### Changed
- `workspace/pages/README.md` and `workspace/README.md` document the composed/generated
  distinction and the required blueprint keys.
- Architecture guide links the information architecture and notes that capture is deferred
  and agent-assisted.

### Decisions
- **Added three pages absent from the original plan.** `Inbox` (capture needs a destination
  requiring no decision), `Today` (execution is distinct from planning and review), and
  `System` (meta-content otherwise leaks into life-area pages). See ADR-0005.
- **Renamed `Family` to `Relationships`.** Family is a subset of the people who matter;
  friends, mentors, and professional contacts otherwise have no home. Family is retained as
  the most heavily weighted tag within the page.
- **Renamed `AI Command Center` to `Command Center`.** Everything on the page is AI-driven,
  so the qualifier adds length without information.
- **No `Tasks` page.** Tasks are always seen in the context that makes them meaningful —
  today's list, or the project they deliver. A global task list is a backlog.
- **Introduced composed versus generated pages.** A page whose content is entirely one
  entity's views is generated, not hand-maintained. Roughly half the workspace needs no
  blueprint, removing the main surface for drift.
- **Capture is separated from routing.** Classifying at capture time is what stops capture
  happening, and is often impossible at that moment. Required fields are enforced at the
  boundary out of the inbox instead — the only boundary-enforced constraint in the system.
  See ADR-0006.

### Notes
- Page blueprints contain forward references to views, dashboards, and templates that land
  in Phases 3 and 5. These are expected and are validated once the targets exist.

---

## [0.1.0] — 2026-07-26

**Phase 1 — Repository Architecture**

### Added
- Repository skeleton with a four-layer architecture: `core/` (specification),
  `workspace/` (surface), `agents/` + `prompts/` (intelligence), `automation/` (execution).
- Root project documents: `README.md`, `ROADMAP.md`, `CHANGELOG.md`, `CONTRIBUTING.md`,
  `CODE_OF_CONDUCT.md`, `SECURITY.md`, `LICENSE`.
- Documentation tree under `docs/` with numbered guide sections and an
  Architecture Decision Record (ADR) log.
- ADR-0001 (four-layer architecture), ADR-0002 (naming and versioning conventions),
  ADR-0003 (Notion as a reference implementation, not the source of truth),
  ADR-0004 (specification format: YAML).
- GitHub standards: issue forms, pull request template, label taxonomy, `CODEOWNERS`,
  Dependabot configuration, and a CI workflow that validates repository structure,
  YAML syntax, and internal documentation links.
- `scripts/validate_repository.py` — dependency-light specification validator.
- `Makefile` with `validate`, `lint`, and `tree` targets.
- Baseline configuration: `.gitignore`, `.gitattributes`, `.editorconfig`, `.env.example`.

### Decisions
- Renamed the proposed `/notion` directory to `workspace/`, and extracted the data model
  into `core/`, so the system is not structurally coupled to a single vendor. See ADR-0003.
- Merged the proposed root-level `/databases` and `/templates` directories into
  `core/schema/` and `workspace/templates/` respectively, to keep one concept in one place.
  See ADR-0001.

[Unreleased]: https://github.com/mittalok-creator/2nd-Brain/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/mittalok-creator/2nd-Brain/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/mittalok-creator/2nd-Brain/releases/tag/v0.1.0
