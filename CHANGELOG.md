# Changelog

## 1.2.0 — 2026-10-17
- `template/docs/WATCHDOG.md`: guardião de execução (hierarquia de decisão, escopo e anti-drift, proteção contra regressão, ações de alto risco, loop de erro, regra de parada). Lido antes de mudança média, grande ou arriscada.
- `template/docs/AUDIT.md`: auditoria final independente (escopo, diff, regressão, qualidade, segurança, caça a atalhos) com severidade CRITICAL/HIGH/MEDIUM/LOW e `AUDIT RESULT: PASS | FAIL` registrado na review.
- Origem: repositório [playertwo1/guardrail](https://github.com/playertwo1/guardrail) (`WATCHDOG.md`, `AUDIT.md`, `AGENTS_GUARDRAILS.md`, commit `5bf7008`), adaptado ao kit: verificação, git e segurança apontam para `RELEASE_CHECKLIST` e `AGENTS.md` em vez de se repetirem; o bloco `AGENTS_GUARDRAILS.md` virou ajustes nas regras 3, 4 e 7 do `template/AGENTS.md` (as 10 regras continuam 10).
- `template/AGENTS.md`, `README.md`, `RELEASE_CHECKLIST` e `templates/REVIEW.md` apontam para os dois arquivos; `GUIA` (papéis, prompt de auditoria, adoção), `examples/command/AGENTS.md` e o `AGENTS.md` deste repositório também.
- Teste novo garante que o template entrega `WATCHDOG.md` e `AUDIT.md` sem marcadores e referenciados no `AGENTS.md`.

## 1.1.0 — 2026-10-11
- `template/DESIGN.md`: a cara do app (tokens de cor, tipografia, forma e componentes no frontmatter + overview, layout, estados e do's/don'ts), compatível com o formato usado pelo Impeccable. Exemplo preenchido em `examples/command/DESIGN.md`.
- `check.py` aceita nomes alternativos (`PRODUCT.md` no lugar de `PROJECT.md`) e confere `DESIGN.md` quando existe. Primeiro atrito do piloto (projeto existente).
- AGENTS, RELEASE_CHECKLIST (V4), GUIA e READMEs apontam para o `DESIGN.md`.

## 1.0.0 — 2026-10-11
- Kit de documentos substitui o Gold V5: `template/` com `PROJECT`, `ROADMAP`, `STATE`, `AGENTS`, `CLAUDE`, `DECISIONS`, `RELEASE_CHECKLIST` e os modelos `FEATURE`, `EXECUTION_PLAN` e `REVIEW`.
- `docs/GUIA.md` (passo a passo, estados, papéis, prompts, adoção) e `docs/PESQUISA.md` (evidências R01–R28, protocolo comparativo), a partir do manual multi-IA v2.
- `scripts/check.py` reescrito, só biblioteca padrão; exemplo preenchido em `examples/command/`.
- Removidos: schemas, lock, manifests, packs, profiles, bundles, adapters, workflows, goldify, sync, fixtures, skills, evidências de auditoria e contratos (`STANDARD`, `PROJECT_GUIDE`, `PROJECT_STATE`, `CLI_CONTRACT`, `VALIDATION_CONTRACT`, `VERSIONING`, `INVARIANTS`, `COMPATIBILITY`, `REFERENCE_MATRIX`). Motivo: nenhum projeto real usava lock, manifest ou packs, e o template entregue era quase vazio.
- Tudo preservado na tag `v0.1-gold-legacy`. Ideias mantidas: contexto progressivo, disciplina de tokens, Builder/Auditor, prova antes de expandir e preservação do trabalho local na adoção.

## 0.1.0-draft — 2026-09-14 a 2026-10-10
Gold V0–V5 (S0–S8, F0–F5). Detalhes na tag `v0.1-gold-legacy`.
