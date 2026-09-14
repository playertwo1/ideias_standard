# IDEIAS STANDARD — PROJECT STATE

- **Versão:** 0.1.0-draft
- **Fase:** S0 — Fundação do padrão
- **Status:** EM_ANDAMENTO
- **Objetivo atual:** definir contratos estruturados, perfis, packs e lifecycle antes da CLI
- **Última concluída:** contrato canônico + bootstrap de agentes
- **Próxima:** schemas de manifest/lock/context + perfis/packs
- **Bloqueios:** nenhum conhecido
- **Implementação CLI:** NOT_RUN
- **Validação de fixtures:** NOT_RUN

## Decisões vigentes

- Ideias Standard é lifecycle manager, não apenas scaffold.
- Perfis: LIGHT / STANDARD / DEEP.
- Packs são composáveis e separados dos perfis.
- Contrato canônico é independente de agente/provider.
- Projetos precisam poder adotar e atualizar o Standard sem recriação.
- Contexto usa carregamento progressivo e nunca trunca obrigação crítica silenciosamente.

## Próxima ação

Materializar schemas, profiles, packs e fixtures mínimas; depois criar validador e primeira CLI `check` antes de `init` completo.
