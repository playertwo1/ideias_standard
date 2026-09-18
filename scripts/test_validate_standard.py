import json
import unittest

import yaml

from scripts.validate_standard import ROOT, self_check, validate


class ValidateStandardTest(unittest.TestCase):
    def codes(self, report):
        return {(c["code"], c["status"]) for c in report["checks"]}

    def test_fixture_manifest_expectations(self):
        manifest = yaml.safe_load((ROOT / "fixtures/fixture-manifest.yaml").read_text(encoding="utf-8"))
        for case in manifest["cases"]:
            with self.subTest(case=case["id"]):
                report = validate(ROOT / case["path"], case.get("kind"))
                self.assertEqual(case["expected_result"], report["result"])
                observed_codes = {c["code"] for c in report["checks"] if c["status"] in {"FAIL", "WARN"}}
                for code in case.get("expected_codes", []):
                    self.assertIn(code, observed_codes)

    def test_valid_context_manifest_passes(self):
        report = validate(ROOT / "fixtures/valid/basic.context-manifest.json")
        self.assertEqual("PASS", report["result"])

    def test_valid_change_passes(self):
        report = validate(ROOT / "fixtures/valid/basic.change.json")
        self.assertEqual("PASS", report["result"])

    def test_valid_bundle_passes(self):
        report = validate(ROOT / "bundles/standard-android-ai/bundle.yaml", "bundle")
        self.assertEqual("PASS", report["result"])

    def test_valid_workflow_passes(self):
        report = validate(ROOT / "workflows/default/workflow.yaml", "workflow")
        self.assertEqual("PASS", report["result"])

    def test_self_check_passes(self):
        report = self_check()
        self.assertEqual("PASS", report["result"], report)
        self.assertIn(("IS-SELF-009", "PASS"), self.codes(report))

    def test_inactive_bundle_adapter_is_rejected(self):
        report = validate(ROOT / "fixtures/invalid/inactive-adapter.bundle.yaml", "bundle")
        self.assertEqual("FAIL", report["result"])
        self.assertIn("IS-SEM-005", {c["code"] for c in report["checks"] if c["status"] == "FAIL"})

    def assert_golden(self, fixture, expected_path, kind="project-manifest"):
        report = validate(ROOT / fixture, kind)
        expected = json.loads((ROOT / expected_path).read_text(encoding="utf-8"))
        normalized = {
            "result": report["result"],
            "checks": sorted(
                [
                    {"code": c["code"], "status": c["status"], "severity": c["severity"]}
                    for c in report["checks"]
                    if c["status"] in {"FAIL", "WARN"}
                ],
                key=lambda item: (item["code"], item["status"], item["severity"]),
            ),
        }
        expected["checks"] = sorted(expected["checks"], key=lambda item: (item["code"], item["status"], item["severity"]))
        self.assertEqual(expected, normalized)

    def test_sensitive_data_golden(self):
        self.assert_golden(
            "fixtures/invalid/sensitive-data-no-human-gates.project.json",
            "fixtures/golden/sensitive-data-no-human-gates.expected.json",
        )

    def test_multi_agent_role_separation_golden(self):
        self.assert_golden(
            "fixtures/invalid/multi-agent-same-builder-auditor.project.json",
            "fixtures/golden/multi-agent-same-builder-auditor.expected.json",
        )


if __name__ == "__main__":
    unittest.main()
