#!/usr/bin/env python3
"""Inicializa um novo projeto com o template do Ideias Standard.

Uso:
  python scripts/init.py <destino> [--name "Nome do Projeto"] [--no-design] [--force]

Execução remota direta (sem clonar o repositório):
  curl -sSL https://raw.githubusercontent.com/playertwo1/ideias_standard/main/scripts/init.py | python3 - meu-projeto
  irm https://raw.githubusercontent.com/playertwo1/ideias_standard/main/scripts/init.py | python - meu-projeto
"""
import io
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


def local_files(template_dir: Path):
    for path in sorted(template_dir.rglob("*")):
        if path.is_file():
            yield path.relative_to(template_dir).as_posix(), path.read_bytes()


def remote_files():
    req = Request(REPO_ZIP_URL, headers={"User-Agent": "ideias_standard-init"})
    with urlopen(req) as resp:
        data = resp.read()
    with zipfile.ZipFile(io.BytesIO(data)) as zf:
        for member in zf.namelist():
            if member.startswith(ZIP_TEMPLATE_PREFIX) and not member.endswith("/"):
                yield member[len(ZIP_TEMPLATE_PREFIX):], zf.read(member)


def init_project(dest: Path, name: str | None = None, no_design: bool = False, force: bool = False) -> list[str]:
    """Cria os arquivos do template em dest. Nunca sobrescreve: devolve os que já existiam e foram mantidos."""
    if dest.exists() and any(dest.iterdir()) and not force:
        raise ValueError(f"pasta de destino não está vazia: {dest}. Use --force para adicionar só os arquivos que faltam.")

    dest.mkdir(parents=True, exist_ok=True)
    project_name = (name or dest.resolve().name).encode("utf-8")
    local_template = find_local_template()
    kept = []
    for rel, data in local_files(local_template) if local_template else remote_files():
        if no_design and rel == "DESIGN.md":
            continue
        target = dest / rel
        if target.exists():
            kept.append(rel)
            continue
        if target.suffix == ".md":
            data = data.replace("{{nome do projeto}}".encode("utf-8"), project_name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    return kept


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
    parser.add_argument("--force", action="store_true", help="Permite destino não vazio; arquivos existentes são mantidos")

    try:
        args = parser.parse_args(argv)
    except SystemExit as e:
        return 2 if e.code != 0 else 0

    try:
        kept = init_project(args.dest, name=args.name, no_design=args.no_design, force=args.force)
    except Exception as err:
        print(f"erro: {err}", file=sys.stderr)
        return 1

    print(f"PASS: projeto inicializado em {args.dest.resolve()}")
    for rel in kept:
        print(f"mantido (já existia): {rel}")
    print("Próximo passo: preencha PROJECT.md, AGENTS.md e STATE.md; confira com o scripts/check.py do ideias_standard")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
