"""Figures of chapter 5 (The Transportation Planning Process)."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from common import BLUE, INK, LIGHT_BLUE, MUTED, ORANGE, save_mpl, t_, write_svg


def demand_supply(outdir, lang="en"):
    """Demand-performance equilibrium in cost space, for two activity levels.

    Used in 05-transportation-planning-process (fig-05-demand-supply-equilibrium).
    The curves are illustrative: an increasing performance (supply) curve and
    two decreasing demand curves for activity levels E1 < E2.
    """
    F = np.linspace(0, 10, 300)
    # performance: travel cost rises with flow
    L_perf = 1 + 0.02 * F**3
    fig, ax = plt.subplots(figsize=(5.6, 3.6))
    ax.plot(F, L_perf, color=BLUE, lw=2, label=t_(lang, "performance (supply)", "性能（供给）") + " $L = P(Q, F, M)$")
    for E, ls, name in ((14, "-", "$E_1$"), (20, "--", "$E_2 > E_1$")):
        # demand drawn in cost space: more trips are made when travel is cheaper
        Fd = np.linspace(0, (E / 2 - 0.2) / 0.9, 300)
        Ld = E / 2 - 0.9 * Fd + 0.5
        ax.plot(Fd, Ld, color=ORANGE, lw=2, ls=ls, label=t_(lang, "demand", "需求") + f" $F = D({name[1:-1]}, L)$")
        # equilibrium: where the two curves cross
        idx = np.argmin(np.abs(np.interp(F, Fd, Ld) - L_perf))
        ax.plot(F[idx], L_perf[idx], "o", ms=7, color=INK, zorder=5)
        # labels sit in clear wedges between the curves, with leader lines
        tx, ty = (0.4, 3.2) if E == 14 else (7.0, 5.8)
        which = name if E == 14 else "$E_2$"
        ax.annotate(
            t_(lang, f"$(F^*, L^*)$ for {which}", f"{which} 下的 $(F^*, L^*)$"),
            (F[idx], L_perf[idx]), xytext=(tx, ty),
            ha="left", va="center", fontsize=9, color=INK,
            arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.8, shrinkB=5),
        )
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 14.5)
    ax.set_xlabel(t_(lang, "traffic flow $F$", "交通流量 $F$"))
    ax.set_ylabel(t_(lang, "travel cost (inverse of level of service)", "出行费用（服务水平的倒数）"))
    ax.set_xticks([])
    ax.set_yticks([])
    ax.legend(loc="upper left", fontsize=8.5)
    return save_mpl(fig, outdir, "05-demand-supply-equilibrium")


def four_step(outdir, lang="en"):
    """The four-step model with the feedback of congested travel times.

    Used in 05-transportation-planning-process (fig-05-four-step-model).
    """
    w, h = 640, 470
    parts = []

    def box(x, y, bw, bh, text, sub=None, accent=False):
        stroke = BLUE if accent else MUTED
        fill = LIGHT_BLUE if accent else "none"
        parts.append(
            f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="8" '
            f'fill="{fill}" stroke="{stroke}" stroke-width="1.6"/>'
        )
        ty = y + bh / 2 + (0 if sub is None else -7) + 5
        parts.append(
            f'<text x="{x + bw / 2}" y="{ty}" text-anchor="middle" fill="{INK}" '
            f'font-weight="600">{text}</text>'
        )
        if sub:
            parts.append(
                f'<text x="{x + bw / 2}" y="{ty + 17}" text-anchor="middle" '
                f'fill="{MUTED}" font-size="11.5">{sub}</text>'
            )

    def arrow(x1, y1, x2, y2, color=INK):
        parts.append(
            f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" '
            f'stroke-width="1.5" marker-end="url(#arr)"/>'
        )

    # inputs: base-year data and the planning-year scenario
    box(20, 15, 270, 52, t_(lang, "Zones, network, base-year data", "小区、网络、基年数据"),
        t_(lang, "land use · population · surveys", "土地利用 · 人口 · 调查"))
    box(350, 15, 270, 52, t_(lang, "Planning-year scenario", "规划年情景"),
        t_(lang, "land use · policies · projects", "土地利用 · 政策 · 项目"))
    arrow(155, 67, 230, 95)
    arrow(485, 67, 410, 95)
    # the four steps, top to bottom
    steps = [
        (t_(lang, "1  Trip generation", "1  出行生成"), t_(lang, "how many trips?  Oᵢ, Dⱼ", "出行量多少？ Oᵢ, Dⱼ")),
        (t_(lang, "2  Trip distribution", "2  出行分布"), t_(lang, "where to?  Tᵢⱼ", "去往何处？ Tᵢⱼ")),
        (t_(lang, "3  Modal split", "3  交通方式划分"), t_(lang, "by which mode?  Tᵢⱼᵐ", "选择何种方式？ Tᵢⱼᵐ")),
        (t_(lang, "4  Traffic assignment", "4  交通分配"), t_(lang, "by which route?  link flows xₐ", "选择哪条路径？ 路段流量 xₐ")),
    ]
    y = 97
    for k, (t, s) in enumerate(steps):
        box(200, y, 240, 54, t, s, accent=True)
        if k < 3:
            arrow(320, y + 54, 320, y + 72)
        y += 72
    # output
    box(200, 400, 240, 52, t_(lang, "Evaluation", "评价"), t_(lang, "level of service · impacts", "服务水平 · 影响"))
    arrow(320, 367, 320, 398)
    # feedback loop: congested times fed back to the demand steps
    parts.append(
        f'<path d="M440,340 C540,340 540,124 442,124" fill="none" stroke="{BLUE}" '
        f'stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#arrb)"/>'
    )
    fb = t_(lang, ["congested", "travel times", "(feedback)"], ["拥堵", "出行时间", "（反馈）"])
    for i, line in enumerate(fb):
        parts.append(f'<text x="548" y="{226 + 16 * i}" fill="{BLUE}" font-size="12">{line}</text>')
    side = t_(lang, [(240, "demand side"), (256, "(steps 1–3)"), (350, "supply meets"), (366, "demand (step 4)")],
              [(240, "需求侧"), (256, "（第 1–3 步）"), (350, "供给与需求"), (366, "相遇（第 4 步）")])
    for yy, line in side:
        parts.append(f'<text x="40" y="{yy}" fill="{MUTED}" font-size="12">{line}</text>')
    return write_svg(outdir, "05-four-step-model", "\n".join(parts) + "\n", w, h)


FIGURES = {
    "05-demand-supply-equilibrium": demand_supply,
    "05-four-step-model": four_step,
}
