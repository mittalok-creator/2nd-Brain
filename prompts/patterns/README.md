# prompts/patterns/ — reusable prompt structures

A pattern is the skeleton of a prompt: the arrangement of role, context, task, constraints,
and output contract that a class of task needs. Library prompts and agent prompts are built
from patterns rather than written from scratch.

Patterns exist so that an improvement discovered in one prompt can be applied to every prompt
of that shape.

---

## Planned patterns

| Pattern | For |
|---|---|
| `extract-structured` | Pull defined fields out of unstructured text — meeting notes, emails, articles |
| `summarise-with-fidelity` | Condense while preserving specifics, numbers, and named entities |
| `analyse-and-recommend` | Review data, then propose a small number of ranked actions |
| `classify-with-taxonomy` | Assign values from a controlled vocabulary in `core/taxonomy/` |
| `critique` | Argue against a plan or decision to surface what it assumes |
| `synthesise-across-sources` | Combine several records into one coherent conclusion |
| `draft-from-template` | Produce content matching a `workspace/templates/` structure |
| `review-period` | The shared skeleton behind daily, weekly, and monthly reviews |

---

## Pattern file format

```markdown
# Pattern — Extract Structured

> **Version** 1.0.0 · **Status** active

## When to use
The class of task this fits, and the class it does not.

## Structure
The ordered sections a prompt of this shape must contain, and why each is present.

## Skeleton
The reusable text, with {{placeholders}} for the task-specific parts.

## Known failure modes
What goes wrong with this shape, and the instruction that prevents it.

## Prompts using this pattern
Links, so an improvement here can be propagated.
```

---

## Why patterns are separate from prompts

Prompt quality problems repeat. The same missing constraint causes the same failure across
every extraction prompt, every summarisation prompt. Fixing it once in the pattern and
propagating is tractable; rediscovering it in fifteen files is not.

The `Known failure modes` section is the point of this directory. It is where hard-won
knowledge about what actually goes wrong accumulates.

---

## Status

⬜ Populated in **Phase 6**.
