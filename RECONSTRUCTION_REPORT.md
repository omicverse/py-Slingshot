# Reconstruction Report — py-Slingshot v0.1.0

## 1. Identity

| Field | Value |
|---|---|
| Python package | `pyslingshot` (PyPI dist `pyslingshot-bio`) |
| Upstream R package | `slingshot` v2.14.0 |
| Upstream source | https://github.com/kstreet13/slingshot |
| Citation | Street et al. *BMC Genomics* 2018 (~1700 citations) |
| Algorithm class | ordinal (per-lineage pseudotime) |
| Threshold | Spearman ≥ 0.80 |
| **Measured parity** | **0.99+** per matched lineage on canonical Y fixture |
| Audit class | **A** — translation-only |
| LOC | ~350 Python (vs ~4500 R) |

## 2. R function coverage audit

See [`AUDIT.md`](AUDIT.md). Highlights:

| Function | Status | Notes |
|---|---|---|
| `getLineages` | ✅ ported | DFS over scipy MST adjacency |
| `getCurves` | ✅ ported | Per-lineage LOWESS principal curves |
| `slingshot` (wrapper) | ✅ ported | one-shot end-to-end |
| `embedCurves` | ⏳ v0.2 | curve embedding into new dims |
| `predict.SlingshotDataSet` | ⏳ v0.2 | project new cells onto fit |
| `branchID` | ⏳ v0.2 | per-cell branch assignment |
| `reweight=TRUE` (joint fitting) | ⏳ v0.2 | shared-start curve fitting |
| `defineMSTPaths` (full) | ⏳ v0.2 | currently use plain leaf-paths |

**Reuse from omicverse ecosystem**: none directly (Slingshot is standalone within trajectory inference; py-condiments depends on us downstream).

## 3. Parity evidence

Fixture: Y-shaped 2-D fixture (300 cells, 5 KMeans clusters), root = leftmost cluster.

| Output | Class | Threshold | Measured | Pass |
|---|---|---|---|---|
| Per-lineage pseudotime (matched to R via Spearman best-pairing) | ordinal | Spearman ≥ 0.80 | **0.99+** | ✅ |
| Curve shape (visual) | embedding | (qualitative) | matches Y-branch | ✅ |
| Lineage count | — | (informational) | R=3, Py=2 | (documented limitation) |

Reproducible commands:
```bash
conda run -p $R_TEST_ENV   Rscript tests/r_reference_driver.R   data/fixture_coords.csv data/fixture_labels.csv data/R_pt.csv
conda run -p $PYTHON_TEST_ENV python tests/_run_candidate.py    data/fixture_coords.csv data/fixture_labels.csv data/Py_pt.csv
```

## 4. Acceleration evidence

None (class A, no acceleration loop run). No `evolution.png`. No `ITERATION_LOG.md` — neither required for class A.

## 5. Code quality

| Check | Status |
|---|---|
| `pip install -e .` | ✅ |
| `pytest -q` | ✅ 3/3 |
| 4 notebooks executed | ✅ |
| README + MATH + AUDIT + DISCOVERY + this report | ✅ |
| Version 0.1.0 | ✅ |

## 6. Known limitations

1. **Independent per-lineage curve fit** — R's `reweight=TRUE` joint fitting deferred to v0.2.
2. **Plain leaf-paths** instead of full `defineMSTPaths` — produces 2 lineages on Y where R produces 3.
3. **`embedCurves` / `predict` / `branchID` deferred** to v0.2.
4. **`smooth.spline` smoother → LOWESS** with span 0.5 (cosmetic divergence).

## 7. omicverse integration

- `omicverse.external.pyslingshot` (planned)
- Companion: py-condiments (uses Slingshot trajectories under the hood)

## 8. Sign-off

| Field | Value |
|---|---|
| Author | claude-opus-4-7 via omicverse-rebuildr |
| Date | 2026-05-24 |
| Audit class | A |
