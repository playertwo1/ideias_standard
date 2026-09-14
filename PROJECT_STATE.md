# IDEIAS STANDARD — PROJECT STATE

- **Versão:** 0.1.0-draft
- **Fase:** S1 — Conformance First
- **Status:** ACTIVE
- **Objetivo atual:** transformar o núcleo validado em interface estável de conformance, conforme `ROADMAP.md`
- **Última concluída:** Gate S0 registrado como PASS pela Product Authority após auditoria independente PASS
- **Próxima:** implementar S1 (`check`/`doctor`) dentro do escopo definido no `ROADMAP.md`
- **Bloqueios do projeto:** nenhum conhecido
- **Gate S0:** PASS — auditoria independente PASS no SHA `a327dc15d7a1a9c138903d6eb700977115166351`; aprovação registrada pela Product Authority
- **Gate S1:** NOT_RUN
- **S2:** NOT_STARTED
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

Executar somente o escopo de S1 — Conformance First definido no `ROADMAP.md`. S2 permanece não iniciada.
