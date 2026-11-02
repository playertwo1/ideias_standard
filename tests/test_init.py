import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import check  # noqa: E402
import init  # noqa: E402


class InitTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)

    def test_init_creates_all_core_files_and_passes_template_check(self):
        dest = self.tmp / "meu_projeto"
        init.init_project(dest, name="Meu Projeto")

        self.assertTrue((dest / "README.md").is_file())
        self.assertTrue((dest / "PROJECT.md").is_file())
        self.assertTrue((dest / "ROADMAP.md").is_file())
        self.assertTrue((dest / "STATE.md").is_file())
        self.assertTrue((dest / "AGENTS.md").is_file())
        self.assertTrue((dest / ".gitignore").is_file())
        self.assertTrue((dest / ".editorconfig").is_file())
        self.assertTrue((dest / "docs" / "WATCHDOG.md").is_file())
        self.assertTrue((dest / "docs" / "AUDIT.md").is_file())

        project_text = (dest / "PROJECT.md").read_text(encoding="utf-8")
        self.assertIn("# PROJECT — Meu Projeto", project_text)

        # Deve passar no check do template
        self.assertEqual(check.check(dest, template=True), [])

    def test_init_no_design_flag_removes_design_md(self):
        dest = self.tmp / "api_projeto"
        init.init_project(dest, no_design=True)
        self.assertFalse((dest / "DESIGN.md").exists())
        self.assertTrue((dest / "PROJECT.md").is_file())

    def test_init_fails_on_existing_non_empty_dir_without_force(self):
        dest = self.tmp / "ocupado"
        dest.mkdir()
        (dest / "arquivo.txt").write_text("conteudo", encoding="utf-8")

        with self.assertRaises(ValueError):
            init.init_project(dest, force=False)

        # Com force deve passar
        init.init_project(dest, force=True)
        self.assertTrue((dest / "PROJECT.md").is_file())

    def test_cli_exit_codes(self):
        dest = self.tmp / "cli_projeto"
        self.assertEqual(init.main([str(dest), "--name", "CLI Projeto"]), 0)
        self.assertEqual(init.main([str(dest)]), 1)  # pasta não vazia sem force
        self.assertEqual(init.main([str(dest), "--force"]), 0)
        self.assertEqual(init.main([]), 2)  # falta argumento obrigatório


if __name__ == "__main__":
    unittest.main()
