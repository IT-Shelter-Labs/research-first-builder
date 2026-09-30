# Desktop full-workflow acceptance: Bookmarks

Reviewed 2026-10-01 on Windows, Python 3.11.0, in the Codex desktop local coding environment.
This is one real full task invoked by explicitly reading the skill, not native skill-selector acceptance
or a comparative benchmark. Model/settings and a desktop build number were not captured.

## Task and invocation

Build a single-user local web bookmark manager: URL/title/optional tags, search, edit/delete, durable storage,
responsive UI, no accounts/cloud/Docker/frontend build. Inspect primary references before implementation;
save research, decisions, plan and actual checks. The user ran the task in another coding chat.

The complete installed folder matched the product's 13 distribution files byte for byte. The skill was absent
from that session's catalog, so the agent read SKILL.md and its references explicitly. The chat's working
directory was the parent workspace; the installation was inside a child test project. Codex scans repository
`.agents/skills` directories from its working directory upward, so naming a child folder in a prompt does not
establish native discovery there. [Official discovery guide](https://learn.chatgpt.com/docs/build-skills).
Native selector acceptance remains pending; no separate CLI is needed to finish it.

## What research contributed

| Inspected primary implementation | Scoped observation | Resulting choice |
| --- | --- | --- |
| [linkding Tag parser](https://github.com/sissbruecker/linkding/blob/27b7303baf41bb28babc610ac8eaa486e1ddfab5/bookmarks/models.py#L30-L46) | Removes blanks and deduplicates tags ignoring case; also replaces internal spaces and sorts | Adopt blank removal/deduplication; keep internal spaces and first spelling in this app |
| [Buku schema](https://github.com/jarun/buku/blob/49204f4026d0fc122f87799a7b0e2e1e58991dbb/buku.py#L562-L580) and [insert](https://github.com/jarun/buku/blob/49204f4026d0fc122f87799a7b0e2e1e58991dbb/buku.py#L878-L885) | SQLite unique URL, bound parameters, default committed insert (delayed commit is an explicit exception) | Adopt one SQLite table and committed row mutations; verify actual restart persistence |
| [Shaarli save](https://github.com/shaarli/Shaarli/blob/030fe09b87cb6fbfe5097f21d3f041db92afed75/application/bookmark/BookmarkFileService.php#L309-L318) | Reorders collection, delegates writing and invalidates caches; underlying write atomicity was not inspected | Reject that collection-file lifecycle for this Python task; no claim that Shaarli is unsafe |

Official Python sqlite3 and http.server documentation also informed the plan. A standard-library loopback
server and linear Unicode substring search were explicitly classified as engineering inferences for a small
personal collection. Automatic metadata/archiving was rejected; advanced query grammar and relational tags
were deferred. The app has no outbound metadata requests, framework/ORM or frontend build.

The original run recorded pinned license inspection: linkding MIT, Shaarli Zlib with asset exceptions,
Buku GPL-3.0, Python documentation PSF. Pattern-only study; no third-party code was copied into the app.
The review re-read the consequential parser/schema/insert/save locators; it is not a legal clearance finding.

## Actual checks and independent repetition

The original task produced RESEARCH.md, PLAN.md, VERIFICATION.md, evidence.json, source notes,
source-audit/prebuild/postbuild outputs and implementation review receipts. Saved prebuild precedes the
first application write in the task record. The original run's final stage is COMPLETE.

Tested implementation fingerprint:

```text
sha256:ce580d3e4f9b59d91423ca02eab0e32c86e66b3374c0788025bb5a630ab23b0b
```

Scope: app.py, three web assets, tests/verify_app.py, README.md and .gitignore. Runtime databases/logs,
research/report files, installed skills and screenshots are excluded from this implementation fingerprint.

The maintainer independently recomputed every included file hash, matched the recorded manifest and
fingerprint, and ran the current helper's postbuild function without modifying original receipts: PASS.
The seven implementation files were copied into a new isolated folder, then the actual HTTP test ran with
its own subprocess and database: **55 assertions passed**. See the [UTF-8 repetition receipt](DESKTOP_BOOKMARKS_HTTP.txt).
These are assertions within one acceptance script, not 55 independent tests or product-suite additions.
The original working collection and running server were untouched.

Coverage includes CRUD, title/URL/tag search, Unicode case folding, literal search characters, duplicate/invalid
input, HTTP guards, inaccessible private paths, records surviving termination and a different process PID,
deletion surviving another restart, SQLite lock failure (503 without insertion), and integrity_check.

The task's browser tool record demonstrates Chromium CRUD, error-preserved inputs, empty states,
delete cancellation/confirmation, literal HTML-like title text and 1280x900 / 360x800 viewport checks.
The maintainer reviewed saved desktop/mobile captures; it did not repeat browser interaction independently.
A distorted screenshot capture was discarded and replaced in the original run. No horizontal overflow
was recorded after reload; the final browser warning/error log was empty.

## Limits and next check

The complete application, source downloads and original host artifacts remain in the local test project;
they are not a redistributable example or publicly reproducible benchmark in this package. This sanitized
report and repetition receipt omit private absolute paths, databases, downloaded third-party files and chat IDs.

Not run: native skill-selector invocation, other native hosts, physical phone, Firefox/Safari, load tests,
power-loss recovery, disk-full/permission failure or a complete accessibility audit. There is no measured
advantage over a strong research prompt and no public production-server claim.

For the remaining discovery check, open the **actual target project folder** containing `.agents/skills`
as the coding workspace. In a fresh session select research-first-build and ask only for its discovered
name/location. Do not rebuild the app solely to test discovery. If discovery succeeds, record that separately;
the full workflow above retains its explicit-file invocation provenance.
