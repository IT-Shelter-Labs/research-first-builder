# Implementation Plan: webhook-inbox

## Goals and non-goals

Goal: Build a durable generic signed webhook-inbox core
Constraints: Python stdlib; one local writer; 1 MiB payload cap; 300-second signature window.
Excluded: HTTP server; Stripe/Svix wire compatibility; job execution; outgoing retries.

## Architecture and components

One original Inbox module, a UNIQUE event-ID table, raw bytes and digest, a local HMAC verifier and a bounded JSON validator. Commit precedes the returned stored receipt; no commands or jobs are executed.

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
| STEP-001 | Build a durable generic signed webhook-inbox core | REQ-001, REQ-002 | DEC-001, DEC-002 | CHECK-002 |
<!-- rfb:plan:end -->

## Testing and verification

Source support audited before implementation. CHECK-002 runs actual behavior tests; any rejected/deferred
choice receives a linked diff review. Application files are hashed together for a current snapshot.
