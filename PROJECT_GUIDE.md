# PROJECT GUIDE — IDEIAS STANDARD

## 1. Quick Start

Se você acabou de chegar ao projeto:

1. Leia `PROJECT_STATE.md`.
2. Leia a solicitação atual.
3. Leia somente a fase relevante do `ROADMAP.md`.
4. Consulte `AGENTS.md`.
5. Abra contratos, schemas e arquivos diretamente necessários.
6. Use este guia apenas se precisar entender arquitetura, contexto ou histórico.

Não faça leitura global do repositório por padrão.

---

## 2. Finalidade

Este documento é o guia de onboarding do Ideias Standard.

Ele explica:

- o que é o projeto;
- por que existe;
- como suas partes se relacionam;
- como autoridade e agentes funcionam;
- como retomar o trabalho sem depender de conversas antigas.

Este arquivo é explicativo.

Não é fonte canônica de estado ou regras operacionais.

---

## 3. Fontes de verdade

- `PROJECT_STATE.md` → onde estamos agora
- `ROADMAP.md` → fases, checklists e gates
- `STANDARD.md` → regras canônicas
- `AGENTS.md` → comportamento dos agentes
- `schemas/` → contratos estruturados
- `fixtures/` + `tests/` → evidência de comportamento
- `PROJECT_GUIDE.md` → explicação e onboarding

Se este guia divergir de uma fonte canônica atual, a fonte canônica prevalece.

---

## 4. O que é o Ideias Standard

O Ideias Standard é um padrão executável, versionado e atualizável para projetos desenvolvidos com agentes de IA.

Ele organiza como um projeto:

nasce → recebe regras → é implementado → é validado → é auditado → é atualizado → evolui

Sua composição central é:

BASE + PROFILE + PACKS + PROJECT RULES = PROJECT CONTRACT

Profiles definem profundidade de governança:

- LIGHT
- STANDARD
- DEEP

Packs adicionam capacidades específicas.

---

## 5. O que o projeto não é

O Ideias Standard não é:

- o aplicativo Idea;
- um agente de IA;
- um runner exclusivo do Codex;
- um transcript permanente das conversas;
- uma substituição da Product Authority;
- um sistema que decide produto autonomamente.

Ele define contratos e lifecycle.

Os agentes executam esses contratos.

---

## 6. Problema que resolve

Projetos conduzidos por agentes de IA podem sofrer com:

- contexto excessivo;
- decisões esquecidas;
- escopo alterado silenciosamente;
- instruções divergentes;
- Builder validando o próprio trabalho;
- auditoria de commit incorreto;
- repetição de documentação;
- desperdício de tokens;
- avanço prematuro de fases;
- dificuldade de retomada;
- dependência de um fornecedor específico.

O Standard combate isso com:

contratos + estado explícito + autoridade + evidência + automação controlada

---

## 7. Princípios

Prioridade:

correção → integridade → autoridade → evidência → economia de contexto/tokens → velocidade

Regras essenciais:

- `NOT_RUN != PASS`;
- PASS pertence ao SHA auditado;
- automação não amplia autoridade;
- decisão `LOCKED` exige autoridade adequada;
- fase futura não corrige deficiência da atual;
- contexto deve ser mínimo, mas suficiente;
- fornecedor de IA nunca é fonte canônica;
- evidência vale mais que suposição.

---

## 8. Minimum Sufficient Context

Agentes devem começar pelo menor contexto suficiente.

Padrão inicial:

estado atual + tarefa atual + regras aplicáveis + arquivos necessários

Após a primeira rodada:

delta + findings pendentes + dependências diretas + invariantes aplicáveis

Priorizar:

- IDs;
- schemas;
- diffs;
- fingerprints;
- evidência existente;
- resultados estruturados.

Evitar:

- transcript completo;
- leitura global sem necessidade;
- releitura redundante;
- narrativa quando dados estruturados forem suficientes.

Objetivo:

minimizar contexto sem perder obrigação crítica

---

## 9. Ownership

Artefatos podem ser:

- MANAGED
- MERGEABLE
- USER_OWNED

`USER_OWNED` não deve ser sobrescrito automaticamente.

Ownership protege customizações durante:

- geração;
- adoção;
- upgrade.

---

## 10. Autoridade e papéis

### Product Authority

Controla:

- decisões materiais;
- escopo;
- alterações `LOCKED`;
- gates humanos;
- conflitos sem solução objetiva.

### Builder

Implementa trabalho autorizado.

Pode:

- alterar arquivos;
- executar testes;
- corrigir findings;
- produzir commits;
- registrar evidências.

Não aprova formalmente o próprio gate.

### Auditor

Verifica o trabalho de forma independente.

Audita um SHA específico e retorna:

- PASS
- FAIL
- ESCALATE

Não corrige o alvo enquanto audita.

