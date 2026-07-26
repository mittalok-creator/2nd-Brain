# ADR-0005 — Workspace information architecture

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-07-26 |
| **Phase** | Phase 2 — Workspace Architecture |
| **Supersedes** | — |
| **Superseded by** | — |

## Context

The initial plan proposed twelve top-level pages: Home, Goals, Planner, Knowledge, Career,
Finance, Health, Learning, Family, Projects, Reviews, AI Command Center.

Working through what each page would contain raised five problems:

1. **No home for meta-content.** The prompt library, the taxonomy reference, and the
   architecture documentation had nowhere to live. In practice they end up scattered — the
   prompt library in Learning, the taxonomy in Knowledge — and become unfindable.

2. **No capture surface.** Twelve destination pages and no inbox. Without one, capture
   requires choosing a destination at the moment of capture, which is the single most
   reliable way to stop capture happening.

3. **`Family` is narrower than the need.** Friends, mentors, and professional contacts have
   no home under that name, so they get no home at all.

4. **Overlapping surfaces.** Planner, Reviews, and the absent Today were not distinguished.
   "Plan the week", "execute today", and "reflect on last week" are three different acts at
   three different cadences.

5. **No stated grouping.** Twelve peer pages in a sidebar, ordered arbitrarily. The structure
   of the system was not legible from its own navigation.

Beyond structure, there was no stated rule for what makes a page worth existing, and no
constraint on depth — the condition under which every Notion workspace eventually becomes a
nested maze nobody navigates.

## Decision

### Page classes

Group pages by the **role they play**, not by life area. Four classes:

| Class | Pages | Role |
|---|---|---|
| `root` | Home | Orientation and capture |
| `rhythm` | Inbox, Today, Planner, Reviews | Time-based operation |
| `direction` | Goals, Projects | What is being pursued and delivered |
| `domain` | Knowledge, Learning, Career, Finance, Health, Relationships | A single area of life |
| `system` | Command Center, System | The system operating on itself |

Home's navigation is grouped by class, so the shape of the system is visible from its front
door.

### Hierarchy

Declared in `workspace/pages/_hierarchy.yaml`, with hard constraints enforced by
`make hierarchy` in CI:

- **Exactly one root** — Home.
- **Maximum depth 3** — root → section → detail.
- **Every page reachable from Home in ≤ 2 clicks.**
- **Explicit, unique `order`** among siblings. Never rely on alphabetisation.

Fifteen top-level pages, each with at most three children.

### Composed versus generated pages

Two kinds of page:

- **Composed** — has a blueprint in `workspace/pages/`. Arranges views, agent output, and
  navigation into a purpose-built surface.
- **Generated** — has no blueprint. Its content is entirely the views of a single entity, so
  it is generated from that entity's view set.

Sixteen composed pages; the rest generated. A blueprint that would only restate "show this
entity's views" adds no information and gives the structure somewhere to drift.

### Changes from the proposed list

| Change | Reasoning |
|---|---|
| **Add `Inbox`** | Capture needs a destination that requires no decision. See ADR-0006. |
| **Add `Today`** | Execution ("what now") is a different act from planning ("when") and review ("what happened"). Three cadences, three surfaces. |
| **Add `System`** | Meta-content needs a home, or it leaks into life-area pages. |
| **`Family` → `Relationships`** | Family is a subset of the people who matter. Friends, mentors, and professional contacts otherwise have no home. Family remains a tag within the page, and the most heavily weighted one. |
| **`AI Command Center` → `Command Center`** | Everything on the page is AI-driven. The qualifier adds length without information. |
| **No `Tasks` page** | Tasks are always seen in the context that makes them meaningful — today's list, or the project they deliver. |
| **`Habits` under `Goals`** | A habit is a recurring commitment to a goal. A habit serving no goal is a preference. |
| **`Journal` and `Decisions` under `Reviews`** | Both are reflection at different cadences. |
| **`Reading` and `Courses` under `Learning`** | Intake pipelines feeding deliberate skill acquisition. |
| **`Resources`, `Bookmarks`, `Documents` under `Knowledge`** | All are reference material at differing levels of processing. |

### Page contract

Every blueprint declares a `question` — the single question the page exists to answer. A page
that needs three questions is three pages. This is the test applied when deciding whether a
new page is warranted.

## Alternatives considered

### The proposed flat list of twelve

Simple, and matches how people describe their lives. Rejected because it has no capture
surface, no home for meta-content, and no stated grouping — so the sidebar order becomes the
information architecture by accident.

### Life-area-first hierarchy (everything nested under a domain)

`Health/Habits`, `Career/Learning`, `Finance/Goals`. Attractive because it matches how life
is described.

Rejected because the cross-cutting surfaces are the ones actually used daily. Today's tasks
span every area; the weekly review reads all of them. Under this structure, Today has no home
and the daily loop requires visiting six pages. Life areas are already modelled properly as a
taxonomy in `core/taxonomy/life-areas.yaml`, applied as a tag — which is where that grouping
belongs.

### Database-per-page (one page per database, no composed surfaces)

Minimal and self-maintaining: fifteen databases, fifteen pages. Rejected because it makes the
human do all the composition work. The value of Today is precisely that it draws from four
entities; a workspace of raw database views is a filing cabinet.

### Deeper hierarchy with fewer top-level pages

Group the six domain pages under a single `Life` parent, reducing top-level count from fifteen
to ten. Genuinely tempting for sidebar tidiness.

Rejected because it costs a click on every domain visit and buys only cosmetic tidiness.
Fifteen items in a sidebar is legible; three clicks to reach Health is not. The ≤ 2 click
constraint is worth more than a shorter list.

## Consequences

**Positive**

- Every surface is one or two clicks from Home.
- The class grouping makes the system's structure self-describing.
- Meta-content has a home, so life-area pages stay about life.
- Capture requires no decision, which is what makes it actually happen.
- The `question` field gives an objective test for whether a page should exist.
- Generated pages mean roughly half the workspace needs no hand-maintained blueprint.

**Negative**

- Fifteen top-level pages is a long sidebar. Accepted as the cost of the click constraint.
- `Relationships` diverges from the requested `Family`. Flagged explicitly; the tag preserves
  the original intent, and reverting is a one-line change since ids are stable.
- Three of the composed pages (Command Center, Agents, Taxonomy) are read-only projections
  from the repository, which requires sync support Notion does not provide natively.

**Neutral / accepted trade-offs**

- Blueprints reference views that do not exist until Phase 3. Forward references are expected
  and are validated when views land.
- Domain pages surface data owned by other pages (Career shows professional contacts from
  Relationships; Health shows habits from Goals). This is projection, not duplication — the
  owning entity is declared in exactly one place via `owns_entities`.

## Revisit when

- Any page's `question` can no longer be stated in one sentence — the page is doing too much.
- The sidebar becomes genuinely unnavigable in practice, at which point a `Life` grouping
  parent is the first thing to reconsider.
- `Relationships` proves to be the wrong scope in use — if only family records ever
  accumulate, the broader name is unearned.
