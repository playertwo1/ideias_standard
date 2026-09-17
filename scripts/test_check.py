import json
import os
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from scripts.check import (
    determine_exit_code,
    format_text_report,
    main,
    run_check,
)
from scripts.validate_standard import ROOT, load_json, schema_registry


class CheckCommandTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        schemas, registry = schema_registry()
        cls.conformance_schema = schemas["conformance-report"]
        cls.schema_validator = Draft202012Validator(cls.conformance_schema, registry=registry)

    def assert_conformance_schema(self, report: dict):
        errors = list(self.schema_validator.iter_errors(report))
        self.assertEqual([], errors, f"Schema validation errors: {[e.message for e in errors]}")

    def test_self_check_json_conformance(self):
        exit_code, output = run_check(is_self_check=True, as_json=True)
        self.assertEqual(0, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("PASS", report["result"])
        self.assertEqual("SELF", report["target"])

    def test_positive_fixture_check(self):
        target = ROOT / "examples" / "standard-android-ai" / "project-manifest.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(0, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("PASS", report["result"])

    def test_directory_with_manifest_check(self):
        target_dir = ROOT / "examples" / "standard-android-ai"
        exit_code, output = run_check(path=target_dir, as_json=True)
        self.assertEqual(0, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("PASS", report["result"])

    def test_invalid_fixture_fails(self):
        target = ROOT / "fixtures" / "invalid" / "unknown-pack.project.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(1, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("FAIL", report["result"])
        codes = [c["code"] for c in report["checks"] if c["status"] == "FAIL"]
        self.assertIn("IS-SEM-001", codes)

    def test_strict_mode_elevates_warn(self):
        # Create temporary standard-lock containing a local_override on MANAGED artifact -> produces WARN IS-WARN-001
        base_lock = load_json(ROOT / "fixtures" / "valid" / "basic.standard-lock.json")
        warn_data = dict(base_lock)
        warn_data["artifacts"] = [
            {
                "path": "STANDARD.md",
                "ownership": "MANAGED",
                "source": "templates/STANDARD.md",
                "source_revision": "0.1",
                "fingerprint": "sha256:standard",
                "profile": "STANDARD",
                "pack": None,
                "local_override": True,
                "rationale": "Managed file override for testing.",
            }
        ]
        with tempfile.TemporaryDirectory() as tmpdir:
            lock_path = Path(tmpdir) / "standard.lock.json"
            lock_path.write_text(json.dumps(warn_data), encoding="utf-8")

            # Normal check: exit code 0
            exit_code_normal, out_normal = run_check(path=lock_path, as_json=True, strict=False)
            self.assertEqual(0, exit_code_normal)
            report_normal = json.loads(out_normal)
            self.assert_conformance_schema(report_normal)
            self.assertEqual("WARN", report_normal["result"])

            # Strict check: exit code 1, but canonical result remains WARN
            exit_code_strict, out_strict = run_check(path=lock_path, as_json=True, strict=True)
            self.assertEqual(1, exit_code_strict)
            report_strict = json.loads(out_strict)
            self.assert_conformance_schema(report_strict)
            self.assertEqual("WARN", report_strict["result"])

    def test_operational_error_on_missing_path(self):
        nonexistent = ROOT / "fixtures" / "nonexistent_file_xyz.json"
        exit_code, output = run_check(path=nonexistent, as_json=True)
        self.assertEqual(2, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("FAIL", report["result"])
        codes = [c["code"] for c in report["checks"]]
        self.assertIn("IS-CLI-001", codes)

    def test_operational_error_on_empty_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            empty_dir = Path(tmpdir)
            exit_code, output = run_check(path=empty_dir, as_json=True)
            self.assertEqual(2, exit_code)
            report = json.loads(output)
            self.assert_conformance_schema(report)
            self.assertEqual("FAIL", report["result"])
            self.assertEqual("IS-CLI-001", report["checks"][0]["code"])

    def test_text_report_no_color(self):
        target = ROOT / "examples" / "standard-android-ai" / "project-manifest.json"
        exit_code, output = run_check(path=target, as_json=False, no_color=True)
        self.assertEqual(0, exit_code)
        self.assertNotIn("\033[", output)
        self.assertIn("PASS:", output)
        self.assertIn("IS-SCHEMA-001", output)

    def test_main_cli_function(self):
        import io
        from contextlib import redirect_stdout

        buf = io.StringIO()
        with redirect_stdout(buf):
            exit_code = main(["--self-check", "--json"])
        self.assertEqual(0, exit_code)
        report = json.loads(buf.getvalue())
        self.assertEqual("PASS", report["result"])

        buf_err = io.StringIO()
        with redirect_stdout(buf_err):
            exit_code_err = main(["nonexistent_path_test_123.json", "--json"])
        self.assertEqual(2, exit_code_err)
        report_err = json.loads(buf_err.getvalue())
        self.assertEqual("FAIL", report_err["result"])


if __name__ == "__main__":
    unittest.main()
