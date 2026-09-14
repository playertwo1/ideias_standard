# S0 Validation Evidence — Ideias Standard

**Data:** 2026-09-14  
**Standard:** `0.1.0-draft`  
**Workflow:** `Conformance`  
**Run:** `34832777706`  
**SHA validado:** `18968a30329f8063ad87bd68543df72f977b3e5a`

## Resultado

`VALIDATION RESULT: PASS`

A matriz executou com sucesso em:

- Python 3.11 — PASS
- Python 3.12 — PASS
- Python 3.13 — PASS

Em cada job passaram:

1. checkout;
2. setup Python;
3. instalação de `requirements-dev.txt`;
4. suíte `scripts.test_validate_standard`;
5. fixtures positivas/adversariais;
6. `validate_standard.py --self-check`;
7. validação do projeto positivo de referência;
8. upload de evidência.

## Artefatos do run

- `conformance-3.11` — artifact id `10342975951`
- `conformance-3.12` — artifact id `10342796420`
- `conformance-3.13` — artifact id `10342043999`

Cada artefato contém `self-check.json` e `project-check.json`.

## Finding de infraestrutura anterior

O primeiro run do workflow falhou antes dos testes porque `actions/setup-python` recebeu `cache: pip` sem `cache-dependency-path` para `requirements-dev.txt`.

Correção aplicada:

`cache-dependency-path: requirements-dev.txt`

Isso foi classificado como finding de CI, não falha de conformance do Standard. Após a correção, a matriz completa passou.

## Escopo desta evidência

Esta evidência prova execução automatizada e reproduzível do núcleo S0 no SHA acima. Ela **não** substitui auditoria independente e **não** registra Gate S0 como concluído.

Próximo gate: auditor independente deve revisar contratos, invariantes, schemas, fixtures, validador e esta evidência e emitir `AUDIT RESULT: PASS|FAIL`.
