# IDEIAS STANDARD — PROJECT STATE

- **Versão:** 0.1.0-draft
- **Fase:** S1 — Conformance First
- **Status:** ACTIVE
- **Objetivo atual:** O0 v2 M1 auditado e aprovado com PASS independente no SHA `38db3f5b31d6f614b841f1133c0b474c8eb0bdc5`; preparar O0 v2 M2 (conectar os adapters ao runner)
- **Última implementada:** O0 v2 M1 — validação não interativa de Antigravity CLI e Codex CLI; auditada e aprovada com PASS independente no SHA `38db3f5b31d6f614b841f1133c0b474c8eb0bdc5`
- **Próxima:** O0 v2 M2 — conectar os adapters ao runner; M2 não iniciado nesta atualização
- **Bloqueios do projeto:** nenhum conhecido
- **Gate S0:** PASS — auditoria independente PASS no SHA `a327dc15d7a1a9c138903d6eb700977115166351`; aprovação registrada pela Product Authority
- **Gate S1:** NOT_RUN
- **O0:** PARTIAL / PRIORITY — O0-C01–O0-C45 implementados; O0 v2 M1 aprovado com PASS independente no SHA `38db3f5b31d6f614b841f1133c0b474c8eb0bdc5`; O0 v2 M2–M5 planejados; Gate S1 = NOT_RUN e S2 = NOT_STARTED
- **S2:** NOT_STARTED
- **CLI completa:** NOT_RUN
- **Validação atual:** PASS no workflow `Conformance` run `34857599652`, SHA `9e013b2f32aad6aaa2febea07f33c6e792efb230`

## Evidência atual

- Auditoria independente de O0 v2 M1: PASS no SHA `38db3f5b31d6f614b841f1133c0b474c8eb0bdc5`. Evidência canônica de aceite: `O0_V2_M1_EVIDENCE_REAUDIT.json` e pacote persistente `O0_V2_M1_EVIDENCE_REAUDIT_PACKAGE/` (com bundle Git do Builder `builder.bundle`, saídas completas e relatório JSON validado do Codex `codex_audit_report.json`). O registro `O0_V2_M1_EVIDENCE.json` permanece identificado como histórico substituído. Nenhum gate humano registrado; M2 e S2 não iniciados.

- Auditoria independente de O0-C19: PASS no SHA `cfa228463f2ed2a92de0cba06225860520bb116b`
- HEAD de reconciliação `1eca5ba80be883fe5491dd9178429f033aed6899`: merge com árvore idêntica ao SHA auditado
- Auditoria independente de O0-C20: PASS no SHA `61d4251f34163b210e11fb4b541b123771ade83d`
- Auditoria independente de O0-C21: PASS no SHA `a9f407d4e6581e328ff9e6b8619b7740a7d6cd12`
- Auditoria independente de O0-C22: PASS no SHA `9b8db74919af6995b9045574a04029d212237730`
- Auditoria independente de O0-C23: PASS no SHA `3471ecfb2b5dc3ba995c9f1730d1bbd55876be86`
- Auditoria independente de O0-C24: PASS no SHA `1c1bcac62269a934f5e0c99cc7ba6269416d62bf`
- Auditoria independente de O0-C25: PASS no SHA `b954bddc568e2be9c4c37f88dd4ea0d22e051878`
- Auditoria independente de O0-C26: PASS no SHA `a5d7f12ccd27370fce8751837ca4ad8751cb84dc`
- Auditoria independente de O0-C27: PASS no SHA `0e53f0e49154688bb07ff74169402b0e33bd82fb`
- Auditoria independente do README até O0-C27: PASS no SHA `019c561493cfaaee6628ac24bd61856bbac6b94a`
- Auditoria independente de O0-C28: PASS no SHA `9b90b8000c16bc08787116fa99553dd8411a520a`
- Auditoria independente de O0-C29: PASS no SHA `1c2388151ed0b5e7105aa34359c0c8c2ac499c99`
- Auditoria independente de O0-C30: PASS no SHA `742dc3798de45f86a56449dbdbc77a6a1d5a29b9`
- Auditoria independente do README: PASS no SHA `bb66a0760f7b9048f174582c90a102a027ad6a75`
- Auditoria independente de O0-C31: PASS no SHA `a479facd9775d6c639c08d5da20a334534e67d63`
- Auditoria independente de O0-C32: PASS no SHA `9f24fe5f724fb06ba4d54477293166fdd5e905cc`
- Auditoria independente de O0-C33: PASS no SHA `13955b605601ad7359d64dad5ddd7ef79284b1f1`
- Auditoria independente de O0-C34: PASS no SHA `37fa3a6a39a026b62144b2c9cd254f1df368a87e`
- Auditoria independente de O0-C35: PASS no SHA `5f27511fe8923df7a7077540016c645a0247758f`
- Auditoria independente de O0-C36: PASS no SHA `8a98790b241247baf271559b7a9a42609e82109b`
- Auditoria independente de O0-C37: PASS no SHA `8f54a67286fa953dbdbde601ba94cedae3d5cd88`
- O0-C38: ciclo real Builder → Auditor FAIL → Builder corrige → Auditor PASS → WAITING_PRODUCT_AUTHORITY executado; evidência em `O0_C38_E2E_EVIDENCE.json`
- Auditoria independente de O0-C38: PASS no SHA `7792e35681911bbb15b328d854068f4d8375375a`
- O0-C39: testes com processos reais comprovam exclusão mútua, rejeição concorrente, recuperação de lock obsoleto e preservação do estado após falha
- Auditoria independente de O0-C39: PASS no SHA `d1f325c4bdcbb8f671bcfe13ef2cf26156c25b65`
- O0-C40: identidade determinística, replay persistido e rejeição de payload divergente validados com processos reais
- Auditoria independente de O0-C40: PASS no SHA `ca347c0aade5ebc9ee5c2568c08cf49fab6d2328`
- O0-C14: invariantes de FAIL → FIX_REQUIRED e rejeições sem mutação cobertos diretamente
- O0-C15: findings mínimos e evidências vinculadas são encaminhados ao Builder; adulteração é rejeitada antes da execução
- O0-C41: journal durável retoma relatório, transição e `operation-record` após encerramento forçado sem reexecutar o ator
- O0-C42: timeout e cancelamento registram `INTERRUPTED` no journal sem transição canônica; retomada exige `resume_interrupted=true`
- O0-C43: falhas persistem em `runner-failures/` com categoria controlada, exit codes e vínculo ao estado; saída textual do ator não é retransmitida
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

Preparar O0 v2 M2 (conectar os adapters ao runner) conforme o `ROADMAP.md`. S1 permanece ACTIVE com implementação pausada até D-C02; Gate S1 = NOT_RUN e S2 permanece não iniciada. Nenhum gate humano registrado; M2 e S2 não iniciados.
