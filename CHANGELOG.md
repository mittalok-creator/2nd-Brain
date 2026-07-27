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

### Added
- **The workspace is fully deployed.** All 23 entities from the Phase 3 catalogue now exist as
  live Notion databases under the `🧠 2nd Brain` root page, with 15 two-way relations and 6
  filtered views. Ids recorded in `config/notion.yaml` (git-ignored); shape in
  `config/notion.example.yaml`.
- Illustrated Notion user guide in Hinglish — `docs/03-user-guide/2nd-Brain-Notion-Guide.pdf`,
  rendered from `notion-guide.html` by `make guide`.

### Changed
- `actions/checkout` bumped to v7 and `actions/setup-python` to v7 across both workflows
  (Dependabot #1).
- PyYAML floor raised to `>=6.0.3` (Dependabot #2).

### Fixed
- Removed the Discussions contact link from the issue-template config. Discussions is disabled
  on this repository, so the link was a 404. Ideas now go to a feature request labelled
  `discussion`.
- Corrected two stale descriptions of what `make validate` and CI cover in `CONTRIBUTING.md` —
  both predated the `hierarchy` and `schema` checks.
- Rewrote the compare links at the bottom of this file to point at commit SHAs. They
  previously referenced `v0.1.0`-`v0.3.0` tags that were never created, and returned 404. The
  tags still need creating from a machine with direct push access — this environment's git
  proxy refuses tag pushes.

### Planned
- Phase 4 — Relations (the relational graph, rollups, referential integrity)

---

## [0.3.0] — 2026-07-26

**Phase 3 — Databases**

### Added
- `core/schema/_catalogue.yaml` — the entity index: 23 entities with group, purpose, owning
  page, and defining file, plus a `rejected:` block recording every entity considered and not
  created, with the reason.
- Field-level schemas for all 23 entities: `goals`, `projects`, `tasks`, `habits`,
  `habit_logs`, `inbox`, `journal`, `reviews`, `decisions`, `meetings`, `knowledge`,
  `resources`, `reading`, `courses`, `skills`, `career_events`, `people`, `accounts`,
  `transactions`, `budgets`, `health_metrics`, `workouts`, `agent_runs`.
- Five shared taxonomies in `core/taxonomy/`: `life-areas` (7 values), `statuses` (6 lifecycle
  sets), `priorities`, `horizons`, `energy` — every value carrying a definition.
- `identity` block on every schema: `primary` field plus `slug_from`, with per-entity
  uniqueness keys documented for automation idempotency.
- `schema` check in the validator, wired into CI and `make schema`: abstract types only, enum
  values resolving to a taxonomy or a local option list, defaults within allowed values,
  `identity` fields existing, `relation`/`rollup` rejected, and every entity catalogued and
  owned by exactly one page.
- `load_yaml` helper so downstream checks report a parse error rather than crashing.
- Two new page blueprints: `habits` (now composed, owning `habits` and `habit_logs`) and
  `prompt_library` (a repository projection).
- ADR-0007 (entity catalogue and normalisation), ADR-0008 (stable identity and slugs).

### Changed
- **Merged three proposed entities into `resources`** with a `resource_type` discriminator.
  Bookmarks, Documents, and Resources had identical field sets. The Bookmarks and Documents
  pages are removed; Resources presents them as views.
- **Merged `achievements` and `career_milestones` into `career_events`** with an `event_type`
  discriminator, and added a `setback` type.
- **Merged `commitments` into `tasks`** via an `is_promise` flag. A promise is a task with a
  person attached; the separate attention it deserves is a view concern.
- **Removed `prompt_library` as an entity.** Prompts live in `prompts/`, so the Prompt Library
  page is a read-only repository projection — consistent with ADR-0003.
- Renamed the decision entity to `decisions` (from the proposed `decision_journal`) to match
  its page id. Illustrative examples across the live docs updated to match; accepted ADRs left
  unchanged as append-only history.
- `capture-routing.yaml`: two rules merged into `reference_material`, three added
  (`training_session`, `career_evidence`, and promise extraction to `tasks`), destinations
  corrected to real entity ids, and gate fields aligned with the schemas.
- `workspace/views/README.md` corrected to say views land in Phase 5, matching the roadmap;
  it previously claimed Phase 3.
- `core/taxonomy/README.md` vocabulary table corrected to the values actually defined.

### Decisions
- **Normalisation rule: merge when field sets are the same, separate when they diverge.**
  Applied to every merge above, and to the cases deliberately kept separate — `reading` versus
  `courses`, `journal` versus `reviews`, `health_metrics` versus `workouts`, `habits` versus
  `habit_logs`. See ADR-0007.
- **`contexts` and `sources` are local enums, not taxonomies.** Each has exactly one consumer,
  and a shared taxonomy with one consumer is indirection with no benefit.
- **Status sets are per-entity-class, not universal.** A single lifecycle would force `at_risk`
  onto tasks and `blocked` onto goals; a status that does not apply is used inconsistently.
- **Every status set has an explicit abandonment state.** A lifecycle whose only exit is
  success is one where nothing gets closed, and stale records corrupt every rollup above them.
- **Health metrics are long-and-narrow**, one row per metric per day, so adding a tracked
  metric is a data change rather than a migration.
- **Three identity layers** — permanent type id, derived readable slug, provider id as
  deployment state. External ids win where the source system supplies one. See ADR-0008.
- **Derived values are never stored.** Progress, completion, and streaks are computed from
  their sources; the few exceptions are automation-maintained and documented as such.

### Notes
- Schemas deliberately carry no `relation` or `rollup` fields — the validator rejects them.
  Relations are declared in `core/relations/` in Phase 4, so the entities exist but are not yet
  connected.
- Page blueprints still contain ~60 forward references to views, which arrive in Phase 5.

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

<!-- Compare links point at commit SHAs rather than tags. The v0.1.0-v0.3.0 tags
     do not exist yet: this environment's git proxy refuses tag pushes, so they
     have to be created from a machine with direct push access. Once they exist,
     these can be rewritten as v0.2.0...v0.3.0 and so on. SHA links resolve today,
     which tag links did not. -->

[Unreleased]: https://github.com/mittalok-creator/2nd-Brain/compare/0ad6f80...main
[0.3.0]: https://github.com/mittalok-creator/2nd-Brain/compare/d6e87fb...0ad6f80
[0.2.0]: https://github.com/mittalok-creator/2nd-Brain/compare/688b8a4...d6e87fb
[0.1.0]: https://github.com/mittalok-creator/2nd-Brain/commit/688b8a4
