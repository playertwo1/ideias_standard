# IDEIAS STANDARD — PROJECT STATE

- **Versão:** 0.1.0-draft
- **Fase:** S0 — Fundação do padrão
- **Status:** AUDIT_READY
- **Objetivo atual:** concluir auditoria independente S0 após a extensão multiagente validada
- **Última concluída:** matriz `Conformance` verde em Python 3.11/3.12/3.13 para a extensão de orquestração Builder ↔ Auditor
- **Próxima:** Auditor independente executar `S0_AUDIT_PACKET.md` no HEAD atual e emitir `AUDIT RESULT: PASS|FAIL`
- **Bloqueios do projeto:** nenhum conhecido além do gate S0 ainda não concluído
- **Gate S0:** NOT_RUN — validação técnica PASS, auditoria independente pendente
- **CLI completa:** NOT_RUN
- **Validação atual:** PASS no workflow `Conformance` run `34841166585`

## Evidência atual

- SHA funcional validado: `2ab2d3881693393e53e2ba324cc947a6eb6821e8`
- Python 3.11: PASS
- Python 3.12: PASS
- Python 3.13: PASS
- Unit/adversarial fixtures: PASS
- Testes de orquestração Builder/Auditor: PASS
- Self-check: PASS
- Projeto positivo de referência: PASS
- Policy de orquestração: PASS
- Evidência detalhada: `S0_VALIDATION_EVIDENCE.md`

O commit que atualiza evidência/estado após o run é documental. O Auditor deve conferir o HEAD atual e confirmar que essas atualizações posteriores não alteraram os contratos executáveis validados.

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

Auditor independente deve usar `S0_AUDIT_PACKET.md`, revisar o HEAD atual e confirmar:

1. contratos/invariantes da extensão multiagente;
2. evidência do run `34841166585`;
3. ausência de regressão nas atualizações documentais posteriores ao SHA funcional validado;
4. manutenção da separação Builder/Auditor/Product Authority.

Somente após `AUDIT RESULT: PASS` registrar Gate S0 como PASS e iniciar S1 (`check`/`doctor`).
