# Ideias Standard — Contrato Canônico

Versão inicial: `0.1.0-draft`.

## 1. Missão

Padronizar como projetos preparados para agentes de IA nascem, são validados, evoluem e trocam contexto, sem acoplar o projeto a um agente, stack ou provedor específico.

O Standard é um **lifecycle manager**, não apenas um scaffold.

## 2. Autoridade

Precedência recomendada para projetos gerenciados:

`invariantes de segurança → pedido vigente da Product Authority → decisões LOCKED → contrato específico do projeto → Standard aplicável → estado operacional → julgamento técnico`

O Standard nunca transforma sugestão de IA em decisão humana nem amplia autoridade por bundle, workflow ou adapter.

## 3. Composição

`BASE + PROFILE + PACKS + PROJECT RULES = PROJECT CONTRACT`

### Profiles

- `LIGHT`: governança mínima proporcional ao risco.
- `STANDARD`: padrão para apps/features normais, com estado, evidência, auditoria proporcional e contexto progressivo.
- `DEEP`: controles adicionais para sistemas sensíveis, amplos, multiagente ou críticos.

Profile define **profundidade**. Pack define **capacidade**. Selecionar DEEP não ativa automaticamente todos os packs.

### Packs

Extensões composáveis como `android`, `python`, `backend`, `ai`, `sensitive-data` e `multi-agent`.

Packs precisam declarar capacidades, regras adicionadas e conflitos detectáveis antes da materialização.

## 4. Bundles

Bundles são composições versionadas de profile + packs + workflow + adapters.

Eles servem como conveniência reutilizável, não como nova fonte de verdade. Um bundle:

- não pode ampliar autoridade;
- não remove gate exigido por risco aplicável;
- precisa manter provenance;
- deve ser expandível para sua composição explícita.

Contrato: `schemas/bundle.schema.json`.

## 5. Workflows

Workflows organizam sequência, artefatos e gates para classes de trabalho, por exemplo fluxo padrão, migration-first ou Builder-Auditor.

Workflow não muda decisões humanas, não transforma `NOT_RUN` em `PASS` e não pode enfraquecer controles de segurança.

Contrato: `schemas/workflow.schema.json`.

## 6. Contratos estruturados

Arquivos principais:

- `project-manifest.json`: intenção operacional do projeto;
- `.idea-standard/standard.lock`: versão efetivamente materializada e provenance;
- `context-manifest.json`: roteamento de contexto;
- artifact policies: ownership e fingerprint por arquivo;
- bundle/workflow/change schemas;
- conformance report estruturado;
- handoffs Builder/Auditor e estado/policy de orquestração quando o pack `multi-agent` se aplica.

Markdown explica; contratos estruturados permitem validação determinística.

## 7. Ownership e provenance

Cada artefato gerenciado pertence a uma classe:

- `MANAGED`: derivado do Standard; alteração local é drift e nunca é sobrescrita sem preview.
- `MERGEABLE`: baseline do Standard + customização local legítima; upgrade usa diff/merge.
- `USER_OWNED`: pertence ao projeto; Standard pode validar/recomendar, mas não sobrescreve automaticamente.

`standard.lock` registra provenance suficiente para upgrades: origem, revisão, fingerprint, profile/pack e overrides conhecidos.

Nunca inferir permissão de overwrite pelo nome do arquivo.

## 8. Contexto

Regra central: **menor contexto suficiente para executar a tarefa corretamente**.

Classes:

- `REQUIRED`;
- `CONDITIONAL`;
- `DISCOVERY`.

Contexto cresce sob demanda. Saída potencialmente grande deve ser limitada inicialmente. Nenhuma obrigação crítica pode ser truncada silenciosamente por orçamento; overflow obrigatório gera `CONTEXT_OVERFLOW`.

O objetivo futuro é medir `critical recall`, redução de contexto e informação irrelevante, não perseguir economia de tokens às custas de correção.

## 9. Conformance first

Antes de gerar projetos, o Standard deve saber dizer se um contrato está correto.

Validação é separada em:

1. parse;
2. JSON Schema;
3. regras semânticas entre documentos/catálogos;
4. relatório com códigos determinísticos.

`VALIDATION_CONTRACT.md` define os códigos iniciais. `schemas/conformance-report.schema.json` define a saída estruturada.

Estados: `NOT_RUN`, `PASS`, `FAIL`, `WARN` e `NOT_APPLICABLE` com rationale. `NOT_RUN != PASS`.

## 10. Atualização

Projetos não precisam ser recriados para receber uma nova versão.

Fluxo alvo:

`check → render target → three-way diff (baseline/local/target) → classify conflicts → preview → apply → validate → update lock`

O lock só muda depois de validação. Conflito nunca vira overwrite implícito.

## 11. Adopt / brownfield

Projeto existente é caso de primeira classe.

`adopt` deve:

1. inventariar sem escrever;
2. recomendar profile/packs;
3. mapear equivalências;
4. tratar arquivos existentes como `USER_OWNED` por padrão;
5. propor baseline sintético apenas para artefatos aceitos;
6. mostrar preview/conflitos;
7. criar lock somente após adoção validada.

## 12. Change lifecycle

Mudanças de feature/correção não devem exigir reprocessar o projeto inteiro.

Uma change unit registra ID, tipo, status, rationale, paths/IDs afetados, acceptance e referências de contexto. O contexto da implementação deve ser composto pelo **delta da mudança + invariantes vigentes**, não por leitura global automática.

Contrato inicial: `schemas/change.schema.json`.

## 13. Independência de agente

O contrato canônico não é `AGENTS.md`, `CLAUDE.md` nem `GEMINI.md`.

Adapters são materializações. O catálogo pode conter adapters `ACTIVE` ou `PLANNED`; somente adapters ativos podem entrar em bundles materializados na versão corrente. Divergência entre adapter e contrato canônico é finding de conformance.

## 14. Orquestração multiagente

Quando o pack `multi-agent` estiver ativo, o Standard define limites de autoridade para Builder e Auditor sem exigir um executor específico.

Regras canônicas:

- Builder e Auditor são distintos;
- o resultado da auditoria identifica o commit verificado e vale somente para ele;
- Auditor independente não possui escrita no alvo auditado;
- findings devem ser verificáveis e encaminhados à correção quando aplicável;
- somente ação explícita da Product Authority pode registrar esse gate;
- automação externa não altera autoridade nem inicia a próxima fase sem autorização do contrato do projeto.

O ciclo executável, seus relatórios e schemas próprios pertencem ao projeto
[Runner](https://github.com/playertwo1/runner). O Standard mantém apenas a
governança provider-neutral.

## 15. Anti-burocracia

Mudança pequena não deve receber o mesmo ritual de projeto sensível. Profundidade cresce com risco, impacto e ambiguidade.

O Standard deve reduzir ambiguidade, drift e desperdício de contexto sem criar processo maior que o problema.

## 16. Regra final

**Correção → integridade → autoridade → evidência → eficiência.**

Dentro desses limites, minimizar leitura, contexto irrelevante, alterações amplas, validações redundantes e retrabalho.
