# Developer Guide

Extending and maintaining 2nd Brain.

> **Status** — current through Phase 3. Conventions, tooling, and extension points below are
> live. Sync adapter internals are documented in a later phase; the test harness in Phase 9.

---

## Mental model

Read [Architecture](../01-architecture/README.md) first. The one rule that governs every
change:

> **Dependencies point inward toward `core/`.** `core/` depends on nothing.
> `workspace/`, `agents/`, and `automation/` depend on `core/` and never on each other.

When deciding where a file belongs, ask: *would this still be true if Notion disappeared?*
If yes, it belongs in `core/`.

---

## Local setup

```bash
git clone https://github.com/mittalok-creator/2nd-Brain.git
cd 2nd-Brain
pip install -r scripts/requirements.txt
make validate
```

| Command | Does |
|---|---|
| `make help` | List available targets |
| `make validate` | Structure, YAML, links, hierarchy, and schema — the full CI check |
| `make structure` | Repository layout only |
| `make yaml` | YAML syntax and spec headers only |
| `make links` | Internal documentation links only |
| `make hierarchy` | Workspace page tree and navigation constraints only |
| `make schema` | Entity field contracts, taxonomy references, and ownership only |
| `make tree` | Print the repository map |

Run `make validate` before every push. CI runs exactly the same script, so a green local
run means a green pipeline.

---

## The validator

`scripts/validate_repository.py` is deliberately dependency-light — standard library plus
PyYAML — so it runs anywhere without a build step.

It enforces five things:

1. **Structure.** Required files and directories exist; every top-level directory has a
   `README.md`; ADR numbers are unique and sequential.
2. **YAML.** Every `.yaml`/`.yml` file parses. Every spec file under `core/`, `workspace/`,
   `agents/`, and `automation/` carries the header contract with a semantic `version` and a
   valid `status`.
3. **Links.** Every relative Markdown link resolves to a real path. External links are not
   checked — network checks make CI flaky.
4. **Hierarchy.** The workspace page tree satisfies the constraints in
   [ADR-0005](../adr/0005-workspace-information-architecture.md): exactly one root, depth ≤ 3,
   explicit and unique sibling order, composed pages have blueprints while generated pages do
   not, and each blueprint's `class`, `parent`, and `order` agree with `_hierarchy.yaml`.
5. **Schema.** Every field uses an abstract type; enum fields resolve to a taxonomy or declare a
   local option list; defaults are allowed values; `identity.primary` and `slug_from` name real
   fields; `relation` and `rollup` are rejected (they belong in `core/relations/`); every entity
   is catalogued and owned by exactly one page. See
   [ADR-0007](../adr/0007-entity-catalogue-and-normalisation.md).

Adding a check: add a function, register it in `CHECKS`, add a `make` target, and add a CI
step. Keep checks offline and deterministic.

---

## Adding to the system

### A new entity

1. Create `core/schema/<entity>.yaml` with the header contract, field definitions, and an
   `identity` block. Use abstract types only, and reference a shared taxonomy for any value set
   used by more than one entity.
2. Add it to `core/schema/_catalogue.yaml` with its group, file, purpose, and owning page.
3. Give it an owner: add it to a composed page's `owns_entities`, or to a generated page's
   `entity` in `_hierarchy.yaml`. Exactly one page must own it.
4. Declare its relations in `core/relations/`.
5. Add views that expose it in `workspace/views/`.
6. `make validate`, then commit as `feat(schema): add <entity>`.

Before adding one, check the `rejected:` block in `_catalogue.yaml` — and apply the
normalisation rule from [ADR-0007](../adr/0007-entity-catalogue-and-normalisation.md): merge
when field sets are the same, separate when they diverge.

### A new agent

1. `cp -r agents/_template agents/<agent-id>`
2. Fill in `agent.yaml`, `prompt.md`, and `sop.md` completely — all nine contract parts.
3. Register it in `agents/_registry.yaml`.
4. Commit as `feat(agents): add <agent-name>`.

### A new automation

1. Create the definition under `automation/`, declaring trigger, steps, and idempotency
   strategy.
2. Export the n8n workflow **without credentials** into `automation/n8n/`.
3. Document it in the [Automation Guide](../06-automation-guide/README.md).
4. Commit as `feat(automation): add <name>`.

### A new provider

Add a definition to `config/providers/`. No schema change should be required — if one is,
the abstraction is leaking and needs an ADR.

---

## Conventions

Full reference in [`CONTRIBUTING.md`](../../CONTRIBUTING.md). The short version:

| Thing | Convention |
|---|---|
| Directory, spec file, agent id | `kebab-case` |
| Entity id, field id, enum value | `snake_case` |
| Display name | Title Case |
| Branch | `feat/…` `fix/…` `docs/…` `refactor/…` `chore/…` |
| Commit | `type(scope): imperative subject` |

Ids are permanent. Display names are free to change. See
[ADR-0002](../adr/0002-naming-and-versioning.md).

---

## Specification header

Every spec file starts with:

```yaml
id: decisions
name: Decisions
version: 1.0.0
status: active        # draft | active | deprecated
owner: core
description: >
  One sentence explaining what this entity is for.
```

Files under a `_`-prefixed path (`_template/`, `_registry.yaml`) are exempt, as are vendor
exports under `automation/n8n/` and `automation/actions/`.

---

## Continuous integration

`.github/workflows/ci.yml` runs three jobs:

| Job | Checks |
|---|---|
| `validate` | Structure, YAML specs, internal links, page hierarchy, entity schemas |
| `hygiene` | No tracked `.env` or credential-shaped files; trailing newlines |
| `commits` | Conventional Commit subjects on pull requests |

`.github/workflows/labels.yml` applies the label taxonomy from `.github/labels.yml` when it
changes on `main`.

---

## Architecture decisions

Anything hard to reverse, cross-layer, or likely to be questioned later gets an ADR:

```bash
cp docs/adr/_template.md docs/adr/000N-short-title.md
```

Add the row to [`docs/adr/README.md`](../adr/README.md) in the same commit. ADRs are
append-only: supersede, never rewrite.

---

## Sections planned for later phases

- Sync adapter architecture and the abstract → Notion type mapping *(Phase 3)*
- Migration authoring and running *(Phase 4)*
- Drift detection between the specification and live Notion *(Phase 9)*
- Specification test suite and the automation dry-run harness *(Phase 9)*
