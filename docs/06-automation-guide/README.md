# Automation Guide

Building, scheduling, and debugging the automations that run 2nd Brain.

> **Status** — ⬜ Written in Phase 7. The platform split and the rules below are settled and
> constrain every automation that gets built.

---

## Which platform for what

Four execution environments, each with a clear remit. Choosing correctly is most of the
design work.

| Platform | Use it for | Avoid it for |
|---|---|---|
| **n8n** | Multi-step flows across services; anything with branching, retries, or human-in-the-loop | Trivial one-step jobs |
| **GitHub Actions** | Anything operating on the repository: validation, sync, drift detection, releases | Anything needing credentials to personal accounts |
| **Axiom** | Observability — event ingestion, dashboards, alerting on failures and streaks | Orchestration |
| **Notion automations** | Purely in-Notion side effects with no external dependency | Anything needing an external service |

Default to n8n for rituals, Actions for repository work.

---

## Non-negotiable rules

1. **Idempotent.** Running an automation twice for the same period converges to the same
   state. Every automation declares how: an upsert key, a date-scoped lookup, or an explicit
   run marker.
2. **Fails loudly.** A silent failure is worse than no automation. Failures emit to Axiom
   and notify.
3. **Retries with backoff.** Transient network and rate-limit errors retry; logic errors do
   not.
4. **No credentials in the repository.** n8n workflows are exported without credentials and
   re-bound on import.
5. **Confirmation before irreversible action.** Sending mail, deleting records, or moving
   money requires a human gate.
6. **Bounded cost.** Any automation invoking a model declares its tier and expected token
   volume.
7. **Observable.** Every run emits a structured event: automation id, trigger, duration,
   outcome, items affected.

---

## Planned automations

**Rituals**

| Automation | Trigger | Produces |
|---|---|---|
| Morning Planning | Daily, early | A drafted plan on the Today dashboard |
| Evening Review | Daily, night | A logged day, closed tasks, slip reasons captured |
| Weekly Review | Weekly | A written review with progress metrics |
| Monthly Review | Monthly | Trend analysis and goal viability assessment |

**Trackers**

| Automation | Trigger | Produces |
|---|---|---|
| Goal Tracking | Data change | Recalculated progress and health per goal |
| Habit Tracking | Daily | Streaks, consistency rate, break detection |
| Reading Progress | Data change | Position, pace, and projected finish |
| Expense Logging | Webhook / manual | Categorised transactions linked to goals |
| Health Tracking | Daily | Metrics rolled up against targets |
| Learning Capture | Data change | Course and skill progress |

**Capture**

| Automation | Trigger | Produces |
|---|---|---|
| Meeting Notes | Calendar event ends | A structured note with actions extracted |
| Knowledge Capture | Inbox item | A routed, tagged, linked knowledge entry |
| Bookmark Processing | Webhook | A summarised, tagged bookmark |
| Document Intake | Drive / OneDrive change | An indexed document record |
| Project Review | Weekly | Per-project status and stall detection |

---

## Sections planned for Phase 7

- Authoring a workflow: structure, naming, and the definition format
- Trigger design: cron, webhook, data change, and chaining
- Idempotency patterns, with worked examples per trigger type
- Error handling, retry policy, and dead-letter handling
- Secrets and credential binding on import
- Observability: the event schema, Axiom dashboards, and alert thresholds
- Cost control for model-invoking automations
- Testing: the dry-run harness and fixture data
- Debugging a failed run, and safely replaying it

---

## Related

- [`automation/README.md`](../../automation/README.md) — file layout and conventions
- [AI Guide](../04-ai-guide/README.md) — agents invoked from automations
- [SECURITY.md](../../SECURITY.md) — credentials and least privilege
