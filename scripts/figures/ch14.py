"""Figures of chapter 14 (System Optimum and Elastic Demand)."""

from __future__ import annotations

from common import BLUE, ORANGE, network_svg


def braess_network(outdir, lang="en"):
    """Braess network: four links from node 1 to node 4 plus a new link 5.

    Link cost functions are written next to the links; the new link is
    dashed. Labels are symbols only, so both editions are identical. Used in
    14-system-optimum-and-elastic-demand (fig-14-braess-network) and
    chapter 29.
    """
    pos = {1: (50, 140), 2: (230, 45), 3: (230, 235), 4: (410, 140)}
    links = [(1, 2, "", "", 0), (3, 4, "", "", 0), (1, 3, "", "", 0),
             (2, 4, "", "", 0), (3, 2, "", "new", 0)]
    # labels placed by hand for readability
    notes = [(118, 80, "[1]  50 + x₁", "middle", BLUE), (342, 80, "[4]  10x₄", "middle", BLUE),
             (118, 210, "[3]  10x₃", "middle", BLUE), (342, 210, "[2]  50 + x₂", "middle", BLUE),
             (240, 144, "[5]  10 + x₅", "start", ORANGE)]
    return network_svg(outdir, "14-braess-network", pos, links, 460, 280,
                       origins=(1,), dests=(4,), notes=notes)


FIGURES = {"14-braess-network": braess_network}
