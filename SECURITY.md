# Security Policy

2nd Brain holds the specification for a system that touches personal calendars, mail,
finances, health notes, and journals. The repository itself must therefore never hold
data or credentials — only structure.

---

## What Belongs in This Repository

| ✅ Commit | ❌ Never commit |
|---|---|
| Schemas, relations, taxonomies | Journal entries, notes, transactions |
| Page and dashboard blueprints | Notion page IDs tied to private content |
| Agent definitions, prompts, SOPs | API keys, tokens, OAuth secrets |
| Automation logic and workflow graphs | n8n credential exports, `.env` files |
| Documentation and design tokens | Health records, financial statements |
| Anonymised example data | Real personal data of any kind |

`.gitignore` blocks the common offenders (`.env`, `*.key`, `*.pem`, `secrets/`,
`**/credentials*.json`, exports). Treat that as a safety net, not a policy.

---

## Secrets Handling

- Local development reads from `.env`, created from [`.env.example`](.env.example).
- CI and automations read from GitHub Actions secrets or the runtime's own secret store.
- n8n workflows are exported **without** credentials; credentials are re-bound on import.
- Rotate any credential that has ever been pasted into a chat, log, or issue.

---

## Least Privilege

Grant each integration the narrowest scope that works:

| Integration | Guidance |
|---|---|
| Notion | Share only the 2nd Brain workspace root with the integration |
| Google | Prefer read-only scopes; grant write only where an automation requires it |
| GitHub | Fine-grained token limited to this repository |
| n8n / Axiom | Separate credentials per workflow so one can be revoked alone |
| AI providers | Disable training on submitted data where the provider allows it |

---

## AI-Specific Considerations

- **Prompt injection.** Content fetched from mail, web pages, or documents is untrusted
  input. Agents must treat it as data to analyse, never as instructions to follow.
- **Data minimisation.** Send an agent the smallest context that answers the question.
- **Sensitive domains.** Health and finance agents operate on summaries and aggregates by
  default; raw records are opt-in per invocation.
- **Human in the loop.** Any irreversible or outward-facing action — sending mail, deleting
  records, moving money — requires explicit confirmation.

---

## Reporting a Vulnerability

Found a security issue in this specification, its automations, or its tooling?

Open a [private security advisory](https://github.com/mittalok-creator/2nd-Brain/security/advisories/new)
rather than a public issue. Include a description, reproduction steps, and impact.

Expect an initial response within seven days.

---

## If a Secret Leaks

1. Revoke and rotate the credential immediately — before touching git history.
2. Remove it from history (`git filter-repo`) and force-push.
3. Audit provider logs for use during the exposure window.
4. Record the incident and its fix in `CHANGELOG.md` without restating the secret.

Rotation comes first. History rewriting does not un-leak a key that has already been read.
