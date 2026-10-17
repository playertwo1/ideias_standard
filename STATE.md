# STATE — ponto de retomada

**Atualizado:** 2026-10-17 · **Marco ativo:** v1.1 — Piloto · **Estado:** READY

## O que funciona hoje (confirmado no código)
- `template/` com o kit completo; `examples/command/` preenchido passa no checker.
- `scripts/check.py` (só biblioteca padrão) e testes em `tests/test_check.py`.
- CI roda testes e checker em Python 3.11–3.13.

## Última atividade
- v1.2.0 (branch `feat/guardrail`, PR aberto, aguardando aceite): `WATCHDOG.md` e `AUDIT.md` do repositório `guardrail` incorporados ao `template/docs/`. Testes: unittest e `check.py` (exemplo, template, raiz) `--strict` → PASS.
- v1.1.0: `DESIGN.md` no template e nomes alternativos no checker (atrito do primeiro projeto existente adotado).
- v1.0: Gold V5 simplificado para kit de documentos, com base no manual multi-IA v2 e na adoção real em um projeto existente. Legado na tag `v0.1-gold-legacy`.
- Testes: ver commit da v1.0 (unittest, `check.py examples/command`, `check.py template --template`).

## Próxima ação
- v1.1-01 — criar o próximo projeto novo a partir do `template/` e registrar atritos (o que sobrou, o que faltou) no `ROADMAP.md`.

## Bloqueios e aprovações humanas
- PR `feat/guardrail` (v1.2.0) aguarda revisão e merge do dono; entrou sem passar pelo piloto (exceção à regra 4 do `AGENTS.md`, pedida pelo dono).

## Divergências entre roadmap e implementação
- Nenhuma.
