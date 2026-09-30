"""Offline repository QA: local Markdown links, JSON, skill license and handoff gate."""

import importlib.util
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "research-first-build"
SPEC = importlib.util.spec_from_file_location("rfb", SKILL / "scripts" / "rfb.py")
rfb = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(rfb)


def main():
    errors = []
    count = 0
    for path in sorted(ROOT.rglob("*")):
        if any(part in (".git", "dist", "__pycache__", ".venv") for part in path.parts):
            continue
        if not path.is_file():
            continue
        if path.suffix == ".json":
            try:
                json.loads(path.read_text(encoding="utf-8"))
            except (ValueError, UnicodeError) as exc:
                errors.append(f"{path.relative_to(ROOT)}: invalid JSON ({exc})")
        if path.suffix != ".md":
            continue
        body = path.read_text(encoding="utf-8")
        # Inline destinations are simple explicit paths in this repository.
        for target in re.findall(r"\]\(([^\n)]+)\)", body):
            target = target.strip().strip("<>")
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith("#"):
                continue
            count += 1
            destination = path.parent / unquote(parsed.path)
            if not destination.exists():
                errors.append(f"{path.relative_to(ROOT)}: missing link {target}")
        if re.search(r"[A-Z]:[\\/]Users[\\/]", body, re.I):
            errors.append(f"{path.relative_to(ROOT)}: private absolute user path")
    if (ROOT / "LICENSE").read_bytes() != (SKILL / "LICENSE").read_bytes():
        errors.append("Root and independently installed skill licenses differ")
    handoff = ROOT / "examples" / "research-only"
    data = rfb.load_json(handoff / "evidence.json")
    errors.extend(rfb.check_run(handoff, data, "prebuild"))
    negative = rfb.check_run(handoff, data, "postbuild")
    if not negative or not any("Research-only" in error for error in negative):
        errors.append("Research-only unexpectedly passes postbuild")
    required = (
        ROOT / "README.md",
        ROOT / "README_RU.md",
        ROOT / "media" / "demo.gif",
        SKILL / "agents" / "openai.yaml",
        ROOT / ".github" / "workflows" / "check.yml",
    )
    errors.extend(
        f"Missing distribution file: {path.relative_to(ROOT)}"
        for path in required
        if not path.is_file()
    )
    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1
    print(f"Repository QA passed: {count} local links, JSON, licenses and research-only gate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
