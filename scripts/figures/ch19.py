"""Figures of chapter 19 (examples: Nonlinear Optimization)."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from common import BLUE, GRID, INK, MUTED, ORANGE, save_mpl, t_, write_svg


def frank_wolfe_example(outdir, lang="en"):
    """Frank-Wolfe iterates for min (x1-2)^2 + (x2-3)^2 over the triangle
    x1, x2 >= 0, x1 + x2 <= 2.

    The iterates x(0) = (0, 0), x(1) = (0, 2), x(2) = (0.5, 1.5) = x*.
    Used in 19-examples-optimization (fig-19-frank-wolfe-example).
    """
    fig, ax = plt.subplots(figsize=(4.4, 4.0))
    g1, g2 = np.meshgrid(np.linspace(-0.3, 3.2, 300), np.linspace(-0.3, 3.4, 300))
    f = (g1 - 2) ** 2 + (g2 - 3) ** 2
    ax.contour(g1, g2, f, levels=[0.5, 2, 4.5, 8, 12.5], colors=GRID, linewidths=0.9)
    # feasible set Omega
    ax.fill([0, 2, 0], [0, 0, 2], color=BLUE, alpha=0.12, lw=0)
    ax.plot([0, 2, 0, 0], [0, 0, 2, 0], color=BLUE, lw=1.4)
    # iterates
    pts = np.array([[0, 0], [0, 2], [0.5, 1.5]])
    ax.plot(pts[:, 0], pts[:, 1], color=ORANGE, lw=2, marker="o", ms=6)
    labels = [r"$\mathbf{x}^{(0)}$", r"$\mathbf{x}^{(1)}$", r"$\mathbf{x}^{(2)}=\mathbf{x}^*$"]
    for (x, y), lab, off in zip(pts, labels, [(6, -12), (6, 4), (8, 2)]):
        ax.annotate(lab, (x, y), textcoords="offset points", xytext=off, fontsize=10, color=INK)
    ax.plot(2, 3, "x", color=INK, ms=7)
    ax.annotate(t_(lang, "unconstrained\nminimum (2, 3)", "无约束\n最小点 (2, 3)"), (2, 3),
                textcoords="offset points", xytext=(-30, -30), fontsize=8.5, color=MUTED)
    ax.text(0.35, 0.35, r"$\Omega$", color=BLUE, fontsize=12)
    ax.set_xlabel("$x_1$")
    ax.set_ylabel("$x_2$")
    ax.set_aspect("equal")
    ax.set_xlim(-0.3, 3.2)
    ax.set_ylim(-0.3, 3.4)
    return save_mpl(fig, outdir, "19-frank-wolfe-example")


def shortest_path_network(outdir, lang="en"):
    """Four-link network of the shortest-path example; numbers are link
    travel times. Used in 19-examples-optimization
    (fig-19-shortest-path-network)."""
    w, h = 360, 190
    pos = {1: (40, 60), 4: (320, 60), 2: (110, 150), 3: (250, 150)}
    links = [(1, 4, 4), (1, 2, 1), (2, 3, 1), (3, 4, 1)]
    p = []
    for a, b, t in links:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        n = np.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / n, (y2 - y1) / n
        p.append(
            f'<line x1="{x1 + ux * 17}" y1="{y1 + uy * 17}" x2="{x2 - ux * 19}" '
            f'y2="{y2 - uy * 19}" stroke="{INK}" stroke-width="1.6" marker-end="url(#arr)"/>'
        )
        # travel time on the left of the link
        mx, my = (x1 + x2) / 2 - uy * 13, (y1 + y2) / 2 + ux * 13
        p.append(f'<text x="{mx}" y="{my + 4}" text-anchor="middle" font-size="12" fill="{BLUE}">{t}</text>')
    for k, (x, y) in pos.items():
        p.append(f'<circle cx="{x}" cy="{y}" r="15" fill="#ffffff" stroke="{MUTED}" stroke-width="1.5"/>')
        p.append(f'<text x="{x}" y="{y + 5}" text-anchor="middle" fill="{INK}" font-weight="600">{k}</text>')
    return write_svg(outdir, "19-shortest-path-network", "\n".join(p) + "\n", w, h)


FIGURES = {
    "19-frank-wolfe-example": frank_wolfe_example,
    "19-shortest-path-network": shortest_path_network,
}
