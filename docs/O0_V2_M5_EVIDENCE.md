# O0 v2 M5 — prova final

Início:

```text
python scripts/o0_m5_final_proof.py
```

Retomada explícita de operação interrompida:

```text
python scripts/o0_runner.py --config <config-com-resume_interrupted-true>
```

Artefatos verificáveis: `O0_V2_M5_EVIDENCE.json` e `O0_V2_M5_EVIDENCE_PACKAGE/`.
O pacote contém bundle Git, relatórios, operations, evidências, estados e provas de interrupção indexados por SHA-256. Nenhum gate ou aprovação humana foi registrado.

Limitação: as provas reais de timeout/cancelamento vêm de M2; a regressão de recuperação é separada. A tentativa de combinar interrupção e retomada real em M5 parou em `taskkill` exit 128. M5 permanece parcial.
