# Information architecture

The page hierarchy, the navigation model, and how anything entering the system finds its way
to the right place.

Decisions and rejected alternatives: [ADR-0005](../adr/0005-workspace-information-architecture.md)
and [ADR-0006](../adr/0006-single-inbox-capture.md).
Authoritative tree: [`workspace/pages/_hierarchy.yaml`](../../workspace/pages/_hierarchy.yaml).

---

## The tree

```
🏠 Home                        Where do I go next?
│
├── 📥 Inbox                   What came in, and where does it belong?
├── ☀️  Today                   What matters right now?
├── 🗓  Planner                 When is this actually going to happen?
│   └── 🗣 Meetings
├── 📊 Reviews                 Is this working?
│   ├── ✍️  Journal
│   └── ⚖️  Decisions
│
├── 🎯 Goals                   Am I pursuing the right things?
│   └── 🔁 Habits
├── 🚀 Projects                What is moving, and what is stuck?
│
├── 🧠 Knowledge               What do I know, and where did I put it?
│   └── 🗂 Resources           bookmarks · documents · files · tools
├── 📚 Learning                Am I getting measurably better?
│   ├── 📖 Reading
│   └── 🎓 Courses
├── 💼 Career                  Am I building toward the next step?
├── 💰 Finance                 Is money going where I said it should?
├── 🏋 Health                  Am I looking after the machine?
├── 🤝 Relationships           Who have I not shown up for?
│
├── 🤖 Command Center          What can the agents do, and what have they done?
│   ├── 💬 Prompt Library
│   └── 🛠 Agents
└── ⚙️  System                  How does this work, and is it healthy?
    └── 🏷 Taxonomy
```

Fifteen top-level pages, maximum depth three, nothing more than two clicks from Home.

---

## Page classes

Pages are grouped by the **role they play**, not by life area. Home's navigation uses these
groups, so the structure of the system is legible from its front door.

| Class | Pages | Role |
|---|---|---|
| `root` | Home | Orientation and capture |
| `rhythm` | Inbox · Today · Planner · Reviews | Time-based operation |
| `direction` | Goals · Projects | What is pursued and delivered |
| `domain` | Knowledge · Learning · Career · Finance · Health · Relationships | One area of life |
| `system` | Command Center · System | The system operating on itself |

Life areas are **not** the hierarchy. They are a taxonomy applied as a tag, so a task can
belong to Health without living under a Health page. This is what allows Today to draw from
every area at once.

---

## Navigation constraints

| Constraint | Value | Enforced by |
|---|---|---|
| Root pages | Exactly one — Home | `make hierarchy` |
| Maximum depth | 3 (root → section → detail) | `make hierarchy` |
| Maximum clicks from Home | 2 | `make hierarchy` |
| Sibling ordering | Explicit and unique `order`; never alphabetical | `make hierarchy` |
| Blueprint agrees with the tree | `class`, `parent`, `order` match | `make hierarchy` |
| Questions per page | One | Review |

The last constraint is the useful one, and the only one a machine cannot check. Every
blueprint declares a `question` — the single
question the page exists to answer. A page needing three questions is three pages. This is
the test applied before any new page is added.

---

## Composed and generated pages

| Kind | Has a blueprint | Content |
|---|---|---|
| **Composed** | Yes — `workspace/pages/<id>.yaml` | Views, agent output, and navigation arranged into a purpose-built surface |
| **Generated** | No | Entirely the views of a single entity, generated from that entity's view set |

Eighteen pages are composed; the rest are generated. A blueprint that would only restate "show
this entity's views" adds no information and gives the structure somewhere to drift from
reality.

Four composed pages — Command Center, Agents, Taxonomy, and Prompt Library — are **read-only
projections from the repository** rather than from Notion databases. Their content comes from
`agents/`, `prompts/`, and `core/taxonomy/`, because the repository is the source of truth for
what agents, prompts, and taxonomies exist. Editing them in Notion would produce a definition
that no longer matches the one being executed.

