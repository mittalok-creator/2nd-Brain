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
- Phase 2 — Notion workspace blueprint (page hierarchy, navigation model)

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

[Unreleased]: https://github.com/mittalok-creator/2nd-Brain/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/mittalok-creator/2nd-Brain/releases/tag/v0.1.0
