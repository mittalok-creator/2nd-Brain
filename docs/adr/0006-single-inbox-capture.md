# ADR-0006 — Single-inbox capture with deferred routing

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-07-26 |
| **Phase** | Phase 2 — Workspace Architecture |
| **Supersedes** | — |
| **Superseded by** | — |

## Context

The system has roughly fifteen destination entities and seven entry points — manual capture,
mobile, voice, forwarded email, web clipper, calendar events, and watched folders. Something
has to decide which destination a captured item belongs in.

The obvious approach is to decide at capture time: a task goes to Tasks, a note goes to
Knowledge, a link goes to Bookmarks. Every personal system starts this way, and the failure
mode is consistent and well documented:

- **Capture friction compounds.** A thought worth capturing is worth roughly three seconds of
  effort. Choosing among fifteen destinations, then filling in that destination's required
  fields, takes considerably longer than the thought is worth.
- **Classification at capture time is often impossible.** Whether "look into vector databases"
  is a task, a knowledge topic, or the seed of a project is frequently not knowable at the
  moment it occurs.
- **Friction routes around the system.** When capture is slow, capture moves to the notes app,
  and the system becomes a place things are filed after the fact — which is to say, never.

Meanwhile the destination databases have real integrity requirements. A project without a goal
breaks the relation graph; a knowledge note with no links is unfindable. Capture cannot simply
dump unstructured rows into them.

These two requirements are in direct tension: capture must be frictionless, and destinations
must be clean.

## Decision

**Separate capture from routing.** One inbox receives everything; routing happens later,
batched, with agent assistance and a completeness gate.

### Capture

- **One destination.** Every entry point writes to the `inbox` entity. No exceptions.
- **One required field.** The content itself. Everything else is optional at capture.
- **No classification.** Capture never asks where something belongs.

### Routing

- **Batched, once a day**, during the evening review. Budget: five minutes.
- **Agent-proposed.** The Knowledge Curator proposes a destination and metadata for each item
  at the `fast` model tier. Proposals are accepted in bulk; corrections override individually.
- **Human-decided.** The agent never deletes, never creates a goal, and never takes an action
  with an external side effect.
- **First match wins** against the ordered rule table in `workspace/capture-routing.yaml`.
- **Exactly one destination.** Nothing is ever routed to two places. Relations connect;
  duplication is forbidden.

### The routing gate

An item may not leave the inbox until every field in its rule's `requires` list is populated.

This is the only place in the system where required fields are enforced at a **boundary**
rather than at creation, and it is the mechanism that resolves the tension: capture stays
free, and destination databases stay clean, because the completeness requirement is moved to
the moment when the information is actually available.

Notable gates:

| Destination | Requires | Why |
|---|---|---|
| `projects` | `goal` | A project serving no goal is unowned work |
| `knowledge` | `related_to` | An unconnected note is never retrieved again |
| `habits` | `goal`, `cadence` | A habit serving no goal is a preference |
| `decision_journal` | `expected_outcome` | Recorded after the fact, reasoning is already contaminated by hindsight |

### Discard is an explicit rule

Items unrouted after 14 days surface for deletion. They are not a backlog to clear — they are
evidence that something was captured which did not matter.

A routing model with no discard path turns the inbox into a permanent, growing source of
guilt, and a surface that produces guilt gets avoided.

### Untrusted sources

Email, web clips, and dropped files carry content authored by someone else. These sources are
marked `untrusted: true`. The classification agent treats their content as data to analyse,
never as instructions to follow.

## Alternatives considered

### Classify at capture time

Choose the destination when capturing. Rejected for the reasons in Context: it is the standard
approach and the standard failure. It optimises for a tidy database at the cost of the capture
actually happening, which is the wrong trade — an empty tidy database is worth nothing.

### One inbox per destination type

Separate quick-capture surfaces for tasks, notes, and links. A middle ground: less choice than
fifteen destinations, more structure than one inbox.

Rejected because it reintroduces the impossible decision in smaller form. The hard cases —
"is this a task or a project?", "is this a note or a bookmark?" — are exactly the ones that
still require a decision, and they are the common cases. Three inboxes also triple the number
of surfaces that can be left unreviewed.

### Fully automatic routing, no human review

Let the agent route everything without confirmation. Faster, and removes the five-minute
review entirely.

Rejected on two grounds. Practically, misrouted items are far more expensive to find and fix
than to prevent, because a wrongly-filed item is invisible. Structurally, the daily routing
pass is not overhead — it is the moment the day's captures are actually reviewed, which is
where most of the value of capturing them lives. Automating it away would remove the thinking
and keep only the filing.

### No inbox — capture directly into a single universal notes database

One `notes` entity holding everything, with tags instead of routing. Genuinely simple, and no
routing step at all.

Rejected because it abandons the relational model. Progress rollups, goal health, habit
streaks, and financial trends all require typed entities with defined relations. A universal
notes table can be searched but cannot be analysed, and analysis is the reason this system
exists rather than a notes app.

## Consequences

**Positive**

- Capture is a single tap to a single field from any device.
- Classification happens when the information to classify is actually available.
- Destination databases keep their integrity guarantees via the gate.
- The daily routing pass doubles as a review of the day's inputs.
- Adding an entry point requires no schema change — it writes to the same inbox.
- The stale rule keeps the inbox bounded without manual triage discipline.

**Negative**

- A daily five-minute routing habit is required. If it lapses, the inbox grows and the stale
  rule starts deleting things. Mitigated by placing routing on the Today page inside the
  evening ritual that already exists, rather than as a separate task.
- Items are briefly in a state where they exist but are not yet part of the relational model.
  Accepted: bounded to at most one day in normal operation.
- The routing gate can block an item indefinitely if a required relation genuinely does not
  exist — for example, a project with no matching goal. This is intended: the block is the
  finding, and it surfaces a missing goal.

**Neutral / accepted trade-offs**

- The `inbox` entity needs its own schema with a nullable destination, adding one entity to the
  model.
- Agent-assisted routing costs tokens daily. Bounded by using the `fast` tier and batching.

## Revisit when

- The daily routing pass is consistently skipped for two weeks — that means the friction moved
  rather than disappeared, and the gate requirements are the first thing to reconsider.
- Agent routing proposals are accepted without correction for a sustained period, which would
  make a case for auto-routing the high-confidence subset while keeping ambiguous items in the
  review queue.
- Stale deletions start removing things that turn out to have mattered, indicating the 14-day
  window is too short.
