# config/ — system configuration

Configuration that is not part of the specification: which providers are connected, how model
tiers resolve, and deployment-specific identifiers.

The distinction from `core/`: `core/` describes **the system**; `config/` describes **this
installation of it**. Two people running 2nd Brain share `core/` and differ here.

---

## Planned contents

| Path | Holds |
|---|---|
| `providers/` | One definition per integration: capabilities, auth method, rate limits |
| `models.yaml` | Tier → concrete model mapping, per provider |
| `system.yaml` | Timezone, locale, week start, currency, working hours |
| `notion.yaml` | Deployment ids for synced Notion objects *(git-ignored where private)* |

---

## Model tier resolution

Agents declare a tier, never a model. This file is the only place a concrete model id appears,
which is what keeps every agent definition stable as models change.

```yaml
tiers:
  reasoning:
    anthropic: claude-opus-5
    openai: gpt-5
    google: gemini-2.5-pro
  balanced:
    anthropic: claude-sonnet-5
    openai: gpt-5-mini
    google: gemini-2.5-flash
  fast:
    anthropic: claude-haiku-4-5-20251001
    openai: gpt-5-nano
    google: gemini-2.5-flash-lite

default_provider: anthropic
```

Adding a provider or upgrading a model is then a change to one file, with no effect on any
agent definition.

---

## Provider definitions

```yaml
id: notion
name: Notion
version: 1.0.0
status: active
owner: config
description: >
  Primary workspace surface. Renders the specification as pages and databases.

capabilities: [read, write, search, schema_management]
auth:
  method: integration_token
  env: NOTION_API_KEY
rate_limits:
  requests_per_second: 3
  batch_size: 100
constraints:
  - Some property type changes cannot be applied in place and require a migration.
```

---

## Rules

1. **No secrets here.** Configuration references environment variable *names*; values live in
   `.env` and in secret stores. See [SECURITY.md](../SECURITY.md).
2. **No private identifiers committed.** Notion page ids pointing at private content are
   deployment state, git-ignored, not specification.
3. **`core/` never reads `config/`.** The specification cannot depend on the installation.
4. **A new provider must not require a schema change.** If it does, the abstraction is leaking
   and needs an ADR.

---

## Status

⬜ Populated in **Phase 3** (providers, models) and **Phase 7** (automation configuration).
