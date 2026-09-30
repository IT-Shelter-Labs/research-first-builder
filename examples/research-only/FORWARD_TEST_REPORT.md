# Independent forward-test result

## Scenario and actual work

Used the installed research-first-build SKILL.md and its selection/evidence/decisions/verification resources, template/schema and helper. Task: research-only local JSON Lines literal top-level-field filter CLI. Quick depth selected JSON Lines, jq, and Python json.tool/standard-library documentation. Primary URLs were actually retrieved with web open/find/click tools; no source projects were installed or executed. A real failed JSON Lines LICENSE lookup is recorded as unavailable, not fabricated evidence.

Actual outputs: evidence.json; RESEARCH.md; PLAN.md; VERIFICATION.md; eight source notes; required manual source audit; required bounded-tree scope inspection; saved helper outputs. Proposed direct Python stdlib script with byte-line streaming, literal string-only matching, preserved matched bytes, explicit flush, strict parser policy, safe line diagnostics and no dependencies. Ordinary jq input framing/expression UX was the one real rejected candidate; no inflated infrastructure was introduced.

## Executed checks

- Helper render: exit 0; managed tables generated and narrative preserved.
- Helper prebuild (final ledger, including actual scope inspection): exit 0, CONTRACT_CHECKED (prebuild).
- Required SOURCE_AUDIT: actual manual original-heading inspection, PASS; saved sampled claim results and source-note-set hash.
- Scope inspection: actual bounded 16-file tree at inspection time, PASS; only Markdown/JSON/text research artifacts. Additional files after inspection are helper receipts and this report, not application code.
- Negative helper postbuild request with no implementation snapshot: exit 1. It explicitly rejects research-only as a completed build, missing snapshot, NOT_RUN application checks and missing rejected-pattern diff review. run.json retained PREBUILD_CHECKED and null postbuild receipt.

Application CHECK-003 through CHECK-005 remain NOT_RUN. No test output or implementation snapshot was invented. Actual saved outputs are checks/render-output.txt, checks/prebuild-output.txt and checks/expected-postbuild-rejection.txt.

## Observed UX and contract limits

No contract failure occurred while authoring a valid research-only handoff. It worked on first render/prebuild attempt. The deliberately invalid postbuild request failed as expected.

1. Even quick depth takes substantial hand-assembly: the tiny scenario needed six requirements, seven claims, five decisions, four plan units and five checks, plus three reports and notes. A starter command or complete research-only example would reduce schema lookup and typing. The intentionally incomplete template is honest but offers little onboarding acceleration.
2. Prebuild success prints "Sources still need semantic review" even when a required PASS source audit exists and semantic inspection has been performed. The caution is valid because the tool cannot prove truth, but wording could say that the supplied audit passed while the tool checks only structure.
3. Managed evidence tables display SRC IDs, without original-source locator/URL links, so reviewing a specific claim requires opening the ledger or notes. A generated source index or links to note files would make the handoff easier to audit.
4. A postbuild call on research-only emits unrelated missing-build-check messages after the decisive intent rejection. Short-circuiting or grouping the intent error would clarify that no implementation should be created to satisfy those messages.

These are workflow/UX observations, not proven safety defects. The checker correctly rejects research-only postbuild and does not execute arbitrary ledger commands.

## Remaining limits and scope boundary

Only documentation-backed evidence was gathered; no immutable source implementation claims or personally observed CLI behavior were made. Actual app behavior, performance, byte preservation, buffering and Windows/Linux checks remain future work. Python availability is an assumption and not a zero-runtime installation promise. JSON Lines licensing remains unknown and no source/text reuse is authorized. Contract receipts do not establish truth, legal compatibility or permission.

All filesystem mutations by this agent stayed in .rfb-work/forward-test. No product repository edits, application source, packaging files or executable tests were written. The authoring code ran transiently through the shell to create research artifacts; it is not application implementation.
