---
name: FRG — Causal kernel evolution
about: Track tasks for Functional Renormalization Group (FRG) solver and validation
title: "[FRG] "
labels: ["enhancement","FRG","CETΩ"]
assignees: []
---

### Goal
Implement and validate CETΩ FRG evolution preserving positivity (ρ(μ) ≥ 0) and Hankel-PSD.

### Tasks
- [ ] Configure `CETOmega_FRGsolver.py` params for current kernel
- [ ] Run FRG → `kernels/kernel_evolved.json`
- [ ] Export `*_Fomega.csv` and inspect saturation/monotonicity
- [ ] Bench Hankel-PSD on evolved kernel (if bench available)
- [ ] Document results in `reports/`

### Artifacts
- `kernels/kernel_evolved.json`
- `kernels/*_Fomega.csv`
- `reports/bench_out/`
