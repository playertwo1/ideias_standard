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
