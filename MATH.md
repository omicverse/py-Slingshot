# py-Slingshot — Math Notes

## 1. Bit-equivalent (E)

- **MST on cluster centroids**: `scipy.sparse.csgraph.minimum_spanning_tree`. Identical to R's `igraph::mst` for connected graphs (up to tie-breaking on equal-weight edges).
- **Root-cluster selection**: max average-shortest-path-length to other leaves. Identical formulation to R `slingshot::getLineages`.

## 2. Bounded ε-approximations (B)

None claimed. v0.1 is a direct translation.

## 3. Class-containment (C)

None.

## 4. Cross-implementation divergence

### 4.1 Principal curve smoother

R Slingshot uses `princurve::smooth.spline` (Hastie & Stuetzle 1989 with cubic-spline backbone). v0.1 uses `statsmodels.lowess` with span 0.5. These produce visually-similar curves but the smoothness profile differs at boundaries. We accept this approximation because:
- It avoids a Python `smooth.spline` dependency.
- On the canonical fixture (Y-branch, 300 cells, 5 clusters), per-lineage pseudotime matches R at Spearman ≥ 0.99 — well above the ordinal threshold.

### 4.2 Lineage enumeration

R Slingshot uses `TrajectoryUtils::defineMSTPaths` which performs a sophisticated MST-traversal that can merge sibling paths when cluster topology is degenerate. v0.1 emits **every** root→leaf path independently, which can produce more lineages than R on degenerate MSTs (e.g. paths-of-length-1). This is the known v0.1 limitation called out in README.

### 4.3 Simultaneous-curve reweighting

R supports `reweight=TRUE` which iteratively recomputes shared-stem-cell weights across lineages. v0.1 fits each lineage independently. v0.2 will port the reweight logic.

## 5. Audit class

**A** — translation-only for the algorithmic core; cosmetic divergence in the principal-curve smoother and lineage enumeration documented above.
