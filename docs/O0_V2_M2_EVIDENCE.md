# O0 v2 M2 — Conexao dos Adapters ao Runner O0

- **Marco:** O0 v2 M2 (Roadmap v3)
- **Status:** Implementado e validado com execucao real; pronto para auditoria independente
- **Artefato verificavel:** [O0_V2_M2_EVIDENCE.json](../O0_V2_M2_EVIDENCE.json) e [pacote persistente](../O0_V2_M2_EVIDENCE_PACKAGE/)
- **Data da execucao:** 2026-09-16
- **Ambiente:** Windows (drive fisico A:\ideias_standard)

---

## 1. Objetivo e Arquitetura

O marco M2 conecta os agentes reais (Antigravity CLI como Builder e OpenAI Codex CLI como Auditor) aos comandos configuraveis (`builder_command` e `auditor_command`) do runner operacional existente (`scripts/o0_runner.py`), eliminando qualquer copia/cola manual entre as ferramentas.

A arquitetura estabelecida preserva a neutralidade de provedores do Standard:
- **Runner neutro (`scripts/o0_runner.py`):** governa a maquina de estados, adquire o lock do processo (`StateLock`), prepara worktrees e snapshots, exige saida canônica e valida hashes SHA-256 e commits antes de qualquer transicao de estado.
- **Adapter Builder (`scripts/o0_antigravity_adapter.py`):** invocado em `cwd=builder_workspace` com variaveis de ambiente `IDEAS_STANDARD_REPORT` e `IDEAS_STANDARD_STATE`. Executa `agy.exe` em modo headless (`--print`), verifica a criacao do novo commit no Git, roda testes unitarios e emite o `builder-report.json` conforme o schema canônico.
- **Adapter Auditor (`scripts/o0_codex_adapter.py`):** invocado em `cwd=audit_workspace` com `IDEAS_STANDARD_REPORT` e `IDEAS_STANDARD_AUDIT_TARGET_SHA`. Executa `codex.CMD exec` com `--sandbox read-only` e stdin fechado (`input=""`), grava esquemas e relatorios intermediarios fora do checkout auditado, valida que o checkout permaneceu imutavel e converte os resultados para o `audit-report.json` canônico.

---

## 2. Execucao Real e Evidencias

A demonstracao real de ponta a ponta foi orquestrada por `scripts/o0_m2_runner_integration.py` em repositorio descartavel, cumprindo todos os criterios:

### Etapa 1: Builder via Runner
- **Comando do runner:** `builder_command: [python, scripts/o0_antigravity_adapter.py, --task, "..."]`
- **Executor ID:** `antigravity-cli`
- **Base SHA:** `49484c51de6283e1bf04d96addb0690c8c01bafc`
- **Produced SHA:** `ccc07302d508194cbd5885e2dd3fc8718d1d7127`
- **Arquivos modificados:** `calc.py`, `test_calc.py`
- **Validacao do Runner:** O runner validou que o commit existe no Git, que o `result_sha` bate com o HEAD do workspace, validou o schema do `builder-report.json` e canonicizou as evidencias em `evidence/r0-builder-check-c7726b6d49927b35.json`.
- **Transicao:** Estado avancou de `READY_FOR_BUILD` para `READY_FOR_AUDIT`, com `audit_target_sha = ccc07302d508194cbd5885e2dd3fc8718d1d7127`.

### Etapa 2: Auditor via Runner
- **Comando do runner:** `auditor_command: [python, scripts/o0_codex_adapter.py, --task, "..."]`
- **Executor ID:** `codex-cli`
- **Alvo auditado:** `ccc07302d508194cbd5885e2dd3fc8718d1d7127`
- **Isolamento:** Executado em worktree desacoplado e protegido contra escrita (`audit-workspaces/ccc07302...`).
- **Verificacao de imutabilidade:** `git status --porcelain` retornou vazio apos a auditoria.
- **Resultado:** `audit_result: PASS`, 5 checks verificados e 0 findings.
- **Validacao do Runner:** O runner validou que o checkout auditado nao foi adulterado, que o relatorio segue o schema `audit`, canonicizou as evidencias (`evidence/r1-audit-check-*.json`) e registrou os journals de operacao.
- **Transicao:** Estado avancou de `READY_FOR_AUDIT` para `WAITING_PRODUCT_AUTHORITY`.

### Parada Estrita e Sem Aprovacao de Gate
- `machine_state`: `WAITING_PRODUCT_AUTHORITY`
- `next_actor`: `PRODUCT_AUTHORITY`
- `approval`: `null`
- `human_gate_required`: `true`
- Nao houve registro automatico de gate ou avanco de fase.

---

## 3. Matriz de Criterios de Aceite (M2)

| Criterio M2 | Verificacao | Status |
| :--- | :--- | :---: |
| Adapters minimos implementados | `o0_antigravity_adapter.py` e `o0_codex_adapter.py` | PASS |
| Chamada via runner configuravel | Executados via `builder_command` e `auditor_command` de `o0_runner.py` | PASS |
| Passagem explicita de contexto | Workspace, tarefa, estado e target SHA passados explicitamente | PASS |
| Relatorios canônicos validados | `builder-report.json` e `audit-report.json` validados contra schemas | PASS |
| Verificacao de SHA e Git commit | Runner verifica existencia de commit e equivalencia ao HEAD | PASS |
| Imutabilidade do checkout do Auditor | Worktree mantido intacto e validado com `git status --porcelain` | PASS |
| Canonicizacao de evidencias | Textos convertidos em envelopes com ID deterministico e SHA-256 | PASS |
| Execucao nao interativa real | Zero interacao humana durante o ciclo do runner | PASS |
| Parada em `WAITING_PRODUCT_AUTHORITY` | Maquina para aguardando autoridade de produto | PASS |
| Sem registro indevido de gate | `approval=null`, `human_gate_required=true`, Gate S1 permanece `NOT_RUN` | PASS |
| Testes unitarios automatizados | `scripts/test_o0_m2_runner_integration.py` verde | PASS |

---

## 4. Pacote de Evidencias (`O0_V2_M2_EVIDENCE_PACKAGE/`)

O pacote duravel contem:
- `builder.bundle`: bundle Git com o commit produzido pelo Antigravity Builder (`ccc07302...`).
- `builder-report.json`: relatorio canônico gerado pelo Builder.
- `audit-report.json`: relatorio canônico gerado pelo Auditor Codex.
- `final-orchestrator-state.json`: estado canônico final persistido pelo runner.
- `evidence/`: colecao de envelopes canônicos de evidencias validados por schema e SHA-256.
- `operations/`: journals atomicos das operacoes `op-*` executadas pelo runner.

---

## 5. Limites e Nao Escopo

- Este marco entrega exclusivamente a conexao dos adapters ao runner (M2).
- M3 (ciclo de correcao com reencaminhamento de findings de FAIL) e S2 nao foram iniciados.
- Nenhum gate de produto ou aprovacao humana foi registrado. Gate S1 permanece `NOT_RUN` e S2 `NOT_STARTED`.
