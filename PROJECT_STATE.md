# IDEIAS STANDARD — PROJECT STATE

- **Versão:** 0.1.0-draft
- **Fase:** S0 — Fundação do padrão
- **Status:** EM_VALIDACAO
- **Objetivo atual:** executar e comprovar a suíte de conformance antes de abrir S1
- **Última concluída:** materialização de bundles/workflows/change lifecycle + fixtures adversariais + validador determinístico
- **Próxima:** executar `python -m unittest scripts.test_validate_standard -v` em checkout limpo; corrigir findings; registrar evidência
- **Bloqueios do projeto:** nenhum conhecido
- **Bloqueio desta sessão:** ambiente não conseguiu resolver `github.com` para clonar o repositório e executar a suíte real
- **CLI completa:** NOT_RUN
- **Validação de fixtures:** NOT_RUN nesta revisão; arquivos/testes foram materializados, mas não homologados por execução

## Materializado

- `STANDARD.md` atualizado com lifecycle manager, ownership, conformance, bundles, workflows e change units;
- schemas de project manifest, standard lock, context manifest, artifact policy, bundle, workflow, change e conformance report;
- `standard.lock` preparado para provenance por artefato;
- perfis LIGHT / STANDARD / DEEP;
- packs Android, Python, backend, AI, sensitive-data e multi-agent;
- bundles `standard-android-ai` e `deep-multi-agent-sensitive`;
- workflows `default` e `migration-first`;
- catálogo de adapters com `generic=ACTIVE` e adapters específicos ainda `PLANNED`;
- política `MANAGED / MERGEABLE / USER_OWNED`;
- `docs/LIFECYCLE_MODEL.md` e `docs/OWNERSHIP_AND_UPGRADE.md`;
- exemplos positivos e fixtures adversariais;
- `VALIDATION_CONTRACT.md`;
- `scripts/validate_standard.py` + testes unitários;
- `REFERENCE_MATRIX.md` com padrões adotados/adaptados;
- roadmap S0–S8.

## Decisões vigentes

- Ideias Standard é lifecycle manager, não apenas scaffold.
- Profiles definem profundidade; packs definem capacidades.
- Bundle é conveniência versionada e nunca amplia autoridade.
- Workflow organiza sequência/gates sem substituir política canônica.
- Contrato canônico é independente de agente/provider.
- Projetos precisam poder adotar e atualizar o Standard sem recriação.
- Upgrade usa preview, provenance, three-way diff e ownership; nunca overwrite implícito.
- Brownfield/adopt é caso de primeira classe.
- Contexto usa carregamento progressivo e nunca trunca obrigação crítica silenciosamente.
- Change unit futura usa delta + invariantes em vez de contexto global.
- Conformance vem antes do gerador completo.

## Próxima ação

Em ambiente com checkout do repositório:

```bash
python -m pip install -r requirements-dev.txt
python -m unittest scripts.test_validate_standard -v
python scripts/validate_standard.py examples/standard-android-ai/project-manifest.json
```

Somente após execução real e correção dos findings registrar Gate S0 como satisfeito e iniciar S1 (`check`/`doctor`).
