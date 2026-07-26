# automation/n8n/ — n8n workflow exports

Vendor exports of the workflows implementing the recipes in
[`../recipes/`](../recipes/README.md). One JSON file per workflow, named to match its recipe.

These files are **generated, not authored**. They are exempt from the specification header
contract. Read the recipe to understand what a workflow does; read the export only when
debugging the implementation.

---

## Export procedure

1. In n8n: workflow menu → **Download**.
2. **Verify no credentials are present** before committing. Exports may embed credential
   references and, depending on version, credential data. Check the JSON for
   `credentials`, `apiKey`, `token`, and `Authorization` before staging the file.
3. Save as `automation/n8n/<recipe-id>.json`, matching the recipe filename.
4. Commit as `feat(automation): export <name> workflow`.

The CI hygiene job blocks credential-shaped files, but it is a safety net, not a substitute
for checking. See [SECURITY.md](../../SECURITY.md).

---

## Import procedure

1. In n8n: **Import from file**.
2. Re-bind every credential — exports deliberately carry none, so a freshly imported workflow
   will fail until this is done.
3. Set the workflow timezone to match `BRAIN_TIMEZONE`. A mismatched timezone is the single
   most common cause of a ritual firing at the wrong hour.
4. Run once manually with a dry-run flag before enabling the schedule.
5. Enable the trigger.

---

## Conventions

- **Filename matches the recipe id.** A workflow with no recipe should not exist.
- **Node names describe intent**, not mechanics: `Read today's tasks`, not `Notion1`.
- **Every external call has an error branch.** No silent failures.
- **Every workflow emits its run event** to Axiom as its final step, on both success and
  failure paths.
- **Re-export after any change made in the n8n UI.** An export that no longer matches the live
  workflow is worse than no export.

---

## Status

⬜ Populated in **Phase 7**.
