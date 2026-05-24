"""Visualisation — 1:1 port of slingshot R plot vignette via ggplot2-python."""

from __future__ import annotations

import numpy as np
import pandas as pd

from ggplot2_py import (
    aes,
    geom_path,
    geom_point,
    ggplot,
    labs,
    scale_color_gradientn,
    scale_color_manual,
    theme_classic,
)

from .core import SlingshotResult


_VIRIDIS = [
    "#440154", "#482878", "#3E4A89", "#31688E", "#26828E",
    "#1F9E89", "#35B779", "#6CCE59", "#B4DE2C", "#FDE725",
]


def _gg_color_hue(n: int) -> list[str]:
    return [
        "#E41A1C", "#377EB8", "#4DAF4A", "#984EA3", "#FF7F00",
        "#FFFF33", "#A65628", "#F781BF", "#999999",
    ][:n] + [
        "#66C2A5", "#FC8D62", "#8DA0CB", "#E78AC3", "#A6D854",
    ][: max(0, n - 9)]


def plot_slingshot(
    sr: SlingshotResult,
    *,
    dim_x: int = 1,
    dim_y: int = 2,
    point_size: float = 1.5,
    curve_size: float = 1.2,
    curve_colour: str = "black",
    point_alpha: float = 0.7,
):
    """Scatter of reduced-dim coloured by cluster + Slingshot curve overlays."""
    i, j = int(dim_x) - 1, int(dim_y) - 1
    df = pd.DataFrame(
        {
            f"Dim{i + 1}": sr.reduced_dim[:, i],
            f"Dim{j + 1}": sr.reduced_dim[:, j],
            "cluster": [str(c) for c in sr.cluster_labels],
        }
    )
    x_col, y_col = df.columns[0], df.columns[1]
    unique = sorted(df["cluster"].unique(), key=str)
    palette = dict(zip(unique, _gg_color_hue(len(unique))))
    p = (
        ggplot(df, aes(x=x_col, y=y_col, colour="cluster"))
        + geom_point(size=point_size, alpha=point_alpha)
        + scale_color_manual(values=palette)
        + theme_classic()
        + labs(x=x_col, y=y_col, colour="Cluster")
    )
    # Add each curve
    for li, curve in enumerate(sr.curves):
        cdf = pd.DataFrame(curve[:, [i, j]], columns=[x_col, y_col])
        cdf["lineage"] = f"L{li + 1}"
        p = p + geom_path(
            aes(x=x_col, y=y_col, group="lineage"),
            data=cdf,
            colour=curve_colour,
            size=curve_size,
        )
    return p


def plot_pseudotime(
    sr: SlingshotResult,
    lineage: int = 0,
    *,
    dim_x: int = 1,
    dim_y: int = 2,
    point_size: float = 1.5,
):
    """Scatter coloured by pseudotime along a chosen lineage."""
    i, j = int(dim_x) - 1, int(dim_y) - 1
    df = pd.DataFrame(
        {
            f"Dim{i + 1}": sr.reduced_dim[:, i],
            f"Dim{j + 1}": sr.reduced_dim[:, j],
            "pseudotime": sr.pseudotime[:, lineage],
        }
    )
    x_col, y_col = df.columns[0], df.columns[1]
    p = (
        ggplot(df, aes(x=x_col, y=y_col, colour="pseudotime"))
        + geom_point(size=point_size)
        + scale_color_gradientn(colours=_VIRIDIS)
        + theme_classic()
        + labs(x=x_col, y=y_col, colour=f"Pseudotime L{lineage + 1}")
    )
    return p
