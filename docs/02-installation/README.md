# Installation

Getting from an empty workspace to a running 2nd Brain.

> **Status** — Phase 1. Repository setup below is complete and works today. Notion
> provisioning, agent registration, and automation deployment are filled in by Phases 2–7.

---

## Prerequisites

| Requirement | Notes |
|---|---|
| Git | Any recent version |
| Python 3.11+ | For the validator and sync tooling |
| GitHub account | The repository is the source of truth |
| Notion account | Any plan; the API is available on free tiers |
| At least one AI provider | Claude, ChatGPT, or Gemini |
| n8n *(optional)* | Cloud or self-hosted; needed from Phase 7 |
| Axiom *(optional)* | Observability; needed from Phase 7 |

---

## 1. Clone and validate

```bash
git clone https://github.com/mittalok-creator/2nd-Brain.git
cd 2nd-Brain
```

Install the tooling dependencies and confirm the specification is well-formed:

```bash
pip install -r scripts/requirements.txt
make validate
```

Expected output:

```
2nd Brain — specification validation
→ structure
→ yaml
→ links

✓ specification valid (0 warning(s))
```

If this fails, the specification is broken — fix it before going further. See
[Troubleshooting](../troubleshooting.md).

---

## 2. Configure the environment

```bash
cp .env.example .env
```

Fill in only what you need right now. Every variable is optional until the phase that uses
it ships, and the validator does not require any of them.

Minimum for local work: nothing.
Minimum to sync Notion: `NOTION_API_KEY`, `NOTION_ROOT_PAGE_ID`.
Minimum to run agents: one provider key.

`.env` is git-ignored. Never commit it. See [SECURITY.md](../../SECURITY.md).

---

## 3. Create the Notion integration

1. Open <https://www.notion.so/my-integrations> and create an internal integration.
2. Copy the integration secret into `NOTION_API_KEY`.
3. Create a single page in Notion to act as the workspace root — name it **2nd Brain**.
4. Share that page with the integration (`•••` → *Connections* → your integration).
5. Copy the page id from its URL into `NOTION_ROOT_PAGE_ID`.

Share **only** the root page. Everything the system creates lives beneath it, so this grants
the narrowest workable scope.

---

## 4. Provision the workspace

> ⬜ **Phase 2–3.** The sync adapter that reads `core/` and `workspace/` and provisions the
> Notion workspace does not exist yet. Until then the specification is the deliverable and
> the workspace is built by following the blueprints in `workspace/pages/` manually.

---

## 5. Register the AI agents

> ⬜ **Phase 6.** Agent definitions, the shared memory protocol, and per-provider prompt
> packaging land here.

---

## 6. Deploy the automations

> ⬜ **Phase 7.** n8n workflow imports, GitHub Actions schedules, and Axiom datasets.

---

## Verifying the install

| Check | Command | Phase |
|---|---|---|
| Specification is valid | `make validate` | 1 ✅ |
| Notion workspace matches the spec | `make sync-check` | 3 |
| Agents respond correctly | `make agent-test` | 6 |
| Automations run end to end | `make automation-dryrun` | 7 |

---

## Upgrading

```bash
git pull origin main
make validate
```

Read `CHANGELOG.md` before upgrading. A **MAJOR** version bump means existing workspace
state requires migration; migration notes ship in the same release.

---

## Uninstalling

The repository holds no personal data, so removing the system is safe:

1. Revoke the Notion integration and every provider credential.
2. Delete or archive the Notion root page — your content lives there, so export first if
   you want to keep it.
3. Delete the local clone.
