<div align="center">

# 🧠 2nd Brain

**A Complete AI-Powered Personal Operating System**

*Think. Organize. Remember. Plan. Automate. Improve.*

[![Status](https://img.shields.io/badge/status-active%20development-0A84FF?style=flat-square)](ROADMAP.md)
[![Version](https://img.shields.io/badge/version-0.2.0-5E5CE6?style=flat-square)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-30D158?style=flat-square)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-read-FF9F0A?style=flat-square)](docs/README.md)

</div>

---

## What This Is

**2nd Brain** is a personal operating system: a single, versioned source of truth that
defines how my life is captured, structured, reviewed, automated, and improved — and how
AI agents operate on top of it.

It is deliberately **not** a Notion template, and **not** a productivity dashboard.
It is a specification-driven system with a real architecture:

| Layer | What lives here | Where |
|---|---|---|
| **Core** | Platform-neutral data model — entities, fields, relations, taxonomy, design tokens | [`core/`](core/) |
| **Workspace** | The human interface — page tree, dashboards, views, templates | [`workspace/`](workspace/) |
| **Agents** | Specialised AI operators with roles, memory, tools, SOPs | [`agents/`](agents/) |
| **Prompts** | Versioned, reusable prompt library and prompt patterns | [`prompts/`](prompts/) |
| **Automation** | n8n flows, GitHub Actions, Axiom jobs, scheduled rituals | [`automation/`](automation/) |
| **Scripts** | Sync, validation, and migration tooling | [`scripts/`](scripts/) |
| **Docs** | Architecture, guides, and Architecture Decision Records | [`docs/`](docs/) |

The guiding rule: **the repository is the source of truth; every surface is a projection of it.**
Notion, n8n, and the AI agents render what `core/` declares. Change the spec, re-sync the surface.

---

## Why It's Built This Way

Most personal systems die because they live inside one tool. When the tool changes, or the
subscription lapses, or a better tool arrives, the system dies with it.

2nd Brain separates **what the system is** (`core/`, plain text, version-controlled) from
**where it is rendered** (`workspace/`, currently Notion). That single separation is what
makes it portable, diffable, reviewable, and safe to evolve for years.

Read the reasoning in the [Architecture Decision Records](docs/adr/).

---

## Design Principles

1. **Spec first.** Nothing exists in a tool that isn't declared in the repo.
2. **Modular.** Every agent, database, and automation is an independently replaceable unit.
3. **Idempotent.** Re-running any sync or automation converges to the same state.
4. **Human-legible.** A person can read the spec and understand the whole system.
5. **Provider-agnostic.** Swapping Notion, or adding a second AI provider, is a config change.
6. **Progressive.** The system is useful at 10% built and better at 100%.
7. **Documented by decision.** Every non-obvious choice has an ADR explaining *why*.

---

## Ecosystem

| Category | Integrations |
|---|---|
| **AI models** | Claude · ChatGPT · Google Gemini |
| **Workspace** | Notion |
| **Source of truth** | GitHub |
| **Automation** | n8n · GitHub Actions · Axiom |
| **Google** | Calendar · Gmail · Drive |
| **Storage** | Google Drive · OneDrive |

New providers are added by dropping a definition into `config/providers/` — see the
[Developer Guide](docs/05-developer-guide/README.md).

---

## Repository Map

```
2nd-Brain/
├── core/            # Platform-neutral specification (the actual system)
│   ├── schema/      #   Database/entity definitions
│   ├── relations/   #   The relational graph between entities
│   ├── taxonomy/    #   Shared vocabularies: life areas, statuses, priorities
│   └── design/      #   Design tokens: colour, type, spacing, iconography
├── workspace/       # Human-facing surface (Notion reference implementation)
│   ├── pages/       #   Page hierarchy and content blueprints
│   ├── dashboards/  #   Dashboard compositions
│   ├── views/       #   Reusable database views (filters, sorts, groupings)
│   ├── templates/   #   Page/entry templates
│   └── capture-routing.yaml  # One inbox → many destinations
├── agents/          # AI agent definitions (role, IO, memory, tools, SOP, prompt)
├── prompts/         # Versioned prompt library and reusable prompt patterns
├── automation/      # n8n workflows, GitHub Actions, Axiom jobs, ritual recipes
├── scripts/         # Sync, validation, migration tooling
├── config/          # Environment, provider, and system configuration
├── docs/            # Architecture, guides, ADRs, FAQ, troubleshooting
├── assets/          # Brand assets and exported design artefacts
└── tests/           # Specification and integration tests
```

Every directory carries its own `README.md` describing purpose, conventions, and file format.

---

## Quickstart

> Full instructions: [Installation Guide](docs/02-installation/README.md)

```bash
git clone https://github.com/mittalok-creator/2nd-Brain.git
cd 2nd-Brain
cp .env.example .env      # add your API keys
make validate             # verify the specification is well-formed
```

---

## Build Status

The system is built in sequenced phases. Each phase is committed, documented, and
independently useful.

| # | Phase | Status |
|---|---|---|
| 1 | Repository Architecture | ✅ Complete |
| 2 | Workspace Architecture | ✅ Complete |
| 3 | Databases | ⬜ Planned |
| 4 | Relations | ⬜ Planned |
| 5 | Dashboards | ⬜ Planned |
| 6 | AI Agents | ⬜ Planned |
| 7 | Automations | ⬜ Planned |
| 8 | Documentation | ⬜ Planned |
| 9 | Testing & Refinement | ⬜ Planned |

Details and target dates in the [Roadmap](ROADMAP.md).

---

## Documentation

| Guide | For |
|---|---|
| [Overview](docs/README.md) | Start here |
| [Architecture](docs/01-architecture/README.md) | How the system is put together |
| [Information architecture](docs/01-architecture/information-architecture.md) | The page hierarchy and capture model |
| [Installation](docs/02-installation/README.md) | Getting it running |
| [User Guide](docs/03-user-guide/README.md) | Daily, weekly, monthly operation |
| [AI Guide](docs/04-ai-guide/README.md) | Working with the agents |
| [Developer Guide](docs/05-developer-guide/README.md) | Extending the system |
| [Automation Guide](docs/06-automation-guide/README.md) | Building and debugging automations |
| [Design System](docs/07-design-system/README.md) | Visual and interaction language |
| [ADRs](docs/adr/) | Why things are the way they are |
| [FAQ](docs/faq.md) · [Troubleshooting](docs/troubleshooting.md) | When stuck |

---

## Contributing

This is a personal system, but it is engineered to public standards.
See [CONTRIBUTING.md](CONTRIBUTING.md) for conventions — commits, branches, ADRs, and reviews.

## License

[MIT](LICENSE)
