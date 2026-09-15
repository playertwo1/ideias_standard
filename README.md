# Ideias Standard

**Ideias Standard** é um padrão executável, versionado e atualizável para criar, validar, adotar, manter e evoluir projetos preparados para trabalhar com agentes de IA.

Ele não é apenas um template, não é um repositório de prompts e não é um framework preso a um agente específico. Seu papel é fornecer um **contrato operacional comum para o ciclo de vida de projetos**, com governança proporcional ao risco, contexto mínimo suficiente, evidência verificável, versionamento, ownership de artefatos e evolução segura.

> Regra central: **correção → integridade → autoridade → evidência → eficiência**.

---

## 1. Por que este projeto existe

Projetos desenvolvidos com ajuda de IA tendem a acumular alguns problemas recorrentes:

- agentes diferentes interpretam o mesmo projeto de maneiras diferentes;
- documentação e estado operacional se contradizem;
- arquivos como `AGENTS.md`, `README.md` e roadmaps crescem até virar depósitos de contexto;
- cada nova sessão de IA relê informação demais ou perde regras críticas;
- sugestões de IA podem ser confundidas com decisões aprovadas;
- projetos antigos precisam ser modernizados sem perder conteúdo local;
- templates tradicionais ajudam no nascimento do projeto, mas pouco ajudam em upgrades futuros;
- auditoria, gates e evidências frequentemente são declarados sem prova reproduzível;
- mudanças pequenas acabam carregando o contexto do projeto inteiro;
- trocar Codex, Claude, Gemini ou outro agente pode exigir reconstruir manualmente instruções e processos.

O Ideias Standard existe para atacar esses problemas de forma estruturada.

Ele procura garantir que um projeto consiga responder, de forma inequívoca:

1. **O que é este projeto?**
2. **Qual é seu escopo?**
3. **Onde estamos agora?**
4. **O que está autorizado neste momento?**
5. **Quem pode decidir o quê?**
6. **Quais regras nunca podem ser violadas?**
7. **Que contexto uma IA realmente precisa para esta tarefa?**
8. **Como sabemos que uma mudança está correta?**
9. **Como um projeto antigo pode adotar o padrão sem ser sobrescrito?**
10. **Como atualizar o Standard no futuro sem perder customizações locais?**

---

## 2. Visão do ecossistema

O fluxo conceitual é:

```text
IDEA / PRODUCT AUTHORITY
        │
        ▼
Project Manifest
        │
        ▼
IDEIAS STANDARD
  ├── Base
  ├── Profile
  ├── Packs
  ├── Bundles
  ├── Workflows
  ├── Invariants
  └── Project Rules
        │
        ▼
Projeto operacional
        │
        ├── validate
        ├── check / doctor        [planejado]
        ├── init                  [planejado]
        ├── adopt                 [planejado]
        ├── upgrade               [planejado]
        └── compile-context       [planejado]
```

O projeto **Idea** decide *o que um projeto precisa*.

O **Ideias Standard** define *como esse projeto deve nascer, ser validado, operado e evoluir*.

O **projeto gerenciado** recebe apenas o necessário para seu próprio contexto. Ele não herda toda a documentação interna do Idea nem do Ideias Standard.

---

## 3. O que o Ideias Standard é — e o que não é

### É

- um **lifecycle manager** para projetos;
- um contrato versionado de governança e conformance;
- uma base para geração futura de projetos;
- um padrão para projetos novos e existentes;
- um sistema de composição de profiles, packs, workflows e regras específicas;
- uma forma de reduzir contexto desperdiçado sem remover contexto crítico;
- uma fundação para interoperar com múltiplos agentes de IA;
- uma forma de tornar decisões, gates, evidências e upgrades verificáveis.

### Não é

- uma coleção de arquivos Markdown a serem copiados cegamente;
- um substituto para decisões humanas de produto;
- uma autorização para a IA promover sugestões a decisões LOCKED;
- uma exigência de burocracia máxima para todo projeto;
- um framework exclusivo de Codex, Claude, Gemini ou qualquer fornecedor;
- um compilador de contexto completo ainda — isso está planejado para fases posteriores;
- uma CLI completa ainda — a fundação de validação existe, mas `init/check/doctor/adopt/upgrade` ainda não foram implementados como interface estável.

---

## 4. Contrato de composição

A fórmula central do Standard é:

```text
BASE + PROFILE + PACKS + PROJECT RULES = PROJECT CONTRACT
```

