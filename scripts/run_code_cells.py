#!/usr/bin/env python3
"""Run the ```python code blocks of a chapter, in order, as one script.

The book does not execute code when it is built. Use this script to check
that the code of the Python chapters (Part V) runs::

    python scripts/run_code_cells.py docs/en/33-python-foundations.md
    python scripts/run_code_cells.py docs/en/*-python-*.md --quiet

Blocks of one chapter share a namespace, as in a notebook. The value of the
last expression of each block is printed (like a notebook output).
"""

from __future__ import annotations

import argparse
import ast
import contextlib
import io
import re
import sys
import time
from pathlib import Path

CELL = re.compile(r"^```python[ \t]*\n(.*?)^```", re.S | re.M)


def run_chapter(path: Path, quiet: bool) -> bool:
    cells = CELL.findall(path.read_text(encoding="utf-8"))
    namespace: dict = {"__name__": "__main__"}
    print(f"=== {path} ({len(cells)} cells)")
    start = time.time()
    for k, code in enumerate(cells, 1):
        code = "\n".join(ln for ln in code.splitlines() if not ln.lstrip().startswith(":tags:"))
        tree = ast.parse(code)
        last = tree.body.pop() if tree.body and isinstance(tree.body[-1], ast.Expr) else None
        buffer = io.StringIO()
        try:
            with contextlib.redirect_stdout(buffer):
                exec(compile(tree, f"{path.name}[cell {k}]", "exec"), namespace)
                if last is not None:
                    value = eval(compile(ast.Expression(last.value), f"{path.name}[cell {k}]", "eval"), namespace)
                    if value is not None:
                        print(value)
        except Exception as exc:  # noqa: BLE001
            print(buffer.getvalue())
            print(f"!!! cell {k} failed: {exc!r}")
            return False
        if not quiet:
            print(f"--- cell {k}\n{buffer.getvalue()}")
    print(f"=== ok in {time.time() - start:.1f} s\n")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("files", nargs="+", type=Path)
    parser.add_argument("--quiet", action="store_true", help="only report success or failure")
    args = parser.parse_args()
    ok = all(run_chapter(p, args.quiet) for p in args.files)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
