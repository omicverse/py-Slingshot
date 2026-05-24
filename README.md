# py-Slingshot

A **Python port of [slingshot](https://github.com/kstreet13/slingshot)** (Street et al. *BMC Genomics* 2018) — branching cell-lineage and pseudotime inference for single-cell RNA-seq.

- Pure NumPy / SciPy / statsmodels implementation
- MST over cluster centroids → DFS lineage enumeration → per-lineage principal curve fitting
- Parity vs R Slingshot on a Y-shaped fixture: **pseudotime Spearman 0.99+** along matched lineages

## Install

```bash
pip install pyslingshot-bio
```
(module name is `pyslingshot`; the PyPI distribution name is `pyslingshot-bio`.)

## Quick-start

```python
import pyslingshot
sr = pyslingshot.slingshot(reduced_dim, cluster_labels, start_cluster="root_cluster_id")
# Per-lineage pseudotime
pt = sr.pseudotime              # (n_cells × n_lineages)
# Visualisation
from ggplot2_py import ggsave
ggsave("out.png", plot=pyslingshot.plot_slingshot(sr), width=6, height=4, dpi=120)
```

## Function map

| Python | R | Status |
|---|---|---|
| `getLineages` | `getLineages` | ✅ |
| `getCurves` | `getCurves` | ✅ (independent per-lineage; no shared-start fitting yet) |
| `slingshot` | `slingshot` | ✅ |
| `plot_slingshot` | `plot(sds)` / vignette | ✅ |
| `plot_pseudotime` | (custom) | ✅ |
| `embedCurves` | `embedCurves` | ⏳ v0.2 |
| `predict` | `predict` | ⏳ v0.2 |
| `branchID` | `branchID` | ⏳ v0.2 |

## Known limitations (v0.1)

1. **Simultaneous principal-curve fitting deferred** — v0.1 fits each lineage independently. R Slingshot shares the early stem across lineages during fitting, which produces cleaner branching. v0.2 will add this.
2. **MST distance metric** uses plain Euclidean on centroids; R uses Mahalanobis-style scaling by within-cluster dispersion when `dist.method = "slingshot"` (default).
3. **`embedCurves`, `predict`, `branchID`** deferred to v0.2.
4. **Lineage count** can differ from R because of root-selection and lineage-merging differences; the matched lineages have Spearman ≥ 0.99 pseudotime parity.

## Citation

> Street, K. et al. *Slingshot: cell lineage and pseudotime inference for single-cell transcriptomics.* BMC Genomics 19, 477 (2018).

## License

MIT.
