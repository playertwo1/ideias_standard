# O0 v2 M2 — Conexao dos Adapters ao Runner O0

- **Marco:** O0 v2 M2 (Roadmap v3)
- **Status:** PASS de reauditoria independente; pronto para homologação
- **Artefato verificavel de aceite:** [O0_V2_M2_EVIDENCE_REAUDIT.json](../O0_V2_M2_EVIDENCE_REAUDIT.json) e [pacote persistente](../O0_V2_M2_EVIDENCE_REAUDIT_PACKAGE/)
- **Registro historico substituido:** [O0_V2_M2_EVIDENCE.json](../O0_V2_M2_EVIDENCE.json) e [pacote anterior](../O0_V2_M2_EVIDENCE_PACKAGE/) mantidos preservados para rastreabilidade
- **Data da reauditoria:** 2026-09-16
- **Ambiente:** Windows (drive fisico A:\ideias_standard)

---

## 1. Objetivo e Arquitetura

O marco M2 conecta os agentes reais (Antigravity CLI como Builder e OpenAI Codex CLI como Auditor) aos comandos configuraveis (`builder_command` e `auditor_command`) do runner operacional existente (`scripts/o0_runner.py`), eliminando qualquer copia/cola manual entre as ferramentas.

A arquitetura estabelecida preserva a neutralidade de provedores do Standard:
- **Runner neutro (`scripts/o0_runner.py`):** governa a maquina de estados, adquire o lock do processo (`StateLock`), prepara worktrees e snapshots, exige saida canônica e valida hashes SHA-256 e commits antes de qualquer transicao de estado. No Windows, encerra a arvore completa de processos filhos (`taskkill /F /T /PID`) em caso de timeout ou cancelamento.
- **Adapter Builder (`scripts/o0_antigravity_adapter.py`):** invocado em `cwd=builder_workspace` com variaveis de ambiente `IDEAS_STANDARD_REPORT` e `IDEAS_STANDARD_STATE`. Executa `agy.exe` em modo headless (`--print`), registra PID do filho em `IDEAS_STANDARD_CHILD_PID_FILE`, verifica a criacao do novo commit no Git, roda testes unitarios e emite o `builder-report.json` conforme o schema canônico.
- **Adapter Auditor (`scripts/o0_codex_adapter.py`):** invocado em `cwd=audit_workspace` com `IDEAS_STANDARD_REPORT` e `IDEAS_STANDARD_AUDIT_TARGET_SHA`. Executa `codex.CMD exec` com `--sandbox read-only` e stdin fechado (`input=""`), registra PID do filho em `IDEAS_STANDARD_CHILD_PID_FILE`, grava esquemas e relatorios intermediarios fora do checkout auditado, valida que o checkout permaneceu imutavel e converte os resultados para o `audit-report.json` canônico.

---

## 2. Correcao dos Findings de Reauditoria

### Finding 1: Bundle Autossuficiente e Clonavel Isoladamente
- **Causa anterior:** O bundle era gerado com exclusao de base (`HEAD ^base_sha`), exigindo commits de pré-requisito externos.
- **Correcao:** `git bundle create builder.bundle HEAD` grava o historico completo da branch.
- **Comprovacao:**
  - `git bundle verify builder.bundle` retorna: `The bundle records a complete history.` sem qualquer pré-requisito pendente.
  - `git clone builder.bundle <dir_temporario>` clona em diretorio isolado com checkout no `builder_sha` e executa a suite de testes com 100% de sucesso.

### Finding 2: Encerramento de Processos Filhos em Timeout e Cancelamento no Windows
- **Causa anterior:** `process.kill()` no Windows encerrava apenas o processo direto do Python (adapter), deixando `agy.exe` ou `codex.CMD`/`node.exe` em execucao orfa.
- **Correcao:** Implementado `_terminate_actor_process(process)` em `scripts/o0_runner.py`, executando `taskkill /F /T /PID <actor_pid>`, garantindo a terminacao de toda a arvore de processos.
- **Comprovacao com CLIs reais:**
  - **Builder Timeout (`agy.exe`):** Timeout de 3.0s interrompe o Builder real. O processo filho `agy.exe` (PID 38136) e todos os seus descendentes sao terminados (`is_pid_alive=False`). Nenhum relatorio parcial e aceito, o estado permanece `READY_FOR_BUILD` e o journal e marcado como `INTERRUPTED` (`TIMEOUT`).
  - **Builder Cancelamento (`agy.exe`):** Requisiçao de cancelamento via `cancel_path` interrompe o Builder real. O processo filho `agy.exe` (PID 21304) e terminado. Estado permanece `READY_FOR_BUILD` e journal registra `INTERRUPTED` (`CANCELLED`).
  - **Auditor Timeout (`codex.CMD`):** Timeout de 3.0s interrompe o Auditor real. O processo filho `codex.CMD` / `node.exe` (PID 15284) e terminado. Estado permanece `READY_FOR_AUDIT` e journal registra `INTERRUPTED` (`TIMEOUT`).
  - **Auditor Cancelamento (`codex.CMD`):** Cancelamento interrompe o Auditor real. Processo filho (PID 42016) e terminado. Estado permanece `READY_FOR_AUDIT` e journal registra `INTERRUPTED` (`CANCELLED`).

---

## 3. Matriz de Criterios de Aceite (M2 Reaudit)

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
| Bundle autossuficiente | `records a complete history` no `git bundle verify` | PASS |
| Clone isolado do bundle | Clone em pasta temporaria reproduz SHA e testes passam | PASS |
| Timeout encerra processos filhos | Arvore de processos do Builder e Auditor terminada no Windows | PASS |
| Cancelamento encerra processos filhos | Arvore de processos terminada sem relatorio ou avanco parcial | PASS |
| Sem avanco parcial em interrupcao | Estado canônico preservado byte a byte | PASS |
| Evidencia anterior preservada | `O0_V2_M2_EVIDENCE.json` mantido integro | PASS |
| Testes unitarios automatizados | `scripts/test_o0_m2_runner_integration.py` (5 testes verdes) | PASS |

---

## 4. Pacote de Evidencias (`O0_V2_M2_EVIDENCE_REAUDIT_PACKAGE/`)

O pacote duravel de aceite contem:
- `builder.bundle`: bundle Git autossuficiente com o commit produzido pelo Antigravity Builder (`8cf01e56...`).
- `builder-report.json`: relatorio canônico gerado pelo Builder.
- `audit-report.json`: relatorio canônico gerado pelo Auditor Codex.
- `final-orchestrator-state.json`: estado canônico final persistido pelo runner.
- `evidence/`: colecao de envelopes canônicos de evidencias validados por schema e SHA-256.
- `operations/`: journals atomicos das operacoes `op-*` executadas pelo runner.

---

## 5. Limites e Nao Escopo

- Este marco entrega exclusivamente a conexao dos adapters ao runner e a resolucao dos findings (M2).
- M3 (ciclo de correcao com reencaminhamento de findings de FAIL) e S2 nao foram iniciados.
- Nenhum gate de produto ou aprovacao humana foi registrado. Gate S1 permanece `NOT_RUN` e S2 `NOT_STARTED`.
