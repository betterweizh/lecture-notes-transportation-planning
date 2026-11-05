"""Figures of chapter 8 (Errors and Uncertainty in Modeling)."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from common import AQUA, BLUE, INK, MUTED, ORANGE, save_mpl, t_


def error_complexity(outdir, lang="en"):
    """Specification, measurement and total error against model complexity.

    Illustrative curves (not data): specification error falls and
    propagated measurement error grows with complexity; the total error
    e = sqrt(e_s^2 + e_m^2) has an interior minimum. Used in
    08-errors-and-uncertainty (fig-08-error-vs-complexity).
    """
    c = np.linspace(0.05, 1, 200)
    es = 0.9 * np.exp(-3.2 * c) + 0.05
    em = 0.08 + 0.55 * c**2
    e = np.sqrt(es**2 + em**2)
    fig, ax = plt.subplots(figsize=(5.4, 3.3))
    ax.plot(c, e, color=BLUE, lw=2.2, label=t_(lang, "total error", "总误差") + " $e$")
    ax.plot(c, es, color=ORANGE, lw=2, ls="--", label=t_(lang, "specification error", "设定误差") + " $e_s$")
    ax.plot(c, em, color=AQUA, lw=2, ls=":", label=t_(lang, "measurement error", "测量误差") + " $e_m$")
    # the minimum of the total error
    k = np.argmin(e)
    ax.plot(c[k], e[k], "o", color=INK, ms=6)
    ax.annotate(t_(lang, "optimum complexity", "最优复杂度"), (c[k], e[k]), xytext=(c[k] - 0.08, 0.6),
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8), fontsize=9, color=INK)
    ax.legend(loc="upper center", fontsize=8.5)
    ax.set_xlabel(t_(lang, "model complexity", "模型复杂度"))
    ax.set_ylabel(t_(lang, "error", "误差"))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_ylim(0, 1.0)
    return save_mpl(fig, outdir, "08-error-vs-complexity")


FIGURES = {"08-error-vs-complexity": error_complexity}
