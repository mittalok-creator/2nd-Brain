# Contributing

2nd Brain is a personal system engineered to public standards. These conventions keep it
coherent as it grows — whether the contributor is a person or an AI agent.

---

## Ground Rules

1. **Specification before surface.** Change `core/` first; render to Notion second.
2. **One concept, one home.** If information exists in two places, one of them is wrong.
3. **Every non-obvious decision gets an ADR.** See [`docs/adr/`](docs/adr/).
4. **Nothing ships undocumented.** A feature without docs is unfinished.
5. **Prefer deletion.** Removing an unused thing is a valid, valuable contribution.

---

## Branching

| Branch | Purpose |
|---|---|
| `main` | Always releasable. Protected. |
| `feat/<slug>` | New capability |
| `fix/<slug>` | Corrections |
| `docs/<slug>` | Documentation only |
| `refactor/<slug>` | Restructuring with no behaviour change |
| `chore/<slug>` | Tooling, CI, dependencies |

Slugs are lowercase kebab-case: `feat/agent-personal-ceo`.

---

## Commits

[Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/):

```
<type>(<scope>): <subject>
```

**Types** — `feat` · `fix` · `docs` · `refactor` · `chore` · `test` · `ci` · `style` · `perf`

**Scopes** map to top-level directories, plus a few cross-cutting ones:

`core` · `schema` · `relations` · `taxonomy` · `design` · `workspace` · `dashboards` ·
`agents` · `prompts` · `automation` · `scripts` · `config` · `docs` · `repo` · `ci`

**Subject** — imperative mood, lowercase, no trailing period, ≤ 72 characters.

```
feat(schema): add decisions entity with confidence calibration
docs(adr): record why notion is a projection, not the source of truth
refactor(workspace): flatten review pages into a single review hub
```

A breaking change appends `!` after the scope and explains the migration in the body:

```
feat(schema)!: split tasks into tasks and subtasks

BREAKING CHANGE: existing task relations must be re-pointed. See docs/migrations/0003.md
```

---

## Pull Requests

- One phase or one concern per PR.
- Fill in the PR template completely.
- CI must be green: structure, YAML, and internal links are all validated.
- Update `CHANGELOG.md` under `[Unreleased]` in the same PR.
- If the change alters architecture, include or reference an ADR.

---

## Specification Style

**Format** — YAML for all specifications (see ADR-0004). Two-space indent, no tabs.

**Naming**

| Thing | Convention | Example |
|---|---|---|
| Directory | `kebab-case` | `core/schema/` |
| Spec file | `kebab-case.yaml` | `career-events.yaml` |
| Entity / database id | `snake_case` | `career_events` |
| Field id | `snake_case` | `expected_outcome` |
| Display name | Title Case | `Career Events` |
| Agent id | `kebab-case` | `personal-ceo` |
| Enum value | `snake_case` | `in_progress` |
| Documentation file | `kebab-case.md` | `system-architecture.md` |

**Every spec file carries a header block:**

```yaml
id: decisions
name: Decisions
version: 1.0.0
status: active        # draft | active | deprecated
owner: core
description: >
  One sentence explaining what this entity is for.
```

---

## Documentation Style

- Sentence case headings.
- Second person for guides ("you"), third person for reference material.
- Tables over long prose lists.
- Every code block is copy-pasteable and correct.
- Relative links only — CI fails on broken internal links.

---

## Architecture Decision Records

Create one whenever a decision is hard to reverse, affects more than one layer, or would
otherwise be re-litigated later.

```bash
cp docs/adr/_template.md docs/adr/000N-short-title.md
```

Statuses: `Proposed` → `Accepted` → (`Superseded by ADR-000M` | `Deprecated`).
ADRs are append-only history: supersede them, never rewrite them.

---

## Local Checks

```bash
make validate   # structure, YAML syntax, internal links
make tree       # print the repository map
```

Run `make validate` before every push. CI runs exactly the same command.

---

## Working With AI Agents

Agents contributing to this repository follow the same rules, plus:

- Read the relevant ADRs before changing architecture.
- Never invent a convention when one is documented here.
- Record any deviation from the roadmap in `CHANGELOG.md` with the reason.
- Keep secrets out of the repository — `.env` is git-ignored and stays that way.
