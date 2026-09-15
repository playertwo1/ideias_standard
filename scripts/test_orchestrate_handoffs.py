import json
import tempfile
import unittest
from pathlib import Path

from scripts.orchestrate_handoffs import (
    HandoffError,
    approve_gate,
    audit_handoff,
    builder_handoff,
    init_state,
    next_actor,
)


SHA_A = "a" * 40
SHA_B = "b" * 40
SHA_C = "c" * 40


def dump(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def policy(builder="builder", auditor="auditor", rounds=3):
    return {
        "schema_version": "0.1",
        "id": "builder-auditor-loop",
        "builder_role_id": builder,
        "auditor_role_id": auditor,
        "product_authority_id": "human-owner",
        "max_audit_rounds": rounds,
        "immutable_audit_target": True,
        "auditor_write_access": False,
        "human_gate_required": True,
        "auto_advance_after_audit": False,
        "persist_handoffs": True,
    }


def builder_report(result="READY_FOR_AUDIT", sha=SHA_A):
    return {
        "schema_version": "0.1",
        "executor_id": "builder-executor",
        "role": "BUILDER",
        "authority": "IMPLEMENTATION",
        "result_sha": sha,
        "result": result,
        "summary": "Mudança concluída dentro do escopo autorizado.",
        "changed_paths": ["src/example.txt"],
        "checks": [{"id": "unit", "status": "PASS", "evidence": "suite green"}],
        "limitations": [],
        "disputed_findings": [],
        "escalation": None,
    }


def audit_report(sha: str, result="PASS", blocking=False):
    findings = []
    if blocking:
        findings.append(
            {
                "id": "AUD-001",
                "severity": "HIGH",
                "blocking": True,
                "files": ["src/example.txt"],
                "evidence": "evidence",
                "problem": "blocking problem",
                "violated_criterion": "criterion",
                "resolution_condition": "fix condition",
            }
        )
    return {
        "schema_version": "0.1",
        "executor_id": "auditor-executor",
        "role": "AUDITOR",
        "authority": "INDEPENDENT_AUDIT",
        "audit_result": result,
        "audited_sha": sha,
        "summary": "Independent review complete.",
        "findings": findings,
        "checks": [{"id": "scope", "status": "PASS", "evidence": "reviewed"}],
        "residual_risks": [],
        "gate_registration": "NOT_AUTHORIZED",
    }


class OrchestrateHandoffsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        self.policy_path = self.root / "policy.json"
        self.state_path = self.root / "state.json"
        dump(self.policy_path, policy())
        init_state(
            self.policy_path,
            self.state_path,
            project_id="sample",
            phase="F01",
            gate="G01",
            builder_branch="work/sample-f01",
        )

    def tearDown(self):
        self.temp.cleanup()

    def test_reference_policy_initializes_exactly_three_audit_rounds(self):
        reference_policy = Path(__file__).resolve().parents[1] / "orchestration" / "builder-auditor-policy.json"
        reference_state = self.root / "reference-state.json"

        state = init_state(
            reference_policy,
            reference_state,
            project_id="sample",
            phase="O0",
            gate="S1",
            builder_branch="builder/o0-c21",
        )

        self.assertEqual(3, state["max_audit_rounds"])

    def test_fail_fix_pass_human_gate_flow(self):
        builder_one = self.root / "builder-1.json"
        dump(builder_one, builder_report())
        state = builder_handoff(self.state_path, builder_one, SHA_A)
        self.assertEqual("READY_FOR_AUDIT", state["machine_state"])
        self.assertEqual(SHA_A, state["audit_target_sha"])

        audit_one = self.root / "audit-1.json"
        dump(audit_one, audit_report(SHA_A, result="FAIL", blocking=True))
        state = audit_handoff(self.state_path, audit_one)
        self.assertEqual("FIX_REQUIRED", state["machine_state"])
        self.assertEqual(1, state["audit_round"])

        builder_two = self.root / "builder-2.json"
        dump(builder_two, builder_report(sha=SHA_B))
        state = builder_handoff(self.state_path, builder_two, SHA_B)
        self.assertEqual(SHA_B, state["audit_target_sha"])

        audit_two = self.root / "audit-2.json"
        dump(audit_two, audit_report(SHA_B))
        state = audit_handoff(self.state_path, audit_two)
        self.assertEqual("WAITING_PRODUCT_AUTHORITY", state["machine_state"])
        self.assertIsNone(state["approval"])
        self.assertEqual("G01", state["gate"])
        self.assertEqual("PRODUCT_AUTHORITY", next_actor(state))

        state = approve_gate(self.state_path, executor_id="human-owner", role="PRODUCT_AUTHORITY", gate="G01", audited_sha=SHA_B)
        self.assertEqual("GATE_APPROVED", state["machine_state"])
        self.assertEqual(SHA_B, state["approval"]["audited_sha"])

    def test_audit_sha_mismatch_is_rejected(self):
        builder_path = self.root / "builder.json"
        dump(builder_path, builder_report())
        builder_handoff(self.state_path, builder_path, SHA_A)
        audit_path = self.root / "audit.json"
        dump(audit_path, audit_report(SHA_B))
        with self.assertRaises(HandoffError):
            audit_handoff(self.state_path, audit_path)

    def test_disputed_builder_report_requires_finding_reference(self):
        disputed_path = self.root / "builder-disputed.json"
        dump(disputed_path, builder_report(result="DISPUTED"))
        before = self.state_path.read_bytes()

        with self.assertRaises(HandoffError):
            builder_handoff(self.state_path, disputed_path, SHA_A)

        self.assertEqual(before, self.state_path.read_bytes())

    def test_disputed_builder_report_blocks_for_product_authority(self):
        disputed_path = self.root / "builder-disputed.json"
        report = builder_report(result="DISPUTED")
        report["disputed_findings"] = ["AUD-020-001"]
        dump(disputed_path, report)

        state = builder_handoff(self.state_path, disputed_path, SHA_A)

        self.assertEqual("BLOCKED", state["machine_state"])
        self.assertEqual("PRODUCT_AUTHORITY", next_actor(state))
        self.assertEqual(str(disputed_path), state["last_builder_report"])
        self.assertIsNone(state["approval"])
        self.assertIn("DISPUTED", state["message"])

    def test_pass_with_blocking_finding_is_rejected(self):
        builder_path = self.root / "builder.json"
        dump(builder_path, builder_report())
        builder_handoff(self.state_path, builder_path, SHA_A)
        audit_path = self.root / "audit.json"
        dump(audit_path, audit_report(SHA_A, result="PASS", blocking=True))
        with self.assertRaises(HandoffError):
            audit_handoff(self.state_path, audit_path)

    def test_same_builder_and_auditor_role_is_rejected(self):
        bad_policy = self.root / "bad-policy.json"
        other_state = self.root / "other-state.json"
        dump(bad_policy, policy(builder="same", auditor="same"))
        with self.assertRaises(HandoffError):
            init_state(
                bad_policy,
                other_state,
                project_id="sample",
                phase="F01",
                gate="G01",
                builder_branch="work/sample-f01",
            )

    def test_same_executor_for_builder_and_auditor_is_rejected(self):
        builder_path = self.root / "builder.json"
        report = builder_report()
        dump(builder_path, report)
        builder_handoff(self.state_path, builder_path, SHA_A)
        audit_path = self.root / "audit.json"
        audit = audit_report(SHA_A)
        audit["executor_id"] = report["executor_id"]
        dump(audit_path, audit)
        with self.assertRaises(HandoffError):
            audit_handoff(self.state_path, audit_path)

    def test_pass_with_fail_check_is_rejected(self):
        self._assert_pass_check_rejected("FAIL")

    def test_pass_with_not_run_check_is_rejected(self):
        self._assert_pass_check_rejected("NOT_RUN")

    def _assert_pass_check_rejected(self, status):
        builder_path = self.root / f"builder-{status}.json"
        dump(builder_path, builder_report())
        builder_handoff(self.state_path, builder_path, SHA_A)
        audit_path = self.root / f"audit-{status}.json"
        report = audit_report(SHA_A)
        report["checks"][0]["status"] = status
        dump(audit_path, report)
        with self.assertRaises(HandoffError):
            audit_handoff(self.state_path, audit_path)

    def test_fail_without_findings_is_rejected(self):
        builder_path = self.root / "builder-empty-findings.json"
        dump(builder_path, builder_report())
        builder_handoff(self.state_path, builder_path, SHA_A)
        audit_path = self.root / "audit-empty-findings.json"
        dump(audit_path, audit_report(SHA_A, result="FAIL"))
        with self.assertRaises(HandoffError):
            audit_handoff(self.state_path, audit_path)

    def test_unauthorized_gate_requester_is_rejected(self):
        builder_path = self.root / "builder-approval.json"
        audit_path = self.root / "audit-approval.json"
        dump(builder_path, builder_report())
        builder_handoff(self.state_path, builder_path, SHA_A)
        dump(audit_path, audit_report(SHA_A))
        audit_handoff(self.state_path, audit_path)
        with self.assertRaises(HandoffError):
            approve_gate(self.state_path, executor_id="runner", role="PRODUCT_AUTHORITY", gate="G01", audited_sha=SHA_A)

    def test_auditor_gate_registration_attempt_is_rejected_without_state_change(self):
        builder_path = self.root / "builder-gate-attempt.json"
        audit_path = self.root / "audit-gate-attempt.json"
        dump(builder_path, builder_report())
        builder_handoff(self.state_path, builder_path, SHA_A)
        report = audit_report(SHA_A)
        report["gate_registration"] = "G01"
        dump(audit_path, report)
        before = self.state_path.read_bytes()

        with self.assertRaisesRegex(HandoffError, "audit schema validation failed"):
            audit_handoff(self.state_path, audit_path)

        self.assertEqual(before, self.state_path.read_bytes())
        unchanged = json.loads(self.state_path.read_text(encoding="utf-8"))
        self.assertEqual("READY_FOR_AUDIT", unchanged["machine_state"])
        self.assertIsNone(unchanged["approval"])
        self.assertEqual("G01", unchanged["gate"])

    def test_third_failed_audit_blocks_default_three_round_loop(self):
        for round_number, sha in enumerate((SHA_A, SHA_B, SHA_C), start=1):
            builder_path = self.root / f"builder-round-{round_number}.json"
            audit_path = self.root / f"audit-round-{round_number}.json"
            dump(builder_path, builder_report(sha=sha))
            dump(audit_path, audit_report(sha, result="FAIL", blocking=True))
            builder_handoff(self.state_path, builder_path, sha)
            state = audit_handoff(self.state_path, audit_path)

            if round_number < 3:
                self.assertEqual("FIX_REQUIRED", state["machine_state"])

        self.assertEqual(3, state["audit_round"])
        self.assertEqual("BLOCKED", state["machine_state"])
        self.assertEqual("PRODUCT_AUTHORITY", next_actor(state))
        self.assertIsNone(state["approval"])


if __name__ == "__main__":
    unittest.main()
