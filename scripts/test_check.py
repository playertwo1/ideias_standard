import json
import os
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
        lock_path = ROOT / "fixtures" / "valid" / "warn.standard-lock.json"

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
        empty_dir = ROOT / "schemas"
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

    def test_offline_flag_forwarded_and_processed(self):
        target = ROOT / "examples" / "standard-android-ai" / "project-manifest.json"
        exit_code, output = run_check(path=target, as_json=True, offline=True)
        self.assertEqual(0, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        codes = [c["code"] for c in report["checks"]]
        self.assertIn("IS-CLI-002", codes)
        offline_check = next(c for c in report["checks"] if c["code"] == "IS-CLI-002")
        self.assertEqual("PASS", offline_check["status"])
        self.assertEqual("INFO", offline_check["severity"])

    def test_dry_run_flag_forwarded_and_processed(self):
        target = ROOT / "examples" / "standard-android-ai" / "project-manifest.json"
        exit_code, output = run_check(path=target, as_json=True, dry_run=True)
        self.assertEqual(0, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        codes = [c["code"] for c in report["checks"]]
        self.assertIn("IS-CLI-003", codes)
        dry_run_check = next(c for c in report["checks"] if c["code"] == "IS-CLI-003")
        self.assertEqual("PASS", dry_run_check["status"])
        self.assertEqual("INFO", dry_run_check["severity"])

    def test_self_check_with_offline_and_dry_run(self):
        exit_code, output = run_check(is_self_check=True, as_json=True, offline=True, dry_run=True)
        self.assertEqual(0, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        codes = [c["code"] for c in report["checks"]]
        self.assertIn("IS-CLI-002", codes)
        self.assertIn("IS-CLI-003", codes)

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

    def test_main_cli_with_offline_and_dry_run(self):
        import io
        from contextlib import redirect_stdout

        buf = io.StringIO()
        with redirect_stdout(buf):
            exit_code = main(["--self-check", "--json", "--offline", "--dry-run"])
        self.assertEqual(0, exit_code)
        report = json.loads(buf.getvalue())
        self.assert_conformance_schema(report)
        codes = [c["code"] for c in report["checks"]]
        self.assertIn("IS-CLI-002", codes)
        self.assertIn("IS-CLI-003", codes)

    def test_text_report_with_offline_and_dry_run(self):
        target = ROOT / "examples" / "standard-android-ai" / "project-manifest.json"
        exit_code, output = run_check(path=target, as_json=False, offline=True, dry_run=True, no_color=True)
        self.assertEqual(0, exit_code)
        self.assertIn("IS-CLI-002", output)
        self.assertIn("IS-CLI-003", output)

    # --- S1-C02: Project Manifest Validation Tests ---

    def test_project_manifest_valid_combinations(self):
        # 1. Sensitive data valid combination
        p1 = ROOT / "fixtures" / "valid" / "sensitive-data-valid.project.json"
        ec1, out1 = run_check(path=p1, as_json=True)
        self.assertEqual(0, ec1)
        rep1 = json.loads(out1)
        self.assert_conformance_schema(rep1)
        self.assertEqual("PASS", rep1["result"])
        codes1 = {c["code"]: c["status"] for c in rep1["checks"]}
        self.assertEqual("PASS", codes1.get("IS-SCHEMA-001"))
        self.assertEqual("PASS", codes1.get("IS-SEM-001"))
        self.assertEqual("PASS", codes1.get("IS-SEM-006"))
        self.assertEqual("PASS", codes1.get("IS-SEM-009"))

        # 2. Multi-agent valid combination
        p2 = ROOT / "fixtures" / "valid" / "multi-agent-valid.project.json"
        ec2, out2 = run_check(path=p2, as_json=True)
        self.assertEqual(0, ec2)
        rep2 = json.loads(out2)
        self.assert_conformance_schema(rep2)
        self.assertEqual("PASS", rep2["result"])
        codes2 = {c["code"]: c["status"] for c in rep2["checks"]}
        self.assertEqual("PASS", codes2.get("IS-SCHEMA-001"))
        self.assertEqual("PASS", codes2.get("IS-SEM-001"))
        self.assertEqual("PASS", codes2.get("IS-SEM-006"))
        self.assertEqual("PASS", codes2.get("IS-SEM-010"))
        self.assertEqual("PASS", codes2.get("IS-SEM-011"))

    def test_project_manifest_directory_yaml(self):
        target = ROOT / "fixtures" / "valid" / "yaml-project"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(0, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("PASS", report["result"])

    def test_project_manifest_schema_failure_full_repo_scan(self):
        target = ROOT / "fixtures" / "invalid" / "full-repo-scan.project.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(1, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("FAIL", report["result"])
        fail_codes = [c["code"] for c in report["checks"] if c["status"] == "FAIL"]
        self.assertIn("IS-SCHEMA-001", fail_codes)

    def test_project_manifest_schema_failure_duplicate_pack(self):
        target = ROOT / "fixtures" / "invalid" / "duplicate-pack.project.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(1, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("FAIL", report["result"])
        fail_codes = [c["code"] for c in report["checks"] if c["status"] == "FAIL"]
        self.assertIn("IS-SCHEMA-001", fail_codes)

    def test_project_manifest_schema_failure_missing_required(self):
        target = ROOT / "fixtures" / "invalid" / "missing-required.project.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(1, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("FAIL", report["result"])
        fail_codes = [c["code"] for c in report["checks"] if c["status"] == "FAIL"]
        self.assertIn("IS-SCHEMA-001", fail_codes)

    def test_project_manifest_semantic_unknown_pack_is_sem_001(self):
        target = ROOT / "fixtures" / "invalid" / "unknown-pack.project.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(1, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("FAIL", report["result"])
        fail_codes = [c["code"] for c in report["checks"] if c["status"] == "FAIL"]
        self.assertIn("IS-SEM-001", fail_codes)

    def test_project_manifest_semantic_unsupported_version_is_sem_006(self):
        target = ROOT / "fixtures" / "invalid" / "invalid-version.project.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(1, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("FAIL", report["result"])
        fail_codes = [c["code"] for c in report["checks"] if c["status"] == "FAIL"]
        self.assertIn("IS-SEM-006", fail_codes)

    def test_project_manifest_semantic_sensitive_data_requires_human_gates_is_sem_009(self):
        target = ROOT / "fixtures" / "invalid" / "sensitive-data-no-human-gates.project.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(1, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("FAIL", report["result"])
        fail_codes = [c["code"] for c in report["checks"] if c["status"] == "FAIL"]
        self.assertIn("IS-SEM-009", fail_codes)

    def test_project_manifest_semantic_multi_agent_requires_independent_audit_is_sem_010(self):
        target = ROOT / "fixtures" / "invalid" / "multi-agent-no-audit.project.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(1, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("FAIL", report["result"])
        fail_codes = [c["code"] for c in report["checks"] if c["status"] == "FAIL"]
        self.assertIn("IS-SEM-010", fail_codes)

    def test_project_manifest_semantic_multi_agent_role_separation_is_sem_011(self):
        target = ROOT / "fixtures" / "invalid" / "multi-agent-same-builder-auditor.project.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(1, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("FAIL", report["result"])
        fail_codes = [c["code"] for c in report["checks"] if c["status"] == "FAIL"]
        self.assertIn("IS-SEM-011", fail_codes)


if __name__ == "__main__":
    unittest.main()
