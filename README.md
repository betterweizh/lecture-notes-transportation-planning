# Lecture Notes on Transportation Planning · 交通规划学习笔记

**English** | [简体中文](README.zh-CN.md) | [Read online](https://betterweizh.github.io/lecture-notes-transportation-planning/en/) | [在线阅读](https://betterweizh.github.io/lecture-notes-transportation-planning/zh)

These notes develop the core models and methods of transportation planning:
the representation of a study area by zones and networks, travel surveys and
sampling, trip generation, trip distribution, modal split and discrete choice
models, and deterministic, stochastic, and dynamic traffic assignment — with
partial worked examples and Python implementations. For each method, the
assumptions are stated first, and the method is then derived from first
principles. The notes are written in Markdown (MyST) and published as a
bilingual website with [Sphinx](https://www.sphinx-doc.org/) and
[sphinx-book-theme](https://sphinx-book-theme.readthedocs.io/), the theme
used by the [Shapely documentation](https://shapely.readthedocs.io/).

**Feedback:** corrections are welcome as
[GitHub issues](https://github.com/betterweizh/lecture-notes-transportation-planning/issues).

## Language switch

The book is published in two complete editions with identical structure:

| Edition | Source | Built pages |
|---|---|---|
| English | `docs/en/` | `_build/html/en/` |
| 简体中文 (Simplified Chinese) | `docs/zh/` | `_build/html/zh/` |

- Every page has a **translate icon** in the header at the top right. Click
  it to open the **same chapter** in the other language.
- The site root (`index.html`) remembers the reader's last choice
  (browser `localStorage`) and otherwise follows the browser language.
- Both editions use the same file names and labels, so links,
  cross-references, and the switch stay aligned.
- Technical terms follow one glossary, kept in `scripts/glossary.py`, which
  generates the *Glossary* appendix of both editions. In the Chinese edition,
  a term is given with its English original in brackets at its first use in
  each chapter, for example 用户均衡（user equilibrium）.

## Contents

| Part | Chapters |
|---|---|
| I · Preliminaries | 1 Probability Distributions for Demand Modeling · 2 Linear Regression and Hypothesis Tests · 3 Nonlinear Optimization for Network Analysis · 4 Matrix Balancing: Bi-proportional Fitting |
| II · Foundations of Transport Modeling | 5 The Transportation Planning Process · 6 Zoning Systems, Networks, and Data · 7 Travel Surveys and Sampling · 8 Errors and Uncertainty in Modeling |
| III · Travel Demand and Network Models | 9 Trip Generation · 10 Trip Distribution: Growth-Factor and Gravity Models · 11 Modal Split: Discrete Choice Models · 12 Aggregate and Combined Modal-Split Models · 13 Traffic Assignment I: Deterministic User Equilibrium · 14 Traffic Assignment II: System Optimum, Elastic Demand, and Combined Models · 15 Traffic Assignment III: Stochastic User Equilibrium · 16 Traffic Assignment IV: Dynamic Assignment and Simulation |
| IV · Examples and Problems | 17 Probability Distributions · 18 Regression and Hypothesis Tests · 19 Nonlinear Optimization · 20 Bi-proportional Fitting · 21 Zoning and Network Coding · 22 Sampling and Survey Design · 23 Errors and Uncertainty · 24 Trip Generation · 25 Trip Distribution · 26 Modal Split: Discrete Choice · 27 Aggregate and Combined Modal Split · 28 User Equilibrium Assignment · 29 System Optimum, Elastic Demand, and Combined Models · 30 Stochastic User Equilibrium · 31 Dynamic Assignment and Simulation |
| V · Implementation in Python | 32 Preliminaries and Foundations in Python · 33 Trip Generation in Python · 34 Trip Distribution in Python · 35 Mode Choice in Python · 36 Traffic Assignment in Python |
| Appendix | Notation · Glossary (English–Chinese) · References |

## Repository layout

```text
docs/
  _shared/            shared by both editions
    conf_common.py    Sphinx settings, MathJax macros, LANGUAGES, NUMFIG_FORMATS
    _ext/             continuous_numbering.py, lang_switch.py, proof_zh.py
    _templates/       lang-switch.html (the translate icon in the header)
    _static/          custom.css, lang-switch.js, open-dropdown.js
    locales/          Chinese names of proof blocks (proof.po, compiled proof.mo)
  en/                 English edition: conf.py, index.md, NN-<topic>.md per chapter
  zh/                 Chinese edition: same file names as en/
  */figures/          figures assembled at build time (not tracked)
scripts/
  build_docs.py       assembles figures, builds both editions and the root page
  make_figures.py     draws the generated figures into docs/<lang>/figures/
  figures/            common.py, chNN.py (one module per chapter), preview.py, README.md
  glossary.py         English–Chinese glossary; writes both glossary.md pages
  run_code_cells.py   runs the code blocks of the Python chapters
  templates/          conf.py files and GitHub workflow, recreated if missing
.github/workflows/    builds and publishes the site on every push to main
```

The original course materials are kept locally in `sources/` and are never
published (the folder is git-ignored).

## Figures

Every figure is generated: one module per chapter, `scripts/figures/chNN.py`,
draws the figures of chapter NN, each named `NN-<name>.svg` after the chapter
that first shows it (label `fig-NN-<name>`). Figures with words have Chinese
labels and are drawn separately for each edition. Figures reused from other
sources would go to `docs/_shared/figures/` (tracked, listed with their
origin in `SOURCES.md`); none are used at present. See
`scripts/figures/README.md`.

## Build locally

Requires Python 3.10 or later.

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate      macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

python scripts/build_docs.py --serve         # build both editions, open http://127.0.0.1:8000/
python scripts/build_docs.py --strict        # fail on any warning (what CI runs)
python scripts/build_docs.py --lang zh       # build only the Chinese edition
python scripts/build_docs.py --clean         # remove _build/html first
python scripts/build_docs.py --prune-legacy  # delete chapter files and figures with old names
```

Figures are assembled automatically: `build_docs.py` draws every figure that
is missing or older than its module, for each edition. Run
`python scripts/glossary.py` after changing the glossary, and
`python scripts/run_code_cells.py docs/en/3*-python-*.md --quiet` to run the
code of the Python chapters.

## Editing workflow

1. Edit the English chapter in `docs/en/` and make the same change in the
   file with the same name in `docs/zh/`; if a figure changes, edit its
   module in `scripts/figures/`. Keep labels identical in both editions.
2. For a new chapter, add it to the table of contents of both `index.md`
   files.
3. Add new terms to `scripts/glossary.py` and run it.
4. Run `python scripts/build_docs.py --strict` and check both editions.
5. Commit and push. The GitHub workflow builds and publishes the site.

## Writing conventions

- Chapter template: Overview · Learning objectives · Notation · body ·
  Summary and Common Mistakes · References
  (概述 · 学习目标 · 符号说明 · … · 本章回顾 · 参考文献). Examples chapters
  open with one sentence naming the theory chapter; code chapters have
  Setup and Summary sections.
- Worked examples use `{prf:example}` (statement open) followed by a
  folded `{dropdown} Solution` (`解答`) with `:class-container: solution`;
  proofs are folded `{dropdown} Proof` (`证明`) blocks with
  `:class-container: proof`. Headings describe the topic of a problem, not
  its source.
- Chapters are numbered continuously across the parts (1–36); figures,
  tables, examples and equations of chapter 7 are numbered 7.1, 7.2, …
- Labels carry the chapter number: `eq-13-beckmann`, `ex-24-tg-zonal`,
  `fig-13-six-node-network`, `sec-06-zoning-rules`.
- Display equations hold one equation per line; long equations are split
  and aligned at `=`; every referenced equation has a label.
- Python code is formatted with `black -l 79`, with comments on their own
  line above the code they describe and `# Expected:` values that match the
  worked examples. Code stays in English in both editions.
- Shared LaTeX macros (`\bx`, `\bT`, `\Prob`, `\E`, `\Var`, `\T`, …) are
  defined, with their meaning, in `docs/_shared/conf_common.py`.
- American spelling; numbers group thousands with a space (12 500).

## Author and license

Written by **Better W.Z.** In November 2026, the content was reviewed,
revised, and organized with the assistance of Claude Opus 5.5 (Anthropic),
translated into Simplified Chinese, and a website was built for it.
Released under the [MIT License](LICENSE): keep the copyright notice
"Copyright (c) 2026 Better W.Z." and the license text when reusing the
material.

## How to cite

> Better W.Z. (2026). *Lecture notes on transportation planning* [Lecture notes].
> GitHub. <https://github.com/betterweizh/lecture-notes-transportation-planning>

```bibtex
@misc{betterwz2026trpln,
  author       = {Better W.Z.},
  title        = {Lecture Notes on Transportation Planning},
  year         = {2026},
  howpublished = {\url{https://github.com/betterweizh/lecture-notes-transportation-planning}},
  note         = {Lecture notes}
}
```
