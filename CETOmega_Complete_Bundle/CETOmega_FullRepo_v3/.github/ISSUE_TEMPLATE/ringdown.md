---
name: Ringdown — CETΩ vs GR vs GR+echoes
about: Compare models on QNM catalogs and decide PASS/FAIL
title: "[Ringdown] "
labels: ["analysis","ringdown","CETΩ"]
assignees: []
---

### Goal
Quantify evidence for CETΩ at ringdown using AIC/BIC/Bayes and bootstrap.

### Steps
- [ ] Prepare `ringdown.csv` (f_obs, sigma_f, ...)
- [ ] Run `CETOmega_RingdownStats.py` (JSON kernel or per-event shifts)
- [ ] Evaluate Bayes factors and BIC
- [ ] Compile decision in `reports/`
