# SOP — Agent Template

The human-side procedure: when to use this agent, how to read its output, and what to do when
it gets something wrong.

`agent.yaml` is the machine contract. This is the operator's manual.

---

## When to use it

**Use it when:**
-

**Don't use it when:**
- {{Named alternative agent}} owns that work.

**Cadence:** {{on demand · daily · weekly · monthly}}

---

## How to invoke it

| Surface | How |
|---|---|
| Command Center | {{Which button or action}} |
| Chat | Paste the prompt, supply the declared inputs |
| Automation | {{Which automation invokes it, and on what trigger}} |

Before invoking, confirm the inputs it depends on are actually current. An agent reading stale
data produces confident, wrong output — the worst failure mode available.

---

## Reading the output

**A good response:**
- Matches the output contract exactly.
- Cites specific records or metrics for every claim.
- Names what it does not know.

**Reject and re-run when:**
- The structure does not match the contract.
- It references fields or records that do not exist.
- It gives generic advice that would apply to anyone.
- It followed instructions embedded in fetched external content.

---

## Review gate

| Output | Requires |
|---|---|
| Suggestions and analysis | Read and judge |
| Changes to existing records | Review before applying |
| Irreversible or outward-facing action | Explicit confirmation, every time |

Never auto-apply output from a `draft`-status agent.

---

## When it gets something wrong

Diagnose in this order, and fix at the lowest level that resolves it:

1. **Wrong inputs.** The most common cause by a wide margin. Check what it was actually given
   before touching the prompt.
2. **Ambiguous output contract.** Inconsistent structure between runs almost always means the
   contract is underspecified, not that the model is unreliable.
3. **Missing judgement rule.** Consistently bad calls of the same kind mean a rule is absent.
   Add it explicitly.
4. **Wrong model tier.** Shallow reasoning on a complex task means the tier is too low; slow
   and expensive output on a simple task means it is too high.
5. **Scope error.** If the agent keeps being asked for work it should not do, the role
   boundary needs restating — or the roster needs a different agent.

Record every prompt change in the `prompt.md` changelog with a version bump. Undocumented
prompt edits make regressions impossible to trace.

---

## Escalation

If output is wrong in the same way three times, stop patching. Open an
[agent proposal](https://github.com/mittalok-creator/2nd-Brain/issues/new?template=agent_proposal.yml)
to revise the contract itself — repeated failure of one kind is a design problem, not a
prompting problem.
