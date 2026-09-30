# Implementation Plan: research-only handoff

## Goals and non-goals

Design a local literal-field filter. This run stops at the researched handoff (DEC-001). All implementation milestones below require a later implementation request. No service, datastore, UI, nested paths, regular expressions, general query language, packaging framework or network access is needed.

## Architecture and components

One proposed script, invoked as `python jsonl_filter.py --field level --equals error`, uses only Python 3.11+ standard-library modules (DEC-004). `--field` and `--equals` are required strings; disable argument abbreviation. The field is a literal top-level key, including dots, empty strings or Unicode. Compare only a decoded string to the supplied string, case-sensitive, with no normalization/coercion. A missing field, null, numeric value or valid non-object JSON is a nonmatch.

Read one binary physical line from stdin, decode UTF-8 strictly, parse one JSON value, inspect the top-level field, and emit the original matching line bytes to stdout (DEC-002). Preserve spacing, escapes and CRLF; append LF only to a matched final record with no newline. Flush each match so it appears before stdin closes. There is no whole-input collection; memory grows with the largest record, not record count. Empty stdin succeeds with no output. Original bytes avoid changing numeric representation while filtering strings.

## Data model and interfaces

A record is one valid JSON value per physical line. JSONL disallows blank lines/BOM and permits scalar values (EV-001). Decode bytes to UTF-8 before parsing so Python's broader byte-encoding detection cannot accept UTF-16 input. Reject NaN/Infinity with parser hooks; reject duplicate object names through object-pairs validation as an explicit application policy (DEC-003). This policy is stricter than the format's unspecified duplicate-name handling.

On first malformed record, stop with exit 1 and `jsonl-filter: line N, column C: malformed JSON` or a safe encoding/duplicate/runtime-limit error kind when column is unavailable. Line/column are 1-based, column measured in decoded characters. Do not echo raw record contents or a traceback. Flush earlier emitted matches; stdout is partial on failure and consumers must inspect exit status. Argument errors use stderr and exit 2; successful/no-match runs exit 0. Input/output errors, including a closed output pipe, produce a short stderr diagnostic and exit 1; verify final-buffer flush handling. Catch decoder ValueError and RecursionError with the record line rather than leaking an exception.

## Security and deployment

All processing stays local. No telemetry, uploads or dependencies. Operators may pipe sensitive logs; diagnostics contain location and error kind only. One-script copying is simple under the Python-present assumption, but does not provide zero-runtime installation. If that assumption fails, revisit a binary or jq based on actual deployment needs. No performance target is invented. Deliberate maximum-line limits or adversarial-input hardening are outside the ordinary operational MVP and must be researched if needed. Database/API sections are not applicable.

## Milestones and acceptance checks

<!-- rfb:plan:start -->
| ID | Outcome | Requirements | Decisions | Acceptance |
| --- | --- | --- | --- | --- |
| STEP-001 | Hand off source-backed research and plan only. | REQ-001 | DEC-001 | CHECK-002 |
| STEP-002 | Later implement literal-key, string-only matching and per-line byte streaming. | REQ-002, REQ-003 | DEC-002 | CHECK-003 |
| STEP-003 | Later implement strict errors, statuses and clean stderr. | REQ-004 | DEC-003 | CHECK-004 |
| STEP-004 | Later document and smoke-check one-script runtime-only installation. | REQ-005, REQ-006 | DEC-004 | CHECK-005 |
<!-- rfb:plan:end -->

## Testing and verification

Required source audit checked primary supporting headings; actual note is checks/CHECK-001.txt. Future behavior checks cover Unicode and literal dotted keys, string-vs-number matching, line endings, partial output and safe failure paths. A subprocess producer must withhold EOF and observe a flushed match to prove streaming. Use byte-safe subprocess I/O for Windows/Linux checks; shell text-pipe transcoding is not a parser result. A later implementation must also review its diff for DEC-005's rejected complexity. All application checks are NOT_RUN here. The helper's prebuild receipt checks artifact consistency, not truth or implementation permission.
