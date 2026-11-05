"""Sphinx configuration shared by the English and Chinese editions.

Each language has its own ``conf.py`` (``docs/en/conf.py`` and
``docs/zh/conf.py``). Both import everything from this module and then set
only the language-specific values (language code, titles, labels). The two
editions use identical file names, which the language switch relies on.
"""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from datetime import date
from pathlib import Path

SHARED_DIR = Path(__file__).resolve().parent
DOCS_DIR = SHARED_DIR.parent
REPO_ROOT = DOCS_DIR.parent

sys.path.insert(0, str(SHARED_DIR / "_ext"))

# -- Project information -----------------------------------------------------

author = "Better W.Z."
copyright = f"{date.today().year}, {author}. MIT License"

# The editions. The key is the output folder name under _build/html/.
LANGUAGES = {
    "en": {"sphinx": "en", "label": "English", "short": "EN", "toc_title": "Contents"},
    "zh": {"sphinx": "zh_CN", "label": "中文", "short": "中文", "toc_title": "本页目录"},
}


def _available(module: str) -> bool:
    return importlib.util.find_spec(module) is not None


def _detect_repository_url() -> str | None:
    """Return the GitHub URL of this repository, if it can be found.

    Order of precedence: the ``DOCS_REPO_URL`` environment variable, the
    ``GITHUB_REPOSITORY`` variable set by GitHub Actions, and finally the
    ``origin`` remote of the local git checkout.
    """
    if os.environ.get("DOCS_REPO_URL"):
        return os.environ["DOCS_REPO_URL"].rstrip("/")
    if os.environ.get("GITHUB_REPOSITORY"):
        return f"https://github.com/{os.environ['GITHUB_REPOSITORY']}"
    try:
        url = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return None
    if url.startswith("git@github.com:"):
        url = "https://github.com/" + url.split(":", 1)[1]
    url = url.removesuffix(".git")
    return url if url.startswith("https://github.com/") else None


REPOSITORY_URL = _detect_repository_url()


def _detect_branch() -> str:
    """Branch for the "edit this page" button: env var, git branch, or main."""
    if os.environ.get("DOCS_REPO_BRANCH"):
        return os.environ["DOCS_REPO_BRANCH"]
    try:
        branch = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            check=True,
        ).stdout.strip()
    except (OSError, subprocess.CalledProcessError):
        return "main"
    return branch if branch and branch != "HEAD" else "main"


REPOSITORY_BRANCH = _detect_branch()

# -- General configuration ---------------------------------------------------

# The Python chapters (Part V) show code in plain ```python blocks; nothing
# is executed when the site is built.
HAS_BOOK_THEME = _available("sphinx_book_theme")

extensions = [
    "myst_parser",
    "sphinx.ext.mathjax",
    # proof_zh must come before sphinx_proof: Sphinx keeps the first message
    # catalog registered for a domain ("例 3.1" instead of "例子 3.1").
    "proof_zh",
    "sphinx_proof",
    "sphinx_copybutton",
    "sphinx_design",
    "continuous_numbering",
    "lang_switch",
]
source_suffix = {".md": "markdown"}
root_doc = "index"
exclude_patterns = [
    "_build", "Thumbs.db", ".DS_Store",
    "**/README.md",
    # Safety net: the original notes (file names with spaces) live in
    # sources/; never publish copies accidentally left in docs/.
    "* *.md",
]

