
import pandas as pd, numpy as np
def compare():
    # scaffold: produce a simple CSV contrast table
    df = pd.DataFrame({
        "observable": ["delta_omega_over_omega", "S8", "ns", "r"],
        "CETOmega": [2.5e-4, 0.77, 0.965, 0.02],
        "GR_LCDM": [0.0, 0.83, 0.965, 0.0]
    })
    df.to_csv("Benchmarks/CausalBench/results.csv", index=False)
if __name__ == "__main__":
    compare()
