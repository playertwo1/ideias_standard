# IDEIAS STANDARD — PROJECT STATE

- **Versão:** 0.1.0-draft
- **Fase:** S0 — Fundação do padrão
- **Status:** AUDIT_READY
- **Objetivo atual:** concluir auditoria independente S0 antes de abrir S1
- **Última concluída:** matriz de conformance verde em Python 3.11/3.12/3.13 + evidência registrada
- **Próxima:** auditor independente executar `S0_AUDIT_PACKET.md` e emitir `AUDIT RESULT: PASS|FAIL`
- **Bloqueios do projeto:** nenhum conhecido
- **Gate S0:** NOT_RUN — validação técnica PASS, auditoria independente pendente
- **CLI completa:** NOT_RUN
- **Validação de fixtures:** PASS no workflow `Conformance` run `34832777706`

## Evidência atual

- SHA validado: `18968a30329f8063ad87bd68543df72f977b3e5a`
- Python 3.11: PASS
- Python 3.12: PASS
- Python 3.13: PASS
- Unit/adversarial fixtures: PASS
- Self-check: PASS
- Projeto positivo de referência: PASS
- Evidência detalhada: `S0_VALIDATION_EVIDENCE.md`

O primeiro run da CI falhou apenas na configuração do cache do `setup-python`; `cache-dependency-path: requirements-dev.txt` foi adicionado e a matriz foi reexecutada com sucesso.

## Materializado

- `STANDARD.md` com lifecycle manager, ownership, conformance, bundles, workflows e change units;
- `INVARIANTS.yaml` com invariantes críticos versionáveis;
- `COMPATIBILITY.yaml` + `VERSIONING.md`;
- `CLI_CONTRACT.md` com comportamento e exit codes futuros;
- schemas de project manifest, standard lock, context manifest, artifact policy, bundle, workflow, change, conformance report e invariants;
- perfis LIGHT / STANDARD / DEEP;
- packs Android, Python, backend, AI, sensitive-data e multi-agent;
- bundles e workflows declarativos;
- catálogo de adapters ACTIVE/PLANNED;
- política `MANAGED / MERGEABLE / USER_OWNED`;
- examples, fixtures adversariais, fixture manifest e golden outputs;
- `VALIDATION_CONTRACT.md`;
- `scripts/validate_standard.py` com self-check e enforcement semântico;
- testes data-driven;
- `.github/workflows/conformance.yml` com matriz Python 3.11/3.12/3.13;
- `S0_VALIDATION_EVIDENCE.md` e `S0_AUDIT_PACKET.md`;
- roadmap S0–S8.

## Invariantes destacados

- `NOT_RUN != PASS`.
- USER_OWNED nunca sofre overwrite automático.
- Contexto REQUIRED nunca é truncado silenciosamente.
- sensitive-data exige human gate.
- multi-agent exige auditoria independente e Builder != Auditor.
- bundle/workflow/adapter nunca amplia autoridade.
- existência de artefato não substitui evidência executada.

## Próxima ação

Auditor independente deve usar `S0_AUDIT_PACKET.md`, revisar o HEAD atual e confirmar que as mudanças documentais posteriores à evidência não introduziram regressão. A CI do HEAD deve permanecer verde.

Somente após `AUDIT RESULT: PASS` registrar Gate S0 como PASS e iniciar S1 (`check`/`doctor`).
