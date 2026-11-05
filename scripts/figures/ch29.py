"""Figures of chapter 29 (examples: System Optimum and Elastic Demand)."""

from __future__ import annotations

from common import network_svg


def parallel_links_network(outdir, lang="en"):
    """Two parallel links from node 1 to node 2 followed by a common link to
    node 3 (one O-D pair 1 -> 3). Used in
    29-examples-system-optimum-and-elastic-demand
    (fig-29-parallel-links-network)."""
    pos = {1: (50, 70), 2: (230, 70), 3: (410, 70)}
    links = [(1, 2, "[1]", "", -38), (1, 2, "[2]", "", 38), (2, 3, "[3]", "", 0)]
    return network_svg(outdir, "29-parallel-links-network", pos, links, 460, 140,
                       origins=(1,), dests=(3,))


FIGURES = {"29-parallel-links-network": parallel_links_network}
