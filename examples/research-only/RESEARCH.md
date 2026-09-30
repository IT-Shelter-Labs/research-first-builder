# Research: local JSON Lines filter

## Project definition

Realistic request: "Research-only: design a small local JSON Lines filter CLI for operational logs. Match a named top-level field to a literal string, stream stdin to stdout, report malformed input clearly, and keep installation simple. Do not implement the application yet."

The operator pipes local logs through a single-purpose filter. Quick depth inspected three relevant primary references: the framing specification, jq as the existing-tool analogue, and Python json.tool/standard library as the smaller direct implementation alternative. No reference projects were installed or executed.

## Assumptions and research questions

Assume Python 3.11+ already exists and records fit in memory individually. These are explicit design assumptions, not requirements supplied by the operator. The three consequential questions concern framing/matching, safe failures, and distribution; the ledger records the answers. Stop discovery now because the sources explain these choices; broader infrastructure would not answer this job better.

## References

<!-- rfb:references:start -->
| ID | Reference | Why relevant | Mismatch | License / reuse |
| --- | --- | --- | --- | --- |
| REF-001 | [https://jsonlines.org/](https://jsonlines.org/) | Format contract for operational logs | Format documentation, not a filtering program | MISSING · unknown · PATTERN_ONLY |
| REF-002 | [https://jqlang.org/manual/v1.8/](https://jqlang.org/manual/v1.8/) | Existing local stdin/stdout JSON filtering CLI | General expression language; default framing accepts whitespace-separated values | INSPECTED · MIT; CC-BY-3.0 · PATTERN_ONLY |
| REF-003 | [https://docs.python.org/3.11/library/json.html](https://docs.python.org/3.11/library/json.html) | Documented local JSON-lines stdin/stdout CLI plus parser and arguments | Validator/formatter does not implement literal-field filtering | INSPECTED · PSF-2.0 · PATTERN_ONLY |
<!-- rfb:references:end -->

## Evidence

<!-- rfb:evidence:start -->
| ID | Claim | Class | Sources / premises | Scope |
| --- | --- | --- | --- | --- |
| EV-001 | UTF-8, no BOM; each physical line is a valid JSON value, including scalars; blank lines invalid. LF and CRLF accepted; last newline optional. Footer generated 2026-09-26. | VERIFIED · documented | [SRC-001](sources/SRC-001.md) | Inspected documentation version and headings only |
| EV-002 | Input consists of whitespace-separated JSON values. --arg binds a string. select passes or drops input. --slurp collects all input; --unbuffered flushes each output. | VERIFIED · documented | [SRC-002](sources/SRC-002.md) | Inspected documentation version and headings only |
| EV-003 | JSONDecodeError exposes message and column. Defaults accept NaN/Infinity and duplicate names (last wins); parse_constant and object_pairs_hook allow changing behavior. json.tool supports --json-lines. | VERIFIED · documented | [SRC-003](sources/SRC-003.md) | Inspected documentation version and headings only |
| EV-004 | ArgumentParser.error prints usage/error to stderr and exits with status 2. | VERIFIED · documented | [SRC-004](sources/SRC-004.md) | Inspected documentation version and headings only |
| EV-005 | Standard streams offer binary buffer objects. Noninteractive stdout is block-buffered; Windows pipes may use locale encoding in text mode. | VERIFIED · documented | [SRC-005](sources/SRC-005.md) | Inspected documentation version and headings only |
| EV-006 | One script using standard-library parsing and binary line I/O fits the narrow job under the Python-available assumption; this is a design inference. | INFERENCE | EV-001, EV-003, EV-004, EV-005, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006 | Proposed local operational CLI only |
| EV-007 | The request explicitly forbids application implementation in this run. | REQUIREMENT | REQ-001 | This run |
<!-- rfb:evidence:end -->

## Cross-project comparison

| Reference mechanism | Fit and mismatch | Choice |
| --- | --- | --- |
| JSON Lines physical-line framing (EV-001) | Same log-stream job; deliberately says nothing about filtering UX | Adopt framing; no framework |
| jq string arguments, object indexing, select and unbuffered output (EV-002) | Solves literal filtering; ordinary parser accepts whitespace-separated values, not strict one-record-per-line | Reject ordinary jq as whole product (DEC-005); retain it as a practical alternative |
| Python json.tool JSONL mode, decoder hooks, argparse and binary streams (EV-003 to EV-005) | Demonstrates simple local CLI primitives; formatter does not supply field filter or policy | Adopt direct stdlib design as inference (EV-006), conditioned on available Python |

## Adopted, rejected and deferred patterns

<!-- rfb:decisions:start -->
| ID | Choice | Outcome | Evidence | Reason / complexity | Revisit |
| --- | --- | --- | --- | --- | --- |
| DEC-001 | Stop after researched handoff | ADOPT | EV-007 | Research-only is the requested outcome. Complexity: Three reports plus ledger; no application writes. | Implement only after a new explicit request. |
| DEC-002 | Direct byte-line loop and literal decoded-string comparison | ADOPT | EV-001, EV-005, EV-006 | JSON Lines offers record-at-a-time framing; byte I/O avoids locale/newline rewriting. Preserve original matching record bytes, adding LF only when final matched line has no terminator. Complexity: One-record parsing and explicit flush after each match. | Revisit parser/runtime if measured throughput or record size exceeds operational bounds. |
| DEC-003 | Strict input with fail-fast safe diagnostics | ADOPT | EV-001, EV-003, EV-004 | Reject blank/invalid UTF-8/BOM/syntax/nonstandard numeric constants; duplicate keys rejected by hook to avoid ambiguous match. Valid non-object JSON is a nonmatch. Catch parser ValueError/RecursionError as record failures. Complexity: Explicit decoder hooks, global line count, safe diagnostics. | Add explicit continue mode only if operators ask for partial recovery and metrics. |
| DEC-004 | Python 3.11+ single script, standard library only | ADOPT | EV-003, EV-004, EV-005, EV-006 | json.tool demonstrates standard-library local JSONL CLI primitives. The job needs no package graph under declared runtime assumption. Complexity: Python runtime prerequisite; no installer or dependencies. | If operators lack Python or need signed binaries, revisit compiled distribution with research. |
| DEC-005 | Use ordinary jq invocation as the whole product | REJECT | EV-001, EV-002 | jq solves general filtering and offers a single binary, but ordinary input framing is whitespace-separated values and its expression UX is broader than the fixed literal-field job; strict physical-line diagnostics need more wrapper policy. Complexity: Extra expression and wrapper contract despite excellent general tool. | Revisit if scope changes to general expressions or deployment forbids Python. |
<!-- rfb:decisions:end -->

### Rejected patterns

Ordinary jq invocation is the only substantive rejected candidate. Its broad expression interface and whitespace-separated framing require extra wrapper policy for this narrow CLI. jq is still the simpler existing option where those constraints do not matter, and its binary avoids a Python prerequisite. No enterprise candidates were invented to pad rejections.

## Risks, licenses and unknowns

All choices use patterns only, with no copied code. jq COPYING distinguishes MIT code and CC BY 3.0 docs, with bundled notices; Python's actual license page was read. JSON Lines LICENSE lookup returned a real Internal Error; rights remain unknown. No legal compatibility verdict is claimed. Documentation versions are recorded; none of the evidence is an implementation or personally observed CLI behavior claim. The parser's default acceptance of NaN/Infinity would contradict strict input unless corrected in DEC-003. Large/deep records still face interpreter limits; throughput and cross-platform behavior remain untested.

## Source index (added after independent run)

<!-- rfb:sources:start -->
| ID / note | Primary source | Locator | Inspection |
| --- | --- | --- | --- |
| [SRC-001](sources/SRC-001.md) | [original](https://jsonlines.org/) | JSON Lines requirements 1-3 and footer | INSPECTED |
| [SRC-002](sources/SRC-002.md) | [original](https://jqlang.org/manual/v1.8/) | jq 1.8: Invoking jq; --arg; --slurp; --unbuffered; Object Index; select(boolean_expression) | INSPECTED |
| [SRC-003](sources/SRC-003.md) | [original](https://docs.python.org/3.11/library/json.html) | Python 3.11.16: json.loads; JSONDecoder; Exceptions; Standard Compliance | INSPECTED |
| [SRC-004](sources/SRC-004.md) | [original](https://docs.python.org/3.11/library/argparse.html) | Python 3.11.16: ArgumentParser.error | INSPECTED |
| [SRC-005](sources/SRC-005.md) | [original](https://docs.python.org/3.11/library/sys.html) | Python 3.11.16: sys.stdin, sys.stdout, sys.stderr | INSPECTED |
| [SRC-006](sources/SRC-006.md) | [original](https://raw.githubusercontent.com/jqlang/jq/jq-1.8.1/COPYING) | jq-1.8.1 COPYING lines 0-26 | INSPECTED |
| [SRC-007](sources/SRC-007.md) | [original](https://docs.python.org/3.11/license.html) | Terms and conditions; PSF License Agreement for Python 3.11.16 | INSPECTED |
| [SRC-008](sources/SRC-008.md) | [original](https://raw.githubusercontent.com/wardi/jsonlines/master/LICENSE) | Attempted LICENSE lookup | UNAVAILABLE |
<!-- rfb:sources:end -->
