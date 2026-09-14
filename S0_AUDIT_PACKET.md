# S0 Audit Packet — Ideias Standard

Objetivo: permitir auditoria independente da fundacao sem exigir leitura integral indiscriminada do repositorio.

## Bootstrap do Auditor

Comece por:

1. `AGENTS.md`
2. `PROJECT_STATE.md`
3. `STANDARD.md`
4. `INVARIANTS.yaml`
5. `VALIDATION_CONTRACT.md`
6. `S0_VALIDATION_EVIDENCE.md`

Depois abra apenas artefatos necessários para verificar findings concretos.

## Escopo S0

Auditar se a fundacao define e protege corretamente:

- authority e gates;
- LIGHT/STANDARD/DEEP;
- packs, bundles, workflows e adapters;
- MANAGED/MERGEABLE/USER_OWNED;
- manifest/lock/context/change/conformance contracts;
- compatibility/versioning;
- invariantes críticos;
- fixtures adversariais e golden expectations;
- validador determinístico e self-check;
- CI em Python 3.11/3.12/3.13.

## Checks adversariais obrigatórios

Tente encontrar:

- regra crítica apenas em Markdown sem enforcement ou rationale;
- bundle/workflow/adapter capaz de ampliar autoridade;
- sensitive-data sem human gate;
- multi-agent sem auditor independente ou com Builder=Auditor;
- USER_OWNED passível de overwrite implícito;
- `NOT_RUN` tratável como PASS;
- contexto REQUIRED truncável silenciosamente;
- catalog path quebrado ou ID duplicado;
- incompatibilidade entre `VERSION`, schemas e `COMPATIBILITY.yaml`;
- fixture que passa/falha por motivo diferente do contrato declarado;
- código de validação reutilizado com significado diferente;
- promessa de CLI/S1 apresentada como capacidade já implementada.

## Evidência reproduzível

Workflow `Conformance`, run `34832777706`, SHA `18968a30329f8063ad87bd68543df72f977b3e5a`: matriz 3.11/3.12/3.13 PASS.

Use a execução atual do HEAD para confirmar que documentação posterior não introduziu regressão.

## Gate

Emitir exatamente uma conclusão:

`AUDIT RESULT: PASS`

ou

`AUDIT RESULT: FAIL`

Finding CRITICAL/HIGH bloqueia S0. MEDIUM bloqueia quando afeta autoridade, integridade, segurança, compatibilidade ou determinismo. LOW pode ser registrado sem bloquear quando realmente não material.

Auditor não inicia S1 e não se autoautoriza a mudar escopo do produto.