### BASE

Regras universais que todos os projetos gerenciados devem respeitar, independentemente da linguagem, stack ou agente usado.

Exemplos:

- `NOT_RUN != PASS`;
- evidência antes de declarar conclusão;
- autoridade humana preservada;
- contexto REQUIRED nunca truncado silenciosamente;
- mudanças devem respeitar ownership e provenance;
- bundles/workflows/adapters não podem ampliar autoridade.

### PROFILE

Define a **profundidade de governança**.

O Standard possui três perfis iniciais:

#### LIGHT

Para projetos pequenos, experimentos controlados e ferramentas de baixo risco.

Objetivo: preservar as regras essenciais sem criar processo maior que o problema.

#### STANDARD

Perfil recomendado para a maioria dos aplicativos e projetos normais.

Inclui estado operacional, validação, contexto progressivo, evidência e governança proporcional.

#### DEEP

Para projetos amplos, sensíveis, críticos ou com múltiplos agentes.

Acrescenta controles mais rigorosos de auditoria, gates, segurança, dados, lifecycle e evidência.

> **Profile define profundidade. Pack define capacidade.**
>
> Selecionar `DEEP` não ativa automaticamente todos os packs.

---

## 5. Packs

Packs adicionam capacidades e regras específicas sem transformar os profiles em blocos monolíticos.

Packs iniciais:

```text
android
python
backend
ai
sensitive-data
multi-agent
```

Um projeto pode, por exemplo, ser:

```text
STANDARD + android + ai
```

ou:

```text
DEEP + android + sensitive-data + multi-agent
```

Cada pack deve declarar de maneira verificável:

- capacidades adicionadas;
- regras adicionais;
- requisitos;
- incompatibilidades ou conflitos;
- impacto de governança quando aplicável.

Packs não substituem regras do projeto e não podem enfraquecer invariantes superiores.

---

## 6. Bundles

Bundles são composições reutilizáveis e versionadas de:

```text
profile + packs + workflow + adapters
```

Eles servem para evitar reconstruir combinações recorrentes.

Exemplos atuais incluem bundles para cenários como Android + IA e projetos DEEP multiagente/sensíveis.

Um bundle:

- não é uma nova fonte de verdade;
- deve ser expandível para sua composição explícita;
- não pode ampliar autoridade;
- não pode remover gates exigidos por risco;
- deve manter provenance;
- só pode usar adapters compatíveis com a versão corrente.

Contrato estruturado: `schemas/bundle.schema.json`.

---

## 7. Workflows

Workflows descrevem **sequências operacionais**, artefatos e gates para classes diferentes de trabalho.

Exemplos materializados:

- `default`;
- `migration-first`;
- `builder-auditor-loop`.

O `builder-auditor-loop` sustenta o Operational Orchestrator: ele elimina a Product Authority como mensageiro manual no fluxo normal, transportando estado, relatórios, findings e SHAs entre Builder e Auditor. A Product Authority volta ao fluxo somente quando uma decisão, bloqueio ou gate humano exige sua autoridade.

```text
Builder → Orchestrator → Auditor → Orchestrator → Builder ou Product Authority
```

Um workflow organiza execução, mas não cria autoridade nova.

Ele nunca pode:

- transformar `NOT_RUN` em `PASS`;
- aprovar um gate humano automaticamente;
- ignorar um invariant;
- remover controle de segurança exigido;
- substituir decisão LOCKED.

Contrato estruturado: `schemas/workflow.schema.json`.

---

## 8. Ownership de artefatos

Um dos problemas mais importantes em scaffolding tradicional é saber **quem é dono de cada arquivo depois que o projeto evolui**.

O Ideias Standard formaliza três classes:

### `MANAGED`

Arquivo derivado do Standard.

Mudanças locais podem representar drift. Mesmo assim, upgrade não deve sobrescrevê-lo silenciosamente: precisa haver preview e validação.

### `MERGEABLE`

Arquivo que combina baseline do Standard com customização legítima do projeto.

Upgrade deve usar comparação entre:

```text
baseline anterior × estado local × versão alvo
```

### `USER_OWNED`

Arquivo pertencente ao projeto.

O Standard pode validar, alertar ou recomendar mudanças, mas **não pode sobrescrevê-lo automaticamente**.

A política detalhada está em:

