# automation/actions/ — GitHub Actions automations

Reusable workflows and composite actions that operate on **the repository itself**:
validation, syncing the specification to Notion, drift detection, and releases.

Workflows that run on repository events live in `.github/workflows/` — GitHub requires that
location. This directory holds the reusable pieces they call, so the logic is shared rather
than copy-pasted across workflow files.

---

## Division of responsibility

| Runs here | Runs in n8n |
|---|---|
| Specification validation | Personal rituals and reviews |
| Specification → Notion sync | Anything reading mail or calendar |
| Drift detection | Expense and health capture |
| Diagram and doc generation | Anything needing personal-account credentials |
| Tagging and releases | Anything with human-in-the-loop steps |

The dividing line is credentials. GitHub Actions holds repository-scoped and integration
tokens. It does not hold broad personal-account access — that stays in n8n, where scope is
bound per workflow and revocable individually.

---

## Planned workflows

| Workflow | Trigger | Does |
|---|---|---|
| `ci.yml` ✅ | Push, PR | Validates structure, YAML, links, hygiene, commits |
| `labels.yml` ✅ | `labels.yml` changes | Applies the label taxonomy |
| `sync-notion.yml` | Manual, or push to `main` | Provisions Notion from the specification |
| `drift-check.yml` | Daily | Reports where live Notion diverges from the specification |
| `generate-diagrams.yml` | `core/relations/` changes | Regenerates the entity-relationship diagram |
| `release.yml` | Tag push | Builds release notes from the changelog |

---

## Conventions

- **Least privilege.** Declare `permissions:` explicitly in every workflow; default to
  `contents: read` and add only what is needed.
- **Pin actions by major version** (`actions/checkout@v4`). Dependabot proposes the bumps.
- **Fail loudly.** Never `continue-on-error` on a validation step.
- **Idempotent.** A workflow re-run must not double-apply its effect.
- **No secrets in logs.** Never echo an environment variable that may hold one.
- **Concurrency groups** on anything that writes, so two runs cannot race.

---

## Status

🚧 `ci.yml` and `labels.yml` are live from **Phase 1**. Sync and drift detection land in
**Phases 3** and **9**.
