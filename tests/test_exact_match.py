"""End-to-end parity test against R Slingshot."""
import json, os, subprocess, sys
from pathlib import Path
import numpy as np
import pandas as pd
import pytest

_PORT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_PORT))


@pytest.fixture(scope="module")
def parity_dumps():
    fixture = _PORT/"data"/"fixture_coords.csv"
    labels  = _PORT/"data"/"fixture_labels.csv"
    r_pt = _PORT/"data"/"R_pt.csv"
    py_pt = _PORT/"data"/"Py_pt.csv"

    if not r_pt.exists():
        R_ENV = os.environ.get("R_TEST_ENV", "/scratch/users/steorra/env/CMAP")
        subprocess.run(
            ["conda","run","-p",R_ENV,"Rscript",
             str(_PORT/"tests"/"r_reference_driver.R"),
             str(fixture), str(labels), str(r_pt)],
            check=True, cwd=_PORT, capture_output=True,
        )
    if not py_pt.exists():
        subprocess.run(
            [sys.executable, str(_PORT/"tests"/"_run_candidate.py"),
             str(fixture), str(labels), str(py_pt)],
            check=True, cwd=_PORT, capture_output=True,
        )
    return pd.read_csv(r_pt).to_numpy(np.float64), pd.read_csv(py_pt).to_numpy(np.float64)


def test_per_lineage_spearman(parity_dumps):
    from scipy.stats import spearmanr
    R, P = parity_dumps
    rhos = np.full((R.shape[1], P.shape[1]), np.nan)
    for i in range(R.shape[1]):
        for j in range(P.shape[1]):
            m = ~np.isnan(R[:,i]) & ~np.isnan(P[:,j])
            if m.sum() > 10:
                rhos[i,j] = abs(spearmanr(R[m,i], P[m,j])[0])
    best = rhos.max(axis=1)
    print(f"  per-R-lineage best Spearman: {best.round(3).tolist()}")
    assert (best >= 0.80).all(), f"Some R lineages have no matching Py lineage at Spearman >= 0.80: best={best}"
