# IDEIAS STANDARD — PROJECT STATE

- **Versão:** 0.1.0-draft
- **Fase:** S0 — Fundação do padrão
- **Status:** REVALIDATION_REQUIRED
- **Objetivo atual:** revalidar S0 após a extensão multiagente autorizada pela Product Authority e então executar auditoria independente
- **Última concluída:** implementação documental/executável do contrato de orquestração Builder ↔ Auditor
- **Próxima:** executar a matriz `Conformance` no HEAD atual, atualizar evidência S0 e entregar o novo SHA ao Auditor independente
- **Bloqueios do projeto:** nenhum bloqueio de produto conhecido; avanço para S1 continua bloqueado por S0
- **Gate S0:** NOT_RUN
- **CLI completa:** NOT_RUN
- **Validação anterior:** PASS no workflow `Conformance` run `34832777706`, referente ao baseline anterior à extensão de orquestração

## Motivo da revalidação

A Product Authority autorizou incorporar ao Standard a automação segura do ciclo Builder → Auditor → correção → reauditoria. Como isso altera contratos e invariantes da fundação S0, o SHA antes validado permanece evidência histórica, mas não é suficiente para fechar o gate atual.

Nenhum PASS anterior é promovido para o novo HEAD por inferência.

## Materializado nesta extensão

- `docs/MULTI_AGENT_ORCHESTRATION.md`;
- `schemas/builder-report.schema.json`;
- `schemas/audit-report.schema.json`;
- `schemas/orchestration-policy.schema.json`;
- `schemas/orchestrator-state.schema.json`;
- `orchestration/builder-auditor-policy.json`;
- workflow `builder-auditor-loop`;
- pack `multi-agent` ampliado com SHA imutável, loop limitado e parada humana;
- `scripts/orchestrate_handoffs.py` como máquina de estados provider-neutral;
- fixtures positivas/adversariais e testes da orquestração;
- conformance ampliada para validar os novos contratos.

## Invariantes destacados

- `NOT_RUN != PASS`.
- USER_OWNED nunca sofre overwrite automático.
- Contexto REQUIRED nunca é truncado silenciosamente.
- sensitive-data exige human gate.
- multi-agent exige auditoria independente e Builder != Auditor.
- resultado de auditoria vale somente para o SHA exato auditado.
- Auditor não escreve no alvo da auditoria independente.
- ciclo automático Builder/Auditor é limitado e escala ao atingir o limite.
- PASS de auditoria não registra gate humano.
- Orquestrador/runner/workflow/adapter não inicia a fase seguinte por conta própria.
- bundle/workflow/adapter nunca amplia autoridade.

## Fronteira do runner

O núcleo implementado coordena estado, handoffs, evidência, SHA e gate. Ele é independente de fornecedor.

A camada que efetivamente inicia Codex, Claude, Gemini ou outro agente é um adapter/runner externo. Esse runner deve consumir os mesmos contratos e não pode ampliar autoridade. Adapters específicos continuam no escopo do lifecycle de ecossistema; a fundação S0 não transforma fornecedor em fonte canônica.

## Próxima ação

1. CI/conformance do HEAD atual.
2. Corrigir qualquer finding real sem reduzir invariantes.
3. Atualizar `S0_VALIDATION_EVIDENCE.md` com o SHA e run atuais.
4. Voltar para `AUDIT_READY` somente com evidência verde.
5. Auditor independente executar `S0_AUDIT_PACKET.md`.
6. Somente após `AUDIT RESULT: PASS` e registro adequado do Gate S0 iniciar S1 (`check`/`doctor`).
