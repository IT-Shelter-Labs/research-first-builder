# Evidence ledger

Read this when writing `evidence.json`. The exact field contract is [evidence.schema.json](../assets/evidence.schema.json); [evidence.template.json](../assets/evidence.template.json) supplies the shape.

## One source of structured facts

Default run directory: `docs/research-first/<task-slug>/`.

- `RESEARCH.md`, `PLAN.md`, `VERIFICATION.md`: readable prose plus generated tables.
- `evidence.json`: canonical records and stable IDs.
- `run.json`: helper-generated receipt cache; do not hand-edit it as approval.
- `sources/SRC-001.md`: minimal provenance/support notes.
- `checks/CHECK-001.txt`: actual command output or signed-in-context inspection notes.

All record paths are relative, use `/`, and stay below `sources/` or `checks/`. No symlinks, traversal, absolute paths or credentials in URLs. The helper has a 2 MiB per-file limit; trim oversized output to relevant lines and explain the truncation.

IDs are stable, e.g. REQ-001, REF-001, SRC-001, EV-001, DEC-001, STEP-001, CHECK-001. Do not renumber after deleting a record or reuse a removed ID.

## Records and trace

| Array | Required meaning |
| --- | --- |
| requirements | User instruction or explicit assumption; acceptance criterion; critical flag |
| references | Canonical URL; relevance/mismatch; selection rationale; dated activity; license record |
| sources | Reference ID; primary URL; actual access time; kind/status; exact locator; saved note |
| claims | Exact statement, class, support explanation, scope, limits; source/premise/requirement IDs |
| decisions | Requirement/evidence IDs; candidate/outcome; rationale; simpler alternatives; complexity/scale/revisit |
| plan_units | Requirement/adopted-decision IDs; incremental outcome; acceptance CHECK IDs |
| verification | Criterion/method; requirement/decision links; required flag; outcome and actual receipt |

`scope` stores goal/constraints/non-goals. `coverage` stores depth, reference-count exception, reason for no substantive rejection, and limitations. `questions` stores critical/open questions; ANSWERED needs linked evidence and a resolution.

Declare planned CHECKs with NOT_RUN and empty `evidence_path`, `tested_snapshot`, `checked_at`. For actual PASS or FAIL these fields must be filled. Manual/source/diff reviews are valid checks: save what was inspected, the result, and scope, not an invented command transcript.

Every requirement needs a decision, plan unit and required check. Every adopted decision needs a plan unit and required check. A plan unit's acceptance check must cover its requirements and decisions. Rejected/deferred decisions are verified through a required DIFF_REVIEW after build.

## Source classes

- **VERIFIED_SOURCE:** a directly supported statement in primary documentation; source kind DOCUMENTATION, status INSPECTED.
- **OPEN_SOURCE_IMPLEMENTATION:** the mechanism is in inspected source; kind IMPLEMENTATION, status INSPECTED, immutable commit SHA and file path.
- **OBSERVED_PUBLIC_BEHAVIOR:** actual observed action/result; kind OBSERVATION with environment/action locator and saved observation.
- **INFERENCE:** interpretation from sources, premise claims or requirements; never promoted transitively to VERIFIED. Premise links must not form cycles.
- **USER_REQUIREMENT:** linked user requirements and a user-instruction locator. An assumption is not USER_REQUIREMENT; keep it in scope/requirements or label derived interpretation INFERENCE.

Keep verified statements narrow. "This file declares Redis" does not prove "Redis is required for every message." Evidence that a mechanism exists does not establish its performance or why the product succeeded.

## Locators and notes

For implementation: repo URL, resolved commit, relevant path/symbol/lines, pinned primary URL, timezone-aware access timestamp. Status UNPINNED is honest but cannot support a VERIFIED implementation claim; use a scoped INFERENCE until inspection is pinned.

For docs: original URL, heading, version/publication date if supplied, actual access time. Do not invent a publication date from access time.

For observations: action, page/API/environment, date and observed result; screenshot locator if available. Public docs about UX belong to documented evidence, not observed behavior.

Source note content:

~~~text
Source: <primary URL>
Inspected: <actual timestamp>
Locator: <commit/path/heading/action>
Supports: EV-...
What the source actually says/does: <minimal extract or precise summary>
What it does not establish: <limits>
~~~

UNAVAILABLE needs a reason and can support only a limited inference, not a verified fact. Do not fabricate quotes, paths or commits. Notes/checksum integrity is not proof of tool provenance.

## License records

Read actual LICENSE/NOTICE and relevant file headers at the inspected revision. Record `status` INSPECTED/DECLARED_ONLY/MISSING/UNRECOGNIZED, SPDX if known, source URL and scope.

Default `reuse_mode: PATTERN_ONLY`, `code_copied: false`. API license null/NOASSERTION is not permissive authorization. Source-available code is not automatically open source.

Intentional SOURCE_REUSE requires inspected rights, a concrete `reuse_review`, compatibility with the target license, notices/attribution and file scope. Unknown rights block that reuse; they do not automatically block studying architectural ideas. The helper checks recorded fields, not legal compatibility.

## Render without losing prose

Copy the three templates or let `render` create them if absent. Write task-specific prose outside `<!-- rfb:... -->` markers. Helper changes only managed tables, then writes the cache last. Each replacement is atomic; a multi-file interruption is detected by subsequent checks, not a transaction guarantee.

Never edit generated tables to change a verdict: update the ledger and render. A correct-looking table can contain wrong claims; perform a source audit separately.
