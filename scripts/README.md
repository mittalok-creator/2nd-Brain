# scripts/ — tooling

Tooling that operates on the specification: validation, syncing, and migration.

Python, standard library plus PyYAML, no build step. Anything requiring a toolchain to run
does not belong here — this tooling has to work in three years from a fresh clone.

---

## Contents

| File | Does |
|---|---|
| `validate_repository.py` | Validates structure, YAML specs, and internal documentation links |
| `requirements.txt` | Tooling dependencies |

---

## `validate_repository.py`

```bash
python3 scripts/validate_repository.py            # everything
python3 scripts/validate_repository.py --only yaml
python3 scripts/validate_repository.py --quiet
```

Or via `make`: `make validate`, `make structure`, `make yaml`, `make links`.

Three checks:

| Check | Enforces |
|---|---|
| `structure` | Required files and directories exist; every top-level directory has a README; ADR numbers are unique |
| `yaml` | Every YAML file parses; spec files carry the header contract with semantic `version` and valid `status` |
| `links` | Every relative Markdown link resolves |

Exits `0` when clean, `1` on any error. Warnings do not fail the build.

CI runs the identical script, so a green local run means a green pipeline.

---

## Conventions

1. **Offline and deterministic.** No network calls in validation — network checks make CI
   flaky, and a flaky check gets ignored.
2. **Dependency-light.** Standard library first. A new dependency needs justification.
3. **Fail with a fixable message.** State the file, the line where possible, and what is
   wrong. `Invalid YAML` is not a useful error.
4. **Read-only by default.** A script that mutates state says so in its name and requires an
   explicit flag.
5. **`--dry-run` on anything that writes**, and it must be the safe default for destructive
   operations.

---

## Adding a check to the validator

1. Write a `check_*(report)` function.
2. Register it in the `CHECKS` dictionary.
3. Add a `make` target and a CI step.
4. Keep it offline and deterministic.

---

## Planned scripts

| Script | Phase | Does |
|---|---|---|
| `sync_notion.py` | 3 | Provisions Notion from `core/` and `workspace/` |
| `check_drift.py` | 9 | Reports divergence between the specification and live Notion |
| `generate_erd.py` | 4 | Renders the entity-relationship diagram from `core/relations/` |
| `migrate.py` | 4 | Applies versioned migrations to existing workspace state |
| `test_agents.py` | 6 | Runs agent definitions against fixture inputs |
