# Actual compatibility status

Recorded 2026-09-30 / 2026-10-01. Distinguish installation, discovery and a complete model workflow.
No host has a full native acceptance badge in this candidate.

| Host | Local copy via skills 1.7.0 | Native model test | Status |
| --- | --- | --- | --- |
| Codex 0.159.2 (bundled local binary) | PASS, `.agents/skills` | Skill discovered/loaded; HTTPS fallback reached model. Nested read-only tool policy denied file reads; no completed artifacts. | Format/install and native discovery tested; full workflow incomplete |
| Claude Code 2.1.190 | PASS, `.claude/skills` | Corrected empty MCP config accepted; authentication HTTP 403 before useful model execution. | Format/install tested; full workflow not verified |
| Cursor (3.6.31 executable available) | PASS, `.agents/skills` | No native model run performed | Compatible beta by format/install only |
| OpenCode | PASS, `.agents/skills` | Executable unavailable; no native model run performed | Compatible beta by format/install only |
| Codex/ChatGPT desktop local coding environment | Installed 13-file folder byte-matched; explicit skill-file invocation | Independent research-only run and full Bookmarks task completed; 55 HTTP assertions independently repeated, current postbuild PASS | Full instruction workflow exercised; native selector discovery pending in correct project context |

The desktop workflow does not require the `codex` terminal command. CLI and desktop acceptance are recorded
separately; neither installation nor discovery alone establishes full workflow compatibility.

## Reproduced locally

- Native Windows / Python 3.11: offline contract/render/packaging tests; one symlink-creation case skipped by host permissions.
- Isolated full-folder install with spaces in paths, changed working directory and no development-checkout dependency.
- Current skill frontmatter passed the official Agent Skills reference validator at [69ef37e](https://github.com/agentskills/agentskills/tree/69ef37e9424c0a7ea9dd2293b559e43ec8176379/skills-ref), including `compatibility`. This validates format, not model behavior.
- Node 24.19.0 + skills 1.7.0 `--copy` install to a scratch project for all four targets.
- Three genuine-source, maintainer-authored educational implementations: actual behavior tests and current postbuild checks.
- One independent research-only agent run and a real negative postbuild test; no application was written in that run.
- One real desktop full task with primary analogue research, prebuild before app code, implementation and actual checks. [Acceptance report and limits](acceptance/DESKTOP_BOOKMARKS.md).
- Public GitHub install using skills 1.7.0 in a clean project with Git credential helpers disabled: 13 distribution files byte-matched and isolated helper init passed. This is installation acceptance, not native model execution.
- Updated skill after the review fixes: skills 1.7.0 local-copy install into an isolated project, all 13 files byte-matched; helper init and actionable starter failures verified in separate processes. No new native-model acceptance is implied.

See [evaluation observations](../evals/README.md) and linked example receipts. Hosted Windows/Linux CI and lint
[passed on e21efae](https://github.com/IT-Shelter-Labs/research-first-builder/actions/runs/36849930287), inspected 2026-10-01.
Native-workflow and public-install observations cover the initial candidate. Subsequent main changes have
offline regression and isolated local-copy coverage, not a new native-model acceptance run; check Actions for the current revision.
Cross-host availability depends on the host's model,
file-tool and source-access settings; installation success alone cannot prove those capabilities.

## Native acceptance to complete

Open the actual target project containing the installed skill as the coding workspace; a child folder named
only in a prompt may lie outside discovery. The desktop full task worked through explicit file invocation.
Its remaining discovery check can be small and does not require rebuilding that application.

In a normal authenticated local coding project, copy the whole skill folder and invoke it through the host's
native skill selector. Run the quick research-only task in [QUICKSTART](QUICKSTART.md), then a bounded full
task with actual checks. Record version, skill discovery, source access, results, errors and artifact receipts;
remove private paths/tokens before sharing. No credential changes or permission bypasses are part of this test.
