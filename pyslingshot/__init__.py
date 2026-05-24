"""pyslingshot — pure-Python port of slingshot (Street et al. BMC Genomics 2018).

Reconstructs branching trajectories from clustered single-cell data:

1. ``getLineages``: MST over cluster centroids → root → enumerate root→leaf paths
2. ``getCurves``: fit smooth principal curves through each lineage, with cells
   weighted by lineage membership
3. ``slingshot``: convenience wrapper running both
4. ``SlingshotResult``: minimal container (curves, pseudotime, weights, lineages, MST)

v0.1 covers all four. Plotting via ``pyslingshot.plotting``.
"""

from __future__ import annotations

__version__ = "0.1.0"

from .core import (
    SlingshotResult,
    getLineages,
    getCurves,
    slingshot,
)
from .plotting import plot_slingshot, plot_pseudotime

__all__ = [
    "SlingshotResult",
    "getLineages",
    "getCurves",
    "slingshot",
    "plot_slingshot",
    "plot_pseudotime",
    "__version__",
]
