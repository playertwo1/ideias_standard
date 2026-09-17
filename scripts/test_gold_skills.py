import hashlib
import json
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class GoldSkillsTest(unittest.TestCase):
    def test_gold_audit_valid_and_defective_fixtures(self):
        valid = json.loads((ROOT / "fixtures/gold-skills/valid-change.json").read_text())
        bad = json.loads((ROOT / "fixtures/gold-skills/defective-change.json").read_text())
        self.assertEqual("PASS", valid["check"])
        self.assertEqual([], bad["acceptance"])

    def test_goldify_fixture_is_existing_project(self):
        self.assertTrue((ROOT / "fixtures/gold-skills/existing-project/README.md").is_file())
        self.assertIn("Golden Diff", (ROOT / ".agents/skills/goldify/SKILL.md").read_text(encoding="utf-8"))

    def test_skill_author_metadata_and_provider_neutrality(self):
        metadata = json.loads((ROOT / "fixtures/gold-skills/skill-metadata.json").read_text())
        self.assertEqual(3, len(metadata["skills"]))
        self.assertTrue(metadata["provider_neutral"])
        for skill in metadata["skills"]:
            text = (ROOT / ".agents/skills" / skill / "SKILL.md").read_text(encoding="utf-8")
            self.assertRegex(text, "Seguran[cç]a")
            self.assertIn("Licença", text)

    def test_evidence_digests_match_files(self):
        evidence = json.loads((ROOT / "F0_SK_EVIDENCE.json").read_text())
        for item in evidence["artifacts"]:
            # Hash the committed blob so checkout newline normalization cannot alter evidence.
            committed = subprocess.check_output(["git", "show", f"HEAD:{item['path']}"])
            digest = hashlib.sha256(committed).hexdigest()
            self.assertEqual(digest, item["sha256"])


if __name__ == "__main__":
    unittest.main()
