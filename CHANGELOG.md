# Changelog

## 0.1.0-draft — 2026-09-14

### Added

- missão e fronteira do Ideias Standard;
- contrato canônico `STANDARD.md`;
- `AGENTS.md` com bootstrap mínimo;
- `PROJECT_STATE.md` operacional;
- roadmap S0–S8;
- decisão arquitetural: lifecycle manager, não apenas scaffold;
- profiles LIGHT/STANDARD/DEEP e packs composáveis;
- schemas de manifest, lock, contexto, artifact policy, bundle, workflow, change e conformance report;
- provenance e ownership `MANAGED / MERGEABLE / USER_OWNED`;
- bundles versionados iniciais;
- workflows `default` e `migration-first`;
- catálogo de adapters com status ACTIVE/PLANNED;
- brownfield/adopt e upgrade com preview + three-way diff;
- change lifecycle baseado em delta + invariantes;
- política de contexto progressivo e `CONTEXT_OVERFLOW`;
- `INVARIANTS.yaml` + schema para invariantes críticos;
- `COMPATIBILITY.yaml` e `VERSIONING.md`;
- `CLI_CONTRACT.md` com exit codes e comportamento futuro;
- `VALIDATION_CONTRACT.md` com códigos determinísticos, self-check e invariantes semânticos;
- fixture manifest data-driven e golden outputs;
- fixtures adversariais para sensitive-data e multi-agent;
- `scripts/validate_standard.py` com autoauditoria do Standard;
- suíte unitária data-driven;
- workflow `Conformance` em Python 3.11/3.12/3.13;
- artefatos de evidência `self-check.json` e `project-check.json` por versão Python;
- `S0_VALIDATION_EVIDENCE.md`;
- `S0_AUDIT_PACKET.md`;
- `docs/LIFECYCLE_MODEL.md` e política de ownership/upgrade;
- `REFERENCE_MATRIX.md` consolidando Copier, Cruft, projen, Spec Kit, OpenSpec e padrões de contexto proporcional observados na comunidade.

### Changed

- `sensitive-data` passa a exigir `human_gates=true` por regra semântica executável;
- `multi-agent` passa a exigir `independent_audit=true` e Builder distinto do Auditor;
- S0 passa a exigir self-check, CI verde, invariantes protegidos e auditoria independente antes de abrir S1.

### Validation status

Workflow `Conformance` run `34832777706`: PASS em Python 3.11, 3.12 e 3.13, com fixtures adversariais, self-check e projeto positivo aprovados.

O primeiro run falhou apenas na configuração de cache do `setup-python`; `cache-dependency-path: requirements-dev.txt` corrigiu o finding de CI. A matriz seguinte ficou verde.

S0 permanece `AUDIT_READY`, não concluída: falta auditoria independente e registro do gate.
