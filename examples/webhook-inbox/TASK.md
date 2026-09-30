# Task

Implement an educational local inbox for generic HMAC-signed JSON messages. The local signed payload binds timestamp, event ID and original body; it is not Stripe-compatible. Store verified events durably, treat identical event-ID retries as duplicate, reject conflicting bodies, bad/stale signatures, nonobject/oversized JSON. No HTTP service or processing queue is requested.

Constraints: Python stdlib; one local writer; 1 MiB payload cap; 300-second signature window.

Non-goals: HTTP server; Stripe/Svix wire compatibility; job execution; outgoing retries.

Acceptance: Signature/timestamp failure, duplicate/conflicting event IDs, payload bounds/format and reopen persistence.
