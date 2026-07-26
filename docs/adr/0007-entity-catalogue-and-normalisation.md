# ADR-0007 — Entity catalogue and normalisation

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-07-26 |
| **Phase** | Phase 3 — Databases |
| **Supersedes** | — |
| **Superseded by** | — |

## Context

The initial plan listed sixteen databases: Goals, Projects, Tasks, Habits, Journal, Knowledge,
Reading, Finance, Health, Meetings, Resources, Prompt Library, Bookmarks, Documents, Courses,
Decision Journal.

Turning that list into actual field-level schemas surfaced four problems:

1. **Several proposed entities had identical field sets.** Bookmarks, Documents, and Resources
   would each have carried title, topic, area, URL or file, and a reason for keeping. Three
   tables, one shape.

2. **Some proposed entities were fields, not tables.** "Finance" and "Health" are life areas
   containing several distinct entities — transactions and accounts are not the same shape, and
   neither is a health measurement and a workout.

3. **One proposed entity belongs in the repository, not in Notion.** The Prompt Library is
   defined in `prompts/`. A Notion-side prompt table would be a second definition able to drift
   from the one actually executed, and the executed one would win silently — exactly what
   ADR-0003 forbids.

4. **Some entities were missing.** Nothing held per-day habit completions, agent invocations,
   budgets, or skills, all of which the Phase 2 page blueprints assume.

There was also no stated rule for when two similar things should be one entity, so the same
argument would be relitigated for every future proposal.

## Decision

**Twenty-three entities**, catalogued in `core/schema/_catalogue.yaml`.

### The normalisation rule

> **Merge when the field sets are the same. Separate when they diverge.**
>
> If two candidate entities would carry the same fields and differ only in a category, they
> are one entity with a discriminator. If merging them would leave rows with many empty
> columns, they are two entities.

This is the test applied to every case below, and to every future proposal.

### Merges applied

| Proposed | Becomes | Reasoning |
|---|---|---|
| `bookmarks`, `documents`, `resources` | `resources` with `resource_type` | Identical fields. Three tables would drift, and cross-searching them would require three queries. |
| `achievements`, `career_milestones` | `career_events` with `event_type` | Identical fields — both are a dated career record with impact. Also gained a `setback` type, since a career log containing only wins cannot reveal a pattern. |
| `commitments` | `tasks` with `is_promise` | A promise made to someone is a task with a person attached. The separate attention it deserves is a *view* concern, not an entity concern. |

### Kept separate, despite similarity

| Candidates | Why not merged |
|---|---|
| `reading` / `courses` | Books have author, pages, position; courses have provider, instructor, modules, cost, deadline. Merging leaves half the columns empty on every row. |
| `journal` / `reviews` | Journal is freeform daily reflection. Reviews carry period bounds, metric snapshots, and tracked actions the weekly dashboard depends on. |
| `health_metrics` / `workouts` | A measurement is (metric, value, date). A session is (type, duration, intensity, how it felt). Different shapes entirely. |
| `habits` / `habit_logs` | A habit is a definition; a log entry is an event. Storing completions on the habit would require a schema change every time the calendar advanced. |
| `transactions` / `accounts` / `budgets` | A movement, a position, and an intention. Three shapes, three lifecycles. |

### Entities removed from the plan

- **`prompt_library`** — prompts live in `prompts/`. The Prompt Library page is a read-only
  projection of the repository, like the Agents and Taxonomy pages. See ADR-0003.
- **`areas`** — a life area is a taxonomy value, not an entity.

### Entities added

`habit_logs`, `budgets`, `accounts`, `skills`, `agent_runs`, `inbox`, `people`, `workouts`,
`career_events` — each required by a Phase 2 page blueprint that had no entity behind it.

### Rejections are recorded

`_catalogue.yaml` carries a `rejected:` block naming every entity considered and not created,
with the reason. Without it, the same proposals return.

### Taxonomies over local enums — with a limit

