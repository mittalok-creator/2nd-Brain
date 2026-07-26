# Architecture Decision Records

An ADR captures a single architectural decision, the context that forced it, the
alternatives rejected, and the consequences accepted.

ADRs exist so that decisions are not re-litigated from memory. They are **append-only
history**: when a decision changes, write a new ADR that supersedes the old one. Never
rewrite an accepted ADR.

---

## Log

| # | Title | Status | Phase |
|---|---|---|---|
| [0001](0001-four-layer-architecture.md) | Four-layer architecture | Accepted | 1 |
| [0002](0002-naming-and-versioning.md) | Naming and versioning conventions | Accepted | 1 |
| [0003](0003-notion-as-projection.md) | Notion as a projection, not the source of truth | Accepted | 1 |
| [0004](0004-yaml-specification-format.md) | YAML as the specification format | Accepted | 1 |

---

## When to write one

Write an ADR when a decision:

- is expensive or disruptive to reverse,
- affects more than one layer of the architecture,
- rejects an obvious approach in favour of a less obvious one,
- or would otherwise be questioned again in six months.

Do **not** write one for routine implementation choices with a conventional answer.

## How to write one

```bash
cp docs/adr/_template.md docs/adr/0005-short-title.md
```

- Number sequentially, zero-padded to four digits. Numbers are never reused.
- Filename is `NNNN-kebab-case-title.md`.
- Status flows `Proposed` → `Accepted` → `Superseded by ADR-NNNN` or `Deprecated`.
- Add the new row to the log table above in the same commit.
- Keep it short. One page is usually enough; two is the practical maximum.
