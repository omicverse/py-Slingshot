# Discovery — py-Slingshot

## 1. Is the target already ported?

`gh repo view omicverse/py-Slingshot` → **not found at port start**.

A community port [mossjacob/pyslingshot](https://github.com/mossjacob/pyslingshot) exists but is unmaintained and lacks parity validation against R. omicverse port is independent.

## 2. R dependencies + py-mirror reuse

R upstream Slingshot DESCRIPTION lists: `igraph`, `princurve`, `Matrix`, `TrajectoryUtils`, `S4Vectors`, `SingleCellExperiment`, `SummarizedExperiment`.

| R dep | Already mirrored? | Reused as |
|---|---|---|
| igraph | n/a | `networkx` + `scipy.sparse.csgraph.minimum_spanning_tree` |
| princurve | ❌ | inline `_principal_curve` using statsmodels LOWESS |
| Matrix | n/a | `scipy.sparse` |
| TrajectoryUtils | ❌ | inline (no reuse needed for v0.1 — only `defineMSTPaths` is used; we re-implement as DFS over MST adjacency) |
| S4Vectors / SingleCellExperiment / SummarizedExperiment | n/a | `anndata.AnnData` (not used in v0.1 — pure numpy in/out) |

## 3. Decision

**Proceed with full port** — algorithm class is ordinal (per-lineage pseudotime). v0.1 fits each lineage's principal curve independently; R's simultaneous-fit + reweight=TRUE is deferred to v0.2.
