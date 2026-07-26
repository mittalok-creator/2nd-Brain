# ADR-0004 — YAML as the specification format

| | |
|---|---|
| **Status** | Accepted |
| **Date** | 2026-07-26 |
| **Phase** | Phase 1 — Repository Architecture |
| **Supersedes** | — |
| **Superseded by** | — |

## Context

Everything in `core/`, `workspace/`, and much of `agents/` and `automation/` is structured
data that must be readable by three audiences at once:

- **A human** reviewing a diff months later, deciding whether a change is correct.
- **Tooling** — the validator, the Notion sync adapter, diagram generators.
- **AI agents** reading the specification as context in order to operate on the system.

The format choice affects all three. It needs to diff cleanly line by line, support
comments (the *why* next to the *what*), express nesting without ceremony, and be parseable
from any language without a custom parser.

## Decision

**YAML for all specifications. Markdown for all prose. JSON only for machine interchange.**

| Content | Format | Location |
|---|---|---|
| Entities, relations, taxonomy, design tokens | YAML | `core/` |
| Page, dashboard, view, template definitions | YAML | `workspace/` |
| Agent definitions | YAML | `agents/*/agent.yaml` |
| Agent prompts and SOPs | Markdown | `agents/*/prompt.md`, `sop.md` |
| Automation definitions | YAML | `automation/` |
| n8n workflow exports | JSON | `automation/n8n/` (vendor format, not hand-edited) |
| Documentation | Markdown | `docs/`, all `README.md` |

Conventions: two-space indent, no tabs, `snake_case` keys, block scalars (`>`) for prose
fields, comments used to record intent rather than restate the key.

Prompts are Markdown files rather than YAML string blocks. Prompts are prose — they are
long, they are edited frequently, and they must diff readably word by word. Embedding them
in YAML would make every prompt revision a single-line diff and invite escaping bugs.

## Alternatives considered

### JSON

Universal, unambiguous, no parser needed anywhere. Rejected on two grounds that matter for a
specification maintained by hand: **no comments**, so the reasoning behind a field cannot
live next to the field; and heavy punctuation noise, which makes a hand-authored schema
tiring to read and diffs harder to scan. JSON stays where a machine produces it.

### TOML

Comments, unambiguous types, excellent for flat configuration. Rejected because the data
here is deeply nested — entities contain fields, fields contain constraints and options.
TOML's nested-table syntax becomes hard to follow past two levels, which is where these
specs start.

### Markdown with front matter

Attractive because it renders natively on GitHub and reads well as documentation. Rejected
because it blurs the line between specification and prose. A schema is not a document, and
front matter tempts contributors to put the real definition in the prose body where tooling
cannot reach it.

### A custom DSL

Maximum expressiveness and tailored validation. Rejected as unjustifiable: it needs a
parser, an editor mode, and documentation, and every AI agent reading the repository would
need to learn it before being useful. YAML is already understood by every tool and model
that will touch this system.

### TypeScript or Python as the definition language

Real types, real IDE support, programmatic composition. Genuinely tempting, and the right
answer for a larger engineering system.

Rejected because it makes the specification executable, and an executable specification can
be conditional. Conditional structure is exactly what must not happen here: the whole value
of `core/` is that it can be read as a static description of the system. Static data also
keeps the barrier to editing low — a spec change should not require a runtime.

## Consequences

**Positive**

- Comments live next to the fields they explain, so intent survives in the file itself.
- Clean, reviewable line-by-line diffs.
- Parseable from Python, JavaScript, n8n, and GitHub Actions with no custom tooling.
- AI agents parse YAML reliably and generate it accurately.
- Low editing barrier — a text editor is sufficient.

**Negative**

- YAML has real sharp edges: significant whitespace, the Norway problem (`no` parsing as
  `false`), tab intolerance, and surprising type coercion. Mitigated by requiring quoted
  values for anything ambiguous and by parsing every file in CI.
- No static type checking. Mitigated by the validator, extended in Phase 3 to enforce
  field-level contracts rather than just the header.

**Neutral / accepted trade-offs**

- Two formats coexist (YAML for structure, Markdown for prose). The split is drawn on a
  clear line — structured data versus prose — so file placement is never ambiguous.
- JSON appears in `automation/n8n/` as a vendor export. These files are generated, not
  authored, and are excluded from the header contract.

## Revisit when

- Specifications grow complex enough that hand-maintained YAML becomes error-prone despite
  validation — the signal would be repeated defects caused by malformed specs rather than
  by wrong ones. A JSON Schema per spec type is the next step before considering a DSL.
- A generated JSON Schema becomes necessary for editor autocompletion; that is additive and
  would not change this decision.
