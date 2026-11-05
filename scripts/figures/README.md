# Figure generators

Every figure of the book is generated: no figure is copied from the course
materials. (Reused figures would go to `docs/_shared/figures/`, listed in
`docs/_shared/figures/SOURCES.md`.)

- One module per chapter: `chNN.py` draws the figures of chapter NN. Only
  files named like this are loaded, so `common.py`, `preview.py` and
  `_example.py` never count as figures.
- One commented function per figure, `func(outdir, lang="en")`, that writes
  exactly one `NN-<name>.svg` and returns its path. The module ends with
  `FIGURES = {"NN-<name>": func, ...}`. The file name is also the label
  (`fig-NN-<name>`) and starts with the number of the chapter that first
  shows the figure; a figure reused later keeps its name.
- `common.py` holds the colors, the matplotlib style (`save_mpl`), the SVG
  writer with arrow markers (`write_svg`), `network_svg`, `svg_text` and
  `t_(lang, en, zh)` for labels with words.
- Plots are matplotlib; diagrams and networks are hand-written SVG. Use the
  book's notation in every label.
- Words in a label get a Chinese version through `t_`, with the terms of
  `scripts/glossary.py`. The English output must stay byte-identical when a
  Chinese label changes: compare the md5 of the English SVGs before and
  after.

Commands:

```bash
python scripts/make_figures.py --list
python scripts/make_figures.py --lang zh 06-junction-coding
python scripts/figures/preview.py --lang zh --make --dark 06-junction-coding
```

`scripts/build_docs.py` redraws every figure that a chapter references and
that is missing or older than its module, for each edition.
