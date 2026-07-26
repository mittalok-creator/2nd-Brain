# workspace/pages/ — page hierarchy and blueprints

One file per page. A blueprint declares what a page contains and why, not what is written on
it.

---

## File format

```yaml
id: today
name: Today
version: 1.0.0
status: active
owner: workspace
description: >
  The single page opened every morning and evening. Answers one question: what matters
  right now?

parent: home
icon: "☀️"
order: 1

blocks:
  - type: heading
    text: Today

  - type: callout
    content: agent_output
    agent: personal-ceo
    description: The plan drafted overnight, accepted or adjusted in the morning.

  - type: view
    view: tasks_due_today          # references workspace/views/
    title: Due today

  - type: view
    view: habits_today
    title: Habits

  - type: view
    view: calendar_today
    title: Schedule

  - type: divider

  - type: view
    view: inbox_unrouted
    title: Inbox
    description: Routed during the evening review, not during the day.
```

---

## Block types

| Type | Renders |
|---|---|
| `heading` | A section heading |
| `text` | Static prose |
| `callout` | Emphasised block, optionally fed by an agent |
| `view` | An embedded database view from `workspace/views/` |
| `dashboard` | An embedded dashboard from `workspace/dashboards/` |
| `link` | Navigation to another page |
| `columns` | A horizontal split containing nested blocks |
| `divider` | Visual separation |
| `template_button` | Creates an entry from a template |
| `agent_action` | Invokes an agent |

---

## Hierarchy rules

1. **`parent` defines the tree.** Exactly one page has no parent: `home`.
2. **`order` is explicit** among siblings. Never rely on filename order.
3. **Two clicks maximum** from Home to any surface.
4. **Maximum depth of three.** Deeper hierarchies stop being navigated.
5. **A page answers one question.** Three questions means three pages.

---

## Planned hierarchy

The shape proposed for Phase 2 — names are finalised there, and deliberately diverge from
the initial sketch where a better structure exists:

```
🏠 Home
├── ☀️  Today
├── 🎯 Goals
├── 📅 Planner
├── 🚀 Projects
├── 🧠 Knowledge
├── 📚 Learning
├── 💼 Career
├── 💰 Finance
├── 🏋 Health
├── 👨‍👩‍👧 Family
├── 📊 Reviews
├── 🤖 Command Center
└── ⚙️  System
```

Two changes from the original list, to be justified by ADR in Phase 2:

- **AI Command Center → Command Center.** Everything here is AI-driven; the qualifier adds
  length without information.
- **A `System` page is added.** Somewhere has to hold the prompt library, the taxonomy
  reference, and configuration. Without it, meta-content leaks into life-area pages.

---

## Status

⬜ Populated in **Phase 2**.
