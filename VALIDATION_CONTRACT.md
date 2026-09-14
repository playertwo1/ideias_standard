# Validation Contract — Ideias Standard

Este contrato define os códigos determinísticos iniciais de conformance. O objetivo é separar falhas estruturais de regras semânticas do Standard.

## Estados

- `PASS`: check executado e satisfeito.
- `FAIL`: check executado e não satisfeito.
- `WARN`: problema real não bloqueante para o check atual.
- `NOT_APPLICABLE`: somente com rationale.

`NOT_RUN != PASS`.

## Códigos

| Código | Tipo | Regra |
|---|---|---|
| `IS-SCHEMA-001` | FAIL | Documento não satisfaz o JSON Schema aplicável. |
| `IS-SEM-001` | FAIL | Manifest referencia pack inexistente no catálogo. |
| `IS-SEM-002` | FAIL | `standard.lock` contém paths de artefatos duplicados. |
| `IS-SEM-003` | FAIL | Bundle referencia pack inexistente. |
| `IS-SEM-004` | FAIL | Bundle referencia workflow inexistente. |
| `IS-SEM-005` | FAIL | Bundle referencia adapter inexistente ou ainda não ACTIVE. |
| `IS-SEM-006` | FAIL | Manifest declara versão do Standard diferente da versão suportada pelo validador atual. |
| `IS-SEM-007` | FAIL | Workflow contém IDs de steps duplicados. |
| `IS-SEM-008` | FAIL | Bundle/profile/packs entram em contradição material com sua composição declarada. |
| `IS-WARN-001` | WARN | Artefato `MANAGED` aparece com `local_override=true`; revisão humana recomendada antes de upgrade. |

## Princípios

- JSON Schema valida forma; regras entre catálogos e documentos são semânticas.
- Um erro deve retornar código estável e mensagem específica.
- Não alterar fixture ou teste apenas para obter verde.
- Novos códigos não devem reutilizar significado antigo dentro da mesma major version.
- O relatório estruturado futuro usa `schemas/conformance-report.schema.json`.
