# CET Ω — Bench Script v1
# Genera curvas simuladas y corre tests básicos de positividad/causalidad para kernels Padé–Stieltjes.
# Requisitos: numpy, matplotlib, pandas (opcional).

import json, numpy as np, matplotlib.pyplot as plt, pandas as pd, os

def load_kernel(json_path):
    with open(json_path, "r") as f:
        return json.load(f)

def response_stieltjes(omega, poles):
    """
    Respuesta tipo Stieltjes: F(ω) = sum_j c_j * ω^2 / (ω^2 + m_j^2).
    omega en rad/s.
    m_j en m^-1 (se asume m_j * c = frecuencia característica; c=1 en unidades naturales de ejemplo).
    """
    w2 = omega**2
    val = np.zeros_like(omega, dtype=float)
    for p in poles:
        cj = float(p["c_j"])
        mj = float(p["m_j"])
        val += cj * w2 / (w2 + mj**2)
    return val

def hankel_psd(poles, order=3):
    """
    Test de positividad: construye una matriz de Hankel H_{ab} = sum_j c_j / m_j^{2(a+b)}
    y verifica que todos los autovalores sean >= -eps (tolerancia numérica).
    """
    m = order + 1
    H = np.zeros((m, m), dtype=float)
    for a in range(m):
        for b in range(m):
            s_ab = 0.0
            for p in poles:
                cj = float(p["c_j"]); mj = float(p["m_j"])
                s_ab += cj / (mj**(2*(a+b)))
            H[a,b] = s_ab
    eig = np.linalg.eigvalsh(H)
    eps = 1e-12 * np.max(np.abs(H)) if np.max(np.abs(H))>0 else 1e-12
    return bool(np.all(eig >= -eps)), eig, H

def causality_proxy(poles):
    """
    Proxy simple de causalidad/retardo: m_j>0 y c_j>0 para todos los polos.
    En kernels de tipo Stieltjes esto implica polos en eje imaginario puro con residuos positivos (retardo).
    """
    for p in poles:
        if not (float(p["m_j"])>0 and float(p["c_j"])>0):
            return False
    return True

def make_frequency_grid(fmin, fmax, n=400):
    import numpy as np
    return np.logspace(np.log10(fmin), np.log10(fmax), n)

def save_curves(omegas, F, tag, outdir):
    import os, pandas as pd, matplotlib.pyplot as plt, numpy as np
    os.makedirs(outdir, exist_ok=True)
    # Guardar CSV
    df = pd.DataFrame({"frequency_Hz": omegas/(2*np.pi), "F_omega": F})
    csv_path = os.path.join(outdir, f"curva_{tag}.csv")
    df.to_csv(csv_path, index=False)
    # Graficar (reglas: 1 figura por gráfico, sin estilo ni colores específicos)
    plt.figure()
    plt.loglog(df["frequency_Hz"].values, df["F_omega"].values)
    plt.xlabel("Frecuencia [Hz]")
    plt.ylabel("Respuesta F(ω) [adim.]")
    plt.title(f"CET Ω — Curva {tag}")
    fig_path = os.path.join(outdir, f"curva_{tag}.png")
    plt.tight_layout()
    plt.savefig(fig_path, dpi=200)
    plt.close()
    return csv_path, fig_path

def main():
    # Paths
    base = "/mnt/data"
    json_kernel = os.path.join(base, "CETOmega_kernel_pro_detecto_vOmegaR1.json")
    outdir = os.path.join(base, "CETOmega_Bench_outputs")
    
    # Cargar kernel
    k = load_kernel(json_kernel)
    poles = k["poles"]
    
    # Grids de frecuencia por plataforma (en Hz)
    grids = {
        "AI": (1e2, 1e4),
        "OM": (1e2, 1e5),
        "cQED": (1e4, 1e7),
    }
    
    results = {}
    
    for tag, (fmin, fmax) in grids.items():
        freqs = make_frequency_grid(fmin, fmax, n=400)
        omegas = 2*np.pi*freqs  # rad/s
        F = response_stieltjes(omegas, poles)
        csv_path, fig_path = save_curves(omegas, F, tag, outdir)
        results[tag] = {"csv": csv_path, "png": fig_path}
    
    # Tests
    psd_ok, eig, H = hankel_psd(poles, order=3)
    caus_ok = causality_proxy(poles)
    
    # Guardar reporte simple
    report = {
        "hankel_psd_ok": bool(psd_ok),
        "hankel_eigenvalues": [float(x) for x in eig],
        "causality_proxy_ok": bool(caus_ok),
        "outputs": results
    }
    with open(os.path.join(outdir, "reporte_tests.json"), "w") as f:
        json.dump(report, f, indent=2)
    
    print("=== CET Ω — Bench Script v1 ===")
    print("Hankel PSD OK:", psd_ok)
    print("Causality proxy OK:", caus_ok)
    for tag, paths in results.items():
        print(f"{tag}: CSV -> {paths['csv']}, PNG -> {paths['png']}")
    print("Reporte:", os.path.join(outdir, "reporte_tests.json"))

if __name__ == "__main__":
    main()
