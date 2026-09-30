import copy
import json
import tempfile
import unittest
from pathlib import Path

from support import cli, finish, rfb, save, seed


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="rfb test spaces ")
        self.root = Path(self.temp.name)
        self.data = seed(self.root)
        self.assertEqual(cli("render", self.root)[0], 0)

    def tearDown(self):
        self.temp.cleanup()

    def errors(self, data=None):
        return "\n".join(rfb.contract(data or self.data, self.root))

    def test_research_prebuild_then_actual_postbuild(self):
        self.assertEqual(cli("check", self.root, "--stage", "prebuild")[0], 0)
        self.assertEqual(finish(self.root, self.data)[0], 0)
        status, output = cli(
            "check", self.root, "--stage", "postbuild", "--snapshot", "files:synthetic-v1"
        )
        self.assertEqual(status, 0, output)
        state = json.loads((self.root / "run.json").read_text())
        self.assertEqual(state["stage"], "COMPLETE")
        self.assertIn("check_outputs", state["postbuild_receipt"])

    def test_missing_duplicate_and_broken_ids(self):
        cases = [
            ("duplicate", lambda d: d["requirements"].append(copy.deepcopy(d["requirements"][0]))),
            ("unknown REQ", lambda d: d["decisions"][0]["requirement_ids"].append("REQ-999")),
            ("unknown EV", lambda d: d["decisions"][0]["evidence_ids"].append("EV-999")),
            (
                "unknown CHECK",
                lambda d: d["plan_units"][0]["acceptance_checks"].append("CHECK-999"),
            ),
            ("no linked plan", lambda d: d["plan_units"].clear()),
        ]
        for expected, mutate in cases:
            with self.subTest(expected=expected):
                data = copy.deepcopy(self.data)
                mutate(data)
                errors = self.errors(data)
                if expected == "no linked plan":
                    self.assertTrue(errors)
                else:
                    self.assertIn(expected, errors)

    def test_schema_boolean_version_and_unknown_fields(self):
        for field, value, expected in [
            ("schema_version", True, "expected integer"),
            ("schema_version", 2, "unsupported value"),
            ("intent", "fake", "expected one of"),
            ("invented_field", 1, "unknown field"),
        ]:
            with self.subTest(field=field):
                data = copy.deepcopy(self.data)
                data[field] = value
                self.assertIn(expected, self.errors(data))

    def test_escaped_surrogate_is_rejected_before_render_mutation(self):
        self.data["claims"][0]["statement"] = "invalid \ud800 text"
        (self.root / "evidence.json").write_text(json.dumps(self.data), encoding="utf-8")
        before = (self.root / "RESEARCH.md").read_bytes()
        status, output = cli("render", self.root)
        self.assertEqual(status, 1)
        self.assertIn("invalid Unicode surrogate", output)
        self.assertNotIn("Traceback", output)
        self.assertEqual((self.root / "RESEARCH.md").read_bytes(), before)

    def test_duplicate_json_keys_and_nonfinite_values_fail_without_traceback(self):
        for content in ('{"schema_version":1,"schema_version":2}', '{"a":NaN}'):
            (self.root / "evidence.json").write_text(content)
            status, output = cli("check", self.root, "--json")
            self.assertEqual(status, 1)
            self.assertEqual(json.loads(output)["status"], "FAIL")
            self.assertNotIn("Traceback", output)

    def test_verified_requires_inspected_matching_source(self):
        for kind, status in [
            ("IMPLEMENTATION", "INSPECTED"),
            ("DOCUMENTATION", "UNPINNED"),
            ("DOCUMENTATION", "UNAVAILABLE"),
        ]:
            data = copy.deepcopy(self.data)
            data["sources"][0].update(kind=kind, inspection_status=status)
            self.assertIn("not inspected DOCUMENTATION", self.errors(data))

    def test_implementation_needs_exact_revision_and_path(self):
        data = copy.deepcopy(self.data)
        data["claims"][0]["class"] = "OPEN_SOURCE_IMPLEMENTATION"
        data["sources"][0]["kind"] = "IMPLEMENTATION"
        self.assertIn("immutable commit", self.errors(data))
        data["sources"][0]["locator"].update(revision="a" * 40, path="src/app.py")
        self.assertEqual(self.errors(data), "")

    def test_circular_inference_and_transitive_promotion(self):
        data = copy.deepcopy(self.data)
        data["claims"][0].update(class_="unused")  # Unknown fields are rejected.
        self.assertIn("unknown field", self.errors(data))
        del data["claims"][0]["class_"]
        data["claims"][0].update({"class": "INFERENCE", "premise_claim_ids": ["EV-001"]})
        self.assertIn("circular", self.errors(data))
        data["claims"][0]["class"] = "VERIFIED_SOURCE"
        self.assertIn("belong to INFERENCE", self.errors(data))

    def test_user_requirement_cannot_mask_assumption(self):
        data = copy.deepcopy(self.data)
        data["claims"][0].update(
            {"class": "USER_REQUIREMENT", "source_ids": [], "requirement_ids": ["REQ-001"]}
        )
        self.assertEqual(self.errors(data), "")
        data["requirements"][0]["origin"] = "ASSUMPTION"
        self.assertIn("assumption", self.errors(data))

    def test_license_unknown_blocks_reuse_not_pattern_learning(self):
        lic = self.data["references"][0]["license_record"]
        lic.update(status="MISSING", locator="", spdx="")
        self.assertEqual(self.errors(), "")
        lic["reuse_mode"] = "SOURCE_REUSE"
        self.assertIn("source reuse requires", self.errors())
        lic.update(reuse_mode="PATTERN_ONLY", code_copied=True)
        self.assertIn("conflicts with copied", self.errors())

    def test_smaller_reference_set_and_no_rejection_need_explanation(self):
        data = copy.deepcopy(self.data)
        data["references"] = data["references"][:1]
        self.assertIn("reference_exception", self.errors(data))
        data["coverage"]["reference_exception"] = "Only one relevant source available."
        data["decisions"] = data["decisions"][:1]
        data["verification"] = data["verification"][:2]
        self.assertIn("rejection_note", self.errors(data))
        data["coverage"]["rejection_note"] = "Direct code; no substantive rejected candidate."
        self.assertEqual(self.errors(data), "")

    def test_rejected_and_deferred_decisions_cannot_enter_build_plan(self):
        for outcome in ("REJECT", "DEFER"):
            data = copy.deepcopy(self.data)
            data["decisions"][0]["outcome"] = outcome
            self.assertIn("cannot be planned", self.errors(data))

    def test_plan_checks_cover_step_requirements_and_decisions(self):
        data = copy.deepcopy(self.data)
        data["verification"][1]["decision_ids"] = []
        self.assertIn("must cover", self.errors(data))
        self.assertIn("no required check", self.errors(data))

    def test_source_audit_alone_is_not_implementation_verification(self):
        data = copy.deepcopy(self.data)
        data["verification"][1]["method"] = "SOURCE_AUDIT"
        self.assertIn("no required acceptance check", self.errors(data))
        self.assertIn("no required check", self.errors(data))

    def test_actual_result_requires_output_snapshot_timestamp(self):
        data = copy.deepcopy(self.data)
        data["verification"][1]["result"] = "PASS"
        errors = self.errors(data)
        self.assertIn("file below checks/", errors)
        self.assertIn("snapshot and timestamp", errors)

    def test_not_run_cannot_claim_an_execution_receipt(self):
        self.data["verification"][1]["tested_snapshot"] = "old"
        self.assertIn("NOT_RUN cannot", self.errors())

    def test_critical_unknown_blocks_prebuild(self):
        self.data["questions"][0]["status"] = "OPEN"
        save(self.root, self.data)
        cli("render", self.root)
        status, output = cli("check", self.root, "--stage", "prebuild")
        self.assertEqual(status, 1)
        self.assertIn("Critical research question", output)

    def test_a_failed_required_audit_blocks_even_when_another_passes(self):
        audit = copy.deepcopy(self.data["verification"][0])
        audit.update(id="CHECK-004", result="FAIL")
        self.data["verification"].append(audit)
        save(self.root, self.data)
        cli("render", self.root)
        status, output = cli("check", self.root, "--stage", "prebuild")
        self.assertEqual(status, 1)
        self.assertIn("source audit", output)

    def test_postbuild_blocks_required_failure_not_run_and_no_snapshot(self):
        self.assertEqual(cli("check", self.root, "--stage", "prebuild")[0], 0)
        status, output = cli("check", self.root, "--stage", "postbuild")
        self.assertEqual(status, 1)
        self.assertIn("Current snapshot missing", output)
        self.assertIn("NOT_RUN", output)
        finish(self.root, self.data)
        self.data["verification"][1]["result"] = "FAIL"
        save(self.root, self.data)
        cli("render", self.root)
        status, output = cli(
            "check", self.root, "--stage", "postbuild", "--snapshot", "files:synthetic-v1"
        )
        self.assertEqual(status, 1)
        self.assertIn("not PASS", output)

    def test_changed_snapshot_cannot_inherit_pass(self):
        cli("check", self.root, "--stage", "prebuild")
        finish(self.root, self.data)
        status, output = cli(
            "check", self.root, "--stage", "postbuild", "--snapshot", "files:synthetic-v2"
        )
        self.assertEqual(status, 1)
        self.assertIn("differs from current", output)

    def test_changed_plan_and_sources_invalidate_readiness(self):
        cli("check", self.root, "--stage", "prebuild")
        self.data["decisions"][0]["rationale"] = "Changed after review."
        save(self.root, self.data)
        cli("render", self.root)
        state = json.loads((self.root / "run.json").read_text())
        self.assertIsNone(state["prebuild_receipt"])
        self.assertEqual(state["stage"], "PLANNED")
        cli("check", self.root, "--stage", "prebuild")
        (self.root / "sources" / "SRC-001.md").write_text("Changed source note.")
        finish(self.root, self.data)
        status, output = cli(
            "check", self.root, "--stage", "postbuild", "--snapshot", "files:synthetic-v1"
        )
        self.assertEqual(status, 1)
        self.assertIn("receipt missing or stale", output)

    def test_research_only_cannot_claim_completed_build(self):
        self.data["intent"] = "research-only"
        save(self.root, self.data)
        cli("render", self.root)
        cli("check", self.root, "--stage", "prebuild")
        finish(self.root, self.data)
        status, output = cli(
            "check", self.root, "--stage", "postbuild", "--snapshot", "files:synthetic-v1"
        )
        self.assertEqual(status, 1)
        self.assertIn("handoff", output)

    def test_diff_review_is_required_for_rejections(self):
        self.data["verification"][2]["required"] = False
        save(self.root, self.data)
        cli("render", self.root)
        cli("check", self.root, "--stage", "prebuild")
        finish(self.root, self.data)
        status, output = cli(
            "check", self.root, "--stage", "postbuild", "--snapshot", "files:synthetic-v1"
        )
        self.assertEqual(status, 1)
        self.assertIn("needs required diff review", output)

    def test_source_paths_cannot_escape_or_use_windows_absolute_paths(self):
        for value in (
            "../secret.txt",
            "sources/../../secret.txt",
            "C:/secret.txt",
            "sources/../checks/CHECK-001.txt",
            r"sources\secret.txt",
            "/sources/a.txt",
            "sources//a.txt",
        ):
            with self.subTest(value=value):
                data = copy.deepcopy(self.data)
                data["sources"][0]["note_path"] = value
                self.assertTrue(self.errors(data))

    def test_symlinks_cannot_read_even_inside_run(self):
        target = self.root / "sources" / "SRC-001.md"
        link = self.root / "sources" / "linked.md"
        try:
            link.symlink_to(target)
        except OSError:
            self.skipTest("Host does not permit symlink creation")
        self.data["sources"][0]["note_path"] = "sources/linked.md"
        self.assertIn("Symlink", self.errors())

    def test_missing_blank_large_and_invalid_utf8_evidence(self):
        note = self.root / "sources" / "SRC-001.md"
        for content, expected in [
            (b"", "blank"),
            (b"x" * (rfb.MAX_BYTES + 1), "exceeds"),
            (b"\xff", "Cannot read"),
        ]:
            note.write_bytes(content)
            self.assertIn(expected, self.errors())
        note.unlink()
        self.assertIn("Missing file", self.errors())

    def test_helper_never_executes_ledger_commands(self):
        self.data["verification"][1]["command"] = "create-a-file helper-must-not-run-this"
        save(self.root, self.data)
        cli("render", self.root)
        self.assertEqual(cli("check", self.root, "--stage", "prebuild")[0], 0)
        self.assertFalse((self.root / "helper-must-not-run-this").exists())

    def test_json_output_has_real_failure_code(self):
        status, output = cli("check", self.root, "--stage", "postbuild", "--json")
        self.assertEqual(status, 1)
        result = json.loads(output)
        self.assertEqual(result["status"], "FAIL")
        self.assertTrue(result["errors"])


if __name__ == "__main__":
    unittest.main()
