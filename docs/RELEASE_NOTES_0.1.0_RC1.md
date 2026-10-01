# Research First Builder 0.1.0-rc1

Make your coding agent justify architecture with real sources before it builds.

Don't build from vibes. Build from evidence.

This preview contains one portable research-first-build skill, classified evidence and Adopt/Reject/Defer decisions,
human research/plan/verification reports, and an offline Python 3.11+ init/render/check helper.

Included: three original educational builds from inspected primary sources, an independent research-only handoff,
meaningful negative tests, local installation checks, English/Russian docs and an edited walkthrough of actual artifacts.
A real desktop Bookmarks task also completed by explicit skill-file invocation. Its current implementation hashes
and postbuild were independently reviewed; all 55 HTTP assertions passed again in an isolated copy.
[Acceptance details](acceptance/DESKTOP_BOOKMARKS.md) distinguish recorded browser checks from independent repetition.

Validation of the published rc1 snapshot: the helper suite contained **38 tests: 37 passed and one Windows
symlink-creation case was skipped by host permissions**. The three example suites added **17 passing behavior
tests** (5 team-chat, 6 webhook-inbox, 6 local-cli), for **54 passed and one skipped in total**. This excludes
the separate 55-assertion desktop acceptance run. Format/lint and clean-archive checks passed. Current main
may contain additional regression tests. The helper needs no pip dependencies, backend, RFB account or MCP server.

**Pre-release limitations:** full native primary-host acceptance remains incomplete; Cursor/OpenCode have
format/install beta status. Comparative evaluation/pilot results are not available. Review current hosted Actions
results separately. No measured superiority or production security certification is claimed.

CONTRACT_CHECKED validates recorded consistency, not factual truth, legal clearance, execution provenance or permission.
Research uses the agent's own tools; their access and costs still apply. Third-party study is pattern-only by default.
