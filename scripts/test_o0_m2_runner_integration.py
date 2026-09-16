"""Unit tests for O0 v2 M2 runner integration and evidence artifact."""
import hashlib
import json
import subprocess
import sys
import unittest
from pathlib import Path

from scripts.orchestrate_handoffs import validate_with_schema


class O0V2M2Test(unittest.TestCase):
    def setUp(self):
        self.root = Path(__file__).resolve().parents[1]
        self.evidence_path = self.root / "O0_V2_M2_EVIDENCE.json"

    def test_m2_evidence_artifact_and_package(self):
        self.assertTrue(self.evidence_path.is_file(), f"Missing evidence at {self.evidence_path}")
        evidence = json.loads(self.evidence_path.read_text(encoding="utf-8"))

        self.assertEqual("0.1", evidence.get("schema_version"))
        self.assertEqual("O0-v2-M2-runner-adapters", evidence.get("scenario"))

        criteria = evidence["acceptance_criteria"]
        self.assertTrue(criteria["adapters_connected_to_runner"])
        self.assertTrue(criteria["explicit_workspace_and_task"])
        self.assertTrue(criteria["canonical_builder_report_accepted"])
        self.assertTrue(criteria["canonical_audit_report_accepted"])
        self.assertTrue(criteria["schema_validation_enforced"])
        self.assertTrue(criteria["sha_verification_enforced"])
        self.assertTrue(criteria["evidence_canonicalized_and_referenced"])
        self.assertTrue(criteria["audit_checkout_immutable"])
        self.assertTrue(criteria["no_human_intervention_in_cycle"])
        self.assertTrue(criteria["no_gate_approval_registered"])
        self.assertTrue(criteria["stops_at_waiting_product_authority"])

        runner_exec = evidence["runner_execution"]
        builder = runner_exec["builder"]
        auditor = runner_exec["auditor"]
        final_state = runner_exec["final_state"]

        self.assertEqual("antigravity-cli", builder["executor_id"])
        self.assertNotEqual(builder["base_sha"], builder["produced_sha"])

        self.assertEqual("codex-cli", auditor["executor_id"])
        self.assertEqual(builder["produced_sha"], auditor["audited_sha"])
        self.assertEqual("PASS", auditor["audit_result"])
        self.assertEqual([], auditor["findings"])

        self.assertEqual("WAITING_PRODUCT_AUTHORITY", final_state["machine_state"])
        self.assertEqual("PRODUCT_AUTHORITY", final_state["next_actor"])
        self.assertIsNone(final_state["approval"])
        self.assertTrue(final_state["human_gate_required"])

        # Package artifacts verification
        package_root = self.root / evidence["package_root"]
        self.assertTrue(package_root.is_dir(), f"Package dir missing at {package_root}")

        artifacts = evidence["artifacts"]
        for key, entry in artifacts.items():
            if key in {"evidence", "operations"}:
                for item_name, item_meta in entry.items():
                    item_path = package_root / item_meta["path"]
                    self.assertTrue(item_path.is_file(), f"Missing {item_name} at {item_path}")
                    self.assertEqual(item_meta["sha256"], hashlib.sha256(item_path.read_bytes()).hexdigest())
            else:
                art_path = package_root / entry["path"]
                self.assertTrue(art_path.is_file(), f"Missing artifact {key} at {art_path}")
                self.assertEqual(entry["sha256"], hashlib.sha256(art_path.read_bytes()).hexdigest())

        # Validate canonical report schemas
        builder_report = json.loads((package_root / artifacts["builder_report"]["path"]).read_text(encoding="utf-8"))
        validate_with_schema(builder_report, "builder")

        audit_report = json.loads((package_root / artifacts["audit_report"]["path"]).read_text(encoding="utf-8"))
        validate_with_schema(audit_report, "audit")

        state_doc = json.loads((package_root / artifacts["final_state"]["path"]).read_text(encoding="utf-8"))
        validate_with_schema(state_doc, "state")

    def test_adapter_binary_discovery(self):
        from scripts.o0_antigravity_adapter import _find_agy_binary
        from scripts.o0_codex_adapter import _find_codex_binary

        agy_bin = _find_agy_binary()
        self.assertTrue(agy_bin.is_file(), f"Antigravity binary not found: {agy_bin}")

        codex_bin = _find_codex_binary()
        self.assertTrue(codex_bin.is_file(), f"Codex binary not found: {codex_bin}")

        with self.assertRaises(FileNotFoundError):
            _find_agy_binary("nonexistent/agy/binary/path")

        with self.assertRaises(FileNotFoundError):
            _find_codex_binary("nonexistent/codex/binary/path")

    def test_canonical_conversion_for_audit_fail(self):
        sample_fail_report = {
            "schema_version": "0.1",
            "executor_id": "codex-cli",
            "role": "AUDITOR",
            "authority": "INDEPENDENT_AUDIT",
            "audit_result": "FAIL",
            "audited_sha": "0" * 40,
            "summary": "Audit failed due to bug in subtract function",
            "findings": [
                {
                    "id": "CODEX-FINDING-001",
                    "severity": "HIGH",
                    "blocking": True,
                    "files": ["."],
                    "evidence": {
                        "evidence_id": "r1-audit-finding-test",
                        "sha256": "0" * 64,
                    },
                    "problem": "Function returns addition instead of subtraction",
                    "violated_criterion": "Implementation correctness",
                    "resolution_condition": "Fix return value in calc.py",
                }
            ],
            "checks": [
                {
                    "id": "codex-check-1",
                    "status": "FAIL",
                    "evidence": {
                        "evidence_id": "r1-audit-check-test",
                        "sha256": "0" * 64,
                    },
                }
            ],
            "residual_risks": [],
            "gate_registration": "NOT_AUTHORIZED",
        }
        # Validate schema passes
        validate_with_schema(sample_fail_report, "audit")


if __name__ == "__main__":
    unittest.main()
