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

    def test_s1_c07_directory_compatibility_check(self):
        report = json.loads(run_check(path=ROOT / "examples" / "standard-android-ai", as_json=True)[1])
        self.assertEqual("PASS", {c["code"]: c["status"] for c in report["checks"]}["IS-SEM-030"])

    def test_s1_c08_applicable_packs_check(self):
        report = json.loads(run_check(path=ROOT / "examples" / "standard-android-ai", as_json=True)[1])
        self.assertEqual("PASS", {c["code"]: c["status"] for c in report["checks"]}["IS-SEM-031"])

    def test_s1_c09_applicable_workflow_check(self):
        report = json.loads(run_check(path=ROOT / "examples" / "standard-android-ai", as_json=True)[1])
        self.assertEqual("PASS", {c["code"]: c["status"] for c in report["checks"]}["IS-SEM-032"])

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

    # --- S1-C03: Standard Lock Validation Tests ---

    def test_standard_lock_valid_json(self):
        target = ROOT / "fixtures" / "valid" / "basic.standard-lock.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(0, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("PASS", report["result"])
        codes = {c["code"]: c["status"] for c in report["checks"]}
        self.assertEqual("PASS", codes.get("IS-SCHEMA-001"))
        self.assertEqual("PASS", codes.get("IS-SEM-001"))
        self.assertEqual("PASS", codes.get("IS-SEM-002"))
        self.assertEqual("PASS", codes.get("IS-SEM-004"))
        self.assertEqual("PASS", codes.get("IS-SEM-005"))
        self.assertEqual("PASS", codes.get("IS-SEM-006"))

    def test_standard_lock_valid_directory(self):
        target_dir = ROOT / "fixtures" / "valid" / "standard-lock-dir"
        exit_code, output = run_check(path=target_dir, as_json=True)
        self.assertEqual(0, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("PASS", report["result"])

    def test_standard_lock_valid_yaml_directory(self):
        target_dir = ROOT / "fixtures" / "valid" / "yaml-standard-lock"
        exit_code, output = run_check(path=target_dir, as_json=True)
        self.assertEqual(0, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("PASS", report["result"])

    def test_standard_lock_explicit_kind_override(self):
        target = ROOT / "fixtures" / "valid" / "basic.standard-lock.json"
        exit_code, output = run_check(path=target, kind="standard-lock", as_json=True)
        self.assertEqual(0, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("PASS", report["result"])

    def test_standard_lock_schema_failure_missing_required(self):
        target = ROOT / "fixtures" / "invalid" / "missing-required.standard-lock.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(1, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("FAIL", report["result"])
        fail_codes = [c["code"] for c in report["checks"] if c["status"] == "FAIL"]
        self.assertIn("IS-SCHEMA-001", fail_codes)

    def test_standard_lock_schema_failure_invalid_profile(self):
        target = ROOT / "fixtures" / "invalid" / "invalid-profile.standard-lock.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(1, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("FAIL", report["result"])
        fail_codes = [c["code"] for c in report["checks"] if c["status"] == "FAIL"]
        self.assertIn("IS-SCHEMA-001", fail_codes)

    def test_standard_lock_schema_failure_invalid_ownership(self):
        target = ROOT / "fixtures" / "invalid" / "invalid-ownership.standard-lock.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(1, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("FAIL", report["result"])
        fail_codes = [c["code"] for c in report["checks"] if c["status"] == "FAIL"]
        self.assertIn("IS-SCHEMA-001", fail_codes)

    def test_standard_lock_schema_failure_duplicate_pack(self):
        target = ROOT / "fixtures" / "invalid" / "duplicate-pack.standard-lock.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(1, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("FAIL", report["result"])
        fail_codes = [c["code"] for c in report["checks"] if c["status"] == "FAIL"]
        self.assertIn("IS-SCHEMA-001", fail_codes)

    def test_standard_lock_semantic_unknown_pack_is_sem_001(self):
        target = ROOT / "fixtures" / "invalid" / "unknown-pack.standard-lock.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(1, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("FAIL", report["result"])
        fail_codes = [c["code"] for c in report["checks"] if c["status"] == "FAIL"]
        self.assertIn("IS-SEM-001", fail_codes)

    def test_standard_lock_semantic_duplicate_artifact_is_sem_002(self):
        target = ROOT / "fixtures" / "invalid" / "duplicate-artifact.standard-lock.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(1, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("FAIL", report["result"])
        fail_codes = [c["code"] for c in report["checks"] if c["status"] == "FAIL"]
        self.assertIn("IS-SEM-002", fail_codes)

    def test_standard_lock_semantic_unknown_workflow_is_sem_004(self):
        target = ROOT / "fixtures" / "invalid" / "unknown-workflow.standard-lock.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(1, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("FAIL", report["result"])
        fail_codes = [c["code"] for c in report["checks"] if c["status"] == "FAIL"]
        self.assertIn("IS-SEM-004", fail_codes)

    def test_standard_lock_semantic_inactive_adapter_is_sem_005(self):
        target = ROOT / "fixtures" / "invalid" / "inactive-adapter.standard-lock.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(1, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("FAIL", report["result"])
        fail_codes = [c["code"] for c in report["checks"] if c["status"] == "FAIL"]
        self.assertIn("IS-SEM-005", fail_codes)

    def test_standard_lock_semantic_unsupported_version_is_sem_006(self):
        target = ROOT / "fixtures" / "invalid" / "invalid-version.standard-lock.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(1, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("FAIL", report["result"])
        fail_codes = [c["code"] for c in report["checks"] if c["status"] == "FAIL"]
        self.assertIn("IS-SEM-006", fail_codes)

    def test_standard_lock_managed_local_override_warn_is_warn_001(self):
        target = ROOT / "fixtures" / "valid" / "warn.standard-lock.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(0, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("WARN", report["result"])
        warn_codes = [c["code"] for c in report["checks"] if c["status"] == "WARN"]
        self.assertIn("IS-WARN-001", warn_codes)

    # -------------------------------------------------------------------------
    # S1-C04: Context manifest validations
    # -------------------------------------------------------------------------

    def test_context_manifest_valid_file_passes_all_checks(self):
        target = ROOT / "fixtures" / "valid" / "basic.context-manifest.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(0, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("PASS", report["result"])
        pass_codes = [c["code"] for c in report["checks"] if c["status"] == "PASS"]
        self.assertIn("IS-SCHEMA-001", pass_codes)
        self.assertIn("IS-SEM-021", pass_codes)
        self.assertIn("IS-SEM-022", pass_codes)
        self.assertIn("IS-SEM-023", pass_codes)

    def test_context_manifest_valid_directory_autodetection(self):
        target = ROOT / "fixtures" / "valid" / "context-manifest-dir"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(0, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("PASS", report["result"])
        pass_codes = [c["code"] for c in report["checks"] if c["status"] == "PASS"]
        self.assertIn("IS-SCHEMA-001", pass_codes)

    def test_context_manifest_valid_directory_with_explicit_kind(self):
        target = ROOT / "fixtures" / "valid" / "context-manifest-dir"
        exit_code, output = run_check(path=target, kind="context-manifest", as_json=True)
        self.assertEqual(0, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("PASS", report["result"])

    def test_context_manifest_valid_yaml(self):
        target = ROOT / "fixtures" / "valid" / "yaml-context-manifest" / "context-manifest.yaml"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(0, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("PASS", report["result"])

    def test_context_manifest_semantic_traversal_path_is_sem_021(self):
        target = ROOT / "fixtures" / "invalid" / "traversal-path.context-manifest.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(1, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("FAIL", report["result"])
        fail_codes = [c["code"] for c in report["checks"] if c["status"] == "FAIL"]
        self.assertIn("IS-SEM-021", fail_codes)

    def test_context_manifest_semantic_overlapping_categories_is_sem_022(self):
        target = ROOT / "fixtures" / "invalid" / "overlapping-categories.context-manifest.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(1, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("FAIL", report["result"])
        fail_codes = [c["code"] for c in report["checks"] if c["status"] == "FAIL"]
        self.assertIn("IS-SEM-022", fail_codes)

    def test_context_manifest_semantic_inverted_budgets_is_sem_023(self):
        target = ROOT / "fixtures" / "invalid" / "inverted-budgets.context-manifest.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(1, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("FAIL", report["result"])
        fail_codes = [c["code"] for c in report["checks"] if c["status"] == "FAIL"]
        self.assertIn("IS-SEM-023", fail_codes)

    def test_context_manifest_schema_missing_required_is_schema_001(self):
        target = ROOT / "fixtures" / "invalid" / "missing-required.context-manifest.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(1, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("FAIL", report["result"])
        fail_codes = [c["code"] for c in report["checks"] if c["status"] == "FAIL"]
        self.assertIn("IS-SCHEMA-001", fail_codes)

    def test_context_manifest_directory_not_found_fails_with_exit_code_2(self):
        target = ROOT / "fixtures" / "valid" / "standard-lock-dir"
        exit_code, output = run_check(path=target, kind="context-manifest", as_json=True)
        self.assertEqual(2, exit_code)
        report = json.loads(output)
        self.assertEqual("FAIL", report["result"])
        fail_codes = [c["code"] for c in report["checks"] if c["status"] == "FAIL"]
        self.assertIn("IS-CLI-001", fail_codes)

    # --- S1-C05: Artifact Policy & Ownership Validation Tests ---

    def test_artifact_policy_valid_json(self):
        target = ROOT / "fixtures" / "valid" / "basic.artifact-policy.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(0, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("PASS", report["result"])
        pass_codes = [c["code"] for c in report["checks"] if c["status"] == "PASS"]
        self.assertIn("IS-SCHEMA-001", pass_codes)
        self.assertIn("IS-SEM-024", pass_codes)
        self.assertIn("IS-SEM-025", pass_codes)
        self.assertIn("IS-SEM-026", pass_codes)
        self.assertIn("IS-SEM-027", pass_codes)

    def test_artifact_policy_valid_yaml(self):
        target = ROOT / "fixtures" / "valid" / "user-owned.artifact-policy.yaml"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(0, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("PASS", report["result"])
        pass_codes = [c["code"] for c in report["checks"] if c["status"] == "PASS"]
        self.assertIn("IS-SCHEMA-001", pass_codes)
        self.assertIn("IS-SEM-024", pass_codes)
        self.assertIn("IS-SEM-027", pass_codes)

    def test_artifact_policy_valid_directory_autodetection(self):
        target = ROOT / "fixtures" / "valid" / "artifact-policy-dir"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(0, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("PASS", report["result"])

    def test_artifact_policy_valid_directory_with_explicit_kind(self):
        target = ROOT / "fixtures" / "valid" / "artifact-policy-dir"
        exit_code, output = run_check(path=target, kind="artifact-policy", as_json=True)
        self.assertEqual(0, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("PASS", report["result"])

    def test_artifact_policy_warn_managed_override(self):
        target = ROOT / "fixtures" / "valid" / "managed-override.artifact-policy.json"
        exit_code, output = run_check(path=target, as_json=True, strict=False)
        self.assertEqual(0, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("WARN", report["result"])
        warn_codes = [c["code"] for c in report["checks"] if c["status"] == "WARN"]
        self.assertIn("IS-WARN-001", warn_codes)

        exit_code_strict, out_strict = run_check(path=target, as_json=True, strict=True)
        self.assertEqual(1, exit_code_strict)
        rep_strict = json.loads(out_strict)
        self.assertEqual("WARN", rep_strict["result"])

    def test_artifact_policy_semantic_traversal_path_is_sem_024(self):
        target = ROOT / "fixtures" / "invalid" / "traversal-path.artifact-policy.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(1, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("FAIL", report["result"])
        fail_codes = [c["code"] for c in report["checks"] if c["status"] == "FAIL"]
        self.assertIn("IS-SEM-024", fail_codes)

    def test_artifact_policy_semantic_unknown_pack_is_sem_025(self):
        target = ROOT / "fixtures" / "invalid" / "unknown-pack.artifact-policy.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(1, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("FAIL", report["result"])
        fail_codes = [c["code"] for c in report["checks"] if c["status"] == "FAIL"]
        self.assertIn("IS-SEM-025", fail_codes)

    def test_artifact_policy_semantic_invalid_profile_is_sem_026(self):
        target = ROOT / "fixtures" / "invalid" / "invalid-profile.artifact-policy.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(1, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("FAIL", report["result"])
        fail_codes = [c["code"] for c in report["checks"] if c["status"] == "FAIL"]
        self.assertIn("IS-SEM-026", fail_codes)

    def test_artifact_policy_semantic_user_owned_override_is_sem_027(self):
        target = ROOT / "fixtures" / "invalid" / "user-owned-override.artifact-policy.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(1, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("FAIL", report["result"])
        fail_codes = [c["code"] for c in report["checks"] if c["status"] == "FAIL"]
        self.assertIn("IS-SEM-027", fail_codes)

    def test_artifact_policy_schema_missing_required_is_schema_001(self):
        target = ROOT / "fixtures" / "invalid" / "missing-required.artifact-policy.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(1, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("FAIL", report["result"])
        fail_codes = [c["code"] for c in report["checks"] if c["status"] == "FAIL"]
        self.assertIn("IS-SCHEMA-001", fail_codes)

    def test_standard_lock_semantic_pack_not_in_lock_is_sem_025(self):
        target = ROOT / "fixtures" / "invalid" / "pack-not-in-lock.standard-lock.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(1, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("FAIL", report["result"])
        fail_codes = [c["code"] for c in report["checks"] if c["status"] == "FAIL"]
        self.assertIn("IS-SEM-025", fail_codes)

    def test_standard_lock_semantic_user_owned_override_is_sem_027(self):
        target = ROOT / "fixtures" / "invalid" / "user-owned-override.standard-lock.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(1, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("FAIL", report["result"])
        fail_codes = [c["code"] for c in report["checks"] if c["status"] == "FAIL"]
        self.assertIn("IS-SEM-027", fail_codes)

    def test_standard_lock_semantic_traversal_artifact_is_sem_024(self):
        target = ROOT / "fixtures" / "invalid" / "traversal-artifact.standard-lock.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(1, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("FAIL", report["result"])
        fail_codes = [c["code"] for c in report["checks"] if c["status"] == "FAIL"]
        self.assertIn("IS-SEM-024", fail_codes)

    def test_standard_lock_semantic_invalid_profile_artifact_is_sem_026(self):
        target = ROOT / "fixtures" / "invalid" / "invalid-profile-artifact.standard-lock.json"
        exit_code, output = run_check(path=target, as_json=True)
        self.assertEqual(1, exit_code)
        report = json.loads(output)
        self.assert_conformance_schema(report)
        self.assertEqual("FAIL", report["result"])
        fail_codes = [c["code"] for c in report["checks"] if c["status"] == "FAIL"]
        self.assertIn("IS-SEM-026", fail_codes)

    def test_artifact_policy_directory_not_found_fails_with_exit_code_2(self):
        target = ROOT / "fixtures" / "valid" / "standard-lock-dir"
        exit_code, output = run_check(path=target, kind="artifact-policy", as_json=True)
        self.assertEqual(2, exit_code)
        report = json.loads(output)
        self.assertEqual("FAIL", report["result"])
        fail_codes = [c["code"] for c in report["checks"] if c["status"] == "FAIL"]
        self.assertIn("IS-CLI-001", fail_codes)


if __name__ == "__main__":
    unittest.main()


