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

No real provider adapter or full FAIL → fix → PASS cycle was executed in this block. Those remain in later O0 criteria, including `O0-C38`.
