# CETΩ Verification Report (Ringdown Focus)

This report aggregates outputs from:
- FRG evolution: `kernels/kernel_evolved.json` (+ `*_Fomega.csv`)
- Bench (if available): `reports/bench_out/`
- Ringdown stats: `reports/ringdown_report.json` and `reports/ringdown_report_boot.json`

## Decision rule (PASS/FAIL)
See `README_ringdown.md` for the exact thresholds.

- PASS if: BIC[CETOmega] minimal AND BayesFactor(CETOmega_vs_GR) > 10 AND
  BayesFactor(CETOmega_vs_GR+echoes) > 10 AND bootstrap majority picks CETOmega.
- Otherwise: FAIL (investigate data/systematics or revise kernel).

---
