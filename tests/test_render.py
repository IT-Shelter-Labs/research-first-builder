import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from support import cli, rfb, save, seed


class RenderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="rfb render ")
        self.root = Path(self.temp.name)
        self.data = seed(self.root)
        self.assertEqual(cli("render", self.root)[0], 0)

    def tearDown(self):
        self.temp.cleanup()

    def test_render_is_stable_preserves_prose_and_handles_crlf(self):
        report = self.root / "PLAN.md"
        report.write_text(
            "Personal design note.\n" + report.read_text(encoding="utf-8"),
            encoding="utf-8",
            newline="\r\n",
        )
        self.assertEqual(cli("render", self.root)[0], 0)
        first = report.read_bytes()
        self.assertEqual(cli("render", self.root)[0], 0)
        self.assertEqual(report.read_bytes(), first)
        self.assertIn("Personal design note.", first.decode("utf-8"))
        self.assertEqual(cli("check", self.root)[0], 0)

    def test_manual_table_edits_fail_and_render_repairs_only_block(self):
        report = self.root / "RESEARCH.md"
        report.write_text(
            report.read_text(encoding="utf-8").replace("DEC-001", "DEC-999"), encoding="utf-8"
        )
        self.assertIn("managed blocks are stale", cli("check", self.root)[1])
        self.assertEqual(cli("render", self.root)[0], 0)
        self.assertEqual(cli("check", self.root)[0], 0)

    def test_missing_and_reversed_markers_preserve_existing_files(self):
        report = self.root / "VERIFICATION.md"
        original = report.read_text(encoding="utf-8")
        for content in (
            original.replace("<!-- rfb:checks:start -->", ""),
            "<!-- rfb:checks:end -->\n<!-- rfb:checks:start -->",
        ):
            report.write_text(content, encoding="utf-8")
            before = {p.name: p.read_bytes() for p in self.root.glob("*.md")}
            self.assertEqual(cli("render", self.root)[0], 1)
            self.assertEqual(before, {p.name: p.read_bytes() for p in self.root.glob("*.md")})

    def test_unknown_state_version_does_not_overwrite_reports(self):
        (self.root / "run.json").write_text(
            json.dumps({"schema_version": 99, "run_id": self.data["run_id"]})
        )
        before = (self.root / "RESEARCH.md").read_bytes()
        status, output = cli("render", self.root)
        self.assertEqual(status, 1)
        self.assertIn("unknown schema", output)
        self.assertEqual(before, (self.root / "RESEARCH.md").read_bytes())

    def test_interrupted_atomic_replace_leaves_original_and_cleans_temp(self):
        report = self.root / "PLAN.md"
        original = report.read_bytes()
        with patch.object(rfb.os, "replace", side_effect=OSError("simulated interruption")):
            with self.assertRaises(rfb.ContractError):
                rfb.atomic_write(self.root, "PLAN.md", "replacement")
        self.assertEqual(report.read_bytes(), original)
        self.assertEqual(list(self.root.glob(".rfb-*")), [])

    def test_untrusted_markdown_cannot_inject_managed_markers(self):
        self.data["claims"][0]["statement"] = (
            "| <!-- rfb:evidence:end -->\n[click](javascript:alert(1))"
        )
        save(self.root, self.data)
        self.assertEqual(cli("render", self.root)[0], 0)
        text = (self.root / "RESEARCH.md").read_text(encoding="utf-8")
        self.assertEqual(text.count("<!-- rfb:evidence:end -->"), 1)
        self.assertIn("&lt;!--", text)
        self.assertEqual(cli("check", self.root)[0], 0)


if __name__ == "__main__":
    unittest.main()
