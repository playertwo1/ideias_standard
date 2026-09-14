# S0 Audit Packet — Ideias Standard

Objetivo: permitir auditoria independente da fundação sem exigir leitura integral indiscriminada do repositório.

## Bootstrap do Auditor

Comece por:

1. `AGENTS.md`
2. `PROJECT_STATE.md`
3. `STANDARD.md`
4. `INVARIANTS.yaml`
5. `VALIDATION_CONTRACT.md`
6. `S0_VALIDATION_EVIDENCE.md`
7. `docs/MULTI_AGENT_ORCHESTRATION.md`

Depois abra apenas artefatos necessários para verificar findings concretos.

## Escopo S0

Auditar se a fundação define e protege corretamente:

- authority e gates;
- LIGHT/STANDARD/DEEP;
- packs, bundles, workflows e adapters;
- MANAGED/MERGEABLE/USER_OWNED;
- manifest/lock/context/change/conformance contracts;
- compatibility/versioning;
- invariantes críticos;
- fixtures adversariais e golden expectations;
- validador determinístico e self-check;
- CI em Python 3.11/3.12/3.13;
- contratos multiagente Builder/Auditor;
- vínculo imutável entre auditoria e SHA;
- loop de correção limitado e escalada;
- Auditor sem escrita no alvo auditado;
- parada obrigatória em Product Authority após PASS quando gate humano se aplica;
- separação entre núcleo provider-neutral e runners/adapters de agentes.

## Checks adversariais obrigatórios

Tente encontrar:

- regra crítica apenas em Markdown sem enforcement ou rationale;
- bundle/workflow/adapter capaz de ampliar autoridade;
- sensitive-data sem human gate;
- multi-agent sem auditor independente ou com Builder=Auditor;
- auditor capaz de editar o alvo da própria revisão;
- PASS de auditoria reutilizável para SHA diferente;
- PASS com finding bloqueante;
- estado `WAITING_PRODUCT_AUTHORITY` sem PASS do SHA congelado;
- `GATE_APPROVED` sem aprovação explícita coerente com o SHA auditado;
- loop Builder/Auditor sem limite ou que continue automaticamente após escalada;
- runner/adapter capaz de registrar gate humano ou iniciar próxima fase sem autorização;
- USER_OWNED passível de overwrite implícito;
- `NOT_RUN` tratável como PASS;
- contexto REQUIRED truncável silenciosamente;
- catalog path quebrado ou ID duplicado;
- incompatibilidade entre `VERSION`, schemas e `COMPATIBILITY.yaml`;
- fixture que passa/falha por motivo diferente do contrato declarado;
- código de validação reutilizado com significado diferente;
- promessa de adapter específico/S1 apresentada como capacidade já implementada.

## Evidência reproduzível

O run `34832777706`, SHA `18968a30329f8063ad87bd68543df72f977b3e5a`, é evidência histórica da fundação anterior à extensão de orquestração.

Ele **não** prova o HEAD atual. Antes da auditoria final, `S0_VALIDATION_EVIDENCE.md` deve registrar uma nova matriz `Conformance` verde para a extensão atual.

O Auditor deve ainda confirmar que eventuais commits documentais posteriores à nova evidência não introduziram regressão e que a CI do HEAD permanece verde.

## Gate

Emitir exatamente uma conclusão:

`AUDIT RESULT: PASS`

ou

`AUDIT RESULT: FAIL`

Finding CRITICAL/HIGH bloqueia S0. MEDIUM bloqueia quando afeta autoridade, integridade, segurança, compatibilidade ou determinismo. LOW pode ser registrado sem bloquear quando realmente não material.

Auditor não registra Gate S0, não inicia S1 e não se autoautoriza a mudar escopo do produto.
