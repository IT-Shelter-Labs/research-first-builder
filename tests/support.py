"""Synthetic contract fixtures. These are not real research or execution records."""

import contextlib
import importlib.util
import io
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "research-first-build"
spec = importlib.util.spec_from_file_location("rfb", SKILL / "scripts" / "rfb.py")
rfb = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rfb)


def seed(root):
    data = json.loads((ROOT / "tests" / "fixtures" / "valid.json").read_text(encoding="utf-8"))
    (root / "sources").mkdir()
    (root / "checks").mkdir()
    (root / "sources" / "SRC-001.md").write_text(
        "SYNTHETIC: contract fixture only. EV-001 support text, not real web research.\n",
        encoding="utf-8",
    )
    (root / "checks" / "CHECK-001.txt").write_text(
        "SYNTHETIC SOURCE_AUDIT receipt. No actual source inspection occurred.\n", encoding="utf-8"
    )
    save(root, data)
    return data


def save(root, data):
    (root / "evidence.json").write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )


def cli(*args):
    out, err = io.StringIO(), io.StringIO()
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        status = rfb.main([str(a) for a in args])
    return status, out.getvalue() + err.getvalue()


def finish(root, data, snapshot="files:synthetic-v1"):
    for check in data["verification"]:
        if check["method"] == "SOURCE_AUDIT":
            continue
        check.update(
            result="PASS",
            evidence_path=f"checks/{check['id']}.txt",
            tested_snapshot=snapshot,
            checked_at="2026-09-30T16:00:00+00:00",
        )
        (root / check["evidence_path"]).write_text(
            "SYNTHETIC actual-result shape for a unit test, not a real test run.\n",
            encoding="utf-8",
        )
    save(root, data)
    return cli("render", root)
