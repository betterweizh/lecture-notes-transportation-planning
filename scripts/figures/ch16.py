"""Figures of chapter 16 (Dynamic Assignment and Simulation)."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from common import BLUE, INK, MUTED, ORANGE, save_mpl, t_


def bottleneck_cumulative(outdir, lang="en"):
    """Cumulative departures and bottleneck exits of the bottleneck example.

    Data of the worked example: N = 5 000 commuters, capacity s = 2 000
    veh/h, departures from t_s = 6:30 to t_e = 9:00, the last on-time
    departure at 7:30 and t* = 8:30. Departure rate 4 000 veh/h before 7:30
    and 2 000/3 veh/h after it. The shaded area is the total queuing time.
    Used in 16-dynamic-assignment-and-simulation
    (fig-16-bottleneck-cumulative).
    """
    N, s, ts, te, tt, tstar = 5000, 2000, 6.5, 9.0, 7.5, 8.5
    t = np.linspace(ts, te, 400)
    dep = np.where(t <= tt, 4000 * (t - ts), 4000 + 2000 / 3 * (t - tt))
    arr = s * (t - ts)
    # the two curves meet at t_e with all N commuters through
    assert abs(dep[-1] - N) < 1e-6 and abs(arr[-1] - N) < 1e-6
    fig, ax = plt.subplots(figsize=(6.0, 3.8))
    ax.plot(t, dep / 1000, color=BLUE, lw=2, label=t_(lang, "cumulative departures", "累计出发量") + " $R(t)$")
    ax.plot(t, arr / 1000, color=ORANGE, lw=2,
            label=t_(lang, "cumulative exits from the bottleneck (rate $s$)", "瓶颈累计驶离量（速率 $s$）"))
    ax.fill_between(t, arr / 1000, dep / 1000, color=BLUE, alpha=0.10, lw=0)
    # maximum queue at the last on-time departure
    ax.vlines(tt, s * (tt - ts) / 1000, 4.0, color=INK, lw=1, ls="--")
    ax.annotate(t_(lang, "maximum queue\n2 000 cars", "最大排队\n2 000 辆"), xy=(tt, 3.0), xytext=(7.62, 0.55),
                fontsize=9, color=INK, arrowprops=dict(arrowstyle="->", color=MUTED, lw=0.8))
    ax.axvline(tstar, color=MUTED, lw=1, ls=":")
    ax.annotate("$t^*$ = 8:30", (tstar, 0.3), textcoords="offset points", xytext=(4, 0), fontsize=9, color=MUTED)
    ax.set_xticks([6.5, 7.5, 8.5, 9.0], ["6:30\n$t_s$", "7:30\n$\\tilde t$", "8:30", "9:00\n$t_e$"])
    ax.set_xlabel(t_(lang, "clock time", "时刻"))
    ax.set_ylabel(t_(lang, "cumulative vehicles (thousands)", "累计车辆数（千辆）"))
    ax.set_ylim(0, 5.3)
    ax.legend(loc="upper left", fontsize=8.5)
    return save_mpl(fig, outdir, "16-bottleneck-cumulative")


FIGURES = {"16-bottleneck-cumulative": bottleneck_cumulative}
