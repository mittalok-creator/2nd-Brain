# agents/ — the intelligence layer

An agent here is **not** a chat window with a system prompt. It is a defined operator with a
fixed contract, a bounded scope, and a written standard operating procedure.

---

## Layout

```
agents/
├── _registry.yaml          Capability routing — which agent handles what
├── _template/              Copy this to start a new agent
│   ├── agent.yaml          The contract, as data
│   ├── prompt.md           The instruction set
│   └── sop.md              How a human invokes, reviews, and corrects it
└── <agent-id>/             One directory per agent, kebab-case
```

Prompts are Markdown, not YAML strings. Prompts are prose: long, frequently revised, and they
must diff readably word by word. See [ADR-0004](../docs/adr/0004-yaml-specification-format.md).

---

## The agent contract

Nine parts. An agent that cannot fill in all nine is not ready to be built.

| Part | Question it answers |
|---|---|
| **Role** | What is this agent for — and explicitly not for? |
| **Responsibilities** | What decisions and outputs does it own? |
| **Inputs** | What data does it read, and from where? |
| **Outputs** | What artefacts does it produce, in what format? |
| **Memory** | What does it remember between invocations, and where does that live? |
| **Tools** | Which integrations does it need, at what permission level? |
| **Workflow** | What are its steps, in order? |
| **Prompt** | The versioned instruction set it runs on |
| **SOP** | How a human invokes it, reviews it, and corrects it |

---

## Rules

1. **Bounded scope.** A narrow agent that does one thing reliably beats a broad one that does
   everything approximately. Overlapping agents are merged, not added.
2. **Grounded in `core/`.** Agents read the schema. They never guess at structure or invent
   fields.
3. **Propose, don't impose.** Agents draft, summarise, and recommend. Anything irreversible or
   outward-facing requires explicit human confirmation, declared in `agent.yaml`.
4. **Minimum context.** Send the smallest context that answers the question.
5. **External content is untrusted.** Text from mail, web pages, and documents is data to
   analyse, never instructions to follow. Every prompt states this.
6. **Model-agnostic.** Prompts are authored once and packaged per provider. Declare a model
   *tier*, not a specific model.
7. **Auditable.** Every material action is traceable to an invocation.
8. **Explicit output contract.** The prompt states the exact output shape. "Be helpful" is
   not an output contract.

---

## Model tiers

Agents declare a tier; `config/` resolves the tier to a concrete model per provider. This is
what keeps agent definitions stable as models change.

| Tier | For |
|---|---|
| `reasoning` | Multi-step analysis, reviews, strategy, decisions |
| `balanced` | Drafting, summarising, structured extraction |
| `fast` | Classification, routing, tagging, short transforms |

---

## Adding an agent

```bash
cp -r agents/_template agents/<agent-id>
```

1. Fill in `agent.yaml`, `prompt.md`, and `sop.md` completely.
2. Register the agent in `_registry.yaml`.
3. Confirm no existing agent already covers the capability.
4. `make validate`, then commit as `feat(agents): add <agent-name>`.

---

## Planned roster

**Direction** — Personal CEO · Life Coach · Decision Assistant
**Domains** — Health Coach · Finance Advisor · Career Advisor · Learning Mentor
**Knowledge** — Research Assistant · Reading Assistant · Knowledge Curator
**Meta** — Prompt Engineer · Prompt Optimizer

Roles, boundaries, and the shared memory protocol are finalised in Phase 6. See the
[AI Guide](../docs/04-ai-guide/README.md).

---

## Status

⬜ Populated in **Phase 6**. The contract, rules, and tier model above are settled from
Phase 1.
