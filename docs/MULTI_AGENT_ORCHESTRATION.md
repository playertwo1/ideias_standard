# Multi-Agent Orchestration — Builder ↔ Auditor

## Objetivo

Este contrato define como projetos com o pack `multi-agent` podem automatizar o ciclo Builder → Auditor → correção → reauditoria sem transferir autoridade de produto para agentes ou para o Orquestrador.

A orquestração é uma capacidade do lifecycle do Standard. Ela não é fonte canônica de produto e não substitui `STANDARD.md`, invariantes, decisões LOCKED ou o contrato específico do projeto.

## Princípio

O Orquestrador é um coordenador determinístico de estado e evidência. Ele decide **quem deve agir a seguir**, não **o que o produto deve decidir**.

Fluxo de referência:

```text
READY_FOR_BUILD
      │
      ▼
   Builder
      │ builder-report.json + commit SHA
      ▼
READY_FOR_AUDIT
      │ audit_target_sha congelado
      ▼
   Auditor
   ┌──┴─────────────────────────┐
   │                            │
 FAIL                         PASS
   │                            │
   ▼                            ▼
FIX_REQUIRED          WAITING_PRODUCT_AUTHORITY
   │                            │
   └────── Builder             │ aprovação explícita
                               ▼
                         GATE_APPROVED
                               │
                              STOP
```

`ESCALATE`, disputa não resolvida ou limite de rodadas atingido levam a `BLOCKED`.

## Papéis

### Product Authority

Continua responsável por decisão nova de produto, mudança material de escopo, decisão LOCKED, conflitos sem regra e registro de gate humano.
Sua identidade autorizada é configurada na policy e persistida no estado; papel (`PRODUCT_AUTHORITY`) e autoridade (`GATE_APPROVAL`) são campos separados.

### Builder

Pode alterar o workspace autorizado e produzir a menor mudança coerente. Ao terminar, produz `builder-report.json` e informa o commit exato candidato à auditoria.
O relatório registra `executor_id`, papel `BUILDER` e autoridade `IMPLEMENTATION` separadamente.

### Auditor

É distinto do Builder. Revisa o commit congelado, não edita o alvo auditado e produz `audit-report.json` com `PASS`, `FAIL` ou `ESCALATE`.
O relatório registra `executor_id`, papel `AUDITOR` e autoridade `INDEPENDENT_AUDIT`; a máquina rejeita o mesmo `executor_id` nos dois handoffs.

### Orquestrador

Valida relatórios, controla transições, congela o SHA de auditoria, limita ciclos e para diante do gate humano. Não implementa feature, não corrige finding, não registra gate por iniciativa própria e não inicia automaticamente a próxima fase.

## SHA imutável de auditoria

Toda auditoria é ligada a `audit_target_sha`.

Se o Builder produz `A`, o Auditor revisa `A`. Se qualquer mudança material produz `B`, o PASS de `A` não se transfere para `B`; `B` precisa de nova auditoria.

Isso evita um PASS ambíguo sobre um repositório que mudou durante a revisão.

## Handoffs estruturados

Builder e Auditor não dependem da memória de uma conversa anterior.

Contratos:

- `schemas/builder-report.schema.json`;
- `schemas/audit-report.schema.json`;
- `schemas/orchestrator-state.schema.json`;
- `schemas/orchestration-policy.schema.json`.

O Builder registra, no mínimo, resultado, resumo, paths alterados, checks, limitações e disputas.

O Auditor registra, no mínimo, SHA auditado, resultado, checks, findings reproduzíveis, riscos residuais e `gate_registration = NOT_AUTHORIZED`.

`PASS` é inválido com check obrigatório `FAIL` ou `NOT_RUN`; `NOT_APPLICABLE` permanece permitido. `FAIL` exige ao menos um finding. `ESCALATE` mantém semântica própria.

## Ciclo de correção

A política de referência usa no máximo três rodadas de auditoria.

- `FAIL` antes do limite → `FIX_REQUIRED`;
- novo handoff do Builder congela um novo SHA → `READY_FOR_AUDIT`;
- `PASS` → `WAITING_PRODUCT_AUTHORITY`;
- `ESCALATE` → `BLOCKED`;
- limite atingido sem PASS → `BLOCKED`.

O limite evita loops infinitos. O projeto pode configurar outro valor permitido pela policy, mas não remover a existência de um limite.

## Disputa de finding

Builder não precisa obedecer silenciosamente a finding incompatível com o contrato. Pode retornar `DISPUTED` com a referência objetiva pertinente. A disputa para o fluxo automático e exige resolução explícita; o Orquestrador não escolhe qual agente “vence”.

## Gate humano

`AUDIT RESULT: PASS` não registra um gate humano.

Quando a auditoria passa, o estado obrigatório é `WAITING_PRODUCT_AUTHORITY`. Somente uma ação explícita da identidade de Product Authority configurada pode registrar a aprovação, declarando novamente o gate e o SHA auditado. Builder, Auditor, Orquestrador, runner, workflow e adapter não podem se autoatribuir essa identidade.

Mesmo após `GATE_APPROVED`, o Orquestrador de referência **não inicia a fase seguinte automaticamente**. O projeto deve materializar a nova autorização/estado conforme seu próprio contrato.

## Runner de agentes é adapter

`scripts/orchestrate_handoffs.py` implementa somente a máquina de estados e a validação dos handoffs. Ele não inicia um fornecedor de IA.

Um runner externo pode observar `next_actor` e iniciar a ferramenta escolhida pelo projeto. Esse runner é um adapter: não é fonte canônica e não pode ampliar autoridade, remover sandbox, mudar o SHA auditado, fabricar evidência ou contornar gate humano.

Isso permite usar ferramentas diferentes para Builder e Auditor sem acoplar o Standard a um fornecedor específico.

## Separação de workspaces

Recomendação para execução local:

- Builder em workspace/worktree com escrita limitada ao escopo autorizado;
- Auditor em checkout/worktree separado e read-only no alvo auditado;
- relatórios fora do conteúdo auditado ou em canal de evidência separado quando necessário;
- nenhuma escrita concorrente no mesmo artefato sem coordenação explícita.

## Evidência e persistência

A implementação de referência persiste `orchestrator-state.json` e os relatórios estruturados. Um adapter externo pode publicar esses artefatos em GitHub, CI ou outro sistema de evidência, desde que preserve provenance e o vínculo ao SHA.

A existência de um relatório não prova execução. Checks declarados como `NOT_RUN` continuam `NOT_RUN`.

## Estados

- `READY_FOR_BUILD`: Builder pode agir.
- `READY_FOR_AUDIT`: SHA candidato congelado e pronto para Auditor.
- `AUDITING`: reservado para runner que queira registrar execução em curso.
- `FIX_REQUIRED`: Auditor falhou e findings voltam ao Builder.
- `WAITING_PRODUCT_AUTHORITY`: auditoria passou; automação parada.
- `GATE_APPROVED`: aprovação humana foi registrada para o SHA auditado.
- `BLOCKED`: decisão, disputa, escalada ou limite exige intervenção.

## Não objetivos

Esta fundação não pretende:

- criar uma fonte canônica específica de Codex, Claude, Gemini ou outro agente;
- permitir que Auditor altere o alvo auditado;
- permitir que Builder aprove o próprio trabalho;
- fechar gate humano por inferência;
- esconder checks não executados;
- substituir lifecycle, ownership, provenance ou context engineering do Standard.
