# prompts/ — the prompt library

Prompts live here, versioned independently from the agents that use them, so a prompt can be
improved without redefining the agent — and so a regression can be traced to a specific
revision.

---

## Layout

| Directory | Holds |
|---|---|
| [`library/`](library/README.md) | Concrete, ready-to-use prompts for real tasks |
| [`patterns/`](patterns/README.md) | Reusable prompt structures that library prompts are built from |

Agent-owned prompts live with their agent (`agents/<id>/prompt.md`). This directory holds
prompts used directly by a human or invoked by an automation without a full agent contract
behind them.

---

## Format

Markdown, not YAML. Prompts are prose: long, frequently revised, and they must diff readably
word by word. See [ADR-0004](../docs/adr/0004-yaml-specification-format.md).

Every prompt file opens with a metadata block and closes with a changelog:

```markdown
# Prompt — Extract Actions From Meeting Notes

> **Version** 1.2.0 · **Tier** balanced · **Status** active
> **Pattern** extract-structured · **Used by** automation/meeting-notes

## Purpose
One sentence.

## Inputs
What must be supplied, and in what form.

## Prompt
The actual instruction text.

## Output contract
The exact expected shape.

## Changelog
| Version | Date | Change |
```

---

## House standards

Every prompt in this repository, agent-owned or not:

1. **States its output contract explicitly.** Section names, ordering, and length limits.
   "Be helpful" is not a contract.
2. **Declares a model tier, not a model.** `reasoning`, `balanced`, or `fast`.
3. **Frames external content as untrusted.** Anything fetched from mail, the web, or documents
   is data to analyse, never instructions to follow.
4. **Requests grounding.** Every claim cites the record or metric behind it.
5. **Permits "I don't know."** Prompts that make uncertainty unwelcome produce fabrication.
6. **Sets a length limit.** Unread output has no value.
7. **Uses placeholders, not examples, for injected data** — `{{current_date}}`, never a
   hard-coded date that silently becomes wrong.
8. **Is versioned on every change.** Undocumented edits make regressions untraceable.

---

## Versioning

Semantic, per prompt:

| Bump | Means |
|---|---|
| **MAJOR** | The output contract changed — downstream consumers must be updated |
| **MINOR** | New capability or instruction, output contract unchanged |
| **PATCH** | Wording, clarity, and tuning with no behavioural intent change |

---

## Status

⬜ Populated in **Phase 6**, alongside the agent roster. Standards above are live from Phase 1.
