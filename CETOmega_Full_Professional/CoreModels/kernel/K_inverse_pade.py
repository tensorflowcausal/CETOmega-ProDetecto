
import numpy as np
def F(omega, poles):  # poles: [(c,m)]
    omega = np.asarray(omega, float)
    if not poles: return np.ones_like(omega)
    num = np.zeros_like(omega)
    csum = 0.0
    for c,m in poles:
        num += c*(omega*omega)/(omega*omega + m*m)
        csum += c
    return num/csum if csum>0 else np.ones_like(omega)
