# workspace/pages/ — page hierarchy and blueprints

A blueprint declares what a page contains and why, not what is written on it.

The authoritative page tree is [`_hierarchy.yaml`](_hierarchy.yaml). Every page in the
workspace appears there exactly once, whether or not it has a blueprint file.

---

## Composed and generated pages

| Kind | Blueprint | Content |
|---|---|---|
| **Composed** | `<id>.yaml` in this directory | Views, agent output, and navigation arranged into a purpose-built surface |
| **Generated** | None | Entirely the views of a single entity, generated from that entity's view set |

Sixteen pages are composed; the rest are generated. A blueprint that would only restate "show
this entity's views" adds no information and gives the structure somewhere to drift from
reality. Generated pages declare their `entity` in `_hierarchy.yaml` and nothing more.

Three composed pages — Command Center, Agents, and Taxonomy — are read-only projections from
the **repository** rather than from Notion databases, declared with a `source:` block. Their
content comes from `agents/_registry.yaml` and `core/taxonomy/`, because the repository is the
source of truth for what agents and taxonomies exist.

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

icon: "☀️"
class: rhythm
parent: home
order: 3
question: What matters right now?
owns_entities: []

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

## Required keys

Beyond the standard header contract, every blueprint declares:

| Key | Meaning |
|---|---|
| `class` | `root` · `rhythm` · `direction` · `domain` · `system` |
| `parent` | Parent page id; `null` for Home only |
| `order` | Explicit position among siblings |
| `question` | The single question this page exists to answer |
| `owns_entities` | Entities defined by this page — `[]` if it only projects others' data |

`owns_entities` is what keeps projection from becoming duplication. Career displays
professional contacts and Health displays health habits, but `people` is owned by
Relationships and `habits` by Goals. An entity is owned by exactly one page.

---

## Hierarchy rules

1. **`parent` defines the tree.** Exactly one page has no parent: `home`.
2. **`order` is explicit** among siblings. Never rely on filename order.
3. **Two clicks maximum** from Home to any surface.
4. **Maximum depth of three.** Deeper hierarchies stop being navigated.
5. **A page answers one question.** Three questions means three pages.

Rules 1–4 are enforced by `make hierarchy`. Rule 5 is enforced by review — it is the one a
machine cannot check.

---

## The hierarchy

See [Information architecture](../../docs/01-architecture/information-architecture.md) for the
full tree with page classes, and
[ADR-0005](../../docs/adr/0005-workspace-information-architecture.md) for why it is shaped this
way — including the renames from the original plan (`Family` → `Relationships`,
`AI Command Center` → `Command Center`) and the additions (`Inbox`, `Today`, `System`).

---

## Status

✅ **Phase 2** — hierarchy and sixteen composed blueprints complete.

Blueprints reference views, dashboards, and templates that arrive in Phases 3 and 5. These
forward references are expected; they are validated once the targets exist.
