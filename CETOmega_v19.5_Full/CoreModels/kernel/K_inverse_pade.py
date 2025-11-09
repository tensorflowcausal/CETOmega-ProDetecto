# Retarded Padé–Stieltjes kernel (scaffold)
import numpy as np
def F(omega, poles):
    # poles: list of (c, m) with c>0,m>0
    omega = np.asarray(omega, dtype=float)
    num = np.zeros_like(omega)
    csum = 0.0
    for c,m in poles:
        num += c*(omega*omega)/(omega*omega + m*m)
        csum += c
    if csum<=0: return np.ones_like(omega)
    return num/csum