- `docs/OWNERSHIP_AND_UPGRADE.md`;
- `schemas/artifact-policy.schema.json`;
- `.idea-standard/standard.lock` nos projetos gerenciados.

---

## 9. Provenance e `standard.lock`

Projetos gerenciados precisam saber **de onde veio cada artefato e contra qual versão do Standard foram materializados**.

O lock é projetado para registrar informações como:

- versão do Standard;
- profile;
- packs;
- bundle/workflow quando aplicável;
- origem do artefato;
- fingerprint;
- overrides conhecidos;
- ownership;
- provenance suficiente para upgrades futuros.

O lock não é mero metadata decorativo. Ele é peça central do lifecycle de upgrade.

Regra importante:

> O lock só deve avançar depois de uma materialização/upgrade validado.

---

## 10. Manifests e contratos estruturados

O Standard evita depender apenas de Markdown para regras que precisam ser verificadas por máquina.

Principais contratos:

### `project-manifest.json`

Declara a intenção operacional do projeto:

- identificação;
- profile;
- packs;
- capacidades;
- governança;
- contexto;
- parâmetros necessários ao Standard.

Schema: `schemas/project-manifest.schema.json`.

### `.idea-standard/standard.lock`

Declara o estado efetivamente materializado e sua provenance.

Schema: `schemas/standard-lock.schema.json`.

### `context-manifest.json`

Declara como contexto deve ser roteado e classificado.

Schema: `schemas/context-manifest.schema.json`.

### `change`

Representa uma unidade de mudança — feature, correção, migração etc. — sem precisar reprocessar o projeto inteiro.

Schema: `schemas/change.schema.json`.

### `conformance-report`

Estrutura saída determinística de validação.

Schema: `schemas/conformance-report.schema.json`.

### Contratos de orquestração

- `orchestration-policy`: papéis, limites e autoridade do loop;
- `orchestrator-state`: estado persistido, rodada, SHAs e `run_id`;
- `builder-report`: resultado e evidência produzidos pelo Builder;
- `audit-report`: resultado, checks e findings produzidos pelo Auditor.

Schemas: `schemas/orchestration-policy.schema.json`, `schemas/orchestrator-state.schema.json`, `schemas/builder-report.schema.json` e `schemas/audit-report.schema.json`.

Outros schemas cobrem invariants, artifact policies, bundles e workflows.

> Markdown explica. Contratos estruturados tornam o comportamento verificável.

---

## 11. Invariantes

Regras críticas não devem existir apenas como prosa espalhada em documentos.

`INVARIANTS.yaml` funciona como registry estruturado de regras que precisam permanecer estáveis e auditáveis.

Entre os invariantes atuais:

- `NOT_RUN != PASS`;
- `USER_OWNED` nunca sofre overwrite automático;
- contexto `REQUIRED` nunca é truncado silenciosamente;
- `sensitive-data` exige human gate;
- `multi-agent` exige auditoria independente;
- Builder e Auditor devem ser distintos em contexto multiagente;
- bundle/workflow/adapter nunca amplia autoridade;
- existência de arquivo não substitui evidência executada.

Esses invariantes são alvo direto de fixtures adversariais e validação semântica.

---

## 12. Context engineering

O princípio central de contexto é:

> **Minimum Sufficient Context — menor contexto suficiente para executar corretamente.**

Não significa “usar o mínimo de tokens possível”. Significa evitar tanto contexto irrelevante quanto omissão de obrigação crítica.

O modelo inicial usa três classes:

### `REQUIRED`

Contexto obrigatório para a tarefa.

Nunca pode ser removido ou truncado silenciosamente por orçamento.

### `CONDITIONAL`

Carregado somente quando um gatilho concreto exige.

Exemplo: segurança, migração, auditoria, persistência ou arquitetura.

### `DISCOVERY`

Usado para localizar informação adicional quando necessário.

O lifecycle futuro de contexto inclui:

- progressive disclosure;
- `why-included` / `why-excluded`;
- fingerprints por bloco;
- delta-context;
- limitação de saída por bytes;
- budgets;
- `CONTEXT_OVERFLOW` quando contexto crítico não cabe;
- métricas de critical recall e irrelevant context.

A implementação completa do Context Compiler está planejada para uma fase posterior do roadmap.

---

## 13. Governança e autoridade

Precedência recomendada nos projetos gerenciados:

```text
invariantes de segurança
        ↓
pedido vigente da Product Authority
        ↓
decisões LOCKED
        ↓
contrato específico do projeto
        ↓
Standard aplicável
        ↓
estado operacional
        ↓
julgamento técnico
```

