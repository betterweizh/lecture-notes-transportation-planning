"""Figures of chapter 6 (Zoning Systems and Network Representation)."""

from __future__ import annotations

import numpy as np

from common import AQUA, BLUE, INK, LIGHT_BLUE, MUTED, ORANGE, t_, write_svg


def junction_coding(outdir, lang="en"):
    """Two ways of coding a four-arm junction (left-hand traffic).

    (a) the junction as one node J; (b) the expanded junction with an
    external, an entry and an exit node per approach and one link per
    movement. Used in 06-zoning-and-networks (fig-06-junction-coding).
    """
    out = []

    def trim(p, q, rp, rq, gap=1.5):
        # shorten segment p->q so that it starts and ends on circle edges
        dx, dy = q[0] - p[0], q[1] - p[1]
        L = np.hypot(dx, dy)
        ux, uy = dx / L, dy / L
        a = (p[0] + ux * (rp + gap), p[1] + uy * (rp + gap))
        b = (q[0] - ux * (rq + gap), q[1] - uy * (rq + gap))
        return a, b

    def line(p, q, rp, rq, color=INK, m="arr", w=1.5):
        a, b = trim(p, q, rp, rq)
        out.append(
            f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" '
            f'stroke="{color}" stroke-width="{w}" marker-end="url(#{m})"/>'
        )

    def node(c, r, label=None, fill="#ffffff", stroke=MUTED, fs=10.5):
        out.append(
            f'<circle cx="{c[0]}" cy="{c[1]}" r="{r}" fill="{fill}" '
            f'stroke="{stroke}" stroke-width="1.4"/>'
        )
        if label:
            out.append(
                f'<text x="{c[0]}" y="{c[1] + 4}" text-anchor="middle" '
                f'font-size="{fs}" fill="{INK}">{label}</text>'
            )

    def lab(x, y, base, sup, anchor="start"):
        out.append(
            f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="12" '
            f'font-style="italic" fill="{INK}">{base}<tspan font-size="8.5" '
            f'font-style="normal" dy="-5">{sup}</tspan></text>'
        )

    # (a) single node J with two-way links to the four approaches
    out.append(
        f'<text x="150" y="22" text-anchor="middle" fill="{INK}" font-weight="600">'
        + t_(lang, "(a) junction as a single node", "(a) 交叉口编码为单个节点")
        + "</text>"
    )
    J, rJ, rX, d = (150, 165), 13, 11, 6
    ext = {"N": (150, 50), "S": (150, 280), "W": (35, 165), "E": (265, 165)}
    rin_j, rin_x = np.sqrt(rJ**2 - d**2), np.sqrt(rX**2 - d**2)
    for k, c in ext.items():
        vert = k in "NS"
        # keep left: offset of the inbound link
        sgn = {"N": 1, "S": -1, "W": -1, "E": 1}[k]

        def off(p, s, vert=vert):
            return (p[0] + s * d, p[1]) if vert else (p[0], p[1] + s * d)

        line(off(c, sgn), off(J, sgn), rin_x, rin_j)
        line(off(J, -sgn), off(c, -sgn), rin_j, rin_x)
        node(c, rX, k)
    node(J, rJ, "J", fill=LIGHT_BLUE, stroke=BLUE, fs=11)
    out.append(
        f'<text x="150" y="345" text-anchor="middle" font-size="11.5" fill="{MUTED}">'
        + t_(lang, "turning delays cannot be distinguished", "无法区分各转向的延误")
        + "</text>"
    )

    # (b) external, entry, and exit node per approach; one link per movement
    cx, cy = 505, 170
    out.append(
        f'<text x="{cx}" y="22" text-anchor="middle" fill="{INK}" font-weight="600">'
        + t_(lang, "(b) expanded junction: one link per movement", "(b) 展开的交叉口：每个流向一条路段")
        + "</text>"
    )
    r, rE, o, D = 6.5, 11, 16, 52
    n = {
        "Nin": (cx + o, cy - D), "Nout": (cx - o, cy - D),
        "Sin": (cx - o, cy + D), "Sout": (cx + o, cy + D),
        "Win": (cx - D, cy - o), "Wout": (cx - D, cy + o),
        "Ein": (cx + D, cy + o), "Eout": (cx + D, cy - o),
    }
    X = {"N": (cx, 50), "S": (cx, 290), "W": (cx - 125, cy), "E": (cx + 125, cy)}
    for k, c in X.items():
        line(c, n[k + "in"], rE, r)
        line(n[k + "out"], c, r, rE)

    def curve(p, ctrl, q, col, m):
        a, _ = trim(p, ctrl, r, 0)
        _, b = trim(ctrl, q, 0, r)
        out.append(
            f'<path d="M{a[0]:.1f},{a[1]:.1f} Q{ctrl[0]},{ctrl[1]} '
            f'{b[0]:.1f},{b[1]:.1f}" fill="none" stroke="{col}" '
            f'stroke-width="1.8" marker-end="url(#{m})"/>'
        )

    # the three movements from the west entry node
    W = n["Win"]
    line(W, n["Eout"], r, r, color=BLUE, m="arrb", w=1.8)
    curve(W, (cx - o, cy - o - 6), n["Nout"], AQUA, "arrg")
    curve(W, (cx + o + 6, cy - o + 4), n["Sout"], ORANGE, "arro")
    for c in n.values():
        node(c, r)
    for k, c in X.items():
        node(c, rE, k)
    lab(n["Win"][0] - 10, n["Win"][1] - 9, "W", "in", "end")
    lab(n["Nout"][0] - 10, n["Nout"][1] - 4, "N", "out", "end")
    lab(n["Eout"][0] + 10, n["Eout"][1] - 9, "E", "out")
    lab(n["Sout"][0] + 11, n["Sout"][1] + 5, "S", "out")
    # legend
    ly = 324
    legend = (
        (340, BLUE, t_(lang, "through", "直行")),
        (440, AQUA, t_(lang, "left turn (free)", "左转（不受信号控制）")),
        (575, ORANGE, t_(lang, "right turn (signal)", "右转（信号控制）")),
    )
    if lang == "zh":
        legend = ((330, BLUE, legend[0][2]), (400, AQUA, legend[1][2]), (555, ORANGE, legend[2][2]))
    for x, col, t in legend:
        out.append(
            f'<line x1="{x}" y1="{ly - 4}" x2="{x + 22}" y2="{ly - 4}" '
            f'stroke="{col}" stroke-width="2.2"/>'
        )
        out.append(f'<text x="{x + 28}" y="{ly}" font-size="11" fill="{INK}">{t}</text>')
    out.append(
        f'<text x="{cx}" y="345" text-anchor="middle" font-size="11.5" fill="{MUTED}">'
        + t_(lang, "movements from the west entry node shown (left-hand traffic)",
             "图中只画出西进口的各流向（靠左行驶）")
        + "</text>"
    )
    return write_svg(outdir, "06-junction-coding", "\n".join(out) + "\n", 700, 350)


FIGURES = {"06-junction-coding": junction_coding}
