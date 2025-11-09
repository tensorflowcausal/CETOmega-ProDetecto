---
name: Quantum — Zeno causal verification
about: Test Γ_Z(Δt) = F(1/Δt)·Γ₀ with the same kernel
title: "[Quantum] "
labels: ["analysis","quantum","CETΩ"]
assignees: []
---

### Goal
Show CETΩ explains interrogation-rate dependence in Quantum Zeno with fixed spectrum.

### Steps
- [ ] Populate `quantum/zeno.csv` (delta_t_ns, P_nojump, sigma_P)
- [ ] Run `CETOmega_QuantumZenoStats.py` with `kernels/kernel_evolved.json`
- [ ] Compare against Markov & Power-law baselines
- [ ] Summarize results and PASS/FAIL
