#!/usr/bin/env python3
"""Draw the generated figures of the book.

One module per chapter in ``scripts/figures/`` (``chNN.py`` for chapter NN)
defines ``FIGURES = {name: function}``; each function draws exactly one
``<name>.svg``. This script merges all modules and draws the requested
figures into ``docs/<lang>/figures/``::

    python scripts/make_figures.py                      # all, English
    python scripts/make_figures.py --lang zh            # all, Chinese labels
    python scripts/make_figures.py --lang en 13-six-node-network
    python scripts/make_figures.py --list

``scripts/build_docs.py`` calls this script for every figure that is missing
or older than its module, so it rarely needs to be run by hand.
"""

from __future__ import annotations

import argparse
import importlib
import re
import sys
from contextlib import nullcontext
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
FIG_DIR = Path(__file__).resolve().parent / "figures"
sys.path.insert(0, str(FIG_DIR))

# Only chapter modules count as figure modules (not common.py, _example.py).
MODULE_PATTERN = re.compile(r"^ch\d{2}\.py$")


def load_figures() -> dict:
    """Return {figure name: (function, module path)} over all chapter modules."""
    figures: dict = {}
    for path in sorted(FIG_DIR.glob("*.py")):
        if not MODULE_PATTERN.match(path.name):
            continue
        module = importlib.import_module(path.stem)
        for name, func in getattr(module, "FIGURES", {}).items():
            if name in figures:
                raise SystemExit(
                    f"duplicate figure name {name!r} in {path.name} and "
                    f"{figures[name][1].name}"
                )
            if not name.startswith(path.stem[2:] + "-"):
                raise SystemExit(f"figure {name!r} in {path.name} must start with {path.stem[2:]}-")
            figures[name] = (func, path)
    return figures


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("names", nargs="*", help="figure names (default: all)")
    parser.add_argument("--lang", default="en", choices=("en", "zh"))
    parser.add_argument("--outdir", type=Path, help="default: docs/<lang>/figures")
    parser.add_argument("--list", action="store_true", help="list the figures and exit")
    args = parser.parse_args(argv)

    figures = load_figures()
    if args.list:
        for name, (_func, path) in figures.items():
            print(f"{name}  ({path.name})")
        return 0
    unknown = [n for n in args.names if n not in figures]
    if unknown:
        raise SystemExit("unknown figure(s): " + ", ".join(unknown))
    outdir = args.outdir or REPO_ROOT / "docs" / args.lang / "figures"
    outdir.mkdir(parents=True, exist_ok=True)

    import matplotlib as mpl
    from common import ZH_RC

    context = mpl.rc_context(ZH_RC) if args.lang == "zh" else nullcontext()
    with context:
        for name in args.names or figures:
            func, _path = figures[name]
            path = func(outdir, lang=args.lang)
            print("wrote", Path(path).relative_to(REPO_ROOT) if Path(path).is_relative_to(REPO_ROOT) else path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
