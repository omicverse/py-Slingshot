"""Smoke tests for pyslingshot."""
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

_PORT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(_PORT))

import pyslingshot


def _make_y_data(seed=42):
    rng = np.random.RandomState(seed)
    n = 80
    t = np.linspace(0, 1, n)
    stem = np.column_stack([t * 4 - 2, np.zeros(n)]) + rng.normal(0, 0.1, (n, 2))
    b1 = np.column_stack([2 + t * 2, t * 2]) + rng.normal(0, 0.1, (n, 2))
    b2 = np.column_stack([2 + t * 2, -t * 2]) + rng.normal(0, 0.1, (n, 2))
    X = np.vstack([stem, b1, b2])
    from sklearn.cluster import KMeans
    cl = (KMeans(n_clusters=5, random_state=42, n_init=10).fit(X).labels_ + 1).astype(str)
    return X, cl


def test_import():
    assert pyslingshot.__version__ == "0.1.0"
    assert hasattr(pyslingshot, "slingshot")


def test_get_lineages_y():
    X, cl = _make_y_data()
    sr = pyslingshot.getLineages(X, cl, start_cluster="1")
    assert len(sr.lineages) >= 1
    # All lineage paths start with the same root cluster
    roots = set(l[0] for l in sr.lineages)
    assert len(roots) == 1


def test_slingshot_full():
    X, cl = _make_y_data()
    sr = pyslingshot.slingshot(X, cl, start_cluster="1")
    assert sr.curves
    assert sr.pseudotime.shape == (X.shape[0], len(sr.lineages))
    # Pseudotime should be monotone-ish along the stem (Dim1)
    L0 = sr.pseudotime[:, 0]
    mask = ~np.isnan(L0)
    from scipy.stats import spearmanr
    rho = spearmanr(X[mask, 0], L0[mask])[0]
    assert abs(rho) > 0.5
