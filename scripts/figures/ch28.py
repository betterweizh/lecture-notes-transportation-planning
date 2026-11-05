"""Figures of chapter 28 (examples: Deterministic User Equilibrium)."""

from __future__ import annotations

from common import network_svg


def two_origin_network(outdir, lang="en"):
    """Five-link network with two O-D pairs, origins 1 and 3, destination 2.

    Link numbers in brackets; no words, so both editions are identical.
    Used in 28-examples-user-equilibrium (fig-28-two-origin-network) and in
    chapter 30.
    """
    pos = {1: (50, 60), 2: (430, 60), 3: (200, 170), 4: (340, 200)}
    links = [(1, 2, "[1]", "", 0), (3, 2, "[2]", "", 0), (1, 3, "[3]", "", 0),
             (3, 4, "[4]", "", 0), (4, 2, "[5]", "", 0)]
    return network_svg(outdir, "28-two-origin-network", pos, links, 480, 240,
                       origins=(1, 3), dests=(2,))


FIGURES = {"28-two-origin-network": two_origin_network}
