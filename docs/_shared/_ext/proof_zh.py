"""Chinese names for sphinx-proof blocks ("例 3.1", not "例子 3.1").

sphinx-proof ships its own zh_CN catalog, which translates "Example" as
"例子". Chinese textbooks write "例". Sphinx keeps the first catalog that is
registered for a message domain, so this extension must be listed *before*
``sphinx_proof`` in ``extensions``. The catalog lives in
``docs/_shared/locales/zh_CN/LC_MESSAGES/proof.po`` (and the compiled
``proof.mo``, which is tracked in git).
"""

from __future__ import annotations

from pathlib import Path

LOCALE_DIR = Path(__file__).resolve().parents[1] / "locales"


def setup(app):
    app.add_message_catalog("proof", str(LOCALE_DIR))
    return {"parallel_read_safe": True, "parallel_write_safe": True}
