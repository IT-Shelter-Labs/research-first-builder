# Research: local-cli

## Project definition

Build a small local JSON Lines filter with field/value arguments, binary stdin/stdout streaming, string-only literal matching, preserved matched bytes, explicit flush and line-number diagnostics. All JSON values may appear; nonobjects do not match. Reject malformed JSON, duplicate keys, nonfinite numbers and lines over 65536 bytes. An error can follow already-emitted matches.

## Assumptions and research questions

This is a small educational subsystem with Python 3.11+ available. It is not a production-ready clone.
Question: What is the smallest mechanism that meets this bounded task?

## References

<!-- rfb:references:start -->
| ID | Reference | Why relevant | Mismatch | License / reuse |
| --- | --- | --- | --- | --- |
| REF-001 | [https://github.com/jqlang/jq](https://github.com/jqlang/jq) | JSON CLI/error-handling mechanism | Much broader expression language | INSPECTED · MIT; docs CC-BY-3.0 · PATTERN_ONLY |
| REF-002 | [https://github.com/BurntSushi/ripgrep](https://github.com/BurntSushi/ripgrep) | Line-oriented CLI contrast | Text patterns, not typed JSON fields | INSPECTED · MIT OR Unlicense · PATTERN_ONLY |
<!-- rfb:references:end -->

## Source index

<!-- rfb:sources:start -->
| ID / note | Primary source | Locator | Inspection |
| --- | --- | --- | --- |
| [SRC-001](sources/SRC-001.md) | [original](https://github.com/jqlang/jq/blob/9a75bb0d4318bb6f6509635d89319ff40ee9ecac/README.md) | 9a75bb0d4318bb6f6509635d89319ff40ee9ecac · README.md · Opening description | INSPECTED |
| [SRC-002](sources/SRC-002.md) | [original](https://github.com/jqlang/jq/blob/9a75bb0d4318bb6f6509635d89319ff40ee9ecac/src/main.c) | 9a75bb0d4318bb6f6509635d89319ff40ee9ecac · src/main.c · Input loop / parse errors, lines 677-705 | INSPECTED |
| [SRC-003](sources/SRC-003.md) | [original](https://github.com/BurntSushi/ripgrep/blob/3fce3b5bb0236da2df6d99672afb8a719642eca7/README.md) | 3fce3b5bb0236da2df6d99672afb8a719642eca7 · README.md · Opening description | INSPECTED |
<!-- rfb:sources:end -->

## Evidence

<!-- rfb:evidence:start -->
| ID | Claim | Class | Sources / premises | Scope |
| --- | --- | --- | --- | --- |
| EV-001 | jq describes a general command-line JSON transformation tool. | VERIFIED · documented | [SRC-001](sources/SRC-001.md) | Documented capability, not a framing/performance guarantee. |
| EV-002 | jq's inspected input loop reports parse errors and records a nonzero failure result. | VERIFIED · implementation | [SRC-002](sources/SRC-002.md) | Default non-sequence branch; our CLI has its own exit contract. |
| EV-003 | ripgrep describes line-oriented pattern search. | VERIFIED · documented | [SRC-003](sources/SRC-003.md) | Text-search job, not JSON field semantics. |
| EV-004 | A direct stdlib line filter fits literal-field matching without a DSL. | INFERENCE | EV-001, EV-002, EV-003 | Our design judgment; tests verify actual framing and byte preservation. |
<!-- rfb:evidence:end -->

## Cross-project comparison

| Reference | Useful principle | Mismatch | Choice |
| --- | --- | --- | --- |
| jq | JSON handling and stderr failure (EV-001/002) | Full expression language | Use narrow principle |
| ripgrep | Line-oriented CLI (EV-003) | Raw text search | Keep JSON semantics |
| Our task | One literal predicate | No frameworks needed | NO-PATTERN direct code (EV-004) |

## Adopted, rejected and deferred patterns

<!-- rfb:decisions:start -->
| ID | Choice | Outcome | Evidence | Reason / complexity | Revisit |
| --- | --- | --- | --- | --- | --- |
| DEC-001 | NO-PATTERN: direct Python stdlib filter | ADOPT | EV-004 | A bounded iterator and a literal predicate satisfy the whole task. Complexity: One script, Python prerequisite | Actual demand for expressions/nested paths |
<!-- rfb:decisions:end -->

### Rejected patterns

No substantive architecture pattern was rejected. A framework/DSL was excluded by the task, not introduced as a fabricated candidate; NO-PATTERN is the adopted outcome.

## Risks, licenses and unknowns

Repository licenses were inspected at the recorded revisions where fetched. Documentation-only rights may remain
unknown; all interactions are PATTERN_ONLY, with no code/text transfer. Source notes paraphrase narrow findings.
No repository runtime, security certification or commercial-success causal claim was tested.