### Orchestrator

Coordena o transporte de:

- estado;
- SHAs;
- findings;
- evidência;
- contexto mínimo.

Ele decide:

> Quem age agora?

Ele não decide:

> Qual decisão de produto tomar?

---

## 11. Orquestração Builder ↔ Auditor

Fluxo pretendido:

Builder → Orchestrator → Auditor → Orchestrator → Builder ou Product Authority

Fluxo principal:

Builder → commit → `audit_target_sha` → Auditor

Se houver FAIL:

FAIL → FIX_REQUIRED → Builder → novo SHA → nova auditoria

Se houver PASS:

PASS → WAITING_PRODUCT_AUTHORITY

Se houver conflito ou necessidade humana:

ESCALATE / DISPUTED → BLOCKED → Product Authority

PASS nunca migra automaticamente para outro SHA.

---

## 12. Loop e retomada

O ciclo automático deve ser limitado.

Valor inicial:

`max_audit_rounds = 3`

Ao exceder:

BLOCKED → Product Authority

Processos longos devem persistir estado suficiente para retomar após interrupção.

Não depender apenas da memória de uma conversa.

Persistir, quando aplicável:

- run;
- tarefa;
- estado;
- SHAs;
- rodada;
- próximo ator;
- motivo de bloqueio.

---

## 13. Provider Neutrality

Arquitetura:

STANDARD → ORCHESTRATOR → RUNNER / ADAPTER → PROVIDER

Codex pode ser o primeiro runner operacional.

Depois podem existir Claude, Gemini ou outros.

Trocar provider não pode alterar:

- autoridade;
- invariantes;
- gates;
- ownership;
- significado dos handoffs.

---

## 14. Relação com o Idea

O Idea ajuda a definir:

> O que construir.

O Ideias Standard define:

> Como o projeto será estruturado, governado, validado e mantido.

Fluxo futuro:

Pessoa → Idea → project-manifest → Ideias Standard → Project Contract → execução

O objetivo é transferir estado estruturado, não reproduzir a conversa inteira.

---

## 15. Visão das fases

Detalhes completos ficam no `ROADMAP.md`.

- S0 — Foundation → contratos e fundação
- O0 — Operational Orchestrator → automação Builder ↔ Auditor
- S1 — Conformance First → check / doctor / findings / CLI
- S2 — Init / Compiler → geração de projetos
- S3 — Adopt / Brownfield → adoção de projetos existentes
- S4 — Upgrade Lifecycle → atualização segura
- S5 — Context Lifecycle → Minimum Sufficient Context formal
- S6 — Multi-provider Ecosystem → runners e adapters estáveis
- S7 — Idea Integration → Idea → Standard
- S8 — Change Lifecycle → evolução por delta

Para saber a fase atualmente ativa, consulte sempre `PROJECT_STATE.md`.

---

## 16. Dogfooding

O Standard deve usar suas próprias capacidades assim que forem confiáveis.

Direção:

- Orchestrator → opera o próprio Standard
- Context Lifecycle → gera contexto do próprio Standard
- Change Lifecycle → mudanças do próprio Standard usam change units

Capacidades maduras devem ser provadas internamente antes de generalização ampla.

---

## 17. Como retomar o projeto

Após uma pausa longa:

1. Leia `PROJECT_STATE.md`.
2. Identifique fase ativa e prioridades.
3. Confira o último gate relevante.
4. Abra somente o checklist correspondente no `ROADMAP.md`.
5. Identifique o primeiro item pendente autorizado.
6. Consulte contratos necessários.
7. Use este guia apenas para contexto conceitual.

Não reconstruir o projeto a partir de chats antigos quando o estado versionado for suficiente.

---

## 18. Quando parar e escalar

Parar quando houver:

- nova decisão de produto;
- mudança material de escopo;
- conflito com `LOCKED`;
- operação destrutiva não autorizada;
- finding disputado sem solução objetiva;
- risco relevante de segurança;
- limite de ciclos;
- evidência insuficiente;
- ambiguidade material.

Resultado:

BLOCKED → Product Authority

Não preencher lacuna material por suposição.

---

## 19. Visão final

- IDEA → define o projeto
- IDEIAS STANDARD → define contrato e lifecycle
- CONTEXT SYSTEM → entrega contexto mínimo
- ORCHESTRATOR → coordena handoffs
- BUILDER → implementa
- AUDITOR → verifica independentemente
- RUNNERS / ADAPTERS → conectam diferentes IAs
- PRODUCT AUTHORITY → mantém decisões materiais e gates

### Regras finais

> Automatizar o transporte do trabalho, não a autoridade.

> Usar o mínimo de contexto possível preservando todas as obrigações críticas.

> PASS pertence ao SHA auditado.

> Evidência substitui suposição.

> Se o contrato não puder decidir legitimamente, bloquear e escalar.
