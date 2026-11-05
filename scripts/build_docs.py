#!/usr/bin/env python3
"""Build the bilingual Sphinx site.

Usage (from the repository root)::

    python scripts/build_docs.py            # build English and Chinese
    python scripts/build_docs.py --strict   # treat warnings as errors (CI)
    python scripts/build_docs.py --serve    # build, then serve on :8000
    python scripts/build_docs.py --clean    # remove _build first
    python scripts/build_docs.py --lang zh  # build one edition only
    python scripts/build_docs.py --prune-legacy  # delete old chapter files and figures
    python scripts/build_docs.py --figures-only  # only assemble docs/<lang>/figures/

Output::

    _build/html/index.html   redirects to /en/ or /zh/ (reader's preference)
    _build/html/en/          English edition
    _build/html/zh/          Chinese edition

Figures: files in docs/_shared/figures/ are copied into every edition;
generated figures are drawn by scripts/make_figures.py when missing or
older than their module (scripts/figures/chNN.py). The Python chapters
(Part V) are plain code blocks and are not executed.
"""

from __future__ import annotations

import argparse
import functools
import re
import http.server
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DOCS = REPO_ROOT / "docs"
OUT = REPO_ROOT / "_build" / "html"
LANGS = ("en", "zh")
TEMPLATES = REPO_ROOT / "scripts" / "templates"
SHARED_FIGURES = DOCS / "_shared" / "figures"
COMMON_MODULE = REPO_ROOT / "scripts" / "figures" / "common.py"
# Figure modules of the old layout (one script for all figures).
LEGACY_FIGURE_MODULES: list[str] = []  # none yet

sys.path.insert(0, str(DOCS / "_shared"))
from conf_common import LEGACY_CHAPTER_FILES  # noqa: E402
# Files that are created from scripts/templates/ when they are missing.
GENERATED = {
    DOCS / "en" / "conf.py": TEMPLATES / "conf_en.py",
    DOCS / "zh" / "conf.py": TEMPLATES / "conf_zh.py",
    REPO_ROOT / ".github" / "workflows" / "docs.yml": TEMPLATES / "github-workflow-docs.yml",
}

