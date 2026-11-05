"""Template for a figure module (copy to chNN.py for chapter NN).

Only files named ``chNN.py`` are loaded by ``make_figures.py``; this file is
ignored. Each function draws exactly one figure named ``NN-<name>.svg``.
"""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from common import BLUE, save_mpl, t_


def example_plot(outdir, lang="en"):
    """What the figure shows, and where it is used (chapter, figure label)."""
    # data: say where the numbers come from
    x = np.linspace(0, 1, 50)
    fig, ax = plt.subplots(figsize=(5, 3))
    # drawing steps, one comment each
    ax.plot(x, x**2, color=BLUE, lw=2)
    ax.set_xlabel(t_(lang, "flow $x$", "流量 $x$"))
    return save_mpl(fig, outdir, "NN-example-plot")


FIGURES = {"NN-example-plot": example_plot}
