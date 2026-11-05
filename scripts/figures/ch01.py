"""Figures of chapter 1 (Probability Distributions)."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from common import AQUA, BLUE, INK, ORANGE, save_mpl, t_


def gumbel_logistic(outdir, lang="en"):
    """Gumbel and logistic densities for three parameter pairs.

    Used in 01-probability-distributions (fig-01-gumbel-logistic): the
    Gumbel density is right-skewed with mode eta, the logistic density is
    symmetric about eta, and halving mu doubles the spread.
    """
    x = np.linspace(-4, 8, 500)
    fig, axes = plt.subplots(1, 2, figsize=(7.4, 2.9), sharey=True)
    # three (location eta, scale mu) pairs, one line style each
    for (eta, mu), col, ls in (((0, 1), BLUE, "-"), ((0, 0.5), ORANGE, "--"), ((2, 1), AQUA, ":")):
        z = mu * (x - eta)
        g = mu * np.exp(-z) * np.exp(-np.exp(-z))
        lg = mu * np.exp(-z) / (1 + np.exp(-z)) ** 2
        lab = rf"$\eta={eta},\ \mu={mu}$"
        axes[0].plot(x, g, color=col, lw=2, ls=ls, label=lab)
        axes[1].plot(x, lg, color=col, lw=2, ls=ls, label=lab)
    axes[0].set_title(t_(lang, "Gumbel$(\\eta,\\mu)$ density", "Gumbel$(\\eta,\\mu)$ 密度"), fontsize=10, color=INK)
    axes[1].set_title(t_(lang, "Logistic$(\\eta,\\mu)$ density", "Logistic$(\\eta,\\mu)$ 密度"), fontsize=10, color=INK)
    for ax in axes:
        ax.set_xlabel("$x$")
    axes[0].legend(fontsize=8.5)
    return save_mpl(fig, outdir, "01-gumbel-logistic")


FIGURES = {"01-gumbel-logistic": gumbel_logistic}
