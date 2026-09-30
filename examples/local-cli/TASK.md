# Task

Build a small local JSON Lines filter with field/value arguments, binary stdin/stdout streaming, string-only literal matching, preserved matched bytes, explicit flush and line-number diagnostics. All JSON values may appear; nonobjects do not match. Reject malformed JSON, duplicate keys, nonfinite numbers and lines over 65536 bytes. An error can follow already-emitted matches.

Constraints: Python stdlib; literal top-level string equality; 65536 bytes per line; preserve matched bytes.

Non-goals: query DSL; regex; nested paths; plugin architecture; whole-input buffering.

Acceptance: Lazy streaming, exact bytes/Unicode/newline, literal string-only matching, invalid-input diagnostics and CLI exit codes.
