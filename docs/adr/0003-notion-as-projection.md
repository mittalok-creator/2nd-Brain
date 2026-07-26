# ADR-0003 — Notion as a projection, not the source of truth

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-07-26 |
| **Phase** | Phase 1 — Repository Architecture |
| **Supersedes** | — |
| **Superseded by** | — |

## Context

Notion is the primary interface for this system: it is where pages are read, tasks are
checked off, journals are written, and dashboards are viewed. The obvious approach is to
build the system in Notion and treat the repository as documentation and backup.

That approach has known failure modes, all of which have been observed in practice with
Notion-based personal systems:

- **No diff, no history, no review.** A structural change to a database cannot be reviewed
  before it lands, and cannot be reverted cleanly afterwards.
- **No reproducibility.** Rebuilding the workspace — after a mistake, or in a new account —
  means manual reconstruction from memory or screenshots.
- **Vendor risk.** Pricing changes, API changes, account loss, or a better tool arriving in
  three years all threaten the whole system rather than one layer of it.
- **API surface limits.** Not every Notion construct is fully addressable through the API;
  a Notion-first design silently becomes dependent on manual steps.
- **AI agents need structure, not screens.** Agents operate far more reliably against an
  explicit schema than against whatever the API happens to return.

At the same time, Notion genuinely is the best available surface today, and pretending
otherwise by building a worse custom UI would make the system unusable in daily life.

## Decision

**The repository is the source of truth. Notion is a projection of it.**

Concretely:

1. `core/` declares entities, fields, relations, and taxonomy in vendor-neutral terms.
   `workspace/` declares the page hierarchy, dashboards, and views in the same terms.
2. Notion is populated by syncing from those declarations. A sync is idempotent: running it
   repeatedly converges on the declared state.
3. Structural changes are made in the repository first, reviewed, then synced.
   A structural change made directly in Notion that contradicts the specification is
   treated as a defect.
4. **Content** — journal entries, tasks, notes, transactions — is created and edited freely
   in Notion. Notion owns the rows; the repository owns the columns.
5. `core/` contains no Notion-specific types. Abstract field types (`text`, `number`,
   `select`, `multi_select`, `date`, `relation`, `rollup`, `formula`, `checkbox`, `url`,
   `person`, `file`) are mapped to vendor types at sync time by an adapter.
6. Notion identifiers (page ids, database ids) are treated as deployment state, held in
   configuration and git-ignored where they point at private content — never as part of the
   specification.

The structure/content split is the load-bearing distinction. Structure is code; content is
data. Only structure is versioned here.

## Alternatives considered

### Notion-first, repository as documentation

Build in the UI, describe it in Markdown afterwards. Fastest to start and the most common
approach.

Rejected because the documentation is guaranteed to fall out of sync — it has no mechanism
forcing it to stay true — and because it solves none of the reproducibility or vendor-risk
problems. The repository would become a stale description of a system living elsewhere.

### Two-way sync between the repository and Notion

Structural changes made in either place propagate to the other. Superficially the most
convenient option.

Rejected as the worst of the available choices. Two-way structural sync requires conflict
resolution over schema changes, which needs a merge policy nobody wants to define or debug.
It also destroys the invariant that makes review meaningful: if Notion can change the
specification, the specification is not authoritative, and a code review no longer tells
you what the system does. One-way flow is a feature.

### Custom application instead of Notion

Full control, no vendor risk, arbitrary UI. Rejected on effort and quality: a hand-built
personal app would take months to reach a fraction of Notion's editing, mobile, and
collaboration quality, and would then need maintaining forever. The point of this
architecture is that the surface is cheap to swap — which means there is no need to own it.

### Notion API responses as the schema

Let the API shape define the model; generate specs by export. Rejected because it inverts
the dependency the wrong way and imports vendor concepts into `core/` permanently.

## Consequences

**Positive**

- The entire workspace is reproducible from the repository.
- Structural change is reviewable, diffable, and revertible.
- Replacing Notion means writing one adapter, not redesigning the system.
- Agents read a stable, explicit schema instead of inferring structure from API responses.
- Vendor risk is contained to a single, thin layer.

**Negative**

- A structural change is slower: edit spec → validate → sync, instead of clicking in the
  UI. Accepted deliberately; structural changes *should* be slower than content changes.
- A sync adapter must be built and maintained. This is the real cost of the decision.
- Discipline is required not to make structural edits directly in Notion. Phase 9 adds
  drift detection so the specification can be checked against reality automatically.

**Neutral / accepted trade-offs**

- Some Notion features may not be expressible in vendor-neutral terms. Where that happens,
  a documented `notion:` extension block on the relevant spec carries the vendor-specific
  detail, keeping the escape hatch explicit and auditable rather than pervasive.

## Revisit when

- Drift detection shows repeated structural edits happening in Notion, indicating the
  spec-first workflow is too slow for real use.
- A second surface is added, at which point the adapter boundary should be re-examined.
- Notion ships a first-class schema-as-code capability that makes the adapter redundant.
