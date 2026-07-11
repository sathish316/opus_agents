---
name: code2spec
description: Reverse-engineer OpenSpec specs from a repository's git history. Traverses commits chronologically, PR-wise, or author-wise using deterministic scripts, understands each change unit, and incrementally updates the final specs in openspec/specs/ — without creating per-change proposal artifacts. Use when the user wants to generate or bootstrap OpenSpec specs from an existing codebase's commit history, mentions code2spec or reverse openspec, or asks to build specs for a project that did not start with spec-driven development.
---

# code2spec — Reverse OpenSpec from Git History

OpenSpec's forward workflow goes spec → change proposal → code. code2spec runs the arrow backwards for repositories that did not start with spec-driven development: it walks the git history in a chosen order, understands what each change did, and reconstructs the **final capability specs** under `openspec/specs/`.

**Core rule: code2spec never writes under `openspec/changes/`.** It does not create a proposal, tasks file, or archived change folder per commit or PR. It understands each change and only keeps updating the final specs. (The `changes/` and archive formats are documented below so you can *read* them when present — never write them.)

## Pipeline

1. **Locate the target repo and its openspec dir.** Confirm `openspec/` exists (look for `openspec/config.yaml` or `openspec/project.md`). If missing, ask the user before running `openspec init`.
2. **Pick a traversal strategy** (ask the user if not stated):
   - `pr` — default when the repo has merge or squash-merge PR history; one unit per PR.
   - `window` — for repos without PR history; consecutive commits by the same author within a time window form one unit.
   - `author` — attribution lens: one unit per author. Useful for reporting who built which capability; it does not change what the final specs say.
3. **Enumerate change units** with `scripts/group_commits.py` (oldest-first). For very large repos, process in batches using `--since`/`--until` or `--limit`.
4. **For each unit, oldest → newest:**
   a. Fetch its diff with `scripts/show_change.py` (start with `--mode stat`; escalate to `--mode patch` only when the stat + commit messages aren't enough).
   b. Classify it (see *Classification* below). Skip noise.
   c. Map it to one or more capabilities (see *Capability mapping*).
   d. Update `openspec/specs/<capability>/spec.md` directly (see *Updating final specs*).
5. **Record progress** after each batch (see *State & resumability*) so a run can resume.
6. **Report**: capabilities created/updated, units processed, units skipped as noise, and anything ambiguous that needs the user's judgment.

## Scripts

Deterministic, stdlib-only Python; each prints JSON to stdout. Run with `python3`. All take `--repo <path>` pointing at the target repository.

| Script | Purpose |
|---|---|
| `scripts/list_commits.py` | Raw commit listing (oldest-first by default) with author, date, subject, body, and per-file change status. Filters: `--author`, `--since`, `--until`, `--no-merges`, `--path`, `--limit`, `--rev`. |
| `scripts/group_commits.py` | Groups commits into change units. `--strategy pr\|window\|author`, plus `--window-hours` (default 24), `--since/--until`, `--limit`. |
| `scripts/show_change.py` | Diff for one unit: `--commit <sha>` or `--base <rev> --head <rev>` (as emitted per unit). `--mode files\|stat\|patch` (default stat), `--max-patch-chars` (default 40000). |

Notes:
- Each unit from `group_commits.py` includes `base`/`head` revs — feed them straight to `show_change.py`. For `window` units on non-linear history the base..head diff is an approximation; `author` units have `base: null` (diff their commits individually).
- Root commits are diffed against git's empty tree automatically.
- `pr_number` is extracted from `#NNN` in merge/squash subjects when present.

## Classification: what updates specs

Judge each unit by its **diff**, not just its commit message — messages lie, diffs don't. When tests changed, read the test diff first: tests state intended behavior directly.

| Unit looks like | Action |
|---|---|
| Dependency bumps, formatting, lint, CI/build config, typos, comments | Skip (noise) |
| Pure refactor — structure changes, behavior doesn't | Skip (noise) |
| New feature / new user-visible behavior | ADD requirement(s) with scenarios |
| Behavior change to an existing feature | MODIFY the matching requirement/scenarios |
| Bug fix | Usually strengthens an existing requirement — add or sharpen a scenario capturing the now-correct behavior |
| Feature removal | REMOVE the matching requirement |
| Rename/move of a feature | RENAME the requirement, keep its scenarios |
| Large mixed unit | Split mentally by capability and apply each part |

Replay discipline: process oldest → newest so later units naturally supersede earlier ones. A feature added in unit 12 and removed in unit 87 must **not** appear in the final specs.

## Capability mapping

- One kebab-case folder per capability under `openspec/specs/`, named for the domain behavior, not the code layout: `user-auth`, `todo-sync`, `config-management` — not `utils` or `src-refactor`.
- Separate framework capabilities from domain-specific ones: reusable framework/platform behaviors live at the top level (`openspec/specs/<capability>/`), while behaviors specific to one product/agent/domain nest under `openspec/specs/domain/<product>/<capability>/` (e.g. `specs/domain/todo-agent/todo-management/`). Ask the user which bucket a capability belongs to when unclear.
- Before inventing a capability, list existing ones (`ls openspec/specs/`) and reuse. Keep the taxonomy small and stable; split a capability only when its spec grows past roughly 10 requirements.
- A unit may touch multiple capabilities; update each affected spec.

## Updating final specs (the write path)

For each spec-relevant unit:

1. Read `openspec/specs/<capability>/spec.md` if it exists; otherwise create it from the template below.
2. Apply the unit's effect directly — the same semantics as delta specs (ADDED / MODIFIED / REMOVED / RENAMED requirements), but written straight into the final spec file.
3. Preserve requirements and scenarios the unit doesn't touch. Edits are surgical, not wholesale rewrites.
4. Keep requirement names stable; rename only when the behavior itself was renamed.

## OpenSpec format reference

### Directory layout

```
openspec/
├── config.yaml                    # schema + project context (newer CLI)
├── project.md                     # project context (classic layout)
├── specs/                         # CURRENT TRUTH — what code2spec writes
│   └── <capability>/
│       └── spec.md
└── changes/                       # forward-workflow artifacts — READ ONLY for code2spec
    ├── <change-name>/             # an in-flight change
    │   ├── .openspec.yaml
    │   ├── proposal.md            # why + what
    │   ├── design.md              # how (technical decisions)
    │   ├── tasks.md               # implementation checklist (- [ ] / - [x])
    │   └── specs/<capability>/spec.md   # delta spec
    └── archive/
        └── YYYY-MM-DD-<change-name>/    # completed changes, moved here on archive
```

### Spec file format (what code2spec writes)

```markdown
# <Capability> Specification

## Purpose
<Short statement of what this capability provides and for whom.>

## Requirements

### Requirement: <Behavior Name>
The system SHALL <normative statement of the behavior>.

#### Scenario: <concrete case>
- **WHEN** <trigger or condition>
- **THEN** <expected outcome>
- **AND** <optional additional outcome>
```

Conventions:
- Each requirement is a `### Requirement: <Name>` heading followed by at least one normative SHALL/MUST sentence.
- Each requirement has at least one `#### Scenario:` block with bolded **WHEN**/**THEN** bullets (**GIVEN**/**AND** also allowed).
- Requirement names are unique within a capability and stable across edits.
- `## Purpose` may be brief; mark `TBD` only as a last resort.

