# Implementation Plan: local-cli

## Goals and non-goals

Goal: Build a literal JSON Lines filter
Constraints: Python stdlib; literal top-level string equality; 65536 bytes per line; preserve matched bytes.
Excluded: query DSL; regex; nested paths; plugin architecture; whole-input buffering.

## Architecture and components

One original binary-line iterator plus argparse entrypoint. No additional architecture pattern is needed. The user requires no external binary dependency; jq remains a good option when that constraint changes.

## Data model and interfaces

One app.py module and behavior tests. Read TASK.md for the bounded interface contract.
The choices follow the adopted DEC IDs below; no reusable application framework is introduced.

## Security and deployment

Local educational code only. No exposed HTTP service, production identity system or deployment automation.
Validate untrusted input at the stated boundaries; tests cover the consequential failure paths.

## Milestones and acceptance checks

<!-- rfb:plan:start -->
| ID | Outcome | Requirements | Decisions | Acceptance |
| --- | --- | --- | --- | --- |
| STEP-001 | Build a literal JSON Lines filter | REQ-001, REQ-002 | DEC-001 | CHECK-002 |
<!-- rfb:plan:end -->

## Testing and verification

Source support audited before implementation. CHECK-002 runs actual behavior tests; any rejected/deferred
choice receives a linked diff review. Application files are hashed together for a current snapshot.
