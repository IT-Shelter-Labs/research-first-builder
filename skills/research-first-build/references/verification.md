# Verification and resume

Read before build or when resuming/verifying an existing run.

## Prebuild

Save the source audit: inspect the original supporting locations for consequential claims and record the sampled EV IDs, exact locators, support/contradictions and outcome under `checks/`. A source audit is agent/reviewer inspection, not proof from the checker itself.

Declare it as a required SOURCE_AUDIT CHECK with an actual PASS/FAIL, source-set snapshot and timestamp. Prebuild requires passing required source audits, resolved critical questions, readable reports, valid trace and current managed tables.

~~~text
python "<skill-dir>/scripts/rfb.py" render "<run-dir>"
python "<skill-dir>/scripts/rfb.py" check "<run-dir>" --stage prebuild
~~~

Any edit to RESEARCH.md or PLAN.md, including prose-only corrections, invalidates the prebuild fingerprint. Finish prose edits before prebuild where possible; after later edits, review, render and recheck prebuild before postbuild.

This writes a prebuild receipt in run.json. It is a freshness cache; never use a cached stage as authorization or skip rechecking on resume.

## Actual checks

Use the host's shell/project tools to run the planned checks. The helper never executes commands from the ledger.

- PASS/FAIL: actual result, relevant saved output/inspection note, timestamp and tested_snapshot.
- NOT_RUN: no execution receipt; state the practical limitation in prose.
- BLOCKED: explain the missing prerequisite in the report; attach actual diagnostic output if available.

Do not label a test PASS because code appears plausible or a previous revision passed. Optional failures remain visible even if they do not gate completion.

After build, review the diff for every REJECT/DEFER decision. Add a required DIFF_REVIEW CHECK linked to those decisions, saving the actual inspected file scope and conclusion.

## Snapshot boundary

The host gathers an actual current implementation snapshot. Use Git revision plus a working-tree/untracked-content fingerprint, or a bounded file manifest for a non-Git project. State included/excluded paths; a moving branch name or HEAD alone does not describe uncommitted edits.

The helper accepts the snapshot identifier through `--snapshot`, compares it with receipts, and does not read arbitrary implementation paths or run git. A forged identifier/transcript can fool structural checks. Record provenance honestly and review it separately.

~~~text
python "<skill-dir>/scripts/rfb.py" render "<run-dir>"
python "<skill-dir>/scripts/rfb.py" check "<run-dir>" --stage postbuild --snapshot "<actual-current-snapshot>"
~~~

Required checks must PASS on that snapshot, except SOURCE_AUDIT checks tied to the researched source set. Rendered tables must match. The prebuild fingerprint must still match research/plan/source inputs.

CONTRACT_CHECKED means the artifact contract passed. It is not legal clearance, a source-truth guarantee, a hard write barrier or permission to deploy/publish.

## Resume and drift

1. Read scope, ledger and human reports; do not start fresh automatically.
2. Run contract checks. Inspect current source/implementation changes with host tools.
3. Revisit only affected research questions/decisions after scope/source changes. Rendering changed planning inputs invalidates old prebuild readiness.
4. Re-run affected actual checks after implementation changes; a new snapshot does not inherit old PASS receipts.
5. Continue the earliest incomplete stage under existing user authorization.

Unknown schema/version or malformed artifacts: preserve them and report the error; no silent migration/overwrite. Missing Python: manual review only, no deterministic status. Research-only can hand off a prebuild-ready plan but cannot pass postbuild as a completed implementation.
