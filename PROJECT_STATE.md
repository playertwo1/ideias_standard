# IDEIAS STANDARD — PROJECT STATE

- **Versão:** 0.1.0-draft
- **Fase:** S0 — Fundação do padrão
- **Status:** EM_ANDAMENTO
- **Objetivo atual:** fechar fixtures negativas e validador determinístico antes da CLI
- **Última concluída:** schemas iniciais + perfis + packs + ownership/upgrade + pesquisa de referências
- **Próxima:** fixtures adversariais + validador `check`
- **Bloqueios:** nenhum conhecido
- **Implementação CLI:** NOT_RUN
- **Validação de fixtures:** PARCIAL — exemplos positivos existem; negativas ainda pendentes

## Materializado

- `STANDARD.md`
- schemas de project manifest, standard lock, context manifest e artifact policy
- perfis LIGHT / STANDARD / DEEP
- packs: Android, Python, backend, AI, sensitive-data e multi-agent
- `packs/catalog.yaml`
- política `MANAGED / MERGEABLE / USER_OWNED`
- exemplos LIGHT Python e STANDARD Android+AI
- `REFERENCE_MATRIX.md`
- roadmap S0–S8

## Decisões vigentes

- Ideias Standard é lifecycle manager, não apenas scaffold.
- Perfis definem profundidade; packs definem capacidades.
- Contrato canônico é independente de agente/provider.
- Projetos precisam poder adotar e atualizar o Standard sem recriação.
- Contexto usa carregamento progressivo e nunca trunca obrigação crítica silenciosamente.
- Upgrade usa preview/diff e ownership; nunca overwrite implícito.
- Brownfield/adopt é caso de primeira classe.
- Workflows/bundles/adapters futuros devem manter provenance e não ampliar autoridade.

## Próxima ação

Criar fixtures negativas/adversariais e um validador determinístico de schemas + regras semânticas. Depois iniciar S1 com `check`/`doctor` antes de implementar `init` completo.
