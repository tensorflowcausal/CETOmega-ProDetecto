#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from pathlib import Path
import numpy as np

from checks.empirical_checks import (
    check_double_slit,
    check_ringdown_bounds,
    check_qft_recovery,
)

ROOT = Path(__file__).resolve().parent
CFG  = json.loads((ROOT / "checks" / "config.json").read_text())

def to_native(x):
    if isinstance(x, (np.bool_, bool)): return bool(x)
    if isinstance(x, np.integer):       return int(x)
    if isinstance(x, np.floating):      return float(x)
    if isinstance(x, np.ndarray):       return x.tolist()
    if isinstance(x, dict):             return {k: to_native(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):    return [to_native(v) for v in x]
    return x

def load_double_slit_model(path):
    arr = np.loadtxt(path, delimiter=",")
    if arr.ndim == 1:          # I
        I = arr
    else:                      # x, I
        I = arr[:, -1]
    # normalizar por si viene en escala arbitraria
    I = (I - I.min()) / (I.max() - I.min() + 1e-12)
    return I

def load_ringdown(path):
    data = np.loadtxt(path, delimiter=",")
    if data.ndim == 1:
        data = data[None, :]
    # dict: spin -> delta
    return {float(s): float(d) for s, d in data}

def load_qft_err(path):
    txt = (Path(path).read_text()).strip()
    return float(txt)

def empirical_checks():
    results = {}

    # A) Double slit
    ref_csv = ROOT / "data" / "double_slit_reference.csv"
    model_csv = ROOT / "data" / "double_slit_model.csv"
    I_model = load_double_slit_model(model_csv)
    okA, infoA = check_double_slit(
        I_model, ref_csv,
        max_rmse=float(CFG["empirical"]["double_slit"]["max_rmse"])
    )
    results["double_slit"] = {"ok": bool(okA), "info": to_native(infoA)}

    # B) Ringdown
    ring_csv = ROOT / "data" / "ringdown.csv"
    deltas = load_ringdown(ring_csv)
    okB, infoB = check_ringdown_bounds(
        deltas,
        rmin=float(CFG["empirical"]["ringdown"]["min"]),
        rmax=float(CFG["empirical"]["ringdown"]["max"]),
    )
    results["ringdown"] = {"ok": bool(okB), "info": to_native(infoB)}

    # C) QFT recovery
    err_file = ROOT / "data" / "qft_recovery_err.txt"
    err_demo = load_qft_err(err_file)
    okC, infoC = check_qft_recovery(
        float(err_demo),
        tol=float(CFG["empirical"]["qft_recovery"]["tol"])
    )
    results["qft_recovery"] = {"ok": bool(okC), "info": to_native(infoC)}

    return results

def main():
    res = empirical_checks()
    summary = {
        "PASS_empirical": bool(all(bool(v["ok"]) for v in res.values())),
        "config": to_native(CFG),
    }
    out = {"empirical": res, "summary": summary}
    out_native = to_native(out)

    rep = ROOT / "reports_checks.json"
    rep.write_text(json.dumps(out_native, indent=2), encoding="utf-8")
    print(json.dumps(out_native, indent=2))

if __name__ == "__main__":
    main()