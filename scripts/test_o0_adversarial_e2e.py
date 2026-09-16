"""O0-C45: Adversarial E2E cycle covering concurrency, interruption, timeout, and retry."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


class O0AdversarialE2ETest(unittest.TestCase):
    def test_adversarial_e2e_cycle_covers_all_dimensions(self):
        source = Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            output = root / "adversarial-evidence.json"
            process = subprocess.run(
                [
                    sys.executable,
                    str(source / "scripts" / "o0_adversarial_e2e.py"),
                    "--work-root",
                    str(root / "run"),
                    "--output",
                    str(output),
                ],
                cwd=source,
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(0, process.returncode, process.stderr)
            self.assertTrue(output.is_file(), "Adversarial evidence file must be created")
            evidence = json.loads(output.read_text(encoding="utf-8"))

            # 1. Coverage verification
            coverage = evidence["adversarial_coverage"]
            self.assertTrue(coverage["retry"])
            self.assertTrue(coverage["concurrency"])
            self.assertTrue(coverage["timeout"])
            self.assertTrue(coverage["interruption_preservation"])
            self.assertTrue(coverage["duplicate_rejection"])

            # 2. Retry verification
            retry = evidence["retry_evidence"]
            self.assertEqual(2, retry["transient_failure_exit_code"])
            self.assertEqual("ACTOR_EXIT_NONZERO", retry["failure_record_kind"])
            self.assertEqual(7, retry["actor_exit_code"])
            self.assertEqual(0, retry["retry_success_exit_code"])
            self.assertEqual("READY_FOR_AUDIT", retry["machine_state_after_retry"])

            # 3. Concurrency verification
            concurrency = evidence["concurrency_evidence"]
            self.assertEqual(2, concurrency["concurrent_rejected_exit_code"])
            self.assertIn("Runner state lock is busy", concurrency["concurrent_error_message"])
            self.assertEqual(0, concurrency["primary_completed_exit_code"])
            self.assertEqual("WAITING_PRODUCT_AUTHORITY", concurrency["machine_state_after_primary"])

            # 4. Timeout verification
            timeout = evidence["timeout_evidence"]
            self.assertEqual(2, timeout["timeout_exit_code"])
            self.assertTrue(timeout["state_preserved"])

            # 5. Final state verification
            final = evidence["final_state"]
            self.assertEqual("WAITING_PRODUCT_AUTHORITY", final["machine_state"])
            self.assertEqual("PRODUCT_AUTHORITY", final["next_actor"])
            self.assertIsNone(final["approval"])
            self.assertTrue(final["human_gate_required"])
            self.assertEqual("O0", final["phase"])
            self.assertEqual("S1", final["gate"])


if __name__ == "__main__":
    unittest.main()
