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

### Automação externa

A execução do ciclo Builder ↔ Auditor pertence ao [Runner](https://github.com/playertwo1/runner). O Standard mantém regras de autoridade e contratos de projeto independentes do executor.

---
## 11. Relação com o Idea

O Idea ajuda a definir:

> O que construir.

O Ideias Standard define:

> Como o projeto será estruturado, governado, validado e mantido.

Fluxo futuro:

Pessoa → Idea → project-manifest → Ideias Standard → Project Contract → execução

O objetivo é transferir estado estruturado, não reproduzir a conversa inteira.

---

## 12. Visão das fases

Detalhes operacionais ficam no `ROADMAP.md`; o estado atual fica no
`PROJECT_STATE.md`.

- F0 — Golden Standard → Core, validação, Skills provadas e dogfooding
- F1 — Create → criação simples de projetos Gold
- F2 — Check + Audit → verificação e revisão independentes
- F3 — Packs + Skills → capacidades opcionais comprovadas
- F4 — Adopt / Goldify → adoção sem sobrescrever o projeto
- F5 — Sync → atualização conservadora e revisável

A sequência S0–S8 é histórica e não deve ser usada para planejar trabalho novo.
Para saber a fase atualmente ativa, consulte sempre `PROJECT_STATE.md`.

---

## 13. Dogfooding

O Standard deve usar suas próprias capacidades assim que forem confiáveis.

Direção:

- o próprio Standard usa suas regras quando aplicáveis;
- mudanças do Standard passam por `check`, diff e auditoria quando pertinente;
- práticas maduras só são promovidas ao Gold depois de prova em uso adequado.

Capacidades maduras devem ser provadas internamente antes de generalização ampla.

---

## 14. Como retomar o projeto

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

## 15. Quando parar e escalar

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

## 16. Visão final

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
