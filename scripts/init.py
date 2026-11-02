#!/usr/bin/env python3
"""Inicializa um novo projeto com o template do Ideias Standard.

Uso:
  python scripts/init.py <destino> [--name "Nome do Projeto"] [--no-design] [--force]

Execução remota direta (sem clonar o repositório):
  curl -sSL https://raw.githubusercontent.com/playertwo1/ideias_standard/main/scripts/init.py | python3 - meu-projeto
  irm https://raw.githubusercontent.com/playertwo1/ideias_standard/main/scripts/init.py | python - meu-projeto
"""
import io
import shutil
import sys
import zipfile
from pathlib import Path
from urllib.request import Request, urlopen

REPO_ZIP_URL = "https://github.com/playertwo1/ideias_standard/archive/refs/heads/main.zip"
ZIP_TEMPLATE_PREFIX = "ideias_standard-main/template/"


def find_local_template() -> Path | None:
    try:
        if "__file__" in globals() and __file__ and not __file__.startswith("<"):
            p = Path(__file__).resolve().parent.parent / "template"
            if p.is_dir():
                return p
    except Exception:
        pass
    return None


def copy_local(template_dir: Path, dest: Path) -> None:
    for item in template_dir.iterdir():
        target = dest / item.name
        if item.is_dir():
            shutil.copytree(item, target, dirs_exist_ok=True)
        else:
            shutil.copy2(item, target)


def download_remote_template(dest: Path) -> None:
    req = Request(REPO_ZIP_URL, headers={"User-Agent": "ideias_standard-init"})
    with urlopen(req) as resp:
        data = resp.read()
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        for member in zf.namelist():
            if member.startswith(ZIP_TEMPLATE_PREFIX) and not member.endswith("/"):
                rel = member[len(ZIP_TEMPLATE_PREFIX):]
                target = dest / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(zf.read(member))


def replace_project_name(dest: Path, name: str) -> None:
    for path in dest.rglob("*"):
        if path.is_file() and path.suffix in (".md", ".txt"):
            try:
                content = path.read_text(encoding="utf-8")
                if "{{nome do projeto}}" in content:
                    path.write_text(content.replace("{{nome do projeto}}", name), encoding="utf-8")
            except (UnicodeDecodeError, PermissionError):
                pass


def init_project(dest: Path, name: str | None = None, no_design: bool = False, force: bool = False) -> None:
    if dest.exists() and any(dest.iterdir()) and not force:
        raise ValueError(f"pasta de destino não está vazia: {dest}. Use --force para sobrescrever.")

    dest.mkdir(parents=True, exist_ok=True)

    local_template = find_local_template()
    if local_template:
        copy_local(local_template, dest)
    else:
        download_remote_template(dest)

    project_name = name or dest.resolve().name
    if project_name:
        replace_project_name(dest, project_name)

    if no_design:
        design_file = dest / "DESIGN.md"
        if design_file.is_file():
            design_file.unlink()


def main(argv: list[str]) -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    import argparse

    parser = argparse.ArgumentParser(
        description="Inicializa um novo projeto com o template do Ideias Standard.",
        prog="init.py",
    )
    parser.add_argument("dest", type=Path, help="Caminho da pasta do novo projeto")
    parser.add_argument("--name", type=str, default=None, help="Nome do projeto (padrão: nome da pasta)")
    parser.add_argument("--no-design", action="store_true", help="Não incluir DESIGN.md (projetos sem interface)")
    parser.add_argument("--force", action="store_true", help="Sobrescreve arquivos se o destino já existir")

    try:
        args = parser.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code != 0 else 0

    try:
        init_project(args.dest, name=args.name, no_design=args.no_design, force=args.force)
    except Exception as err:
        print(f"erro: {err}", file=sys.stderr)
        return 1

    print(f"PASS: projeto inicializado em {args.dest.resolve()}")
    print("Próximo passo: preencha PROJECT.md e confira com python scripts/check.py <projeto>")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
