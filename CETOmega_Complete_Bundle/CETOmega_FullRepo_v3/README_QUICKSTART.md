# CETΩ — Quickstart (Gravity + Quantum Verification)

This guide runs the **full empirical pipeline** for CETΩ across **ringdown (gravity)** and **Quantum Zeno (measurement)** with a single command set.

## 1) Install
```bash
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)
pip install -r requirements.txt
```

## 2) Run full pipeline (end-to-end)
```bash
# FRG -> (Bench if present) -> Ringdown stats -> Quantum Zeno stats
bash run_all.sh

# Or using Makefile:
make all         # FRG + Bench + Ringdown
make quantum     # Quantum Zeno (uses kernels/kernel_evolved.json)
make quantum_boot
```

Outputs will be placed in `reports/`:
- `ringdown_report.json`, `ringdown_report_boot.json`
- `zeno_report.json`, `zeno_report_boot.json` (if you ran quantum_boot)
- Bench outputs (if `CETOmega_bench_v1.py` is available): `reports/bench_out/`

## 3) Decision rules (PASS/FAIL)
A dataset **supports CETΩ** if:
- **Ringdown:** `BIC[CETOmega]` minimal, Bayes factors > 10 vs GR and GR+echoes, bootstrap majority for CETΩ.
- **Quantum Zeno:** `BIC[CETOmega]` minimal, Bayes factor > 10 vs Markov, bootstrap majority for CETΩ.

Passing both domains with the **same kernel** (or its FRG evolution) yields **cross-domain empirical corroboration**.

## 4) Custom data
- Replace `ringdown.csv` with your catalog (same columns).
- Replace `quantum/zeno.csv` with your measurements.
- Replace `/kernels/kernel_example.json` with your calibrated kernel; re-run `make frg` before stats.

## 5) Reproducibility
- All scripts are CLI tools with JSON/CSV I/O.
- Use Git tags + `reports/` artifacts for traceability.
- For blinded analyses, freeze `{c_j, m_j}` before final fits.
