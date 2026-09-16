# O0 First Block — Validation Evidence

- Scope: `O0-C01`–`O0-C13`
- Implementation SHA: `9e013b2f32aad6aaa2febea07f33c6e792efb230`
- Conformance run: `34857599652`
- Matrix: Python 3.11 / 3.12 / 3.13
- Result: PASS

## Covered behavior

- state load and deterministic `next_actor`;
- configured Builder/Auditor command launch without implicit shell;
- separate Builder and immutable Auditor workspaces;
- Builder report requires `result_sha`;
- `result_sha` becomes `audit_target_sha`;
- Auditor report is validated against the frozen SHA;
- regression tests for runner configuration, workspace separation, command dispatch and frozen read-only audit checkout.

## Boundary

No real provider adapter or full FAIL → fix → PASS cycle was executed in this first block. The later O0-C38 evidence is recorded below.

## O0-C38 — controlled real E2E cycle

- Command: `python3 scripts/o0_e2e.py --work-root <empty-directory> --output <evidence-file>`
- Evidence: `O0_C38_E2E_EVIDENCE.json`
- Flow: `READY_FOR_AUDIT → FIX_REQUIRED → READY_FOR_AUDIT → WAITING_PRODUCT_AUTHORITY`
- Audit rounds: `0 → 1 → 1 → 2`
- Initial SHA: `77ead7d1a0b587a45c028654c900906df4244c7d`
- Corrected SHA: `082bdd575665bcd70ee8e260842a2ed9b90a5328`
- Boundary: local provider-neutral subprocess actors; no external provider adapter or product gate.

## O0-C39 — process concurrency

- Commands: `python -m unittest scripts.test_o0_concurrency` and `wsl python3 -m unittest scripts.test_o0_concurrency`
- Result: one actor and one transition under contention; the concurrent runner exits deterministically.
- Stale handling: kernel ownership releases the lock after forced process termination; a leftover lock file does not block recovery.
- Failure handling: actor failure preserves canonical state bytes and releases the lock.

## O0-C40 — idempotent operation identity

- Command: `python -m unittest scripts.test_o0_idempotency` (também executado em WSL).
- Identity: SHA-256 canônico de `run_id`, estado de origem, ator, rodada e SHAs relevantes.
- Replay: novo processo retorna o resultado persistido sem executar novamente o ator.
- Conflict: mesmo `operation_id` com relatório divergente é rejeitado sem mutação ou duplicação.
- Independent audit: PASS no SHA `ca347c0aade5ebc9ee5c2568c08cf49fab6d2328`.

## O0-C14/O0-C15 — formal regularization

- Commands: `python -m unittest scripts.test_orchestrate_handoffs scripts.test_o0_runner` em ambiente POSIX/WSL.
- O0-C14: FAIL válido produz `FIX_REQUIRED`, incrementa uma rodada, preserva SHAs/gate/aprovação e direciona ao Builder; relatórios inválidos não alteram o estado.
- O0-C15: `builder-findings` contém somente alvo, rodada e findings canônicos com evidências referenciadas; o digest do relatório aceito fica no estado e impede adulteração conjunta de relatório/snapshot. No Linux, o Builder recebe um descritor de memória selado, não o caminho mutável; troca durante preparação é rejeitada antes do spawn.
- Round limit: o terceiro FAIL produz `BLOCKED`, sem avanço indevido.
- Boundary: entrega imutável depende de `memfd`/seals do Linux; outros sistemas recusam a execução Builder em FIX_REQUIRED.

## O0-C41 — interruption recovery journal

- Command: `python -m unittest scripts.test_o0_recovery` (também executado em WSL).
- Real processes: o runner é encerrado à força após o relatório, após a transição e após o snapshot do relatório.
- Recovery: a retomada conclui estado e `operation-record` sem uma segunda execução do Builder.
- Integrity: journal, relatório, estado resultante e snapshot são vinculados à identidade e a digests canônicos.
- Boundary: timeout e cancelamento explícitos permanecem em O0-C42.

## O0-C42 — timeout and cancellation

- Tests: `python -m unittest scripts.test_o0_timeout_cancel scripts.test_o0_recovery scripts.test_o0_idempotency` em processos reais.
- Timeout/cancelamento: journal `INTERRUPTED` com motivo estruturado; estado canônico e rodada não avançam.
- Regressão: processos reais escrevem relatório parcial antes de timeout/cancelamento; o arquivo está ausente antes da retomada explícita e o journal permanece `INTERRUPTED`.
- Resume: requer `resume_interrupted=true`, estado de origem intacto e pedido de cancelamento removido; C41 continua recuperando o período após relatório/transição.
- Boundary: encerramento de descendentes no Windows e falhas estruturadas do runner ficam fora de O0-C42.

## O0-C43 — structured runner failures

- Tests: `python -m unittest scripts.test_o0_failures scripts.test_o0_recovery scripts.test_o0_timeout_cancel scripts.test_o0_idempotency` com processos reais.
- Falhas de ator e relatórios inválidos persistem evidência canônica de categoria, exit code e vínculo ao estado, sem saída textual, traceback ou payload sensível.
- Journal de operação com JSON malformado persiste evidência estruturada de INVALID_JSON, exit code 2 e saída sem secrets, sem executar o ator ou alterar o estado canônico.
- Processo reiniciado preserva evidência; se o ator saiu com código não zero após gerar relatório válido, C41 valida e recupera sem reexecutá-lo.
- Configuração inválida persiste evidência mínima ao lado da configuração; falha de escrita da evidência retorna erro seguro.