Papéis conceituais:

### Product Authority

Pessoa ou autoridade responsável por decisões de produto, mudanças de escopo, decisões LOCKED e gates humanos.

### Builder

Agente ou pessoa que implementa mudanças dentro do escopo autorizado.

### Auditor

Revisor independente quando exigido pelo risco/profile/pack. Não deve simplesmente reproduzir a conclusão do Builder.

O Standard nunca promove automaticamente uma sugestão de IA para uma decisão humana.

---

## 14. Conformance first

Uma decisão importante deste projeto foi **aprender a validar antes de aprender a gerar**.

Antes de implementar uma CLI completa de scaffolding, o Standard precisa ser capaz de determinar se um contrato está correto.

A validação atual separa:

1. parse;
2. JSON Schema;
3. regras semânticas entre documentos/catálogos;
4. invariants;
5. relatório estruturado e códigos determinísticos.

Estados reconhecidos:

```text
NOT_RUN
PASS
FAIL
WARN
NOT_APPLICABLE
```

Regra permanente:

```text
NOT_RUN != PASS
```

O contrato dos códigos de validação está em `VALIDATION_CONTRACT.md`.

---

## 15. Validador atual

A fundação executável já existe em:

```text
scripts/validate_standard.py
```

Ela valida estrutura e semântica e também consegue realizar self-check de partes do próprio Standard.

Fixtures positivas e adversariais vivem em:

```text
fixtures/
```

O manifesto central de casos esperados está em:

```text
fixtures/fixture-manifest.yaml
```

Golden outputs garantem que comportamentos críticos não mudem silenciosamente entre versões.

---

## 16. Como validar localmente

Requisitos de desenvolvimento estão em `requirements-dev.txt`.

Execução de referência:

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate_standard.py examples/standard-android-ai/project-manifest.json
python -m unittest scripts.test_validate_standard -v
```

A CI também executa a suíte de conformance em múltiplas versões suportadas de Python por meio de:

```text
.github/workflows/conformance.yml
```

Evidência da fundação S0 está registrada em:

```text
S0_VALIDATION_EVIDENCE.md
```

---

## 17. Lifecycle planejado

### Novo projeto

Fluxo alvo:

```text
manifest
  → validate
  → dry-run
  → diff
  → materialize
  → validate
  → lock
```

A escrita em disco deve ocorrer somente depois de uma composição válida e, quando aplicável, preview.

### Projeto existente / brownfield

Fluxo alvo:

```text
inventory read-only
  → recommend profile/packs
  → gap analysis
  → map equivalences
  → preview
  → adopt
  → validate
  → lock
```

Regra inicial de segurança:

> Arquivo já existente deve ser tratado como `USER_OWNED` por padrão até ownership ser aceito explicitamente.

### Upgrade

Fluxo alvo:

```text
check
  → render target
  → three-way diff
  → classify conflicts
  → preview
  → apply
  → validate
  → update lock
```

Conflito nunca vira overwrite implícito.

### Change lifecycle

Mudanças pequenas não devem exigir reconstrução ou leitura global do projeto.

Fluxo conceitual:

```text
change unit
  → delta de requisitos/decisões
  → contexto mínimo + invariantes
  → implementação
  → validação proporcional
  → auditoria/gate quando aplicável
  → fechamento
