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