# Chapter files are named "NN-topic.md" (chapter number first). Copies with
# old names (unnumbered, or numbered before chapters were merged) and the
# removed errata page may survive in a local checkout; exclude them so that
# they are not built as orphan pages. They can be deleted.
LEGACY_CHAPTER_FILES = [
    "11-entropy-maximization.md",
    "12-discrete-choice-models.md",
    "13-aggregate-modal-split.md",
    "14-user-equilibrium-assignment.md",
    "15-system-optimum-and-elastic-demand.md",
    "16-stochastic-user-equilibrium.md",
    "17-dynamic-assignment-and-simulation.md",
    "18-examples-probability.md",
    "19-examples-regression.md",
    "20-examples-optimization.md",
    "21-examples-biproportional-fitting.md",
    "22-examples-zoning-and-networks.md",
    "23-examples-sampling.md",
    "24-examples-errors.md",
    "25-examples-trip-generation.md",
    "26-examples-trip-distribution.md",
    "27-examples-discrete-choice.md",
    "28-examples-modal-split.md",
    "29-examples-user-equilibrium.md",
    "30-examples-system-optimum-and-elastic-demand.md",
    "31-examples-stochastic-user-equilibrium.md",
    "32-examples-dynamic-assignment.md",
    "33-python-foundations.md",
    "34-python-trip-generation.md",
    "35-python-trip-distribution.md",
    "36-python-mode-choice.md",
    "37-python-traffic-assignment.md",
    "errata.md",
    "probability-distributions.md",
    "regression-and-hypothesis-tests.md",
    "nonlinear-optimization.md",
    "transportation-planning-process.md",
    "zoning-and-networks.md",
    "travel-surveys-and-sampling.md",
    "errors-and-uncertainty.md",
    "trip-generation.md",
    "trip-distribution.md",
    "entropy-and-biproportional-models.md",
    "discrete-choice-models.md",
    "aggregate-modal-split.md",
    "user-equilibrium-assignment.md",
    "system-optimum-and-elastic-demand.md",
    "stochastic-user-equilibrium.md",
    "dynamic-assignment-and-simulation.md",
    "examples-probability.md",
    "examples-regression.md",
    "examples-optimization.md",
    "examples-zoning-and-networks.md",
    "examples-sampling.md",
    "examples-errors.md",
    "examples-trip-generation.md",
    "examples-trip-distribution.md",
    "examples-discrete-choice.md",
    "examples-modal-split.md",
    "examples-user-equilibrium.md",
    "examples-system-optimum-and-elastic-demand.md",
    "examples-stochastic-user-equilibrium.md",
    "examples-dynamic-assignment.md",
    "python-foundations.md",
    "python-trip-generation.md",
    "python-trip-distribution.md",
    "python-mode-choice.md",
    "python-traffic-assignment.md",
]
exclude_patterns += LEGACY_CHAPTER_FILES
templates_path = [str(SHARED_DIR / "_templates")]

# MyST Markdown: $...$ / $$...$$ math, ::: fences for directives, etc.
myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "fieldlist",
    "smartquotes",
]
myst_heading_anchors = 3
myst_dmath_double_inline = True

# Chapters are numbered continuously across the parts (1 ... 36); equations,
# figures, tables and proof-style blocks are numbered per chapter, e.g.
# "(9.3)", "Example 24.2", "Figure 13.1". See _ext/continuous_numbering.py.
BOOK_NUMBERING = "continuous"
book_numbering = BOOK_NUMBERING
math_numfig = True
numfig = True
numfig_secnum_depth = 1
math_eqref_format = "({number})"

# Caption and reference prefixes per language (applied by apply_language).
NUMFIG_FORMATS = {
    "en": {"figure": "Figure %s", "table": "Table %s", "code-block": "Listing %s", "section": "Section %s"},
    "zh": {"figure": "图 %s", "table": "表 %s", "code-block": "代码 %s", "section": "第 %s 节"},
}