```

---

## 18. Adapters e independência de agente

O contrato canônico do projeto **não é** `AGENTS.md`, `CLAUDE.md`, `GEMINI.md` nem arquivo equivalente de um fornecedor.

Esses arquivos são materializações/adapters.

Catálogo atual:

```text
generic  → ACTIVE
codex    → PLANNED
claude   → PLANNED
gemini   → PLANNED
```

Fonte: `adapters/catalog.yaml`.

Regras:

- adapter nunca é fonte canônica;
- divergência entre adapter e contrato canônico é finding de conformance;
- bundle só pode materializar adapters compatíveis/ativos na versão corrente.

Isso permite trocar agentes sem reconstruir a governança do projeto.

---

## 19. Relação com o projeto Idea

A separação de responsabilidades é deliberada.

### Idea

Responsável por transformar intenção humana em especificação coerente:

```text
Capture
→ Clarify
→ Decide
→ Cut
→ Specify
→ Plan
→ Export
```

O Idea pode, no futuro, produzir um `project-manifest` compatível com o Standard.

### Ideias Standard

Responsável por transformar o manifesto em um projeto operacional versionado e governado.

### Projeto final

Contém apenas:

- regras específicas do projeto;
- profile/packs aplicáveis;
- artefatos operacionais necessários;
- contratos e adapters realmente utilizados.

Ele não deve receber uma cópia integral da documentação do Idea ou do Ideias Standard.

---

## 20. Estrutura do repositório

Visão conceitual da organização atual:

```text
ideias_standard/
│
├── README.md
│   └── porta de entrada e mapa conceitual
│
├── STANDARD.md
│   └── contrato canônico do Standard
│
├── PROJECT_STATE.md
│   └── estado operacional atual
│
├── ROADMAP.md
│   └── evolução planejada S0–S8
│
├── AGENTS.md
│   └── regras de trabalho para agentes dentro deste repositório
│
├── INVARIANTS.yaml
│   └── registry estruturado de regras críticas
│
├── COMPATIBILITY.yaml
│   └── compatibilidade entre versão do Standard e contratos
│
├── VERSION
├── VERSIONING.md
├── CLI_CONTRACT.md
├── VALIDATION_CONTRACT.md
├── CHANGELOG.md
├── REFERENCE_MATRIX.md
│
├── schemas/
│   ├── project-manifest.schema.json
│   ├── standard-lock.schema.json
│   ├── context-manifest.schema.json
│   ├── artifact-policy.schema.json
│   ├── bundle.schema.json
│   ├── workflow.schema.json
│   ├── change.schema.json
│   ├── conformance-report.schema.json
│   ├── invariants.schema.json
│   ├── orchestration-policy.schema.json
│   ├── orchestrator-state.schema.json
│   ├── builder-report.schema.json
│   └── audit-report.schema.json
│
├── profiles/
│   ├── light/
│   ├── standard/
│   └── deep/
│
├── packs/
│   ├── android/
│   ├── python/
│   ├── backend/
│   ├── ai/
│   ├── sensitive-data/
│   └── multi-agent/
│
├── bundles/
│   ├── catalog.yaml
│   └── ...
│
├── workflows/
│   ├── default/
│   ├── migration-first/
│   └── builder-auditor-loop/
│
├── orchestration/
│   ├── builder-auditor-policy.json
│   └── o0-runner.example.json
│
├── adapters/
│   └── catalog.yaml
│
├── examples/
│   ├── light-python/
│   └── standard-android-ai/
│
├── fixtures/
│   ├── fixture-manifest.yaml
│   ├── valid/
│   ├── invalid/
│   └── golden/
│
├── scripts/
│   ├── validate_standard.py
│   ├── test_validate_standard.py
│   ├── orchestrate_handoffs.py
│   ├── o0_runner.py
│   ├── test_orchestrate_handoffs.py
│   └── test_o0_runner.py
│
├── docs/
│   ├── LIFECYCLE_MODEL.md
│   ├── OWNERSHIP_AND_UPGRADE.md
│   └── MULTI_AGENT_ORCHESTRATION.md
│
├── S0_VALIDATION_EVIDENCE.md
├── S0_AUDIT_PACKET.md
├── O0_VALIDATION_EVIDENCE.md
└── .github/workflows/conformance.yml
```

A árvore real pode evoluir. `STANDARD.md`, schemas e contratos estruturados têm precedência sobre esta representação resumida quando houver diferença.

---

## 21. Onde encontrar cada tipo de verdade

Para evitar duplicação e drift:

| Pergunta | Fonte principal |
|---|---|
| O que é o Standard e quais são suas regras? | `STANDARD.md` |
| Onde o projeto está agora? | `PROJECT_STATE.md` |
| O que será construído depois? | `ROADMAP.md` |
| Quais invariants são críticos? | `INVARIANTS.yaml` |
| Como versões se relacionam? | `COMPATIBILITY.yaml` e `VERSIONING.md` |
| Como a futura CLI deve se comportar? | `CLI_CONTRACT.md` |
| Quais códigos de validação existem? | `VALIDATION_CONTRACT.md` |
| Qual é o formato de cada contrato? | `schemas/` |
| Como ownership/upgrade funcionam? | `docs/OWNERSHIP_AND_UPGRADE.md` |
| Como o lifecycle funciona? | `docs/LIFECYCLE_MODEL.md` |
| Quais referências externas inspiraram decisões? | `REFERENCE_MATRIX.md` |
| Qual evidência existe para S0? | `S0_VALIDATION_EVIDENCE.md` |
| Como auditar S0? | `S0_AUDIT_PACKET.md` |
| Como funciona o Orchestrator? | `docs/MULTI_AGENT_ORCHESTRATION.md` |
| Quais são a policy e configuração do runner? | `orchestration/` |
| Qual evidência existe para O0? | `O0_VALIDATION_EVIDENCE.md` e `PROJECT_STATE.md` |

Este README explica e roteia. Ele não deve substituir essas fontes canônicas.

---

## 22. Estado atual do projeto

Versão atual:

```text
0.1.0-draft
```

Fase atual:

```text
S1 — Conformance First
```

Estado operacional:

```text
O0 — Operational Orchestrator: PARTIAL
Gate S1 = NOT_RUN
S2 = NOT_STARTED
```

O Operational Orchestrator coordena o loop e atua como mensageiro operacional entre os papéis. Builder e Auditor não são implementações presas a fornecedor: são comandos externos configuráveis, iniciados pelo runner dentro das fronteiras e contratos do Standard.

As funções O0 implementadas e aprovadas por auditoria independente até O0-C29 são:

- carregar o estado, identificar e iniciar o próximo Builder ou Auditor autorizado (O0-C01–C04);
- separar workspaces e restringir escrita do Auditor sobre o alvo (O0-C05–C07);
- validar relatórios, propagar e congelar o SHA exato para auditoria independente (O0-C08–C13);
- exigir novo SHA e nova auditoria após correção, parando após PASS para a Product Authority (O0-C16–C18);
- bloquear resultados `ESCALATE` ou `DISPUTED` (O0-C19–C20);
- limitar auditorias a três rodadas e persistir estado entre reinícios/interrupções (O0-C21–C23);
- rejeitar JSON inválido, SHA inválido/inexistente, divergência de SHA e PASS com finding bloqueante (O0-C24–C27);
- impedir registro automático de gate humano e avanço automático de fase (O0-C28–C29).

O0-C30, que adiciona `run_id` persistido, está implementado e aguarda auditoria independente. O0 **não está concluído**. Critérios não listados acima permanecem pendentes conforme o `ROADMAP.md`; nenhuma dessas auditorias registra Gate S1 ou PASS de produto.

Fonte de verdade operacional: `PROJECT_STATE.md`.

---

## 23. Roadmap resumido

### S0 — Fundação

Contrato, schemas, profiles, packs, bundles, workflows, invariants, conformance, fixtures, validador e CI.

**Status atual:** fechado com auditoria independente e gate registrados.

### O0 — Operational Orchestrator

Runner provider-neutral para coordenar Builder, Auditor, estado, handoffs, findings, SHAs, limites e paradas humanas.

**Status atual:** parcial e prioritário; O0-C30 implementado, aguardando auditoria independente.

### S1 — Conformance first

Transformar a fundação em interface estável de `check` e `doctor`.

**Status atual:** ativo; Gate S1 = `NOT_RUN`.

### S2 — Init / compiler

Gerar projetos deterministicamente a partir de manifests.

### S3 — Adopt / brownfield

Trazer projetos existentes para o Standard com inventário, gap analysis e preview seguro.

### S4 — Upgrade lifecycle

Atualizar projetos gerenciados preservando customizações e ownership.

### S5 — Context lifecycle

Compilar contexto mínimo verificável por tarefa.

### S6 — Ecosystem adapters / workflows / bundles

Materializar integrações para múltiplos agentes sem criar fontes concorrentes.

### S7 — Integração com Idea

Permitir que o Idea produza manifests consumíveis diretamente pelo Standard.

### S8 — Change lifecycle

Tratar evolução de features por delta, sem reprocessar todo o projeto.

Detalhes, critérios e gates: `ROADMAP.md`.

---

## 24. O que já existe versus o que ainda é planejado

### Materializado hoje

- contrato canônico;
- profiles LIGHT/STANDARD/DEEP;
- packs iniciais;
- bundles e workflows declarativos;
- adapters catalogados;
- schemas estruturados;
- registry de invariants;
- ownership/provenance model;
- compatibility/versioning contract;
- CLI contract futuro;
- validation contract;
- fixtures positivas/adversariais;
- golden outputs;
- validador estrutural + semântico;
- self-check;
- testes data-driven;
- CI multi-Python;
- evidência S0;
- pacote de auditoria S0.
- workflow, policy e configuração de exemplo do Operational Orchestrator;
- máquina de estados e runner provider-neutral;
- contratos estruturados de policy, estado, Builder e Auditor;
- testes de handoff, isolamento, persistência, limites e rejeições adversariais;
- evidência operacional O0.

### Ainda não implementado como produto completo

- CLI estável de `check`;
- `doctor`;
- `init` / compiler;
- `adopt` automatizado;
- `upgrade` automatizado;
- Context Compiler completo;
- adapters específicos ativos para Codex/Claude/Gemini;
- integração ponta a ponta com Idea;
- change lifecycle automatizado.

Não confundir documentação/contrato de uma fase futura com funcionalidade já implementada.

---

## 25. Como uma IA deve entrar neste repositório

Se você é um agente de IA entrando no projeto pela primeira vez, **não faça uma leitura global automática do repositório**.

Comece nesta ordem:

```text
1. AGENTS.md
2. PROJECT_STATE.md
3. pedido atual da Product Authority
```

Depois expanda somente o contexto necessário. Use `README.md` para visão geral e `STANDARD.md` quando o contrato canônico for necessário à tarefa.

### Se a tarefa for validação/conformance

Leia:

```text
VALIDATION_CONTRACT.md
INVARIANTS.yaml
COMPATIBILITY.yaml
schemas relevantes
fixtures relevantes
scripts/validate_standard.py
```

### Se a tarefa for planejamento de próxima fase

Leia:

```text
ROADMAP.md
PROJECT_STATE.md
contratos específicos daquela fase
```

### Se a tarefa envolver o Operational Orchestrator

Leia somente o subconjunto necessário de:

```text
docs/MULTI_AGENT_ORCHESTRATION.md
orchestration/
schemas/orchestration-policy.schema.json
schemas/orchestrator-state.schema.json
schemas/builder-report.schema.json
schemas/audit-report.schema.json
scripts/orchestrate_handoffs.py
scripts/o0_runner.py
```

### Se a tarefa envolver ownership/upgrade/adoption

Leia:

```text
docs/OWNERSHIP_AND_UPGRADE.md
docs/LIFECYCLE_MODEL.md
schemas/standard-lock.schema.json
schemas/artifact-policy.schema.json
```

### Se a tarefa for auditoria S0

Use:

```text
S0_AUDIT_PACKET.md
S0_VALIDATION_EVIDENCE.md
```

Não declare uma fase concluída apenas porque seus artefatos existem.

---

## 26. Regras rápidas para agentes

Ao trabalhar neste repositório:

1. Não invente evidência.
2. Não transforme `NOT_RUN` em `PASS`.
3. Não avance fase para compensar contrato incompleto da fase atual.
4. Não trate adapters como fonte canônica.
5. Não amplie autoridade através de bundle, workflow ou pack.
6. Não remova human gate exigido por risco.
7. Não sobrescreva `USER_OWNED` automaticamente.
8. Não silencie conflito em upgrade.
9. Não trunque contexto `REQUIRED` para cumprir orçamento.
10. Não confunda documentação de funcionalidade futura com implementação atual.
11. Prefira contexto progressivo a leitura global.
12. Faça mudanças proporcionais ao risco e ao escopo.
13. Preserve provenance e compatibilidade.
14. Execute validação antes de declarar sucesso.
15. Consulte `PROJECT_STATE.md` antes de decidir qual fase está ativa.

---

## 27. Princípios finais

O Ideias Standard foi desenhado em torno de algumas ideias simples:

> **Um projeto preparado para IA precisa ser compreensível sem depender da memória de uma conversa.**

> **Governança deve crescer com risco, não com entusiasmo por documentação.**

> **O melhor contexto não é o menor possível; é o menor suficiente.**

> **Templates criam projetos. Lifecycle managers mantêm projetos vivos.**

> **A IA pode interpretar, sugerir, construir e auditar; autoridade continua explícita.**

> **Evidência executada vale mais que alegação documental.**

---

## 28. Próxima ação oficial

A próxima ação autorizável em O0 é:

```text
Auditoria independente de O0-C30 — Estado persistido inclui run_id
```

O0 não deve ser declarado concluído, O0-C31 não deve iniciar sem autorização e S2 permanece não iniciada.

Para estado atualizado, consulte sempre `PROJECT_STATE.md`.
