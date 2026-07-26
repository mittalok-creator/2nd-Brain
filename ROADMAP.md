# Roadmap

**2nd Brain** is built in nine sequenced phases. Each phase ends with a commit, a
documentation update, a changelog entry, and a recorded architectural rationale.

Legend: ✅ complete · 🚧 in progress · ⬜ planned

---

## Phase 1 — Repository Architecture ✅ `v0.1.0`

Establish the foundation everything else is built on.

- [x] Four-layer architecture: specification, surface, intelligence, execution
- [x] Root project documents and license
- [x] Documentation tree and ADR log
- [x] GitHub standards: issue forms, PR template, labels, CODEOWNERS, Dependabot
- [x] CI pipeline validating structure, YAML, and internal links
- [x] Naming, versioning, and commit conventions

---

## Phase 2 — Workspace Architecture ⬜ `v0.2.0`

Design the human-facing surface before designing the data.

- [ ] Page hierarchy for the Notion workspace (Home, Command Center, life domains)
- [ ] Navigation model: how any surface is reachable in ≤ 2 clicks
- [ ] Capture model: one inbox, many destinations
- [ ] Page blueprints in `workspace/pages/`
- [ ] Information architecture ADR

---

## Phase 3 — Databases ⬜ `v0.3.0`

The normalised data model, declared platform-neutrally.

- [ ] Entity catalogue and canonical naming
- [ ] Field-level schemas in `core/schema/` (types, defaults, validation, required-ness)
- [ ] Shared taxonomies in `core/taxonomy/`: life areas, statuses, priorities, energy, horizons
- [ ] Identity and slug strategy for stable cross-tool references
- [ ] Schema validator extended to enforce field contracts

---

## Phase 4 — Relations ⬜ `v0.4.0`

The graph that turns tables into a system.

- [ ] Relation map in `core/relations/` with cardinality and ownership direction
- [ ] Rollups and derived metrics (progress, streaks, burn rate, velocity)
- [ ] Referential integrity rules and orphan detection
- [ ] Generated entity-relationship diagram committed to `docs/01-architecture/`

---

## Phase 5 — Dashboards ⬜ `v0.5.0`

Premium, low-noise surfaces for decision-making.

- [ ] Executive · Today · Weekly Review · Monthly Review
- [ ] Finance · Health · Learning · Career · Projects · AI Command Center
- [ ] Reusable view definitions in `workspace/views/`
- [ ] Design tokens finalised in `core/design/` — light and dark, accessible contrast

---

## Phase 6 — AI Agents ⬜ `v0.6.0`

The intelligence layer.

- [ ] Agent contract: role, responsibilities, inputs, outputs, memory, tools, workflow, prompt, SOP
- [ ] Core roster: Personal CEO, Life Coach, Health Coach, Finance Advisor, Career Advisor,
      Learning Mentor, Research Assistant, Reading Assistant, Decision Assistant,
      Prompt Engineer, Prompt Optimizer, Knowledge Curator
- [ ] Shared memory protocol and context-retrieval strategy
- [ ] Agent registry with capability routing
- [ ] Model-agnostic prompt packaging (Claude · ChatGPT · Gemini)

---

## Phase 7 — Automations ⬜ `v0.7.0`

The system running itself.

- [ ] Rituals: morning planning, evening review, weekly review, monthly review
- [ ] Trackers: goals, habits, reading, expenses, health, learning
- [ ] Capture: meeting notes, knowledge, bookmarks, documents
- [ ] n8n workflows, GitHub Actions schedules, Axiom jobs
- [ ] Failure handling, retries, idempotency, and observability

---

## Phase 8 — Documentation ⬜ `v0.8.0`

- [ ] Complete User, AI, Developer, and Automation guides
- [ ] Design system reference with tokens and component specs
- [ ] FAQ and troubleshooting expanded from real usage
- [ ] Onboarding path: zero to running in under an hour

---

## Phase 9 — Testing & Refinement ⬜ `v1.0.0`

- [ ] Specification test suite (schema, relations, agent contracts)
- [ ] Automation dry-run harness
- [ ] Live usage cycle: one full week and one full month operated end to end
- [ ] Performance and noise audit — remove anything unused
- [ ] `v1.0.0` release

---

## Beyond 1.0

| Theme | Intent |
|---|---|
| **Memory** | Long-term vector memory shared across agents and models |
| **Voice** | Capture and review by voice, hands-free |
| **Mobile** | Fast capture surface optimised for phone |
| **Analytics** | Longitudinal life analytics — trends, correlations, forecasts |
| **Multi-model routing** | Route each task to the model that handles it best |
| **Offline mirror** | Local, private copy of the entire brain |

---

## Principles That Constrain the Roadmap

- No phase ships without documentation.
- No tool is adopted that cannot be replaced.
- Anything unused for a month is a candidate for deletion.
- Complexity must be earned by demonstrated value.
