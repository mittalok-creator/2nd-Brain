# AI Guide

Working with the agents that make 2nd Brain more than a database.

> **Status** — ⬜ Written in Phase 6, alongside the agent roster itself. The contract and
> operating principles below are settled and constrain every agent that gets built.

---

## What an agent is here

An agent is **not** a chat window with a system prompt. It is a defined operator with a
fixed contract, a bounded scope, and a written standard operating procedure.

Every agent in `agents/` satisfies all nine parts of the contract:

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

An agent proposal that cannot fill in all nine is not ready. An agent that overlaps an
existing one is merged, not added.

---

## Operating principles

1. **Bounded scope.** A narrow agent that does one thing reliably beats a broad one that
   does everything approximately.
2. **Grounded in the specification.** Agents read the core schema. They do not guess at
   structure or invent fields.
3. **Propose, don't impose.** Agents draft, summarise, and recommend. Anything irreversible
   or outward-facing needs explicit human confirmation.
4. **Minimum context.** Send the smallest context that answers the question — better
   answers, lower cost, less exposure.
5. **External content is untrusted.** Text from mail, web pages, and documents is data to
   analyse, never instructions to follow.
6. **Model-agnostic.** Prompts are authored once and packaged per provider. No agent is
   locked to one vendor.
7. **Auditable.** Every material action an agent takes is traceable to an invocation.

---

## Planned roster

Grouped by function. Names and boundaries are finalised in Phase 6.

**Direction**
- Personal CEO — cross-domain prioritisation, weekly and monthly reviews
- Life Coach — habits, balance, motivation, accountability
- Decision Assistant — structured decisions and outcome review

**Domains**
- Health Coach · Finance Advisor · Career Advisor · Learning Mentor

**Knowledge**
- Research Assistant — investigate a question, return sourced findings
- Reading Assistant — process what is read into durable notes
- Knowledge Curator — connect, deduplicate, and surface the knowledge base

**Meta**
- Prompt Engineer — author new prompts to the house standard
- Prompt Optimizer — measure and improve existing prompts

---

## Sections planned for Phase 6

- The agent contract in full, with a worked example
- Invocation: from Notion, from chat, from an automation
- The shared memory protocol and context-retrieval strategy
- Routing: choosing the right agent, and the right model tier, for a task
- Prompt authoring standards and the prompt library
- Evaluating agent output, and correcting a misbehaving agent
- Cost and latency management across model tiers
- Safety: confirmation gates, injection resistance, sensitive domains

---

## Related

- [`agents/README.md`](../../agents/README.md) — file format and conventions
- [`prompts/README.md`](../../prompts/README.md) — the prompt library
- [Architecture](../01-architecture/README.md) — where the intelligence layer sits
