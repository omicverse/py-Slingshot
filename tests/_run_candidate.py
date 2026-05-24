"""Run pyslingshot on the same fixture and dump pseudotime + curve points."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

_PORT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_PORT))

import pyslingshot


def main():
    fixture, labels_path, out = sys.argv[1], sys.argv[2], sys.argv[3]
    X = pd.read_csv(fixture).to_numpy(dtype=np.float64)
    cl = pd.read_csv(labels_path)["cluster"].to_numpy()
    print(f"X: {X.shape}  clusters: {len(np.unique(cl))}")

    sr = pyslingshot.slingshot(X, cl, start_cluster="1" if "1" in set(cl.astype(str)) else cl[0])
    pd.DataFrame(sr.pseudotime).to_csv(Path(out).parent / "Py_pt.csv", index=False)
    pd.DataFrame(sr.weights).to_csv(Path(out).parent / "Py_W.csv", index=False)
    for i, c in enumerate(sr.curves):
        pd.DataFrame(c).to_csv(Path(out).parent / f"Py_curve_{i + 1}.csv", index=False)
    print("Py done")


if __name__ == "__main__":
    main()
