# Inspect the evidence, then run the checks

These are real-source educational examples, not production-ready systems or claims of autonomous benchmark wins.
Primary sources were inspected; reference applications were not installed or executed. Original code was written
only after each example's prebuild check passed. Third-party study is PATTERN_ONLY.

| Example | Useful decision | Result |
| --- | --- | --- |
| [Team-chat storage](team-chat/RESEARCH.md) | Durable room history in SQLite; reject disappearing retention/federation, defer push infrastructure | 5 behavior tests + actual diff review |
| [Signed webhook inbox](webhook-inbox/RESEARCH.md) | Unique event ID and raw-body verification; defer separate services, reject command execution | 6 behavior tests + actual diff review |
| [Local JSON Lines CLI](local-cli/RESEARCH.md) | NO-PATTERN: direct stdlib literal filter | 6 behavior tests; no fabricated rejection quota |
| [Independent research-only run](research-only/PROVENANCE.md) | Compare existing tools, propose a scoped direct implementation | Research/plan handoff; app checks intentionally NOT_RUN |

Each build includes TASK, RESEARCH, PLAN, VERIFICATION, canonical evidence, source notes, actual outputs,
app.py and test_app.py. Read RESEARCH's comparison/decisions before opening the code.

From the repository root:

```text
python tools/verify_examples.py
```

This runs fixed behavior tests in isolated processes, hashes app.py/test_app.py and checks postbuild against
recorded receipts. It does not execute commands from the ledger or quietly renew stale planning.
It writes no research or verification records by default. Caches/temporary files are not part of the snapshot.

To run an individual example, enter its folder and run:

```text
python -m unittest discover -s . -p test_app.py -v
```

The chat core is storage only, without authentication or network access. Its room filter is not authorization.
The signed inbox uses its own educational HMAC wire format and is not Stripe/Svix compatible. It has no HTTP
server or downstream job processing. The CLI preserves matched bytes; input errors can follow already-emitted
output. Its line cap is 65536 bytes including the delimiter.

Maintainers changing code must first review whether the plan is affected. Record an actual diff review for
REJECT/DEFER decisions with the new file fingerprint, then use `python tools/verify_examples.py --record` to
execute tests and record fresh results. This does not renew prebuild; stale planning fails until separately reviewed.