Five shared taxonomies: `life_areas`, `statuses`, `priorities`, `horizons`, `energy`. A value
set used by more than one entity belongs in `core/taxonomy/`; a set used by exactly one stays
local to that entity.

`contexts` (desk, phone, errand) and `sources` were both planned as taxonomies and are instead
local enums, because only `tasks` and `inbox` respectively use them. A shared taxonomy with one
consumer is indirection with no benefit.

Status sets are deliberately **not** universal. A single shared lifecycle would force
`at_risk` onto tasks and `blocked` onto goals, and a status that does not apply is one that
gets used inconsistently.

### Relations are absent by design

Schemas carry no `relation` or `rollup` fields — the validator rejects them. Relations are
declared in `core/relations/` in Phase 4, so cardinality is stated once rather than twice.
The consequence is that Phase 3 delivers entities that exist but are not yet connected.

### Derived values are never stored

Progress, completion percentage, streaks, and category totals are computed from their sources.
Where a field looks like a stored derivation — `projects.last_activity`, `skills.practice_minutes_total`
— it is maintained by automation and documented as such, because the alternative requires
scanning every child row to detect a project with no children at all.

## Alternatives considered

### Keep the original sixteen and add the missing nine

Twenty-five entities, minimal deviation from the plan. Rejected because three of them would
have had identical schemas, which guarantees divergence: a field added to Bookmarks and not to
Documents is invisible until something breaks.

### One universal `items` table with a `type` discriminator

Radically simple — one table, one set of views, no relations needed between types. Genuinely
attractive for capture.

Rejected because it abandons typed fields entirely. A goal's `success_criteria`, a
transaction's `amount`, and a workout's `intensity` cannot share a column meaningfully. Every
consumer would need to know which fields apply to which type, moving the schema from the
specification into the head of whoever wrote the last view.

### A wide `health` table with one column per metric

`weight`, `sleep_hours`, `resting_heart_rate` as columns on a daily row. Conventional, and
easier to chart.

Rejected because adding a tracked metric would then be a schema change, and a schema change is
a migration. The long-and-narrow shape — one row per metric per day — makes adding a metric a
data change. The charting cost is real and accepted.

### Merge everything consumable into one `sources` entity

`reading`, `courses`, and `resources` as one table with a `format` field. Rejected by the
normalisation rule: the field sets genuinely diverge, and the merged table would be mostly
empty cells.

## Consequences

**Positive**

- One shape lives in one place; there is no pair of tables that can silently diverge.
- The normalisation rule makes future proposals decidable rather than debatable.
- Recorded rejections stop the same entities being re-proposed.
- Adding a health metric or a resource type is a data change, not a migration.
- Every entity is machine-checked: field contracts, taxonomy references, and ownership.

**Negative**

- Three Phase 2 artefacts had to change: the Bookmarks and Documents pages were removed, the
  Habits and Prompt Library pages became composed, and the routing table lost two rules and
  gained three. Phase 2's output was correct given what was known then; discovering this in
  Phase 3 is the process working, not failing.
- Discriminated entities need filtered views to feel like separate things. `resources` needs
  four views to present as bookmarks, documents, files, and tools.
- Twenty-three entities is a large model for a personal system. Justified per entity by a page
  that needs it, and the catalogue makes any unused one visible for deletion.

**Neutral / accepted trade-offs**

- Schemas are incomplete until Phase 4 adds relations. Stated explicitly in the catalogue
  header rather than left to be discovered.
- `owned_by` in the catalogue duplicates ownership declared in the page blueprints. The
  validator checks that the two agree, so the duplication cannot rot.

## Revisit when

- Any entity has produced no records after a month of real use — that is a deletion candidate,
  and the catalogue exists to make it visible.
- A discriminated entity's types start needing genuinely different fields, at which point the
  normalisation rule says to split it.
- The entity count grows past roughly thirty without a page demanding each addition, which
  would indicate the model is being extended for completeness rather than for use.