# MathJax 3: shared macros keep the notation identical in every chapter.
# Every macro and its meaning:
MACROS = {
    # sets, operators, probability
    "R": r"\mathbb{R}",                       # real numbers
    "E": r"\mathbb{E}",                       # expectation
    "Prob": r"\mathbb{P}",                    # probability
    "Var": r"\operatorname{Var}",             # variance
    "Cov": r"\operatorname{Cov}",             # covariance
    "se": r"\operatorname{se}",               # standard error
    "diag": r"\operatorname{diag}",           # diagonal matrix of a vector
    "T": r"^{\top}",                          # transpose
    "diff": r"\mathrm{d}",                    # differential d (upright)
    "argmin": r"\operatorname*{arg\,min}",    # minimizer
    # vectors (lower case) and matrices (upper case), bold
    "ba": r"\mathbf{a}",                      # balancing factors (vector of a_i)
    "bb": r"\mathbf{b}",                      # right-hand side / balancing factors b_j
    "bc": r"\mathbf{c}",                      # cost vector
    "bd": r"\mathbf{d}",                      # search direction
    "bff": r"\mathbf{f}",                     # path-flow vector (\bf is taken by TeX)
    "bg": r"\mathbf{g}",                      # constraint vector / gradient
    "bq": r"\mathbf{q}",                      # O-D demand vector
    "bt": r"\mathbf{t}",                      # seed (prior) trip matrix / link-time vector
    "bu": r"\mathbf{u}",                      # utility vector
    "bv": r"\mathbf{v}",                      # auxiliary (all-or-nothing) demand
    "bx": r"\mathbf{x}",                      # link-flow vector / decision variables
    "by": r"\mathbf{y}",                      # response vector / auxiliary flows
    "bz": r"\mathbf{z}",                      # attributes of an alternative
    "bA": r"\mathbf{A}",                      # constraint or transformation matrix
    "bH": r"\mathbf{H}",                      # Hessian matrix
    "bP": r"\mathbf{P}",                      # matrix (e.g. path-choice probabilities)
    "bT": r"\mathbf{T}",                      # trip matrix
    "bX": r"\mathbf{X}",                      # design matrix / random vector
    "bzero": r"\mathbf{0}",                   # zero vector
    # bold Greek
    "balpha": r"\boldsymbol{\alpha}",         # coefficient vector
    "bbeta": r"\boldsymbol{\beta}",           # regression / utility coefficients
    "btheta": r"\boldsymbol{\theta}",         # parameter vector
    "blambda": r"\boldsymbol{\lambda}",       # Lagrange multipliers
    "bmu": r"\boldsymbol{\mu}",               # mean vector
    "bSigma": r"\boldsymbol{\Sigma}",         # covariance matrix
    "bDelta": r"\boldsymbol{\Delta}",         # link-path incidence matrix
    "bvarepsilon": r"\boldsymbol{\varepsilon}",  # error vector
}
mathjax3_config = {"tex": {"macros": MACROS}}

copybutton_prompt_text = r">>> |\.\.\. |\$ "
copybutton_prompt_is_regexp = True

# -- HTML output -------------------------------------------------------------

html_static_path = [str(SHARED_DIR / "_static")]
html_css_files = ["custom.css"]
html_js_files = ["lang-switch.js", ("open-dropdown.js", {"defer": "defer"})]
html_last_updated_fmt = "%Y-%m-%d"
html_copy_source = True
html_show_sourcelink = False

if HAS_BOOK_THEME:
    html_theme = "sphinx_book_theme"
    html_theme_options = {
        "home_page_in_toc": True,
        "show_toc_level": 2,
        "show_navbar_depth": 1,
        "navigation_with_keys": False,
        "use_download_button": True,
        "use_fullscreen_button": True,
        # The language switch sits in the header next to the standard buttons.
        "article_header_end": ["lang-switch.html", "article-header-buttons.html"],
    }
    if REPOSITORY_URL:
        html_theme_options.update(
            {
                "repository_url": REPOSITORY_URL,
                "repository_branch": REPOSITORY_BRANCH,
                "use_repository_button": True,
                "use_issues_button": True,
                "use_edit_page_button": True,
            }
        )
else:  # pragma: no cover - only for quick previews without the theme
    html_theme = "alabaster"
    html_theme_options = {}
    # Keep the language switch available in plain previews as well.
    html_sidebars = {
        "**": ["lang-switch.html", "about.html", "navigation.html", "searchbox.html"]
    }


def apply_language(lang: str, conf_globals: dict) -> None:
    """Set the values that differ between editions.

    Call this at the end of each language's ``conf.py``::

        apply_language("en", globals())
    """
    info = LANGUAGES[lang]
    conf_globals["language"] = info["sphinx"]
    conf_globals["lang_switch_current"] = lang
    conf_globals["lang_switch_languages"] = LANGUAGES
    conf_globals["numfig_format"] = dict(NUMFIG_FORMATS[lang])
    options = dict(conf_globals["html_theme_options"])
    if HAS_BOOK_THEME:
        options["toc_title"] = info["toc_title"]  # heading of the right-hand page TOC
        if REPOSITORY_URL:
            options["path_to_docs"] = f"docs/{lang}"
    conf_globals["html_theme_options"] = options
