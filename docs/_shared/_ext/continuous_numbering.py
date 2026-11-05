"""Book-wide chapter numbers for a book whose parts are separate toctrees.

Sphinx restarts chapter numbers in every ``:numbered:`` toctree, so the
first chapter of Part II would be "1" again. Worse, it keys its figure,
table, equation and theorem counters on that *local* number, so chapters at
the same position in different parts share one counter (the first figure of
the first chapter of Part II would be "1.2" if the first chapter of Part I
already has a figure).

After the toctree collector has run, this extension walks the numbered
toctrees of the root document in order and gives each chapter its number:

``book_numbering = "continuous"``
    chapters run 1, 2, ..., N across all parts; inside chapter 7 the
    numbers are 7.1, 7.2, ...
``book_numbering = "part"``
    the c-th chapter of part p is chapter p.c; its numbers are p.c.1, ...

It rewrites the section numbers (headings, previous/next links, the
navigation) and renumbers every figure, table, code block, equation and
sphinx-proof block as prefix + (k,), with k counting from 1 per type in
document order. Unnumbered toctrees (the appendix) are left alone.
"""

from __future__ import annotations

from docutils import nodes
from sphinx import addnodes


def _numbered_chapters(env):
    """Yield the chapter documents of the numbered toctrees, by part."""
    root = env.config.root_doc
    doctree = env.get_doctree(root)
    for part, toctree in enumerate(
        (t for t in doctree.findall(addnodes.toctree) if t.get("numbered")),
        start=1,
    ):
        yield part, [docname for _title, docname in toctree["entries"]]


def _renumber(app, env):
    mode = app.config.book_numbering
    global_index = 0
    for part, chapters in _numbered_chapters(env):
        for local, docname in enumerate(chapters, start=1):
            global_index += 1
            prefix = (part, local) if mode == "part" else (global_index,)

            numbers = env.toc_secnumbers.get(docname)
            if numbers:
                renumbered = {
                    anchor: prefix + tuple(number[1:])
                    for anchor, number in numbers.items()
                }
                env.toc_secnumbers[docname] = renumbered
                title = env.titles.get(docname)
                if title is not None and title.get("secnumber"):
                    title["secnumber"] = list(prefix) + list(title["secnumber"][1:])
                toc = env.tocs.get(docname)
                if toc is not None:
                    for ref in toc.findall(nodes.reference):
                        if "secnumber" in ref:
                            ref["secnumber"] = renumbered.get(
                                ref.get("anchorname", ""), ref["secnumber"]
                            )

            # Figures, tables, code blocks, equations, proof blocks: number
            # per type from 1 in document order (the order Sphinx assigned).
            for figtype, ids in env.toc_fignumbers.get(docname, {}).items():
                ordered = sorted(ids.items(), key=lambda item: item[1])
                for k, (node_id, _old) in enumerate(ordered, start=1):
                    ids[node_id] = prefix + (k,)
    return []


def setup(app):
    app.add_config_value("book_numbering", "part", "env")
    # Run after Sphinx's own TocTreeCollector (default priority 500).
    app.connect("env-get-updated", _renumber, priority=900)
    return {"parallel_read_safe": True, "parallel_write_safe": True}
