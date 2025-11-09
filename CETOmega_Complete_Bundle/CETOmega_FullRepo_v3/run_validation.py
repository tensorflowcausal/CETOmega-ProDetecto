#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Auto-generated on 2025-11-09T10:13:49.201837Z


import json, os, subprocess, sys, shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PY = sys.executable or "python"

def run(cmd, cwd=None):
    print(f"[run] {cmd}")
    res = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    print(res.stdout)
    if res.returncode != 0:
        print(res.stderr)
    return res.returncode, res.stdout, res.stderr

def main():
    reports = ROOT / "reports"
    reports.mkdir(exist_ok=True, parents=True)

    # 1) FRG evolve
    kernel_in = ROOT / "kernels" / "kernel_example.json"
    kernel_out = ROOT / "kernels" / "kernel_evolved.json"
    frg = ROOT / "CETOmega_FRGsolver.py"
    if frg.exists():
        code, _, _ = run(f'"{PY}" "{frg}" --in "{kernel_in}" --out "{kernel_out}" --steps 200 --dell 0.01 --alpha 1.0 --sigma 1.0 --c0 0.0 --tau 0.0 --keep-norm --export-F --wmin 0.0 --wmax 10.0 --wpts 256')
    else:
        print("[warn] FRG solver not found; skipping.")
        kernel_out = kernel_in

    # 2) Bench (optional)
    bench = ROOT / "CETOmega_bench_v1.py"
    if bench.exists():
        (reports / "bench_out").mkdir(exist_ok=True, parents=True)
        run(f'"{PY}" "{bench}" --json "{kernel_out}" --out "{reports}/bench_out/"')
    else:
        print("[info] Bench script not found; continuing.")

    # 3) Ringdown stats
    ring = ROOT / "CETOmega_RingdownStats.py"
    ring_data = ROOT / "ringdown.csv"
    if ring.exists() and ring_data.exists():
        run(f'"{PY}" "{ring}" --data "{ring_data}" --cet-json "{kernel_out}" --out "{reports}/ringdown_report.json"')
    else:
        print("[info] Ringdown script or data not found; skipping.")

    # 4) Quantum Zeno stats
    zeno = ROOT / "CETOmega_QuantumZenoStats.py"
    zeno_data = ROOT / "quantum" / "zeno.csv"
    if zeno.exists() and zeno_data.exists():
        run(f'"{PY}" "{zeno}" --data "{zeno_data}" --cet-json "{kernel_out}" --out "{reports}/zeno_report.json"')
    else:
        print("[info] Quantum Zeno script or data not found; skipping.")

    # 5) Summary
    summary = {
        "kernel_out": str(kernel_out),
        "reports": [str(p) for p in reports.glob("*.json")]
    }
    with open(reports / "SUMMARY.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
