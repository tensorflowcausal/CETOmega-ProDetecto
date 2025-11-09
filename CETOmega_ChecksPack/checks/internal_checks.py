
import numpy as np

def check_spectral_positivity(rho_samples):
    """rho_samples: array-like (μ, ρ(μ)). Returns (ok: bool, info: dict)."""
    rho = np.asarray(rho_samples)[:,1]
    ok = np.all(rho >= -1e-15)  # numerical slack
    info = {"min_rho": float(np.min(rho)), "violations": int(np.sum(rho < 0))}
    return ok, info

def _hankel_matrix(m, n, seq):
    # Simple Hankel from moments seq[0..m+n]
    H = np.empty((m+1, n+1))
    for i in range(m+1):
        for j in range(n+1):
            H[i,j] = seq[i+j]
    return H

def check_hankel_psd_from_moments(moments, order=8):
    """moments: array-like of nonnegative moments; order: Hankel size minus 1.
    Returns (ok: bool, info: dict), using eigenvalues >= -eps.
    """
    import numpy.linalg as LA
    seq = np.asarray(moments, dtype=float)
    k = min(order, len(seq)//2 - 1)
    if k < 1:
        return False, {"reason": "insufficient moments", "required": 2*(order+1)}
    H = _hankel_matrix(k, k, seq)
    w = LA.eigvalsh(H)
    eps = 1e-12
    ok = np.min(w) >= -eps
    return ok, {"min_eig": float(np.min(w)), "order": int(k)}

def check_local_limit(F_func, omega_grid, tol=1e-4):
    """Verify F(ω) -> 1 within tolerance on omega_grid (local/QFT recovery)."""
    Fvals = F_func(omega_grid)
    err = np.max(np.abs(Fvals - 1.0))
    return err <= tol, {"max_abs_err": float(err), "tol": float(tol)}
