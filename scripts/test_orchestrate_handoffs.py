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
)


SHA_A = "a" * 40
SHA_B = "b" * 40


def dump(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def policy(builder="builder", auditor="auditor", rounds=3):
    return {
        "schema_version": "0.1",
        "id": "builder-auditor-loop",
        "builder_role_id": builder,
        "auditor_role_id": auditor,
        "max_audit_rounds": rounds,
        "immutable_audit_target": True,
        "auditor_write_access": False,
        "human_gate_required": True,
        "auto_advance_after_audit": False,
        "persist_handoffs": True,
    }


def builder_report(result="READY_FOR_AUDIT"):
    return {
        "schema_version": "0.1",
        "role": "BUILDER",
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
        "role": "AUDITOR",
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
        dump(builder_two, builder_report())
        state = builder_handoff(self.state_path, builder_two, SHA_B)
        self.assertEqual(SHA_B, state["audit_target_sha"])

        audit_two = self.root / "audit-2.json"
        dump(audit_two, audit_report(SHA_B))
        state = audit_handoff(self.state_path, audit_two)
        self.assertEqual("WAITING_PRODUCT_AUTHORITY", state["machine_state"])
        self.assertIsNone(state["approval"])

        state = approve_gate(self.state_path, authority="product-authority")
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

    def test_round_limit_blocks_loop(self):
        temp_policy = self.root / "one-round.json"
        temp_state = self.root / "one-round-state.json"
        dump(temp_policy, policy(rounds=1))
        init_state(
            temp_policy,
            temp_state,
            project_id="sample",
            phase="F01",
            gate="G01",
            builder_branch="work/sample-f01",
        )
        builder_path = self.root / "builder-round.json"
        audit_path = self.root / "audit-round.json"
        dump(builder_path, builder_report())
        dump(audit_path, audit_report(SHA_A, result="FAIL", blocking=True))
        builder_handoff(temp_state, builder_path, SHA_A)
        state = audit_handoff(temp_state, audit_path)
        self.assertEqual("BLOCKED", state["machine_state"])


if __name__ == "__main__":
    unittest.main()
