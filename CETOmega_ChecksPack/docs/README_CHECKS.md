
# CETOmega Checks Pack — Theory vs Empirical

This pack separates **internal (theory)** checks from **external (empirical)** checks so results are not circular.

## Usage
```bash
# Run only internal/theory checks
python run_checks.py --theory-checks

# Run only empirical/external checks
python run_checks.py --empirical-checks

# Run both
python run_checks.py --all
```

## What is tested?
- **Internal:** spectral positivity (ρ≥0), Hankel-PSD (moments), local/QFT recovery F(ω)→1.
- **Empirical:** double-slit pattern RMSE vs reference, ringdown shift bounds, QFT-recovery threshold.

Thresholds are configurable in `checks/config.json`.
Output JSON is written to `reports_checks.json`.
