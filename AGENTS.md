# Research First Builder maintenance

Keep one self-contained skill in skills/research-first-build. The bundled helper
uses Python 3.11+ standard library only; it must not execute ledger commands or
make network calls.

Preserve the distinction between structural checks, source-truth review and user
authorization. Never promote fictional fixtures, advertised compatibility or
unexecuted commands to real evidence.

Run python -m unittest discover -s tests -v after meaningful helper/contract changes.
Run tools/verify_examples.py after changes affecting examples. Keep docs, templates,
schema and checker consistent. Do not update recorded receipts without actual checks.

Do not add backend services, host-specific skill forks or automatic publication.
