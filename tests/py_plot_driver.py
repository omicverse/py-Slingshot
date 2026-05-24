"""Render py-Slingshot plot."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd

_PORT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_PORT))

import pyslingshot
from ggplot2_py import ggsave


def main():
    out_dir = Path(sys.argv[1])
    out_dir.mkdir(parents=True, exist_ok=True)
    X = pd.read_csv(_PORT / "data/fixture_coords.csv").to_numpy(dtype=np.float64)
    cl = pd.read_csv(_PORT / "data/fixture_labels.csv")["cluster"].to_numpy()
    sr = pyslingshot.slingshot(X, cl, start_cluster="1")
    p = pyslingshot.plot_slingshot(sr)
    ggsave(str(out_dir / "Py_slingshot.png"), plot=p, width=6, height=4, dpi=100)
    print("done")


if __name__ == "__main__":
    main()
