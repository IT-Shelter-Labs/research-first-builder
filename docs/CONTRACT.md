# Artifact contract and helper

[Schema](../skills/research-first-build/assets/evidence.schema.json) ·
[Evidence guide](../skills/research-first-build/references/evidence.md) ·
[Verification guide](../skills/research-first-build/references/verification.md).

## Operations

| Operation | Writes | Meaning |
| --- | --- | --- |
| `init <new-task-dir> [--intent research-only]` | Incomplete JSON/Markdown templates, sources/checks directories | Starter only; it does not inspect sources or produce PASS records. |
| `render <run-dir>` | Managed report tables; advisory run.json cache | No tests executed; prose outside markers remains. |
| `check <run-dir>` | None | Schema/trace/file/table consistency. |
| `check <run-dir> --stage prebuild` | Receipt on success | Required recorded source audit passed, critical questions resolved, planning inputs structurally ready. |
| `check <run-dir> --stage postbuild --snapshot <actual-snapshot>` | Receipt on success | Current recorded required checks pass, prebuild is fresh, rejected/deferred decisions have diff reviews. |

Exit 0 means the requested operation passed; exit 1 means artifact/contract failure; argparse usage errors exit 2.
`check --json` emits a machine-readable result. `--version` shows the package version.
Failed checks do not certify or renew cached receipts; an older cached stage may remain and must never override a failed fresh check.

The run directory is explicit. Relative record paths are POSIX-style, contained beneath it, without `..`,
drive names, symlinks or escaping junctions. Text inputs are capped at 2 MiB each. Invalid UTF-8, duplicate JSON
keys and nonfinite JSON constants fail. CRLF is normalized for text freshness checks.

## Records and trace

Q identifies a research question (optional in older version-1 ledgers); REQ a requirement with USER_REQUIREMENT/ASSUMPTION origin; REF a relevant reference;
SRC an inspected location; EV a classified claim; DEC a scoped decision; STEP planned work; CHECK verification.
IDs are stable within a run. Broken links, duplicate IDs, inference cycles, adopted orphan decisions,
rejected/deferred planned work, and required acceptance omissions fail.

| Evidence class | Required basis |
| --- | --- |
| VERIFIED_SOURCE | Actually inspected documentation and a support explanation |
| OPEN_SOURCE_IMPLEMENTATION | Actually inspected implementation at exact revision/path |
| OBSERVED_PUBLIC_BEHAVIOR | Recorded observed action and limits |
| INFERENCE | Linked premises and explicit scoped reasoning |
| USER_REQUIREMENT | Linked user requirement, not a disguised assumption |

These labels describe supplied provenance. The checker cannot verify that inspection really happened.
Inspect license/notice scope separately; SPDX text and an API license label alone are insufficient.
SOURCE_REUSE requires inspected rights and a recorded review; the checker cannot determine legal compatibility.

## Freshness and snapshots

Prebuild fingerprints planning records, research/plan prose, source notes and source-audit receipts.
Actual build results can be appended without rewriting the approved plan. Any edit to RESEARCH.md or PLAN.md,
including a prose-only typo correction, changes the fingerprint and requires review and a fresh prebuild check.
Rendering clears the postbuild receipt; rendering is not verification.

New postbuild cache records contain only a planning fingerprint, check timestamp and implementation snapshot.
Older caches may also contain `evidence_hash`, `verification_hash` and `check_outputs`; these were unused audit
metadata, not enforced integrity guarantees. They remain readable and are omitted when a successful check renews
the receipt. Each fresh check reads the current ledger, reports and required evidence files; a cached COMPLETE
stage cannot override a failure. The helper does not prove that saved transcripts are authentic.

The host supplies a current snapshot covering implementation plus uncommitted/untracked files where relevant.
Required implementation receipts must use that same snapshot; source audits retain their source-set snapshot.
The helper cannot discover omitted files or prove the snapshot's origin. An arbitrary `HEAD` label is insufficient.

The example verifier hashes named app.py/test_app.py files with LF normalization and reruns their fixed tests.
It fails after code drift without refreshing receipts. This bounded mechanism is development tooling for those
examples, not an automatic production project watcher.

PASS/FAIL receipts need actual output or inspection note, timestamp and snapshot. NOT_RUN has no fabricated
execution receipt. BLOCKED remains incomplete with an explanation. Source audits are separate from behavior tests.
Research-only can pass prebuild and hand off; it cannot certify a completed implementation.

## What checks cannot establish

Factual truth, claim applicability, meaningful coverage, real execution, license clearance, permission,
security certification and deployment readiness require their respective reviewers/tools. A malicious author
can fabricate structurally valid records. The helper prevents mistakes in the contract, not dishonest provenance.
No test transcript or reference source is executed by the helper.
