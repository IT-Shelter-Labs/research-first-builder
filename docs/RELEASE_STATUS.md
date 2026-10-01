# Release readiness

Recorded 2026-10-01. The public [v0.1.0-rc1 preview](https://github.com/IT-Shelter-Labs/research-first-builder/releases/tag/v0.1.0-rc1)
includes the complete repository archive, a standalone skill archive and SHA256SUMS.
[Hosted CI passed on e21efae](https://github.com/IT-Shelter-Labs/research-first-builder/actions/runs/36849930287).
Anonymous GitHub installation and isolated helper init passed. Private vulnerability reporting is enabled.

| Capability | Observed state |
| --- | --- |
| Product workflow | Research → Evidence → Evaluate → Reject/Adopt → Design → Plan → Build → Verify, in one portable skill |
| Installation | Local four-target copy and anonymous GitHub install passed; complete standalone skill package |
| Research-only | Independent primary-source run and handoff; no application implemented in that run |
| Offline helper | Contract/render/packaging regression suite; no runtime dependencies beyond Python 3.11+ |
| Evidence | Five source classes, scoped locators, license records and explicit audit boundaries |
| Build and drift | Three educational builds and a desktop Bookmarks task; stale plan/source/snapshot and failed/not-run checks covered by regression tests |
| Desktop acceptance | Full workflow passed by explicit skill-file invocation; 55 HTTP assertions independently repeated. Native selector discovery pending in the correct project context |
| Other hosts | CLI discovery/install results and incomplete native workflow attempts documented in [compatibility status](COMPATIBILITY.md) |
| Examples and demo | Three original genuine-source builds, an independent handoff and a reproducible edited artifact animation |
| Comparison and pilot | Method/cases/rubric prepared; paired runs and external pilot not executed |
| Public package | English/Russian docs, examples/demo, MIT, release archives and hosted CI |

## Stable-release and evaluation work remaining

- Complete native discovery in the actual desktop target project and native acceptance in other primary hosts. [Desktop full-workflow report](acceptance/DESKTOP_BOOKMARKS.md) preserves what already passed.
- Declare evaluation budget and run a comparison/pilot before making measured benefit claims.

The preview is ready for an honest public announcement and feedback. The incomplete gates do not turn
verification into stable native-host certification. Published v0.1.0-rc1 assets remain a fixed release snapshot;
later changes on main do not replace its archives. See [Unreleased changes](../CHANGELOG.md) for subsequent fixes
and the Actions badge for current main checks. Native acceptance reports cover the initial candidate's tested scope.
