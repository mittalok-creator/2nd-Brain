# automation/axiom/ — observability

Axiom is where the system reports on itself. Without it, a broken automation is discovered
weeks later by noticing that a habit streak looks wrong.

---

## What is instrumented

| Event | Emitted when | Answers |
|---|---|---|
| `automation.run` | Every automation finishes | Did it run? How long? What did it change? |
| `automation.error` | A step fails after retries | What broke, and where? |
| `agent.invocation` | An agent is called | Which agent, which tier, how many tokens, how long? |
| `sync.applied` | The specification syncs to Notion | What structural change landed? |
| `sync.drift` | Drift detection finds divergence | Where does live state contradict the spec? |
| `ritual.completed` | A daily or weekly ritual is finished by the human | Is the system actually being used? |

`ritual.completed` is the one that matters most. Automation health is easy to measure and
easy to over-value; whether the reviews are actually happening is the real signal of whether
the system is working.

---

## Event schema

Every event carries a common envelope so that unrelated events remain joinable:

```yaml
_time: 2026-07-26T21:00:04Z
event: automation.run
source: n8n
version: 1
correlation_id: 2026-07-26-evening-review
outcome: success              # success | partial | failure | skipped
duration_ms: 4210
payload:
  automation_id: evening_review
  trigger: schedule
  items_affected: 12
```

Rules:

- **No personal content in events.** Counts, ids, and durations — never the text of a journal
  entry, task title, or transaction description.
- **`correlation_id`** ties a ritual, the agent invocations it made, and the writes it
  produced into one traceable chain.
- **`version`** on every event, so the schema can evolve without breaking dashboards.

---

## Planned contents

| File | Holds |
|---|---|
| `event-schema.yaml` | The full event contract, per event type |
| `dashboards/` | Dashboard definitions: automation health, agent cost, ritual adherence |
| `alerts.yaml` | Alert rules and thresholds |

---

## Planned alerts

| Alert | Condition |
|---|---|
| Automation failing | Any automation fails twice consecutively |
| Ritual skipped | A daily ritual has no completion event for two days |
| Cost spike | Agent token spend exceeds twice its trailing weekly average |
| Sync drift | Drift detection reports any structural divergence |
| Silent automation | A scheduled automation emits no event within its expected window |

The last one is the important one. An automation that fails visibly gets fixed; an automation
that quietly stops running does not.

---

## Status

⬜ Populated in **Phase 7**.
