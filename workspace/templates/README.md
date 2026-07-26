# workspace/templates/ — page and entry templates

A template is the structure a new entry starts with. Its job is to make the right thing easy
to write and the important field impossible to skip.

---

## File format

```yaml
id: decision-entry
name: Decision
version: 1.0.0
status: active
owner: workspace
description: >
  Captures a significant decision at the moment it is made, before the outcome is known and
  hindsight distorts the reasoning.

entity: decision_journal

prefill:
  decided_on: today
  reversibility: reversible

blocks:
  - type: heading
    text: The decision

  - type: prompt
    text: State it as a decision, not as a question.

  - type: heading
    text: Why

  - type: prompt
    text: What do you believe that makes this the right call?

  - type: heading
    text: What you expect to happen

  - type: prompt
    text: Be specific enough that you could later be shown to have been wrong.

  - type: heading
    text: What would change your mind

  - type: prompt
    text: Name the evidence that would make you reverse this.

  - type: heading
    text: Review

  - type: prompt
    text: When should this be checked against reality?
```

---

## Planned templates

| Template | Entity | Used by |
|---|---|---|
| `daily-log` | Journal | Evening review |
| `weekly-review-entry` | Reviews | Weekly review dashboard |
| `monthly-review-entry` | Reviews | Monthly review dashboard |
| `project-brief` | Projects | Project creation |
| `meeting-note` | Meetings | Meeting Notes automation |
| `knowledge-note` | Knowledge | Knowledge capture |
| `book-note` | Reading | Reading Assistant |
| `decision-entry` | Decision Journal | Decision Assistant |
| `goal-definition` | Goals | Goal setting |
| `habit-definition` | Habits | Habit design |

---

## Conventions

1. **Prompts, not placeholders.** A question a person answers beats greyed-out example text.
2. **Prefill everything derivable.** Dates, areas, and links should already be filled in.
3. **Put the hard question first.** The section most likely to be skipped goes at the top,
   while attention is highest.
4. **Short.** A template long enough to feel like a form does not get used. Five sections is
   usually the limit.
5. **Structure mirrors review.** A template's sections should map to what the corresponding
   review reads, so writing it is never wasted effort.

---

## Status

⬜ Populated in **Phase 5**, alongside the dashboards that invoke them.
