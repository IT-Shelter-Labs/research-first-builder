# First useful run

## Install the complete folder

Use the root README's local-copy route. The installed folder must contain SKILL.md, LICENSE, agents,
references, assets and scripts; copying just SKILL.md breaks progressive resources and offline checks.
Keep your existing skills/configuration. Install once in a fresh target project or inspect any existing same-name
installation before updating it. No global hooks, MCP configuration or permission overrides are needed.

Install from GitHub, from the target project:

```text
npx skills@1.7.0 add IT-Shelter-Labs/research-first-builder --skill research-first-build --agent codex --copy
```

This route was checked in a clean project without Git credentials on 2026-10-01. All 13 distribution files
matched the source skill and the isolated helper init passed. For a local checkout instead:

```text
npx skills@1.7.0 add "<local-checkout>" --skill research-first-build --agent codex --copy
```

This route was exercised with Node 24.19.0. Node 22.20+ satisfies the tested installer's engine requirement.
The installer is external tooling; manual copy avoids it entirely. Upgrade by replacing only this skill folder
after reviewing local modifications. Remove that folder to uninstall; your generated research remains.

Official discovery references, inspected 2026-10-01:
[Codex/desktop local skills](https://learn.chatgpt.com/docs/build-skills),
[Claude Code](https://code.claude.com/docs/en/skills),
[Cursor](https://cursor.com/docs/skills), [OpenCode](https://opencode.ai/docs/skills/).
These describe the directory format; they do not certify this package's runtime quality.

For desktop Codex, open the actual target folder containing `.agents/skills` as the coding workspace.
Discovery scans from the working directory upward; a child project named only in a prompt is insufficient.
A real [desktop full task](acceptance/DESKTOP_BOOKMARKS.md) completed through explicit skill-file invocation
when that project-context mismatch left the skill absent from the catalog.

## Start with research-only

Open your target coding project in the agent. Ask:

```text
Use research-first-build in research-only mode. I need a local JSON Lines
filter for a literal top-level string field. Python 3.11 is available.
Inspect a few relevant references, explain the minimum design and give me
the plan without implementation. Save docs/research-first/jsonl-filter.
```

The agent should capture scope, inspect primary sources, write evidence/decisions and concise human reports,
audit consequential claims, render tables and check prebuild. Read the rejected/adopted comparison first;
you should not have to review raw JSON to understand the recommendation.

You can see an actual independent run at [research-only](../examples/research-only/PROVENANCE.md).
Treat its findings as scoped evidence, not reusable facts about your own task.

## Continue to build

After reviewing the handoff, ask the same agent to continue the existing run and build its plan.
It should recheck drift, execute actual acceptance checks and record their current implementation snapshot.
When it was already authorized to build a full task, it continues without unnecessary approval rounds.
Publishing/deployment still needs whatever authorization your project requires.

## Common failures

| Message/situation | Action |
| --- | --- |
| Skill not listed | Check the project's discovery directory and complete folder; restart if needed. Read the installed SKILL.md explicitly to distinguish discovery from workflow failure. |
| `codex` not recognized | You do not need that command to use a skill in the desktop application. Open the local coding project there. |
| Python missing | Let the agent perform a labelled manual review; deterministic helper checks require Python 3.11+. |
| No usable primary-source access | Preserve partial findings and explain missing evidence; do not replace inspection with remembered claims. |
| `init` refuses a directory | Existing files are preserved. Resume the run or choose a new task slug. |
| Managed blocks stale | Edit canonical evidence.json; render, inspect reports, then recheck. Preserve prose outside markers. |
| Prebuild receipt stale | Review changed research/plan/audit inputs; only then run a new prebuild check. |
| Postbuild says required check NOT_RUN | Execute it or report an incomplete/blocked build. Do not change the label to get a green result. |
| Research-only postbuild rejected | Prebuild is the handoff endpoint. Do not build application code just to satisfy postbuild. |

Keep research notes concise. Quick mode reduces reference count, not evidence honesty. For a trivial edit, skip the skill.
