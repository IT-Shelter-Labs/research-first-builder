# Decisions that fit this project

Read after inspection and before design. The objective is the smallest coherent solution, not maximum pattern reuse.

## Cross-project comparison

Compare only consequential areas raised by the research questions. Write a short matrix in RESEARCH.md: reference mechanisms → applicability → decision. Use EV IDs rather than repeating unverifiable architecture summaries.

For each decision answer:

1. What problem does the mechanism solve in the reference? Which source supports that?
2. Does the user have that problem?
3. Are scale, deployment, team and failure/threat assumptions comparable?
4. What operations, dependencies, abstractions and failure modes does it add?
5. What simpler/direct alternative works now?
6. When should it be revisited, and what migration path preserves that option?

Outcomes: **ADOPT** now, **REJECT** for a concrete mismatch, **DEFER** until a named trigger. Direct implementation / NO-PATTERN is valid. An explicit user choice can constrain the outcome; evidence informs tradeoffs without silently replacing that choice.

The rejection section is mandatory. It may say no substantive candidates were rejected if that is true, using `coverage.rejection_note`. Do not introduce Kafka, Kubernetes or an abstraction solely to reject it.

## Design and plan

Assemble adopted choices into one minimal architecture. State components/interfaces/data flow only at useful depth; mark non-applicable template sections rather than inventing databases or APIs.

PLAN.md includes goals/non-goals, design, relevant data/API/security/deployment decisions, incremental outcomes and acceptance checks. Each STEP links requirements and ADOPT decisions. REJECT/DEFER decisions must not be planned for implementation.

Tests should check behavior, not mirror code. A manual inspection can verify absence of unnecessary infrastructure. Include failure-path checks when the adopted mechanism protects data, auth or external side effects.

Build authorization and evidence readiness are separate. Preserve the user's approval requirements; do not ask again for already-authorized development merely because a stage changed.

If building reveals a missing decision, explain the new evidence, update affected requirements/decisions/plan, audit it and refresh prebuild readiness before continuing the affected work.
