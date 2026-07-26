# automation/ — the execution layer

How the system runs itself: the rituals, trackers, and capture pipelines that keep 2nd Brain
current without manual maintenance.

---

## Layout

| Directory | Holds |
|---|---|
| [`recipes/`](recipes/README.md) | Platform-neutral automation definitions — the source of truth |
| [`n8n/`](n8n/README.md) | n8n workflow exports (JSON, credential-free) |
| [`actions/`](actions/README.md) | GitHub Actions workflows operating on the repository |
| [`axiom/`](axiom/README.md) | Observability: event schema, dashboards, alerts |

A **recipe** declares what an automation does, its trigger, and its idempotency strategy. The
platform directories hold the implementation. The recipe is reviewable; the export is not.

---

## Platform selection

| Platform | Use for | Avoid for |
|---|---|---|
| **n8n** | Multi-step flows across services; branching, retries, human-in-the-loop | Trivial one-step jobs |
| **GitHub Actions** | Repository work: validation, sync, drift detection, releases | Anything needing personal-account credentials |
| **Axiom** | Event ingestion, dashboards, alerting | Orchestration |
| **Notion automations** | Purely in-Notion side effects | Anything touching an external service |

Default to n8n for rituals, Actions for repository work.

---

## Non-negotiable rules

1. **Idempotent.** Running twice for the same period converges to the same state. Every recipe
   declares how — an upsert key, a date-scoped lookup, or an explicit run marker.
2. **Fails loudly.** A silent failure is worse than no automation. Failures emit to Axiom and
   notify.
3. **Retries with backoff** on transient errors only. Logic errors fail immediately.
4. **No credentials in the repository.** n8n exports exclude them; they are re-bound on import.
5. **Confirmation before irreversible action.** Sending mail, deleting records, moving money.
6. **Bounded cost.** Any automation invoking a model declares its tier and expected volume.
7. **Observable.** Every run emits: automation id, trigger, duration, outcome, items affected.

---

## Recipe format

```yaml
id: evening_review
name: Evening Review
version: 1.0.0
status: active
owner: automation
description: >
  Closes the day: logs what happened, closes completed work, and captures why anything
  slipped. The slip reason is the input to the weekly review.

platform: n8n
trigger:
  type: schedule
  cron: "0 21 * * *"
  timezone: Asia/Kolkata

idempotency:
  strategy: date_scoped_upsert
  key: [journal.date]
  description: >
    One journal entry per date. A second run updates that entry rather than creating another.

steps:
  - id: gather
    action: Read today's tasks, habits, and calendar events.
  - id: draft
    action: Invoke the Life Coach agent to draft the day's log.
    agent: life-coach
    model_tier: balanced
  - id: write
    action: Upsert the journal entry for today.
  - id: notify
    action: Send a summary notification.

on_failure:
  retries: 3
  backoff: exponential
  notify: true
  fallback: >
    Leave the journal entry uncreated rather than creating a partial one. A missing entry is
    obvious; a half-written one is not.

observability:
  event: automation.run
  fields: [automation_id, trigger, duration_ms, outcome, items_affected]
```

---

## Planned automations

Full list with triggers and outputs in the
[Automation Guide](../docs/06-automation-guide/README.md).

**Rituals** — Morning Planning · Evening Review · Weekly Review · Monthly Review
**Trackers** — Goals · Habits · Reading · Expenses · Health · Learning
**Capture** — Meeting Notes · Knowledge · Bookmarks · Documents · Project Review

---

## Status

⬜ Populated in **Phase 7**. Rules and recipe format above are settled from Phase 1.
