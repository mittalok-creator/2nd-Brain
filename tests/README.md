# tests/ — specification tests

Tests that assert the specification is internally consistent and that agents and automations
behave as declared.

The page tree itself — one root, depth ≤ 3, unique sibling order, composed versus generated
pages — is already enforced by `make hierarchy` from Phase 2, so these suites do not repeat it.

Distinct from `scripts/validate_repository.py`, which checks that files are *well-formed*.
These tests check that the system is *correct*: that relations resolve, that no entity is
orphaned, that agents satisfy their contracts, and that automations converge on re-run.

---

## Planned suites

| Suite | Phase | Asserts |
|---|---|---|
| `test_schema.py` | 3 | Every field has a valid type; enums reference `core/taxonomy/`; ids are unique |
| `test_relations.py` | 4 | Both endpoints exist; cardinality is consistent; ownership is acyclic; no unreachable entity |
| `test_taxonomy.py` | 3 | Values are unique and ordered; every value has a description; colours reference semantic tokens |
| `test_workspace.py` | 5 | Views reference real entities and fields; every page's `owns_entities` names a real entity, and no entity is owned twice |
| `test_agents.py` | 6 | All nine contract parts are present; declared entities exist; every agent is registered; no capability is owned twice |
| `test_prompts.py` | 6 | Every prompt states an output contract, a tier, and untrusted-content framing |
| `test_automations.py` | 7 | Every recipe declares an idempotency strategy and a failure path; cron expressions parse; triggers do not collide |
| `test_design.py` | 5 | No hex value outside `tokens.yaml`; every colour defined for both themes; text contrast meets WCAG AA |
| `test_idempotency.py` | 9 | Dry-running an automation twice produces no second effect |

---

## Principles

1. **Offline and deterministic.** No network, no live Notion, no model calls. Fixtures only.
2. **Assert the invariants** stated in [Architecture](../docs/01-architecture/README.md) — that
   document and this suite must agree.
3. **Fail with a fixable message.** Name the file, the field, and the rule violated.
4. **Fixtures carry no personal data.** Example content only.
5. **A test for every bug.** Anything that breaks once gets an assertion so it cannot break
   silently again.

---

## Running

```bash
pytest tests/          # Phase 3 onward
make validate          # available now — structure, YAML, and links
```

---

## Status

⬜ First suites land in **Phase 3**; the full set completes in **Phase 9**.
