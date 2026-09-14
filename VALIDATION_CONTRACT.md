# Validation Contract — Ideias Standard

Este contrato define os códigos determinísticos iniciais de conformance. O objetivo é separar falhas estruturais, semânticas, invariantes e integridade interna do próprio Standard.

## Estados

- `PASS`: check executado e satisfeito.
- `FAIL`: check executado e não satisfeito.
- `WARN`: problema real não bloqueante para o check atual.
- `NOT_APPLICABLE`: somente com rationale.

`NOT_RUN != PASS`.

## Códigos de documento

| Código | Tipo | Regra |
|---|---|---|
| `IS-SCHEMA-001` | FAIL | Documento não satisfaz o JSON Schema aplicável. |
| `IS-SEM-001` | FAIL | Manifest/lock referencia pack inexistente. |
| `IS-SEM-002` | FAIL | `standard.lock` contém paths de artefatos duplicados. |
| `IS-SEM-003` | FAIL | Bundle referencia pack inexistente. |
| `IS-SEM-004` | FAIL | Documento materializável referencia workflow inexistente. |
| `IS-SEM-005` | FAIL | Documento materializável referencia adapter inexistente ou não `ACTIVE`. |
| `IS-SEM-006` | FAIL | Manifest declara versão do Standard diferente da versão suportada. |
| `IS-SEM-007` | FAIL | Workflow contém IDs de steps duplicados. |
| `IS-SEM-008` | FAIL | Reservado para contradição material de composição profile/bundle/packs. |
| `IS-SEM-009` | FAIL/CRITICAL | `sensitive-data` exige `capabilities.human_gates=true`. |
| `IS-SEM-010` | FAIL/CRITICAL | `multi-agent` exige `capabilities.independent_audit=true`. |
| `IS-SEM-011` | FAIL/CRITICAL | `multi-agent` exige Builder e Auditor distintos. |
| `IS-SEM-012` | FAIL/CRITICAL | Policy de orquestração exige IDs distintos para Builder e Auditor. |
| `IS-SEM-013` | FAIL/CRITICAL | `WAITING_PRODUCT_AUTHORITY` exige auditoria PASS do SHA congelado exato e ausência de aprovação prévia. |
| `IS-SEM-014` | FAIL/CRITICAL | Relatório de auditoria não pode declarar PASS com finding bloqueante. |
| `IS-SEM-015` | FAIL/CRITICAL | `GATE_APPROVED` exige aprovação explícita coerente com gate e SHA auditado. |
| `IS-SEM-016` | FAIL/HIGH | `audit_round` não pode exceder `max_audit_rounds`. |
| `IS-INV-001` | FAIL/CRITICAL | Registry contém IDs de invariantes duplicados. |
| `IS-WARN-001` | WARN | Artefato `MANAGED` possui `local_override=true`; revisar antes de upgrade. |

## Códigos de autoauditoria

| Código | Regra |
|---|---|
| `IS-SELF-001` | JSON Schema interno é inválido. |
| `IS-SELF-002` | Catálogo possui IDs duplicados. |
| `IS-SELF-003` | Catálogo aponta para path inexistente. |
| `IS-SELF-004` | `COMPATIBILITY.yaml` diverge de `VERSION`. |
| `IS-SELF-005` | `INVARIANTS.yaml` falhou validação. |
| `IS-SELF-006` | Bundle canônico falhou validação. |
| `IS-SELF-007` | Workflow canônico falhou validação. |
| `IS-SELF-008` | Policy canônica de orquestração multiagente falhou validação. |
| `IS-CLI-001` | Erro operacional da ferramenta; exit code 2. |

## Princípios

- JSON Schema valida forma; regras entre documentos e catálogos são semânticas.
- Invariantes críticos possuem IDs estáveis em `INVARIANTS.yaml`.
- Um erro deve retornar código estável e mensagem específica.
- Não alterar fixture ou teste apenas para obter verde.
- Novo código não reutiliza significado antigo dentro da mesma major version.
- `doctor` deve explicar os mesmos findings de `check`, não criar regra paralela.
- `--strict` futuro pode elevar WARN operacionalmente, mas não muda o significado canônico do check.
- O relatório estruturado usa `schemas/conformance-report.schema.json`.
- Exit codes da futura CLI seguem `CLI_CONTRACT.md`.
- Orquestração multiagente valida estado, handoffs e autoridade separadamente da execução do provider.
- PASS de Auditor é evidência para o SHA auditado; não é registro automático de gate humano.
