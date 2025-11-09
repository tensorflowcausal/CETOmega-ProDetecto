
import numpy as np, json, math
from pathlib import Path

def _rmse(a, b):
    a = np.asarray(a, float); b = np.asarray(b, float)
    return float(np.sqrt(np.mean((a-b)**2)) / (np.max(b)-np.min(b) + 1e-12))

def check_double_slit(model_pattern, reference_csv, max_rmse=0.03):
    """model_pattern: array-like intensities; reference_csv: path with 'x,I_ref'.
       Returns (ok: bool, info: dict)."""
    import csv
    xs, Iref = [], []
    with open(reference_csv, newline='') as f:
        rd = csv.DictReader(f)
        for row in rd:
            xs.append(float(row['x'])); Iref.append(float(row['I_ref']))
    n = min(len(model_pattern), len(Iref))
    rmse = _rmse(model_pattern[:n], Iref[:n])
    return rmse <= max_rmse, {"rmse": rmse, "max_rmse": max_rmse, "n_points": n}

def check_ringdown_bounds(delta_dict, rmin=1e-6, rmax=1e-3):
    """delta_dict: {a*: delta_omega_over_omega}. Ensure values lie within [rmin, rmax]."""
    vals = list(delta_dict.values())
    ok = all((v >= rmin and v <= rmax) for v in vals)
    return ok, {"range": [min(vals), max(vals)], "bounds": [rmin, rmax]}

def check_qft_recovery(err_value, tol=1e-4):
    """err_value: max|F(ω)-1| in local limit from an external routine."""
    return err_value <= tol, {"max_abs_err": err_value, "tol": tol}