### Delta specs (read-only context)

In the forward workflow, a change's `specs/<capability>/spec.md` expresses intent against the main spec using these sections:

```markdown
## ADDED Requirements
### Requirement: New Feature
The system SHALL ...
#### Scenario: ...

## MODIFIED Requirements
### Requirement: Existing Feature      <- partial: only what changed
#### Scenario: New scenario to add

## REMOVED Requirements
### Requirement: Deprecated Feature

## RENAMED Requirements
- FROM: `### Requirement: Old Name`
- TO: `### Requirement: New Name`
```

code2spec applies these *semantics* directly to final specs; it never writes delta files.

### How development artifacts are archived (read-only context)

When a forward-workflow change is complete, its delta specs are synced into the main specs and the entire change folder is **moved** to `openspec/changes/archive/YYYY-MM-DD-<change-name>/` (date of archiving, `.openspec.yaml` preserved). Archived changes are therefore a historical record — if the target repo has them, read them: they are high-quality ground truth for what its specs should contain. code2spec never creates or modifies archives.

## Checkpoint file (resume only)

Track the last commit that was reversed to spec in a checkpoint file at `openspec/.reverse-open-spec-commit` in the target repo. It contains exactly one line: the full SHA of the head commit of the last processed unit. Nothing else — it exists only so a run can resume from where the previous one stopped.

- After each batch of processed units, overwrite the file with the new SHA.
- On start, if the file exists, resume from the commit after it (skip units whose head is an ancestor of the checkpoint SHA) instead of reprocessing from the beginning.
- Commit the checkpoint alongside spec updates so resume points survive across machines.

## Validation

After a run:
- Re-read each touched spec: heading structure matches the format, every requirement has at least one scenario, no delta-section headings (`## ADDED ...`) leaked into final specs.
- If the `openspec` CLI is available, run `openspec status` in the target repo to confirm nothing is broken.
- Spot-check 2–3 requirements against the current code to confirm the replay converged on present-day behavior.
