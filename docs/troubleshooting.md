# Troubleshooting

Diagnostics for things that actually go wrong, organised by symptom.

> Sections for the Notion sync, agents, and automations grow as those phases ship. Anything
> marked with a phase is not yet applicable.

---

## Validation

### `make validate` fails with `missing required file`

A required root or `.github` file has been deleted or renamed. The required set is listed in
`REQUIRED_FILES` in `scripts/validate_repository.py`. Restore the file, or update the
contract if the removal was intentional — and say why in the commit.

### `make validate` fails with `missing required directory`

Git does not track empty directories, so a directory whose only contents were deleted
disappears on clone. Every required directory must contain at least one committed file — in
practice its `README.md`.

### `'<dir>/' has no README.md describing its purpose`

Every top-level directory documents itself. Add a `README.md` covering purpose, file format,
and conventions. This is enforced because an undocumented directory becomes a dumping ground.

### `spec header is missing 'id'` (or `name`, `version`, `status`, `description`)

Every specification file under `core/`, `workspace/`, `agents/`, and `automation/` carries
the header contract:

```yaml
id: decision_journal
name: Decision Journal
version: 1.0.0
status: active
owner: core
description: >
  One sentence explaining what this entity is for.
```

Exempt: paths containing a `_`-prefixed segment, and vendor exports under
`automation/n8n/` and `automation/actions/`.

### `version '1.0' is not semantic (x.y.z)`

Use three components: `1.0.0`. See [ADR-0002](adr/0002-naming-and-versioning.md).

### `failed to parse` on a YAML file

Usual causes, in order of likelihood:

1. **A tab character.** YAML forbids tabs for indentation. `.editorconfig` prevents this if
   your editor honours it.
2. **Inconsistent indentation.** Two spaces per level, uniformly.
3. **An unquoted special value.** `no`, `yes`, `on`, `off`, `null`, and `~` are booleans and
   nulls in YAML 1.1. Quote them: `status: "no"`.
4. **An unquoted colon inside a value.** `description: Goals: the plan` breaks — quote the
   whole value.
5. **A tab or trailing colon inside a block scalar.**

Isolate the file:

```bash
python3 -c "import yaml,sys; yaml.safe_load(open(sys.argv[1]))" path/to/file.yaml
```

### `broken link` in a Markdown file

The link target does not exist relative to the file containing it. Common causes: a moved
file, a missing `../`, or a link written against the GitHub URL structure rather than the
filesystem. Only relative links are checked — external URLs are deliberately not, to keep CI
deterministic.

### `hierarchy: composed page '<id>' has no blueprint file`

`_hierarchy.yaml` marks the page `kind: composed`, but no blueprint in `workspace/pages/`
declares that `id`. Either write the blueprint, or change the page to `kind: generated` and
give it an `entity`.

The reverse error — `generated page must not have a blueprint` — means a blueprint exists for a
page whose content is entirely one entity's views. Delete the blueprint; generated pages are
built from the entity's view set. See
[ADR-0005](adr/0005-workspace-information-architecture.md).

### `hierarchy: <file> order='N' contradicts _hierarchy.yaml 'M'`

A blueprint's `class`, `parent`, or `order` disagrees with the tree. `_hierarchy.yaml` is
authoritative — fix the blueprint, unless the tree itself is what changed.

### `hierarchy: '<id>' is at depth N, exceeding max 3`

A page is nested too deeply, meaning it is more than two clicks from Home. Flatten it: either
promote it a level, or fold its content into its parent. Depth is a hard constraint, not a
guideline — see [ADR-0005](adr/0005-workspace-information-architecture.md).

### `hierarchy: '<a>' and '<b>' share order N under '<parent>'`

Sibling order must be explicit and unique, because relying on file or alphabetical order means
the sidebar silently reorders whenever a page is added.

### `warn yaml: PyYAML not installed`

The YAML check was skipped. Install the tooling:

```bash
pip install -r scripts/requirements.txt
```

CI always installs it, so a locally skipped check can still fail the pipeline.

---

## CI

### The `hygiene` job fails on a tracked `.env` file

A `.env` was committed. **Rotate every credential in it first** — before touching git
history. Then remove it from tracking and from history:

```bash
git rm --cached .env
git commit -m "chore(repo): untrack .env"
```

History rewriting does not un-leak a key that has already been read. See
[SECURITY.md](../SECURITY.md).

### The `hygiene` job fails on a missing trailing newline

Every `.md`, `.yaml`, `.yml`, and `.py` file must end with a newline. `.editorconfig` handles
this automatically in editors that honour it. To fix in bulk:

```bash
for f in $(git ls-files '*.md' '*.yaml' '*.yml' '*.py'); do
  [ -n "$(tail -c 1 "$f")" ] && printf '\n' >> "$f"
done
```

### The `commits` job fails with `Not a conventional commit`

A commit subject does not match `type(scope): subject`. Valid types: `feat` `fix` `docs`
`refactor` `chore` `test` `ci` `style` `perf` `revert`. Rewrite the offending subjects:

```bash
git rebase -i origin/main   # not available in every environment; amend instead if so
```

For the most recent commit only: `git commit --amend`.

### CI passes locally but fails on GitHub

Almost always one of:

- **An untracked file.** The validator sees your working tree; CI sees the clone. Check
  `git status`.
- **An empty directory.** Present locally, absent after clone.
- **PyYAML skipped locally.** See above.

Reproduce CI exactly against a clean clone:

```bash
git clone --depth 1 file://$(pwd) /tmp/ci-check && cd /tmp/ci-check
pip install -r scripts/requirements.txt && make validate
```

---

## Notion sync — *Phase 3*

Placeholders for the failures this layer will produce:

| Symptom | Likely cause |
|---|---|
| `401 unauthorized` | Integration secret wrong or revoked |
| `404 not found` on the root page | The root page was never shared with the integration |
| `object_not_found` on a database | Deleted in Notion but still declared in the spec |
| Rate limiting (`429`) | Sync not backing off; batch size too large |
| Property type change rejected | Notion forbids some in-place type changes — needs a migration |
| Drift detected | A structural change was made directly in Notion |

---

## Agents — *Phase 6*

| Symptom | Likely cause |
|---|---|
| Agent invents fields that do not exist | Schema not included in context, or context truncated |
| Output format inconsistent between runs | Prompt lacks an explicit output contract |
| Agent follows instructions found in fetched content | Prompt injection — external content must be framed as untrusted data |
| Responses too slow or too costly | Wrong model tier, or context far larger than needed |
| Agent contradicts another agent | Overlapping scopes — merge them |

---

## Automations — *Phase 7*

| Symptom | Likely cause |
|---|---|
| Duplicate tasks or double-counted metrics | Automation is not idempotent |
| Ran at the wrong hour | Timezone mismatch between cron and `BRAIN_TIMEZONE` |
| Silent failure | No error path; failures must emit to Axiom and notify |
| Workflow fails after import | Credentials not re-bound — exports deliberately exclude them |
| Ritual fired twice | Overlapping trigger and manual invocation without a run marker |

---

## Still stuck

1. Re-read the relevant [ADR](adr/) — the behaviour may be intentional.
2. Run `make validate` and read the full output, not just the last line.
3. [Open an issue](https://github.com/mittalok-creator/2nd-Brain/issues/new/choose) with the
   command you ran, the full output, and your environment — minus any secrets.
