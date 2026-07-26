# Documentation

Everything you need to understand, run, operate, and extend **2nd Brain**.

---

## Start here

| If you want to… | Read |
|---|---|
| Understand how the system is built | [Architecture](01-architecture/README.md) |
| See the page hierarchy and capture model | [Information architecture](01-architecture/information-architecture.md) |
| Get it running | [Installation](02-installation/README.md) |
| Operate it day to day | [User Guide](03-user-guide/README.md) |
| Work with the AI agents | [AI Guide](04-ai-guide/README.md) |
| Extend or modify it | [Developer Guide](05-developer-guide/README.md) |
| Build or debug automations | [Automation Guide](06-automation-guide/README.md) |
| Match the visual language | [Design System](07-design-system/README.md) |
| Know *why* something is the way it is | [Decision Records](adr/) |
| Fix something that broke | [Troubleshooting](troubleshooting.md) |
| Ask a common question | [FAQ](faq.md) |

---

## How this documentation is organised

Sections are numbered so their reading order is unambiguous, from conceptual to practical
to extensible:

```
docs/
├── 01-architecture/     What the system is and how its layers fit together
├── 02-installation/     Getting from an empty workspace to a running system
├── 03-user-guide/       The daily, weekly, monthly operating rhythm
├── 04-ai-guide/         Agents: what they do and how to invoke them
├── 05-developer-guide/  Conventions, extension points, and tooling
├── 06-automation-guide/ Workflow authoring, scheduling, observability
├── 07-design-system/    Colour, type, spacing, components, dark and light
├── adr/                 Architecture Decision Records — the "why", append-only
├── faq.md
└── troubleshooting.md
```

Reference material describing a *specification* lives next to that specification —
each directory under `core/`, `workspace/`, `agents/`, and `automation/` carries its own
`README.md`. These guides explain concepts and workflows; the directory READMEs explain
file formats and conventions.

---

## Documentation status

Documentation is written alongside the phase that produces it, not retrofitted afterwards.

| Section | Status | Completed by |
|---|---|---|
| Architecture | 🚧 Foundation documented | Phase 4 |
| Installation | 🚧 Outline | Phase 7 |
| User Guide | ⬜ Planned | Phase 8 |
| AI Guide | ⬜ Planned | Phase 6 |
| Developer Guide | 🚧 Conventions documented | Phase 8 |
| Automation Guide | ⬜ Planned | Phase 7 |
| Design System | ⬜ Planned | Phase 5 |
| Decision Records | ✅ Live from Phase 1 | Ongoing |

Track progress in the [Roadmap](../ROADMAP.md).

---

## Conventions

- Sentence case headings; second person in guides.
- Tables in preference to long lists.
- Relative links only — CI fails the build on a broken internal link.
- Every code block is copy-pasteable and correct as written.
- No secrets or personal data in examples, ever. See [SECURITY.md](../SECURITY.md).
