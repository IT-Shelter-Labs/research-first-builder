# Contributing

Keep the product focused: help an agent justify and verify a small design through inspectable evidence.
Prefer a demonstrated workflow failure and a narrow fix over adding another universal instruction.

Python 3.11+ is sufficient for development checks; no pip dependencies:

```text
python -m unittest discover -s tests -v
python tools/verify_examples.py
python tools/check_repository.py
```

Tests/fixtures are deliberately synthetic and must remain labelled. Examples contain actual source inspection
and execution records. Never promote mock receipts to real evidence. Do not modify recorded PASS results
without executing the corresponding checks. Host acceptance requires a model/tool run, not just valid frontmatter.

Keep one self-contained skill folder. Update schema, checker, templates and docs together when the contract changes.
Unknown schema versions should fail with artifacts intact. The helper must not fetch sources, run ledger commands,
grant permission or imply factual truth. Document any new prerequisite before introducing it.

Skill frontmatter follows the [Agent Skills specification](https://agentskills.io/specification), including its
standard `compatibility` field for environment requirements. For format validation, use the current official
[skills-ref reference validator](https://github.com/agentskills/agentskills/tree/main/skills-ref); older validators
may reject supported optional fields. Its development dependencies are separate from the standalone skill runtime.

A useful issue includes task, host/version, relevant redacted artifacts, expected/actual behavior and reproducible
steps. A useful PR explains the concrete trigger, resulting behavior and actual validation. Use meaningful regression
tests for behavior/contract changes, not assertions on prose formatting. Ordinary documentation edits need link review.

For formatting/linting, install the pinned development tool in your own virtual environment:

```text
python -m pip install -r requirements-dev.txt
python -m ruff check .
python -m ruff format --check .
```

Use `python -m ruff format .` to format changes. Runtime helpers and behavior tests require no Ruff.
Configuration follows the [official Ruff guide](https://docs.astral.sh/ruff/configuration/);
the pinned [0.16.9 release](https://github.com/astral-sh/ruff/releases/tag/0.16.9) was actually exercised locally.

Good starting contributions: native host acceptance reports, a concise real-source counterexample, or a reduced
failure fixture for drift/trace behavior. Comparative/pilot work needs a declared budget and consenting participants.
Do not send invitations or publish private artifacts automatically.

Animation regeneration is optional: `python tools/make_demo.py` needs Pillow, which is a development-media
dependency only. Runtime/product checks remain standard-library-only.
