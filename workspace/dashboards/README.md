# workspace/dashboards/ — dashboard compositions

A dashboard composes existing views and metrics to answer one question at one cadence. It
contains no new data definitions — only arrangement and emphasis.

---

## File format

```yaml
id: weekly_review
name: Weekly Review
version: 1.0.0
status: active
owner: workspace
description: >
  The thirty-minute weekly loop. Answers one question: am I moving on what I said mattered?

cadence: weekly
question: Am I moving on what I said mattered?
duration_minutes: 30

metrics:
  - id: goal_momentum
    name: Goal momentum
    source: goals.goal_progress
    aggregate: delta_week
    format: percent
    target: positive
    description: Change in average goal progress over the week.

  - id: habit_consistency
    name: Habit consistency
    source: habits.completion_rate
    aggregate: average
    format: percent
    target: { min: 80 }

  - id: tasks_slipped
    name: Slipped
    source: tasks
    aggregate: count
    filter: { all: [{ field: slipped_this_week, operator: is, value: true }] }
    target: { max: 5 }

sections:
  - title: Where things stand
    views: [goals_active, projects_stalled]

  - title: What slipped, and why
    views: [tasks_slipped_this_week]
    description: The slip reason is the point of this section.

  - title: Agent analysis
    agent: personal-ceo
    prompt: weekly-review

  - title: Write the review
    template: weekly-review-entry
```

---

## Keys

| Key | Meaning |
|---|---|
| `cadence` | `continuous` · `daily` · `weekly` · `monthly` · `quarterly` |
| `question` | The single question this dashboard exists to answer |
| `duration_minutes` | Intended time to work through it — a budget, and a design constraint |
| `metrics` | Headline figures shown at the top, with targets |
| `sections` | Ordered blocks of views, agent output, and templates |

Each metric declares a `target` so a number is never shown without a judgement attached:
`positive`, `negative`, `{ min: n }`, `{ max: n }`, or `{ range: [a, b] }`. A figure with no
target cannot be acted on.

---

## Planned dashboards

| Dashboard | Cadence | Question |
|---|---|---|
| Executive | Continuous | What is the state of everything? |
| Today | Daily | What matters right now? |
| Weekly Review | Weekly | Am I moving on what I said mattered? |
| Monthly Review | Monthly | Is the direction still right? |
| Finance | Weekly | Am I financially on track? |
| Health | Daily | Am I looking after the machine? |
| Learning | Weekly | Am I getting better at something specific? |
| Career | Monthly | Am I building toward the next step? |
| Projects | Weekly | What is moving, what is stuck? |
| Command Center | On demand | What can the agents do for me? |

---

## Design rules

1. **One question per dashboard.** Stated in the `question` field, and enforced by review.
2. **Metrics before lists.** Three to five headline figures, then the detail behind them.
3. **Every metric has a target.** Otherwise it is decoration.
4. **Respect the duration budget.** If a review consistently overruns, the dashboard is
   asking too much and must be cut.
5. **Emphasis is scarce.** If everything is highlighted, nothing is.
6. **Empty is a valid state, and should look intentional.**

---

## Status

⬜ Populated in **Phase 5**.
