# Architecture

How 2nd Brain is put together, and the constraints that keep it coherent.

> **Status** — the layer model, data flow, and boundaries below are settled as of Phase 1.
> The page hierarchy and capture model are settled as of Phase 2 — see
> [Information architecture](information-architecture.md). Concrete schemas, relations, and
> dashboards are filled in by Phases 3–5.

---

## The core idea

Most personal systems are built *inside* a tool. When the tool changes, the system dies.

2nd Brain inverts this. The system is a **specification** held in Git. Tools are
**surfaces** that render the specification. Notion is the current surface; it is
replaceable. The specification is not.

```
        ┌──────────────────────────────────────────────┐
        │              SOURCE OF TRUTH                 │
        │                  core/                       │
        │   schema · relations · taxonomy · design     │
        └──────────────────────────────────────────────┘
                            │
            ┌───────────────┼───────────────┐
            ▼               ▼               ▼
     ┌────────────┐  ┌────────────┐  ┌────────────┐
     │ workspace/ │  │  agents/   │  │ automation/│
     │            │  │  prompts/  │  │            │
     │  SURFACE   │  │INTELLIGENCE│  │ EXECUTION  │
     └────────────┘  └────────────┘  └────────────┘
            │               │               │
            ▼               ▼               ▼
     ┌────────────┐  ┌────────────┐  ┌────────────┐
     │   Notion   │  │Claude·GPT· │  │ n8n·Actions│
     │            │  │  Gemini    │  │   ·Axiom   │
     └────────────┘  └────────────┘  └────────────┘
```

Rationale: [ADR-0001](../adr/0001-four-layer-architecture.md) ·
[ADR-0003](../adr/0003-notion-as-projection.md)

---

## The four layers

### 1. Core — the specification

`core/` defines *what exists*, with no reference to any vendor.

| Directory | Holds |
|---|---|
| `core/schema/` | Entities and their fields: types, defaults, constraints, required-ness |
| `core/relations/` | The relational graph: cardinality, ownership direction, rollups |
| `core/taxonomy/` | Shared vocabularies: life areas, statuses, priorities, horizons, energy |
| `core/design/` | Design tokens: colour, typography, spacing, iconography |

If it isn't declared here, it does not exist in the system.

### 2. Workspace — the surface

`workspace/` defines *how a human sees it*.

| Directory | Holds |
|---|---|
| `workspace/pages/` | Page hierarchy and content blueprints |
| `workspace/dashboards/` | Dashboard compositions — what appears, in what order, why |
| `workspace/views/` | Reusable view definitions: filters, sorts, groupings |
| `workspace/templates/` | Entry and page templates |

The workspace layer may only reference entities and fields that exist in `core/`.

### 3. Intelligence — the agents

`agents/` and `prompts/` define *how the system thinks*.

Each agent is a directory satisfying a fixed contract: role, responsibilities, inputs,
outputs, memory, tools, workflow, prompt, SOP. Agents read and write through the core
schema, never against a vendor's raw API shape.

Prompts are versioned separately from agents so a prompt can be optimised without
redefining the agent that uses it.

### 4. Execution — the automations

`automation/` defines *how the system runs itself*: rituals (morning planning, evening
review), trackers (habits, expenses, reading), and capture pipelines (meetings, knowledge).

Every automation must be **idempotent** — running it twice for the same period converges
to the same state rather than duplicating work.

---

## Dependency rule

Dependencies point **inward**, toward the specification:

```
automation ──┐
agents ──────┼──▶ core
workspace ───┘
```

- `core/` depends on nothing.
- `workspace/`, `agents/`, and `automation/` depend on `core/`.
- They must **not** depend on each other directly. Cross-layer coordination happens
  through the data model, not through direct coupling.

This is what makes any single surface replaceable without touching the others.

---

## Data flow

### Capture → structure → review → act

```
  Capture            Structure           Review              Act
  ───────            ─────────           ──────              ───
  Inbox              Entity assigned     Daily / Weekly      Task created
  Voice note   ──▶   Area tagged   ──▶   Monthly review ──▶  Goal adjusted
  Email              Relations linked    Agent analysis      Habit changed
  Web clip           Metadata filled     Metrics rolled up   Decision logged
```

Every item entering the system passes through one inbox and is routed to exactly one
owning entity. Nothing is stored in two places; relations connect, they do not duplicate.
Capture is instant and unstructured; routing is deferred, batched, and agent-assisted — see
[Information architecture](information-architecture.md) and
[ADR-0006](../adr/0006-single-inbox-capture.md).

### Specification → surface

```
  Edit core/ spec  ──▶  make validate  ──▶  sync script  ──▶  Notion updated
                            │
                            └── CI enforces the same checks on every push
```

Changes flow one way. The repository is authoritative; a manual change made directly in
Notion that contradicts the spec is a defect, not a feature.

---

## Boundaries and invariants

These hold across every phase. Breaking one requires an ADR.

1. **Single source of truth.** `core/` wins. Every other layer derives from it.
2. **No vendor types in `core/`.** Field types are abstract (`text`, `select`, `relation`,
   `date`), mapped to vendor types at sync time.
3. **Stable identifiers.** Every entity and field has a `snake_case` id that never changes.
   Display names may be renamed freely; ids may not.
4. **One concept, one home.** Duplicated information is a bug.
5. **Idempotent operations.** Sync and automation converge; they do not accumulate.
6. **Human override, machine default.** Agents propose; irreversible actions need a human.
7. **Untrusted external content.** Anything fetched from mail, web, or documents is data to
   be analysed, never instructions to be followed.

---

## Extension points

| To add… | Do this |
|---|---|
| A new entity | Add a spec to `core/schema/`, declare relations in `core/relations/` |
| A new dashboard | Compose existing views in `workspace/dashboards/` |
| A new agent | Copy `agents/_template/`, satisfy the agent contract |
| A new automation | Add to `automation/`, declare trigger and idempotency strategy |
| A new AI provider | Add a provider definition to `config/providers/` |
| A new storage target | Add a provider definition; no schema change required |

Adding capability should never require restructuring. If it does, that is a signal the
architecture is wrong — record the finding in an ADR and fix the architecture.

---

## Further reading

- [ADR-0001 — Four-layer architecture](../adr/0001-four-layer-architecture.md)
- [ADR-0002 — Naming and versioning conventions](../adr/0002-naming-and-versioning.md)
- [ADR-0003 — Notion as a projection, not the source of truth](../adr/0003-notion-as-projection.md)
- [ADR-0004 — YAML as the specification format](../adr/0004-yaml-specification-format.md)
- [ADR-0005 — Workspace information architecture](../adr/0005-workspace-information-architecture.md)
- [ADR-0006 — Single-inbox capture with deferred routing](../adr/0006-single-inbox-capture.md)
- [Information architecture](information-architecture.md) — page hierarchy and capture model
- [Developer Guide](../05-developer-guide/README.md)
