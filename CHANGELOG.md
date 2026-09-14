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
- `REFERENCE_MATRIX.md` consolidando Copier, Cruft, projen, Spec Kit, OpenSpec e padrões de contexto proporcional observados na comunidade;
- contrato provider-neutral de orquestração Builder ↔ Auditor em `docs/MULTI_AGENT_ORCHESTRATION.md`;
- schemas estruturados de `builder-report`, `audit-report`, `orchestration-policy` e `orchestrator-state`;
- policy de referência `orchestration/builder-auditor-policy.json`;
- workflow `builder-auditor-loop`;
- máquina de estados `scripts/orchestrate_handoffs.py` com SHA de auditoria congelado, reauditoria limitada, escalada e gate humano;
- testes e fixtures adversariais para mismatch de SHA, PASS com blocker, papel duplicado e limite de rodadas.

### Changed

- `sensitive-data` passa a exigir `human_gates=true` por regra semântica executável;
- `multi-agent` passa a exigir `independent_audit=true` e Builder distinto do Auditor;
- `multi-agent` passa a formalizar handoffs estruturados, Auditor read-only no alvo, SHA imutável e parada em Product Authority;
- bundle `deep-multi-agent-sensitive` passa a usar o workflow `builder-auditor-loop`;
- CI passa a descobrir todas as suítes `test_*.py` e validar a policy de orquestração;
- S0 passa a exigir self-check, CI verde, invariantes protegidos e auditoria independente antes de abrir S1.

### Validation status

Workflow `Conformance` run `34832777706`: PASS em Python 3.11, 3.12 e 3.13 para o baseline anterior à extensão multiagente.

A extensão de orquestração autorizada em 14/09/2026 altera a fundação S0 e exige nova execução da matriz antes da auditoria final. O run anterior permanece evidência histórica e não é promovido ao novo HEAD.

S0 permanece `NOT_RUN` e S1 continua bloqueada até revalidação + auditoria independente + registro adequado do gate.