---

## Ownership versus projection

Each of the 23 entities is **owned** by exactly one page — declared either in a composed
blueprint's `owns_entities`, or by a generated page's `entity`. Other pages may display the
same data, but only the owner defines it. `make schema` enforces that ownership is complete and
unique.

```
Goals          owns  goals
Habits         owns  habits, habit_logs
Projects       owns  projects, tasks
Knowledge      owns  knowledge
Resources      owns  resources
Learning       owns  skills
Career         owns  career_events
Relationships  owns  people
Finance        owns  accounts, transactions, budgets
Health         owns  health_metrics, workouts
Command Center owns  agent_runs
```

Career shows professional contacts; Health shows health habits. Both are **projections** of
data owned elsewhere. This is not duplication — the entity is defined once, and relations do
the connecting.

---

## The capture model

One inbox, many destinations. Capture is instant and unstructured; routing is deferred,
batched, and agent-assisted.

```
   Seven entry points                One inbox            Sixteen destinations
   ─────────────────                 ─────────            ────────────────────
   Manual  ─┐
   Mobile  ─┤
   Voice   ─┤                     ┌──────────┐    daily,   ┌─ tasks
   Email   ─┼───────────────────▶ │  inbox   │  batched  ──┼─ projects
   Web clip─┤   one field,        │          │ ─────────▶  ├─ knowledge
   Calendar─┤   no decision       └──────────┘   + agent   ├─ people
   Files   ─┘                                     assist   ├─ transactions
                                                           └─ … or delete
```

Full routing table: [`workspace/capture-routing.yaml`](../../workspace/capture-routing.yaml).

### Why routing is deferred

Choosing among sixteen destinations at the moment of capture is what stops capture happening.
Worse, classification is frequently impossible at that moment — whether "look into vector
databases" is a task, a knowledge topic, or a project seed is often not yet knowable.

So capture asks nothing, and routing happens once a day in a five-minute pass inside the
existing evening ritual. That pass doubles as a review of the day's inputs, which is where
much of the value of capturing them lives.

### The routing gate

Destination databases still need integrity — a project without a goal breaks the relation
graph, an unlinked knowledge note is unretrievable. So required fields are enforced at the
**boundary out of the inbox**, not at capture:

| Destination | Gate | Why |
|---|---|---|
| `projects` | `goal` | A project serving no goal is unowned work |
| `knowledge` | `related_to` | An unconnected note is never found again |
| `habits` | `goal`, `cadence` | A habit serving no goal is a preference |
| `decisions` | `expected_outcome` | Recorded later, reasoning is contaminated by hindsight |

This is the only boundary-enforced constraint in the system, and it is what lets capture stay
free while destinations stay clean.

### Discard is a first-class rule

Items unrouted after 14 days surface for deletion. They are not a backlog — they are evidence
that something was captured which did not matter. A routing model with no discard path turns
the inbox into a growing source of guilt, and surfaces that produce guilt get avoided.

---

## The daily and weekly path through the system

```
  Morning        Today        accept the drafted plan            5 min
  Continuous     Inbox        capture, no decisions              seconds
  Evening        Today        log the day, route the inbox        5 min
  Weekly         Reviews      progress, slips, adjustments       30 min
  Monthly        Reviews      trends, goal viability             60 min
```

Four pages carry daily and weekly operation. The other eleven are consulted when their domain
is the subject, not as part of the routine. A system requiring a tour of fifteen pages to stay
current is a system that will not stay current.

---

## Related

- [Architecture](README.md) — the four layers and their dependency rule
- [`workspace/README.md`](../../workspace/README.md) — surface layer conventions
- [`workspace/pages/README.md`](../../workspace/pages/README.md) — blueprint file format
- [User Guide](../03-user-guide/README.md) — operating the rhythm in practice
