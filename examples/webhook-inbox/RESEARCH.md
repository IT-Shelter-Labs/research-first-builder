# Research: webhook-inbox

## Project definition

Implement an educational local inbox for generic HMAC-signed JSON messages. The local signed payload binds timestamp, event ID and original body; it is not Stripe-compatible. Store verified events durably, treat identical event-ID retries as duplicate, reject conflicting bodies, bad/stale signatures, nonobject/oversized JSON. No HTTP service or processing queue is requested.

## Assumptions and research questions

This is a small educational subsystem with Python 3.11+ available. It is not a production-ready clone.
Question: What is the smallest mechanism that meets this bounded task?

## References

<!-- rfb:references:start -->
| ID | Reference | Why relevant | Mismatch | License / reuse |
| --- | --- | --- | --- | --- |
| REF-001 | [https://github.com/adnanh/webhook](https://github.com/adnanh/webhook) | Small incoming-hook boundary | Executes configured commands | INSPECTED · MIT · PATTERN_ONLY |
| REF-002 | [https://github.com/svix/svix-webhooks](https://github.com/svix/svix-webhooks) | Webhook storage/queue comparison | Primarily delivery service with broader deployment | INSPECTED · MIT · PATTERN_ONLY |
| REF-003 | [https://docs.stripe.com/webhooks](https://docs.stripe.com/webhooks) | Duplicate/replay and raw-body verification mechanisms | Primary mechanism documentation, not a like-for-like complete application. | MISSING · unknown · PATTERN_ONLY |
| REF-004 | [https://www.sqlite.org/lang_conflict.html](https://www.sqlite.org/lang_conflict.html) | Local uniqueness conflict behavior | Primary mechanism documentation, not a like-for-like complete application. | MISSING · unknown · PATTERN_ONLY |
<!-- rfb:references:end -->

## Source index

<!-- rfb:sources:start -->
| ID / note | Primary source | Locator | Inspection |
| --- | --- | --- | --- |
| [SRC-001](sources/SRC-001.md) | [original](https://github.com/adnanh/webhook/blob/2bbdeb9f90b5f98c7b7b8976881efd6da9f69571/docs/Hook-Definition.md) | 2bbdeb9f90b5f98c7b7b8976881efd6da9f69571 · docs/Hook-Definition.md · id/execute-command; include-command-output-in-response | INSPECTED |
| [SRC-002](sources/SRC-002.md) | [original](https://github.com/svix/svix-webhooks/blob/dd4d50efb234b4a9c313f6c31cdb84ba150c3bd2/README.md) | dd4d50efb234b4a9c313f6c31cdb84ba150c3bd2 · README.md · Runtime dependencies | INSPECTED |
| [SRC-003](sources/SRC-003.md) | [original](https://docs.stripe.com/webhooks) | Handle duplicate events; signature verification; preventing replay attacks | INSPECTED |
| [SRC-004](sources/SRC-004.md) | [original](https://www.sqlite.org/lang_conflict.html) | IGNORE / UNIQUE constraints | INSPECTED |
<!-- rfb:sources:end -->

## Evidence

<!-- rfb:evidence:start -->
| ID | Claim | Class | Sources / premises | Scope |
| --- | --- | --- | --- | --- |
| EV-001 | adnanh/webhook defines command execution and an option to wait for command output. | VERIFIED · documented | [SRC-001](sources/SRC-001.md) | Documented hook configuration, not its measured execution timing. |
| EV-002 | Svix documents PostgreSQL event storage and an optional Redis queue/cache. | VERIFIED · documented | [SRC-002](sources/SRC-002.md) | Self-hosted Svix README; not a claim about its hosted internals. |
| EV-003 | Stripe documents duplicate event deliveries and event-ID tracking. | VERIFIED · documented | [SRC-003](sources/SRC-003.md) | Same event-ID retries; not semantic deduplication of different events. |
| EV-004 | Stripe documents raw-body signing with timestamp checks and constant-time comparison. | VERIFIED · documented | [SRC-003](sources/SRC-003.md) | Generic principle only; our local example is not a Stripe protocol implementation. |
| EV-005 | SQLite documents IGNORE behavior for relevant uniqueness conflicts. | VERIFIED · documented | [SRC-004](sources/SRC-004.md) | SQLite conflict behavior, not universal exactly-once delivery. |
| EV-006 | A local signed inbox can persist and deduplicate without a broker. | INFERENCE | EV-002, EV-003, EV-005 | Educational one-process ingest core; downstream processing is excluded. |
<!-- rfb:evidence:end -->

## Cross-project comparison

| Area | adnanh/webhook | Svix | Stripe docs | Our choice |
| --- | --- | --- | --- | --- |
| Work | Commands (EV-001) | Storage/optional queue (EV-002) | Duplicates/signatures (EV-003/004) | Verify + persist only |
| Deployment | Small hook server | External services | Provider delivery | One local SQLite file |

## Adopted, rejected and deferred patterns

<!-- rfb:decisions:start -->
| ID | Choice | Outcome | Evidence | Reason / complexity | Revisit |
| --- | --- | --- | --- | --- | --- |
| DEC-001 | Unique event ID in a local SQLite inbox | ADOPT | EV-003, EV-005, EV-006 | Deduplication and durable acceptance are the requested mechanisms. Complexity: One table/transaction | Independent ingest replicas or measured contention |
| DEC-002 | Raw-body HMAC, timestamp window, bounded JSON input | ADOPT | EV-004 | Untrusted input must be checked before recording it. Complexity: Local crypto/validation; own educational wire format | Real provider integration requires its official verifier |
| DEC-003 | PostgreSQL + separate Redis queue | DEFER | EV-002, EV-006 | No distributed processing or outgoing retries in the task. Complexity: External services and operational failure modes | Documented asynchronous processing requirement |
| DEC-004 | Execute incoming payload-selected shell commands | REJECT | EV-001 | The task is to store events; command execution would add unnecessary authority. Complexity: Execution surface and response coupling | Separate explicitly authorized automation feature |
<!-- rfb:decisions:end -->

### Rejected patterns

The REJECT/DEFER records above describe actual candidates considered, with concrete scope mismatches.

## Risks, licenses and unknowns

Repository licenses were inspected at the recorded revisions where fetched. Documentation-only rights may remain
unknown; all interactions are PATTERN_ONLY, with no code/text transfer. Source notes paraphrase narrow findings.
No repository runtime, security certification or commercial-success causal claim was tested.
