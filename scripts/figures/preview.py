#!/usr/bin/env python3
"""Render figures to PNG for a quick look (needs Playwright's Chromium).

    python scripts/figures/preview.py --lang zh --make 06-junction-coding
    python scripts/figures/preview.py --dark --width 520 13-six-node-network

PNGs are written to ``_build/preview/<lang>/``. ``--make`` redraws the
figures first; ``--dark`` applies the dark-mode filter of custom.css.
"""

from __future__ import annotations

import argparse
import base64
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("names", nargs="*", help="figure names (default: all in docs/<lang>/figures)")
    parser.add_argument("--lang", default="en", choices=("en", "zh"))
    parser.add_argument("--make", action="store_true", help="redraw the figures first")
    parser.add_argument("--dark", action="store_true", help="preview with the dark-mode filter")
    parser.add_argument("--width", type=int, default=640, help="display width in px")
    args = parser.parse_args()

    if args.make:
        subprocess.run([sys.executable, str(REPO_ROOT / "scripts" / "make_figures.py"), "--lang", args.lang, *args.names],
                       check=True)
    fig_dir = REPO_ROOT / "docs" / args.lang / "figures"
    svgs = [fig_dir / f"{n}.svg" for n in args.names] if args.names else sorted(fig_dir.glob("*.svg"))
    out = REPO_ROOT / "_build" / "preview" / args.lang
    out.mkdir(parents=True, exist_ok=True)

    from playwright.sync_api import sync_playwright

    style = "filter: invert(0.88) hue-rotate(180deg);" if args.dark else ""
    bg = "#14181e" if args.dark else "#ffffff"
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(device_scale_factor=2)
        for svg in svgs:
            # embed the SVG: a page set from a string cannot load file:// URLs
            data = base64.b64encode(svg.read_bytes()).decode("ascii")
            html = (f'<body style="margin:12px;background:{bg}">'
                    f'<img src="data:image/svg+xml;base64,{data}" '
                    f'style="width:{args.width}px;max-width:100%;{style}"></body>')
            page.set_content(html)
            page.wait_for_load_state("networkidle")
            png = out / (svg.stem + ("-dark" if args.dark else "") + ".png")
            page.locator("img").screenshot(path=str(png))
            print("wrote", png.relative_to(REPO_ROOT))
        browser.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
