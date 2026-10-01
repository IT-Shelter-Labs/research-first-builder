import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from support import SKILL, seed


class PackagingTests(unittest.TestCase):
    def test_only_skill_directory_is_needed_from_another_cwd(self):
        with tempfile.TemporaryDirectory(prefix="rfb install with spaces ") as temp:
            root = Path(temp)
            installed = root / ".agents" / "skills" / "research-first-build"
            shutil.copytree(SKILL, installed, ignore=shutil.ignore_patterns("__pycache__"))
            run = root / "run"
            run.mkdir()
            seed(run)
            for action in ("render", "check"):
                result = subprocess.run(
                    [sys.executable, str(installed / "scripts" / "rfb.py"), action, str(run)],
                    cwd=root,
                    capture_output=True,
                    text=True,
                    encoding="utf-8",
                )
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertTrue((run / "PLAN.md").is_file())

    def test_bundled_schema_uses_only_supported_vocabulary(self):
        schema = json.loads((SKILL / "assets" / "evidence.schema.json").read_text())
        vocabulary = {
            "$schema",
            "$defs",
            "$ref",
            "title",
            "description",
            "type",
            "properties",
            "required",
            "additionalProperties",
            "items",
            "minItems",
            "maxItems",
            "uniqueItems",
            "minLength",
            "maxLength",
            "pattern",
            "format",
            "enum",
            "const",
        }

        def walk(node):
            self.assertFalse(set(node) - vocabulary, set(node) - vocabulary)
            for value in node.get("properties", {}).values():
                walk(value)
            for value in node.get("$defs", {}).values():
                walk(value)
            if "items" in node:
                walk(node["items"])

        walk(schema)

    def test_template_cannot_be_claimed_as_finished_research(self):
        from support import rfb

        with tempfile.TemporaryDirectory() as temp:
            data = json.loads((SKILL / "assets" / "evidence.template.json").read_text())
            self.assertTrue(rfb.contract(data, Path(temp)))

    def test_starter_is_incomplete_and_preserves_existing_work(self):
        from support import cli, rfb

        with tempfile.TemporaryDirectory() as temp:
            run = Path(temp) / "new-task"
            self.assertEqual(cli("init", run, "--intent", "research-only")[0], 0)
            data = rfb.load_json(run / "evidence.json")
            self.assertEqual(data["intent"], "research-only")
            self.assertEqual(data["run_id"], "new-task")
            self.assertEqual(cli("check", run, "--stage", "prebuild")[0], 1)
            (run / "RESEARCH.md").write_text("User's existing research", encoding="utf-8")
            self.assertEqual(cli("init", run)[0], 1)
            self.assertEqual((run / "RESEARCH.md").read_text(), "User's existing research")

    def test_fresh_starter_is_actionable_without_mutating_artifacts(self):
        from support import cli, rfb

        with tempfile.TemporaryDirectory() as temp:
            run = Path(temp) / "new-task"
            self.assertEqual(cli("init", run)[0], 0)
            before = {p.name: p.read_bytes() for p in run.iterdir() if p.is_file()}
            for args in (("render", run), ("check", run, "--stage", "prebuild", "--json")):
                status, output = cli(*args)
                self.assertEqual(status, 1)
                self.assertIn("fill evidence.json first", output)
                self.assertNotIn("must not be blank", output)
            result = json.loads(output)
            self.assertEqual(result["status"], "FAIL")
            self.assertEqual(len(result["errors"]), 1)
            process = subprocess.run(
                [sys.executable, str(SKILL / "scripts" / "rfb.py"), "render", str(run)],
                capture_output=True,
                text=True,
                encoding="utf-8",
            )
            self.assertEqual(process.returncode, 1)
            self.assertIn("fill evidence.json first", process.stderr)
            self.assertEqual(before, {p.name: p.read_bytes() for p in run.iterdir() if p.is_file()})
            data = rfb.load_json(run / "evidence.json")
            data["scope"]["goal"] = "Partially filled research"
            (run / "evidence.json").write_text(json.dumps(data))
            status, output = cli("render", run)
            self.assertEqual(status, 1)
            self.assertNotIn("still a template", output)
            self.assertIn("must not be blank", output)

    def test_non_object_ledger_fails_without_traceback(self):
        from support import cli

        with tempfile.TemporaryDirectory() as temp:
            run = Path(temp)
            (run / "evidence.json").write_text("[]")
            for command in ("render", "check"):
                status, output = cli(command, run)
                self.assertEqual(status, 1)
                self.assertIn("JSON object", output)
                self.assertNotIn("Traceback", output)


if __name__ == "__main__":
    unittest.main()
