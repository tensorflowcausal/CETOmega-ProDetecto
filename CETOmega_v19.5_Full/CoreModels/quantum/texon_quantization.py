# Stieltjes spectral quantization (scaffold)
import numpy as np
def level_shift(E, poles):
    # relative shift ~ 1 - F(E/hbar)
    hbar = 1.054e-34
    from CoreModels.kernel.K_inverse_pade import F
    return 1.0 - F(E/hbar, poles)
