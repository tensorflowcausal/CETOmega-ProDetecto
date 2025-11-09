#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Run internal vs empirical checks as separate modes.

Usage:
  python run_checks.py --theory-checks
  python run_checks.py --empirical-checks
  python run_checks.py --all
"""
import argparse, json
from pathlib import Path
from typing import Any
import numpy as np

from checks.internal_checks import (
    check_spectral_positivity,
    check_hankel_psd_from_moments,
    check_local_limit,
)
from checks.empirical_checks import (
    check_double_slit,
    check_ringdown_bounds,
    check_qft_recovery,
)

ROOT = Path(__file__).resolve().parent
CFG = json.loads((ROOT / "checks" / "config.json").read_text())

# --------------------- helpers: NumPy → tipos Python ------------------------
def json_default(o: Any):
    """Fallback para json.dumps(default=...). Convierte tipos no serializables."""
    if isinstance(o, (np.bool_, bool)):
        return bool(o)
    if isinstance(o, np.integer):
        return int(o)
    if isinstance(o, np.floating):
        return float(o)
    if isinstance(o, np.ndarray):
        return o.tolist()
    return str(o)


def to_native(x: Any):
    """Conversión recursiva a tipos nativos JSON-serializables."""
    if isinstance(x, (np.bool_, bool)):
        return bool(x)
    if isinstance(x, np.integer):
        return int(x)
    if isinstance(x, np.floating):
        return float(x)
    if isinstance(x, np.ndarray):
        return x.tolist()
    if isinstance(x, dict):
        return {k: to_native(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [to_native(v) for v in x]
    return x
# ---------------------------------------------------------------------------


def load_reference_pattern():
    return ROOT / "data" / "double_slit_reference.csv"


def mock_model_pattern(n: int = 201):
    # Replace with your model output
    x = np.linspace(-1, 1, n)
    I = (np.cos(10 * np.pi * x) ** 2) * np.exp(-3 * x**2)
    I = (I - I.min()) / (I.max() - I.min() + 1e-12)
    return I


def theory_checks():
    results = {}

    # 1) Spectral positivity
    mu = np.linspace(0.01, 2.0, 64)
    rho = np.abs(np.sin(mu)) * 0.1
    ok1, info1 = check_spectral_positivity(np.c_[mu, rho])
    results["spectral_positivity"] = {"ok": bool(ok1), "info": to_native(info1)}

    # 2) Hankel-PSD from moments
    moments = [1.0] + [1.0 / (k + 1) for k in range(1, 40)]
    ok2, info2 = check_hankel_psd_from_moments(
        moments, order=int(CFG["internal"]["hankel_psd_order"])
    )
    results["hankel_psd"] = {"ok": bool(ok2), "info": to_native(info2)}

    # 3) Local/QFT recovery
    def F_demo(omega):
        omega = np.asarray(omega)
        return 1.0 - 1e-5 * np.exp(-omega)

    grid = np.linspace(0, 10, 128)
    ok3, info3 = check_local_limit(
        F_demo, grid, tol=float(CFG["empirical"]["qft_recovery"]["tol"])
    )
    results["local_limit"] = {"ok": bool(ok3), "info": to_native(info3)}

    return results


def empirical_checks():
    results = {}

    # A) Double slit
    ref_csv = load_reference_pattern()
    model_I = mock_model_pattern()
    okA, infoA = check_double_slit(
        model_I, ref_csv, max_rmse=float(CFG["empirical"]["double_slit"]["max_rmse"])
    )
    results["double_slit"] = {"ok": bool(okA), "info": to_native(infoA)}

    # B) Ringdown
    deltas = {0.7: 2.0e-4, 0.9: 3.5e-4, 0.99: 5.0e-4}
    okB, infoB = check_ringdown_bounds(
        deltas,
        rmin=float(CFG["empirical"]["ringdown"]["min"]),
        rmax=float(CFG["empirical"]["ringdown"]["max"]),
    )
    results["ringdown"] = {"ok": bool(okB), "info": to_native(infoB)}

    # C) QFT recovery
    err_demo = 1.0e-5
    okC, infoC = check_qft_recovery(
        float(err_demo), tol=float(CFG["empirical"]["qft_recovery"]["tol"])
    )
    results["qft_recovery"] = {"ok": bool(okC), "info": to_native(infoC)}

    return results


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--theory-checks", action="store_true", help="Run internal consistency checks only")
    ap.add_argument("--empirical-checks", action="store_true", help="Run external/empirical checks only")
    ap.add_argument("--all", action="store_true", help="Run both")
    args = ap.parse_args()

    out = {"theory": None, "empirical": None}

    if args.theory_checks or args.all:
        out["theory"] = theory_checks()
    if args.empirical_checks or args.all:
        out["empirical"] = empirical_checks()

    def decide(block):
        if block is None:
            return None
        oks = [bool(v["ok"]) for v in block.values()]
        return bool(all(oks))

    summary = {
        "PASS_theory": decide(out["theory"]),
        "PASS_empirical": decide(out["empirical"]),
        "config": to_native(CFG),
    }
    out["summary"] = summary

    # Conversión total antes de volcar a JSON
    out_native = to_native(out)

    rep = ROOT / "reports_checks.json"
    rep.write_text(json.dumps(out_native, indent=2, default=json_default), encoding="utf-8")
    print(json.dumps(out_native, indent=2, default=json_default))


if __name__ == "__main__":
    main()
