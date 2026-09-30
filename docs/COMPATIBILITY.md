# Actual compatibility status

Recorded 2026-09-30 / 2026-10-01. Distinguish installation, discovery and a complete model workflow.
No host has a full native acceptance badge in this candidate.

| Host | Local copy via skills 1.7.0 | Native model test | Status |
| --- | --- | --- | --- |
| Codex 0.159.2 (bundled local binary) | PASS, `.agents/skills` | Skill discovered/loaded; HTTPS fallback reached model. Nested read-only tool policy denied file reads; no completed artifacts. | Format/install and native discovery tested; full workflow incomplete |
| Claude Code 2.1.190 | PASS, `.claude/skills` | Corrected empty MCP config accepted; authentication HTTP 403 before useful model execution. | Format/install tested; full workflow not verified |
| Cursor (3.6.31 executable available) | PASS, `.agents/skills` | No native model run performed | Compatible beta by format/install only |
| OpenCode | PASS, `.agents/skills` | Executable unavailable; no native model run performed | Compatible beta by format/install only |
| Codex/ChatGPT desktop local coding environment | Manual skill-path independent agent run completed | Real research-only forward test with primary web tools; this is explicit file invocation, not native installed-skill discovery | Instruction workflow exercised; UI installation acceptance pending |

The user-facing Windows terminal did not have `codex` on PATH. That is not a requirement for desktop installation
and does not imply the desktop skill is broken. We did not alter credentials, install another agent CLI,
change global permissions or replace user configuration to force a pass.

## Reproduced locally

- Native Windows / Python 3.11: offline contract/render/packaging tests; one symlink-creation case skipped by host permissions.
- Isolated full-folder install with spaces in paths, changed working directory and no development-checkout dependency.
- Node 24.19.0 + skills 1.7.0 `--copy` install to a scratch project for all four targets.
- Three genuine-source, maintainer-authored educational implementations: actual behavior tests and current postbuild checks.
- One independent research-only agent run and a real negative postbuild test; no application was written in that run.

See [evaluation observations](../evals/README.md) and linked example receipts. Hosted Windows/Linux CI is
configured, not yet executed on a public repository. Cross-host availability depends on the host's model,
file-tool and source-access settings; installation success alone cannot prove those capabilities.

## Native acceptance to complete

In a normal authenticated local coding project, copy the whole skill folder and invoke it through the host's
native skill selector. Run the quick research-only task in [QUICKSTART](QUICKSTART.md), then a bounded full
task with actual checks. Record version, skill discovery, source access, results, errors and artifact receipts;
remove private paths/tokens before sharing. No credential changes or permission bypasses are part of this test.