ROOT_INDEX = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Lecture Notes on Transportation Planning · 交通规划学习笔记</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="alternate" hreflang="en" href="en/index.html">
  <link rel="alternate" hreflang="zh-CN" href="zh/index.html">
  <noscript><meta http-equiv="refresh" content="0; url=en/index.html"></noscript>
  <script>
    (function () {
      var lang = null;
      try { lang = localStorage.getItem("lntp-preferred-language"); } catch (e) {}
      if (lang !== "en" && lang !== "zh") {
        var nav = (navigator.languages && navigator.languages[0]) || navigator.language || "";
        lang = nav.toLowerCase().indexOf("zh") === 0 ? "zh" : "en";
      }
      window.location.replace(lang + "/index.html");
    })();
  </script>
  <style>
    body { font-family: system-ui, sans-serif; display: grid; place-items: center;
           min-height: 90vh; margin: 0; background: #fff; color: #222; }
    a { margin: 0 .75rem; font-size: 1.15rem; }
    @media (prefers-color-scheme: dark) { body { background: #14181e; color: #ddd; } a { color: #79b0ef; } }
  </style>
</head>
<body>
  <p><a href="en/index.html">English</a> | <a href="zh/index.html">中文</a></p>
</body>
</html>
"""


def ensure_generated_files() -> None:
    """Create conf.py and the GitHub workflow from their templates if missing."""
    for target, template in GENERATED.items():
        if not target.exists() and template.exists():
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(template.read_text(encoding="utf-8"), encoding="utf-8")
            print(f"created {target.relative_to(REPO_ROOT)} from {template.relative_to(REPO_ROOT)}")


def _figure_names(md_text: str) -> list[str]:
    return re.findall(r"figures/([\w.-]+\.(?:svg|png|jpe?g|gif))", md_text)


def _editions() -> list[str]:
    return [lang for lang in LANGS if (DOCS / lang / "conf.py").exists()]


def assemble_figures(langs) -> None:
    """Put every figure an edition references into docs/<lang>/figures/.

    1. Copy the existing (reused) figures of docs/_shared/figures/.
    2. Draw, with scripts/make_figures.py --lang <lang>, every referenced
       figure that is missing or older than its generator module.
    A reference with neither a file nor a generator stops the build.
    """
    sys.path.insert(0, str(REPO_ROOT / "scripts"))
    from make_figures import load_figures  # noqa: E402

    generators = load_figures()
    shared = {p.name for p in SHARED_FIGURES.glob("*") if p.is_file() and p.name != "SOURCES.md"}
    for name in sorted(shared):
        if Path(name).stem in generators:
            print(f"warning: figure {name} exists in docs/_shared/figures/ and has a generator")
    problems = []
    for lang in langs:
        target = DOCS / lang / "figures"
        target.mkdir(parents=True, exist_ok=True)
        for name in shared:
            src, dst = SHARED_FIGURES / name, target / name
            if not dst.exists() or dst.stat().st_mtime < src.stat().st_mtime:
                shutil.copy2(src, dst)
        todo = []
        for md in sorted((DOCS / lang).glob("*.md")):
            if md.name in LEGACY_CHAPTER_FILES:
                continue
            for name in _figure_names(md.read_text(encoding="utf-8")):
                stem = Path(name).stem
                if name in shared:
                    continue
                if stem not in generators:
                    problems.append(f"docs/{lang}/{md.name}: figure {name} has no file in "
                                    "docs/_shared/figures/ and no generator in scripts/figures/")
                    continue
                dst = target / name
                module = generators[stem][1]
                newest = max(module.stat().st_mtime, COMMON_MODULE.stat().st_mtime)
                if (not dst.exists() or dst.stat().st_mtime < newest) and stem not in todo:
                    todo.append(stem)
        if todo:
            print(f"[{lang}] drawing {len(todo)} figure(s)", flush=True)
            subprocess.run([sys.executable, str(REPO_ROOT / "scripts" / "make_figures.py"),
                            "--lang", lang, *todo], check=True, cwd=REPO_ROOT)
    if problems:
        legacy = [p for lang in LANGS for p in (DOCS / lang).glob("*.md") if p.name in LEGACY_CHAPTER_FILES]
        hint = ("\nOld chapter files are still on disk; run with --prune-legacy." if legacy else "")
        raise SystemExit("\n".join(problems) + hint)


def build(lang: str, strict: bool, quiet: bool = False) -> None:
    cmd = [
        sys.executable, "-m", "sphinx",
        "-b", "html",
        str(DOCS / lang),
        str(OUT / lang),
    ]
    if strict:
        cmd[3:3] = ["-W", "--keep-going"]
    if quiet:
        cmd[3:3] = ["-q"]
    print(f"\n=== Building '{lang}' edition ===\n$ {' '.join(cmd)}", flush=True)
    subprocess.run(cmd, check=True, cwd=REPO_ROOT)


def write_root_files() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "index.html").write_text(ROOT_INDEX, encoding="utf-8")
    (OUT / ".nojekyll").write_text("", encoding="utf-8")  # GitHub Pages: keep _static/


def serve(port: int) -> None:
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(OUT))
    with http.server.ThreadingHTTPServer(("127.0.0.1", port), handler) as httpd:
        print(f"\nServing {OUT} at http://127.0.0.1:{port}/  (Ctrl+C to stop)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass


def report_legacy_files(delete: bool = False) -> None:
    """List (or delete) chapter files and figure modules with old names."""
    old = [DOCS / lang / name for lang in LANGS for name in LEGACY_CHAPTER_FILES
           if (DOCS / lang / name).exists()]
    old += [REPO_ROOT / rel for rel in LEGACY_FIGURE_MODULES if (REPO_ROOT / rel).exists()]
    # figures with old names left in the assembled folders
    for lang in LANGS:
        folder = DOCS / lang / "figures"
        if folder.exists():
            shared = {q.name for q in SHARED_FIGURES.glob("*")}
            old += [p for p in folder.iterdir()
                    if p.is_file() and p.name not in shared and not re.match(r"^\d{2}-", p.name)]
    old = sorted(set(old))
    if not old:
        return
    names = ", ".join(str(p.relative_to(REPO_ROOT)) for p in old)
    if delete:
        for p in old:
            p.unlink()
        print(f"Deleted {len(old)} legacy file(s): {names}")
    else:
        print(f"Note: {len(old)} legacy file(s) are not used; delete them with --prune-legacy: {names}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--lang", choices=LANGS, action="append", help="edition(s) to build (default: all)")
    parser.add_argument("--strict", action="store_true", help="fail on warnings")
    parser.add_argument("--clean", action="store_true", help="delete _build before building")
    parser.add_argument("--serve", action="store_true", help="serve the site after building")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--prune-legacy", action="store_true", help="delete chapter files and figures with old names")
    parser.add_argument("--figures-only", action="store_true", help="assemble the figures and stop")
    parser.add_argument("--outdir", type=Path, help="output folder (default: _build/html)")
    parser.add_argument("--quiet", action="store_true", help="pass -q to Sphinx")
    args = parser.parse_args()
    global OUT
    if args.outdir:
        OUT = args.outdir.resolve()

    ensure_generated_files()
    report_legacy_files(delete=args.prune_legacy)
    if args.clean and OUT.exists():
        shutil.rmtree(OUT)
    langs = args.lang or _editions()
    assemble_figures(langs)
    if args.figures_only:
        return 0
    for lang in langs:
        build(lang, args.strict, args.quiet)
    write_root_files()
    print(f"\nDone. Open {OUT / 'index.html'}")
    if args.serve:
        serve(args.port)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
