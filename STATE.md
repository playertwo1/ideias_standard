# STATE — ponto de retomada

**Atualizado:** 2026-11-11 · **Marco ativo:** v1.1 — Piloto · **Estado:** READY

## O que funciona hoje (confirmado no código)
- `template/` com o kit completo; `examples/command/` preenchido passa no checker.
- `scripts/check.py` (verificador só com biblioteca padrão) e testes em `tests/test_check.py`.
- `scripts/init.py` (inicializador só com biblioteca padrão) com suporte local e remoto em uma linha; testes em `tests/test_init.py`.
- Repositório configurado como Template no GitHub (`isTemplate: true`).

## Última atividade
- v1.4.0: corte de redundância no template (`WATCHDOG`, `AUDIT`, `README`) e no `README.md`; `init.py --force` não sobrescreve mais. Testes: `python -m unittest discover -s tests` → PASS (13); `check.py` em `examples/command`, `template --template` e `.` com `--strict` → PASS.
- v1.3.0: `scripts/init.py` implementado para eliminar o atrito de cópia manual ao iniciar projetos novos. Suporte a execução remota de uma linha (PowerShell e bash), substituição de nome e `--no-design`. Testes unitários cobrindo o inicializador. Branches remotas antigas limpas.
- v1.2.0: `WATCHDOG.md` e `AUDIT.md` do repositório `guardrail` incorporados ao `template/docs/`.
- v1.1.0: `DESIGN.md` no template e nomes alternativos no checker.
- v1.0.0: Gold V5 simplificado para kit de documentos.

## Próxima ação
- v1.1-01 — usar o `scripts/init.py` para criar o próximo projeto piloto e validar o fluxo ponta a ponta.

## Bloqueios e aprovações humanas
- Nenhum.

## Divergências entre roadmap e implementação
- Nenhuma.
