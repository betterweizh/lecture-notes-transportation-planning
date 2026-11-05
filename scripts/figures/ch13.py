"""Figures of chapter 13 (Deterministic User Equilibrium)."""

from __future__ import annotations

from common import AQUA, ORANGE, network_svg, t_


def six_node_network(outdir, lang="en"):
    """Six-node network with origins 1, 5 and destinations 2, 6.

    Link numbers in brackets. Used in 13-user-equilibrium-assignment
    (fig-13-six-node-network) and in the examples of chapter 28.
    """
    pos = {1: (60, 50), 2: (460, 50), 3: (190, 150), 4: (330, 150), 5: (60, 250), 6: (460, 250)}
    links = [(1, 2, "[1]", "", 0), (1, 3, "[2]", "", 0), (4, 2, "[3]", "", 0), (3, 4, "[4]", "", 0),
             (5, 3, "[5]", "", 0), (5, 6, "[6]", "", 0), (4, 6, "[7]", "", 0)]
    notes = [(14, 30, t_(lang, "origin", "起点"), "start", AQUA),
             (506, 30, t_(lang, "destination", "终点"), "end", ORANGE)]
    return network_svg(outdir, "13-six-node-network", pos, links, 520, 290,
                       origins=(1, 5), dests=(2, 6), notes=notes)


FIGURES = {"13-six-node-network": six_node_network}
