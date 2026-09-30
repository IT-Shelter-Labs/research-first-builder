"""Run real example tests and check current artifacts; --record updates test receipts.

This development tool runs a fixed test command, never commands from evidence.json.
It cannot perform a source or diff review. Those notes must already be supplied.
"""

import argparse
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HELPER = ROOT / "skills" / "research-first-build" / "scripts" / "rfb.py"
SPEC = importlib.util.spec_from_file_location("rfb", HELPER)
rfb = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(rfb)
EXAMPLES = ("team-chat", "webhook-inbox", "local-cli")


def snapshot(directory):
    """Bounded manifest: app.py and test_app.py, normalized LF on all platforms."""
    digest = hashlib.sha256()
    for name in ("app.py", "test_app.py"):
        body = (directory / name).read_bytes().replace(b"\r\n", b"\n")
        digest.update(name.encode() + b"\0" + body + b"\0")
    return "files:sha256:" + digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", action="store_true")
    args = parser.parse_args()
    failures = []
    for slug in EXAMPLES:
        directory = ROOT / "examples" / slug
        current = snapshot(directory)
        env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONDONTWRITEBYTECODE="1")
        result = subprocess.run(
            [sys.executable, "-m", "unittest", "discover", "-s", ".", "-p", "test_app.py", "-v"],
            cwd=directory,
            capture_output=True,
            text=True,
            encoding="utf-8",
            env=env,
        )
        print(f"{slug}: tests {'PASS' if result.returncode == 0 else 'FAIL'}")
        if result.returncode:
            failures.append(slug + ": " + result.stdout + result.stderr)
            continue
        data = rfb.load_json(directory / "evidence.json")
        if args.record:
            for check in data["verification"]:
                if check["method"] == "DIFF_REVIEW":
                    note = directory / f"checks/{check['id']}.txt"
                    if not note.exists() or current not in note.read_text(encoding="utf-8"):
                        failures.append(slug + ": supply actual diff review of " + current)
                        break
            else:
                now = datetime.now(timezone.utc).isoformat(timespec="seconds")
                for check in data["verification"]:
                    if check["method"] == "SOURCE_AUDIT":
                        continue
                    if check["method"] == "COMMAND":
                        (directory / f"checks/{check['id']}.txt").write_text(
                            f"Actual run: Python {sys.version.split()[0]}, {sys.platform}\n"
                            f"Command: python -m unittest discover -s . -p test_app.py -v\n"
                            f"Snapshot: {current}\nExit: {result.returncode}\n\n"
                            + result.stdout
                            + result.stderr,
                            encoding="utf-8",
                        )
                    check.update(
                        result="PASS",
                        evidence_path=f"checks/{check['id']}.txt",
                        tested_snapshot=current,
                        checked_at=now,
                    )
                rfb.atomic_write(directory, "evidence.json", json.dumps(data, indent=2) + "\n")
                if rfb.main(["render", str(directory)]):
                    failures.append(slug + ": render failed")
                    continue
                # Never renew prebuild here: a changed plan needs separate review.
                if rfb.main(
                    ["check", str(directory), "--stage", "postbuild", "--snapshot", current]
                ):
                    failures.append(slug + ": postbuild failed")
                continue
            continue
        errors = rfb.check_run(directory, data, "postbuild", current)
        if errors:
            failures.extend(slug + ": " + error for error in errors)
        else:
            print(f"{slug}: current artifact contract PASS")
    for failure in failures:
        print(failure, file=sys.stderr)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
