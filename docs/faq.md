# FAQ

---

## About the project

### What is 2nd Brain, in one sentence?

A version-controlled specification for a personal operating system, plus the AI agents and
automations that run on top of it.

### Why isn't this just a Notion template?

A template is a starting layout. This is a specification with an architecture: the data
model, the page hierarchy, the agents, and the automations are all defined as versioned
files, reviewed like code, and rendered into Notion. Templates cannot be diffed, reviewed,
reverted, or reproduced. This can.

### Why is the repository the source of truth rather than Notion?

So that structural change is reviewable and the whole workspace is reproducible, and so that
replacing Notion means writing one adapter rather than redesigning the system. Full reasoning
in [ADR-0003](adr/0003-notion-as-projection.md).

### Is this usable by someone other than the author?

The architecture is general and the specification is public, so yes — but the taxonomy, goal
structure, and agent SOPs encode one person's life. Expect to fork and adapt rather than
adopt as-is.

### Why so much documentation for a personal project?

Because the main risk to a personal system is the author returning after three months and no
longer understanding it. The ADRs exist specifically so past decisions do not have to be
reconstructed from memory.

---

## Using it

### Do I need every integration listed in the README?

No. The only hard requirements are Git and Python for the tooling, and Notion plus one AI
provider to have a working system. n8n, Axiom, Google, and OneDrive are additive.

### Can I use ChatGPT or Gemini instead of Claude?

Yes. Prompts are authored once and packaged per provider, and no agent is locked to a vendor.
Model quality does differ on the reasoning-heavy agents.

### Where does my actual data live?

In Notion. The repository holds structure only — columns, not rows. Nothing personal is ever
committed. See [SECURITY.md](../SECURITY.md).

### Can I edit things directly in Notion?

**Content, yes** — write journal entries, check off tasks, add notes freely. That is what
Notion is for.

**Structure, no.** Adding a database, adding a property, or changing the page hierarchy in
the UI creates drift from the specification. Change the spec and re-sync instead.

### How much time does this take to run daily?

Ten minutes: five in the morning to accept or adjust the drafted plan, five in the evening to
log what happened. Thirty minutes weekly, an hour monthly. If it needs more, that is a defect
in the system.

### What if I stop using it for a month?

Nothing breaks. Automations keep running or are paused; the specification is unchanged. The
weekly review is designed to be resumable without catching up on backlog.

---

## Building on it

### How do I add a new database?

Add a spec to `core/schema/`, declare its relations in `core/relations/`, and expose it via
`workspace/views/` and `workspace/pages/`. Steps in the
[Developer Guide](05-developer-guide/README.md).

### How do I add a new agent?

Copy `agents/_template/`, satisfy all nine parts of the agent contract, and register it in
`agents/_registry.yaml`. If it overlaps an existing agent, extend that one instead.

### Why YAML and not JSON or TypeScript?

YAML supports comments — the reasoning lives next to the field it explains — and stays
readable when deeply nested. TypeScript would make the specification executable, and an
executable specification can be conditional, which defeats the purpose.
[ADR-0004](adr/0004-yaml-specification-format.md).

### Why is there no `src/` directory?

The specification *is* the deliverable. A `src/` directory would imply compiled output and
obscure that. [ADR-0001](adr/0001-four-layer-architecture.md).

### Can I contribute?

It is a personal system, but it is engineered to public standards and the conventions are
documented. See [CONTRIBUTING.md](../CONTRIBUTING.md).

---

## Design decisions

### Why did the folder names change from the original plan?

`/notion` became `workspace/` because the surface is a role, not a vendor. `/databases`
became `core/schema/` because database definitions *are* the specification. `/templates` and
`/workflows` were merged into `workspace/templates/` and `automation/` because they were
duplicate homes for concepts that already had one. Reasoning in
[ADR-0001](adr/0001-four-layer-architecture.md).

### Why are there so many small agents instead of one big one?

A narrow agent with a defined scope and a written SOP is testable, correctable, and reliable.
One general agent is none of those things — when it gets something wrong there is nowhere to
apply the fix.

### Why must every automation be idempotent?

Because automations will re-run: retries, backfills, manual triggers, timezone edge cases.
Non-idempotent automations produce duplicate tasks and double-counted metrics, and the
cleanup costs more than the automation ever saved.

### Will this still work in five years?

That is what the architecture is for. The specification is plain text under version control
and depends on nothing. Tools will be replaced; the layer boundaries are drawn so that
replacing one does not disturb the others.

---

Something missing here?
[Open a documentation issue](https://github.com/mittalok-creator/2nd-Brain/issues/new?template=documentation.yml).
