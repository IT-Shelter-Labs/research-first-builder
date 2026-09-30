# Evaluation: observed behavior and unfinished comparison

This candidate has **one independent research-only forward test**, three maintainer-authored full examples,
offline regression tests, and local installation checks. It does not have a completed paired benchmark,
external pilot or measured advantage over a strong research prompt.

## Observed results

| Actual exercise | Outcome | What it establishes |
| --- | --- | --- |
| Independent agent, local literal JSONL research-only task | Primary sources retrieved; research/decisions/plan and source audit; actual render/prebuild PASS; postbuild correctly rejected; no application written | One scoped instruction workflow and its UX findings |
| Team-chat, inbox, CLI examples | Actual original behavior tests and postbuild checks pass | Contract/build walkthroughs work locally; not autonomous comparative results |
| Native Codex discovery attempt | Skill loaded; tool policy blocked reads after HTTPS fallback | Native discovery, honest capability failure; not workflow completion |
| Native Claude attempt | Authentication HTTP 403 | Environment failure; no reasoning-quality evidence |
| Isolated copied-skill packaging | Helper works from path with spaces and different working directory | Self-contained installed folder; not all host model behavior |

[Independent artifacts and historical report](../examples/research-only/PROVENANCE.md) preserve what was
actually done. Three UX issues were corrected (links, wording, intent rejection), and an incomplete starter
command reduces directory/template setup. The independent agent did not retest the revised package;
current helper checks and regression tests verify those mechanical changes. Manual ledger authoring
remains a cost to measure.

## Reproducible comparison protocol

Use [cases.json](cases.json) and [rubric](RUBRIC.md). Select a declared host/model, settings, source/tool
access and budget before running. Use independent fresh sessions, randomize order, and preserve redacted
prompts, artifacts, tool transcripts, settings, actual elapsed time and available usage/cost data. Missing metrics
stay missing. Do not substitute the maintainer examples for experimental outcomes.

For each case compare:

1. **Plain build:** the task and scope only.
2. **Strong research prompt:** the task plus the baseline below.
3. **RFB:** the same task plus native research-first-build invocation.

Strong baseline:

```text
Before implementation, inspect relevant primary documentation and open-source
analogues. Explain source support and uncertainties, compare applicability and
scale, consider simpler alternatives, explicitly reject unsuitable complexity,
and make a minimal plan. Then implement and run meaningful acceptance checks.
Preserve user scope and report what was actually verified.
```

The proposed larger design is 8 cases × 3 arms × 3 independent repeats = 72 runs, contingent on an explicit
compute/time budget. A smaller pilot must report its size and uncertainty. No extra paid runs or invitations
were launched for this candidate.

Freeze a source packet for the judgement comparison, with primary locators and access/version manifest.
Use original synthetic fixtures for intentional contradictions/prompt injection and label them as such.
Do not redistribute unlicensed source documents. Keep a separate smaller live-retrieval sample to test
discovery/relevance; live-search variation should not be presented as a controlled reasoning comparison.

Reviewers should be unaware of the arm while assessing source support/decision fit where practical.
Record rubric dimensions separately, reviewer disagreements and source pointers; no arbitrary composite
score or unsupported statistical significance. Identify whether research changed/justified a consequential
decision a developer found useful, and measure artifact-authoring/review effort separately from token cost.

External pilot: 3–5 consenting developers when available. Record install friction, completion and decision
usefulness. Contacting participants needs explicit authorization. Testimonials must be real and approved.

## Run result record

For each actual run capture: case ID; arm; UTC start/end; host/model/settings/tool versions; randomization
order; frozen-source manifest; original prompt; installed skill version/hash; artifact paths; actual checks;
reviewer dimensions and evidence pointers; deviations; failures; missing metrics; raw/redacted output location.
Do not create placeholder PASS runs. An interrupted/blocked session remains an outcome, not silently dropped data.
