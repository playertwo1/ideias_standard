import unittest

from scripts.validate_standard import ROOT, validate


class ValidateStandardTest(unittest.TestCase):
    def codes(self, report):
        return {(c["code"], c["status"]) for c in report["checks"]}

    def test_positive_project_manifest_passes(self):
        report = validate(ROOT / "examples/standard-android-ai/project-manifest.json")
        self.assertEqual("PASS", report["result"])

    def test_valid_lock_passes(self):
        report = validate(ROOT / "fixtures/valid/basic.standard-lock.json", "standard-lock")
        self.assertEqual("PASS", report["result"])

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

    def test_unknown_pack_fails_semantically(self):
        report = validate(ROOT / "fixtures/invalid/unknown-pack.project.json", "project-manifest")
        self.assertIn(("IS-SEM-001", "FAIL"), self.codes(report))

    def test_full_repo_scan_fails_structurally(self):
        report = validate(ROOT / "fixtures/invalid/full-repo-scan.project.json", "project-manifest")
        self.assertIn(("IS-SCHEMA-001", "FAIL"), self.codes(report))

    def test_duplicate_pack_fails_structurally(self):
        report = validate(ROOT / "fixtures/invalid/duplicate-pack.project.json", "project-manifest")
        self.assertIn(("IS-SCHEMA-001", "FAIL"), self.codes(report))

    def test_duplicate_artifact_path_fails_semantically(self):
        report = validate(ROOT / "fixtures/invalid/duplicate-artifact.standard-lock.json", "standard-lock")
        self.assertIn(("IS-SEM-002", "FAIL"), self.codes(report))

    def test_inactive_adapter_fails_semantically(self):
        report = validate(ROOT / "fixtures/invalid/inactive-adapter.bundle.yaml", "bundle")
        self.assertIn(("IS-SEM-005", "FAIL"), self.codes(report))

    def test_unknown_workflow_fails_semantically(self):
        report = validate(ROOT / "fixtures/invalid/unknown-workflow.bundle.yaml", "bundle")
        self.assertIn(("IS-SEM-004", "FAIL"), self.codes(report))

    def test_duplicate_workflow_step_fails_semantically(self):
        report = validate(ROOT / "fixtures/invalid/duplicate-step.workflow.yaml", "workflow")
        self.assertIn(("IS-SEM-007", "FAIL"), self.codes(report))


if __name__ == "__main__":
    unittest.main()
