"""Style and drawing helpers shared by all figure modules.

Plots are drawn with matplotlib (``save_mpl``); schematics and networks are
hand-written SVG (``write_svg``, ``network_svg``). Every figure has a
transparent background and neutral ink, so that the dark-mode filter in
``custom.css`` (``img.dark-light``) renders it well.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

# ---- Colors -----------------------------------------------------------------
INK = "#2b2b2b"
MUTED = "#6b6b6b"
GRID = "#d9d9d9"
BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
LIGHT_BLUE = "#eaf2fc"

# Fonts of hand-written SVG. CJK fonts follow DejaVu Sans so that Chinese
# labels render; Latin text keeps DejaVu Sans.
CJK_FONTS = "Noto Sans CJK SC, Source Han Sans SC, Microsoft YaHei, PingFang SC, SimHei"
FONT = f"DejaVu Sans, {CJK_FONTS}, Helvetica, Arial, sans-serif"

plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "font.size": 10,
        "axes.edgecolor": MUTED,
        "axes.labelcolor": INK,
        "xtick.color": MUTED,
        "ytick.color": MUTED,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.grid": True,
        "grid.color": GRID,
        "grid.linewidth": 0.6,
        "legend.frameon": False,
        "svg.fonttype": "none",
        "svg.hashsalt": "lecture-notes-transportation-planning",
        "savefig.transparent": True,
    }
)

# matplotlib settings for the Chinese edition: a CJK font first, so that
# labels mixing Chinese text and $...$ math keep their CJK glyphs.
ZH_RC = {
    "font.family": "sans-serif",
    "font.sans-serif": [
        "Noto Sans CJK SC",
        "Source Han Sans SC",
        "Microsoft YaHei",
        "PingFang SC",
        "SimHei",
        "DejaVu Sans",
    ],
    "axes.unicode_minus": False,
}


def t_(lang: str, en: str, zh: str) -> str:
    """Return the label for the edition being drawn."""
    return zh if lang == "zh" else en


def save_mpl(fig, outdir: Path, name: str) -> Path:
    """Save a matplotlib figure as ``<outdir>/<name>.svg`` and close it."""
    path = Path(outdir) / f"{name}.svg"
    # No date in the metadata, so that unchanged figures are byte-identical.
    fig.savefig(path, bbox_inches="tight", metadata={"Date": None})
    plt.close(fig)
    return path


def _marker(mid: str, color: str) -> str:
    return (
        f'  <marker id="{mid}" viewBox="0 0 10 10" refX="9" refY="5" '
        'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
        f'<path d="M0,0 L10,5 L0,10 z" fill="{color}"/></marker>\n'
    )


def write_svg(outdir: Path, name: str, body: str, width: int, height: int) -> Path:
    """Write a hand-made SVG with arrow markers ``arr`` (ink), ``arrb``
    (blue), ``arro`` (orange) and ``arrg`` (green)."""
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}" font-family="{FONT}" font-size="13">\n'
        "<defs>\n"
        + _marker("arr", INK)
        + _marker("arrb", BLUE)
        + _marker("arro", ORANGE)
        + _marker("arrg", AQUA)
        + "</defs>\n"
        + body
        + "</svg>\n"
    )
    path = Path(outdir) / f"{name}.svg"
    path.write_text(svg, encoding="utf-8")
    return path


def svg_text(x, y, text, size=13, color=INK, anchor="start", weight=None, italic=False) -> str:
    """One SVG ``<text>`` element."""
    extra = ""
    if weight:
        extra += f' font-weight="{weight}"'
    if italic:
        extra += ' font-style="italic"'
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" '
        f'fill="{color}"{extra}>{text}</text>'
    )


def text_width(text: str, size: float) -> float:
    """Rough width of a label in px: 0.6 em per Latin, 1 em per CJK character."""
    return sum(size if ord(ch) > 0x2E80 else 0.6 * size for ch in text)


def network_svg(outdir, name, pos, links, w, h, origins=(), dests=(), r=16, notes=()) -> Path:
    """Draw a directed network.

    Parameters
    ----------
    pos : dict
        node -> (x, y) in px.
    links : list of tuple
        (tail, head, label, style, bend); style "" or "new" (dashed orange);
        bend is the curvature in px (0: straight line).
    origins, dests : iterable
        Nodes drawn with a green (origin) or orange (destination) ring.
    notes : list of tuple
        Free labels (x, y, text, anchor, color).
    """
    p = []
    for a, b, lab, style, bend in links:
        (x1, y1), (x2, y2) = pos[a], pos[b]
        n = np.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / n, (y2 - y1) / n
        # left normal of the link direction
        nx, ny = -uy, ux
        color = ORANGE if style == "new" else INK
        dash = ' stroke-dasharray="6 4"' if style == "new" else ""
        marker = "arro" if style == "new" else "arr"
        if bend:
            cx, cy = (x1 + x2) / 2 + nx * bend, (y1 + y2) / 2 + ny * bend

            # start/end points pushed off the node circles along the tangents
            def off(px, py, qx, qy, d):
                m = np.hypot(qx - px, qy - py)
                return px + (qx - px) / m * d, py + (qy - py) / m * d

            sx, sy = off(x1, y1, cx, cy, r + 1)
            ex, ey = off(x2, y2, cx, cy, r + 3)
            p.append(
                f'<path d="M{sx:.1f},{sy:.1f} Q{cx:.1f},{cy:.1f} {ex:.1f},{ey:.1f}" '
                f'fill="none" stroke="{color}" stroke-width="1.6"{dash} '
                f'marker-end="url(#{marker})"/>'
            )
            shift = bend * 0.5 + np.sign(bend) * 13
            lx, ly = (x1 + x2) / 2 + nx * shift, (y1 + y2) / 2 + ny * shift
        else:
            p.append(
                f'<line x1="{x1 + ux * (r + 1):.1f}" y1="{y1 + uy * (r + 1):.1f}" '
                f'x2="{x2 - ux * (r + 3):.1f}" y2="{y2 - uy * (r + 3):.1f}" '
                f'stroke="{color}" stroke-width="1.6"{dash} '
                f'marker-end="url(#{marker})"/>'
            )
            lx, ly = (x1 + x2) / 2 + nx * 14, (y1 + y2) / 2 + ny * 14
        lc = ORANGE if style == "new" else BLUE
        p.append(
            f'<text x="{lx:.1f}" y="{ly + 4:.1f}" text-anchor="middle" '
            f'font-size="12" fill="{lc}">{lab}</text>'
        )
    for k, (x, y) in pos.items():
        stroke = AQUA if k in origins else (ORANGE if k in dests else MUTED)
        width = 2.4 if (k in origins or k in dests) else 1.5
        p.append(
            f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ffffff" '
            f'stroke="{stroke}" stroke-width="{width}"/>'
        )
        p.append(
            f'<text x="{x}" y="{y + 5}" text-anchor="middle" fill="{INK}" '
            f'font-weight="600">{k}</text>'
        )
    for x, y, txt, anchor, col in notes:
        p.append(svg_text(x, y, txt, size=12, color=col, anchor=anchor))
    return write_svg(outdir, name, "\n".join(p) + "\n", w, h)
