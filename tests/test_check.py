import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import check  # noqa: E402


def levels(found):
    return [level for level, _ in found]


class CheckTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)

    def copy(self, src):
        dst = self.tmp / "p"
        shutil.copytree(ROOT / src, dst)
        return dst

    def test_template_passes_only_in_template_mode(self):
        p = self.copy("template")
        self.assertEqual(check.check(p, template=True), [])
        self.assertIn("FAIL", levels(check.check(p)))

    def test_filled_example_passes(self):
        self.assertEqual(check.check(ROOT / "examples" / "command"), [])

    def test_missing_state_fails(self):
        p = self.copy("examples/command")
        (p / "STATE.md").unlink()
        self.assertTrue(any("STATE.md" in m for _, m in check.check(p)))

    def test_empty_next_action_fails(self):
        p = self.copy("examples/command")
        (p / "STATE.md").write_text("# STATE\n\n## Próxima ação\n- \n\n## Bloqueios\n- nenhum\n", encoding="utf-8")
        self.assertTrue(any("Próxima ação" in m for _, m in check.check(p)))

    def test_long_agents_and_bad_claude_warn(self):
        p = self.copy("examples/command")
        (p / "AGENTS.md").write_text("regra\n" * 200, encoding="utf-8")
        (p / "CLAUDE.md").write_text("cópia das regras\n", encoding="utf-8")
        self.assertEqual(levels(check.check(p)), ["WARN", "WARN"])

    def test_product_md_replaces_project_md(self):
        p = self.copy("examples/command")
        (p / "PROJECT.md").rename(p / "PRODUCT.md")
        self.assertEqual(check.check(p), [])
        (p / "PRODUCT.md").unlink()
        self.assertTrue(any("PROJECT.md ou PRODUCT.md" in m for _, m in check.check(p)))

    def test_unfilled_design_fails_only_when_present(self):
        p = self.copy("examples/command")
        (p / "DESIGN.md").unlink()
        self.assertEqual(check.check(p), [])
        shutil.copy(ROOT / "template" / "DESIGN.md", p / "DESIGN.md")
        self.assertTrue(any(m.startswith("DESIGN.md") for _, m in check.check(p)))

    def test_template_ships_guardrails(self):
        # WATCHDOG e AUDIT são usados como estão: existem, sem marcadores, e o AGENTS.md aponta para eles.
        agents = (ROOT / "template" / "AGENTS.md").read_text(encoding="utf-8")
        for name in ("WATCHDOG.md", "AUDIT.md"):
            path = ROOT / "template" / "docs" / name
            self.assertTrue(path.is_file(), name)
            self.assertIsNone(check.PLACEHOLDER.search(path.read_text(encoding="utf-8")), name)
            self.assertIn(f"docs/{name}", agents)

    def test_exit_codes(self):
        self.assertEqual(check.main([str(ROOT / "examples" / "command")]), 0)
        self.assertEqual(check.main([str(ROOT / "template")]), 1)
        self.assertEqual(check.main([str(self.tmp / "nao-existe")]), 2)
        self.assertEqual(check.main([]), 2)


if __name__ == "__main__":
    unittest.main()
