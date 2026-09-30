# Implementation Plan: team-chat

## Goals and non-goals

Goal: Build a durable room-scoped message-history core
Constraints: Python stdlib; one process/local database; 30-user product context.
Excluded: HTTP/UI; authentication; federation; push delivery.

## Architecture and components

One original ChatStore module with a parameterized message table and (room, id) index. Persistence is ADOPT; federation/ephemeral retention are REJECT; push/jobs are DEFER.

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
| STEP-001 | Build a durable room-scoped message-history core | REQ-001, REQ-002 | DEC-001, DEC-002 | CHECK-002 |
<!-- rfb:plan:end -->

## Testing and verification

Source support audited before implementation. CHECK-002 runs actual behavior tests; any rejected/deferred
choice receives a linked diff review. Application files are hashed together for a current snapshot.
