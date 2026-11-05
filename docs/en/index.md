# Lecture Notes on Transportation Planning

These notes develop the core models and methods of transportation planning: the representation of a study area by zones and networks, travel surveys and sampling, trip generation, trip distribution, modal split and discrete choice models, and deterministic, stochastic, and dynamic traffic assignment. For each method, the assumptions are stated first, and the method is then derived from first principles. The probability, statistics, and optimization tools needed are reviewed in a preliminaries section.

Some methods are accompanied by worked examples and exercises with complete solutions, and all numerical results have been recomputed and verified with code. The final part implements some of the algorithms in Python and demonstrates how to solve the same models with NumPy, SciPy, pandas, and NetworkX.

These notes are based on lecture notes from the course CE5205 Transportation Planning at the National University of Singapore (lecturer: Prof. MENG Qiang; the author took the course in the 2021/22 academic year). They are further supplemented by the author's personal study notes and classic reference books, in particular Ortúzar and Willumsen's *Modelling Transport* and Sheffi's *Urban Transportation Networks*. All material has been reorganized into a single set of notes with unified notation.

In November 2026, the content was reviewed, revised, and organized with the assistance of Claude Opus 5.5 (Anthropic), translated into Simplified Chinese, and a website was built for it.

The author's knowledge is limited, and these notes inevitably contain omissions and errors. Corrections from readers are sincerely welcome. If you find any problems, please submit feedback via a [GitHub issue](https://github.com/betterweizh/lecture-notes-transportation-planning/issues) to help improve these notes.

:::{admonition} 中文版
:class: tip
A complete Simplified Chinese edition is available. Click the translate icon {fas}`language` at the top right of any page to open the same chapter in the other language.
:::

## How the book is organized

- **Part I — Preliminaries** reviews the mathematical tools used
  throughout the book: the probability distributions behind choice models,
  linear regression and hypothesis tests, nonlinear optimization, and
  bi-proportional matrix balancing with its entropy-maximizing
  interpretation.
- **Part II — Foundations of Transport Modeling** introduces the planning
  process and the four-step model, zoning and network representation,
  travel surveys and sampling, and errors in modeling.
- **Part III — Travel Demand and Network Models** develops the four-step
  model: trip generation; growth-factor and gravity trip distribution;
  discrete choice and aggregate modal split; and deterministic,
  system-optimal, elastic-demand, stochastic, and dynamic traffic
  assignment.
- **Part IV — Examples and Problems** solves the examples and problems of
  Parts I–III step by step, one chapter per topic.
- **Part V — Implementation in Python** implements the models from scratch
  with NumPy and SciPy and reproduces the numbers of Part IV.

Chapters are numbered continuously across the parts, and the figures, tables, examples and equations of chapter 7 are numbered 7.1, 7.2, … Proofs and the solutions of examples and problems are folded: click a **Proof** or **Solution** bar to open it, and try each problem before you look.

{doc}`notation` collects the symbols, {doc}`glossary` lists the English and Chinese terms, and {doc}`references` gathers the literature cited in all chapters.

## License

The text, figures, and code of these notes are released under the
[MIT License](https://opensource.org/license/mit): they may be used, copied,
modified, and redistributed, including commercially, provided that the
copyright notice "Copyright (c) 2026 Better W.Z." and the license text are
kept. The material comes without warranty. The license covers the material
written for these notes; the original course materials and the cited works
remain the property of their authors and publishers.

## How to cite

If you use these notes, please cite them as follows (APA Style):

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

When citing a specific model or result, please consider also citing the
original source given in the chapter's references.

## Table of contents

```{toctree}
:caption: Part I — Preliminaries
:numbered:
:maxdepth: 1

01-probability-distributions
02-regression-and-hypothesis-tests
03-nonlinear-optimization
04-biproportional-fitting
```

```{toctree}
:caption: Part II — Foundations of Transport Modeling
:numbered:
:maxdepth: 1

05-transportation-planning-process
06-zoning-and-networks
07-travel-surveys-and-sampling
08-errors-and-uncertainty
```

```{toctree}
:caption: Part III — Travel Demand and Network Models
:numbered:
:maxdepth: 1

09-trip-generation
10-trip-distribution
11-discrete-choice-models
12-aggregate-modal-split
13-user-equilibrium-assignment
14-system-optimum-and-elastic-demand
15-stochastic-user-equilibrium
16-dynamic-assignment-and-simulation
```

```{toctree}
:caption: Part IV — Examples and Problems
:numbered:
:maxdepth: 1

17-examples-probability
18-examples-regression
19-examples-optimization
20-examples-biproportional-fitting
21-examples-zoning-and-networks
22-examples-sampling
23-examples-errors
24-examples-trip-generation
25-examples-trip-distribution
26-examples-discrete-choice
27-examples-modal-split
28-examples-user-equilibrium
29-examples-system-optimum-and-elastic-demand
30-examples-stochastic-user-equilibrium
31-examples-dynamic-assignment
```

```{toctree}
:caption: Part V — Implementation in Python
:numbered:
:maxdepth: 1

32-python-foundations
33-python-trip-generation
34-python-trip-distribution
35-python-mode-choice
36-python-traffic-assignment
```

```{toctree}
:caption: Appendix
:maxdepth: 1

notation
glossary
references
```