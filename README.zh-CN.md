# 交通规划学习笔记 · Lecture Notes on Transportation Planning

[English](README.md) | **中文** | [Read online](https://betterweizh.github.io/lecture-notes-transportation-planning/en/) | [在线阅读](https://betterweizh.github.io/lecture-notes-transportation-planning/zh)


本学习笔记系统阐述交通规划的核心模型与方法：以交通小区和网络表示研究区域、出行调查与抽样、出行生成、出行分布、交通方式划分与离散选择模型，以及确定性、随机和动态交通分配，并配有部分的算例解答和 Python 实现。每种方法均先陈述其假设，再从基本原理出发加以推导。笔记用 Markdown（MyST）编写，通过 [Sphinx](https://www.sphinx-doc.org/) 和 [sphinx-book-theme](https://sphinx-book-theme.readthedocs.io/)（与 [Shapely 文档](https://shapely.readthedocs.io/) 相同的主题）发布为中英双语网站。

**反馈：** 欢迎通过 [GitHub Issue](https://github.com/betterweizh/lecture-notes-transportation-planning/issues) 指出错误。

## 语言切换

本书提供两个结构完全相同的完整版本：

| 版本 | 源文件 | 生成的网页 |
|---|---|---|
| English（英文） | `docs/en/` | `_build/html/en/` |
| 简体中文 | `docs/zh/` | `_build/html/zh/` |

- 每个页面右上角的页眉中都有一个**翻译图标**，点击即可打开另一种语言中的**同一章节**。
- 网站根页面（`index.html`）会记住读者上一次选择的语言（保存在浏览器的 `localStorage` 中）；没有记录时按浏览器语言自动跳转。
- 两个版本的文件名和标签完全相同，因此链接、交叉引用和语言切换始终对应。
- 专业术语统一以 `scripts/glossary.py` 中的术语表为准，该脚本同时生成两个版本的附录“术语表”。中文版中，每章首次出现的术语在括号中注明英文原文，例如：用户均衡（user equilibrium）。

## 内容

| 部分 | 章节 |
|---|---|
| 第一部分 · 预备知识 | 1 需求建模中的概率分布 · 2 线性回归与假设检验 · 3 网络分析中的非线性最优化 · 4 矩阵平衡：双比例拟合 |
| 第二部分 · 交通建模基础 | 5 交通规划过程 · 6 交通小区、网络与数据 · 7 出行调查与抽样 · 8 建模中的误差与不确定性 |
| 第三部分 · 出行需求与网络模型 | 9 出行生成 · 10 出行分布：增长系数法与重力模型 · 11 交通方式划分：离散选择模型 · 12 集计与组合交通方式划分模型 · 13 交通分配（一）：确定性用户均衡 · 14 交通分配（二）：系统最优、弹性需求与组合模型 · 15 交通分配（三）：随机用户均衡 · 16 交通分配（四）：动态分配与仿真 |
| 第四部分 · 算例与习题 | 17 概率分布 · 18 回归与假设检验 · 19 非线性最优化 · 20 双比例拟合 · 21 交通小区划分与网络编码 · 22 抽样与调查设计 · 23 误差与不确定性 · 24 出行生成 · 25 出行分布 · 26 交通方式划分：离散选择 · 27 集计与组合的交通方式划分 · 28 用户均衡分配 · 29 系统最优、弹性需求与组合模型 · 30 随机用户均衡 · 31 动态分配与仿真 |
| 第五部分 · Python 实现 | 32 Python 实现：预备知识与基础 · 33 Python 实现：出行生成 · 34 Python 实现：出行分布 · 35 Python 实现：交通方式选择 · 36 Python 实现：交通分配 |
| 附录 | 符号说明 · 术语表（中英对照） · 参考文献 |

## 仓库结构

```text
docs/
  _shared/            两个版本共用
    conf_common.py    Sphinx 设置、MathJax 宏、LANGUAGES、NUMFIG_FORMATS
    _ext/             continuous_numbering.py、lang_switch.py、proof_zh.py
    _templates/       lang-switch.html（页眉中的翻译图标）
    _static/          custom.css、lang-switch.js、open-dropdown.js
    locales/          证明类块的中文名称（proof.po 与编译后的 proof.mo）
  en/                 英文版：conf.py、index.md、每章一个 NN-<主题>.md
  zh/                 中文版：文件名与 en/ 相同
  */figures/          构建时汇集的图（不纳入版本控制）
scripts/
  build_docs.py       汇集图、构建两个版本和根页面
  make_figures.py     把生成的图绘制到 docs/<lang>/figures/
  figures/            common.py、chNN.py（每章一个模块）、preview.py、README.md
  glossary.py         中英术语表；生成两个版本的 glossary.md
  run_code_cells.py   运行 Python 章节中的代码块
  templates/          conf.py 和 GitHub 工作流模板，缺失时自动重建
.github/workflows/    每次推送到 main 时构建并发布网站
```

原始课程资料只保存在本地的 `sources/` 中，不会发布（该文件夹已列入 `.gitignore`）。

## 图

所有图均由代码生成：每章一个模块 `scripts/figures/chNN.py`，绘制第 NN 章的图；每个图以首次出现它的章号命名，即 `NN-<名称>.svg`（标签 `fig-NN-<名称>`）。含文字的图带有中文标注，按版本分别绘制。若引用其他来源的图，应放入 `docs/_shared/figures/`（纳入版本控制，并在 `SOURCES.md` 中注明来源）；目前没有这类图。详见 `scripts/figures/README.md`。

## 本地构建

需要 Python 3.10 或更高版本。

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate      macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt

python scripts/build_docs.py --serve         # 构建两个版本，打开 http://127.0.0.1:8000/
python scripts/build_docs.py --strict        # 有任何警告即失败（CI 使用此选项）
python scripts/build_docs.py --lang zh       # 只构建中文版
python scripts/build_docs.py --clean         # 先删除 _build/html
python scripts/build_docs.py --prune-legacy  # 删除旧文件名的章节文件和图
```

图会自动汇集：`build_docs.py` 会为每个版本绘制缺失或比其模块旧的图。修改术语表后请运行 `python scripts/glossary.py`；运行 `python scripts/run_code_cells.py docs/en/3*-python-*.md --quiet` 可检查 Python 章节的代码。若安装了 `jieba`（已列在 `requirements.txt` 中），中文搜索会使用它进行分词。

## 编辑流程

1. 修改 `docs/en/` 中的英文章节，并对 `docs/zh/` 中同名文件作相同修改；若图有变化，修改 `scripts/figures/` 中对应的模块。两个版本的标签保持一致。
2. 新增章节时，把它加入两个 `index.md` 的目录。
3. 新术语加入 `scripts/glossary.py` 并运行该脚本。
4. 运行 `python scripts/build_docs.py --strict`，检查两个版本。
5. 提交并推送，GitHub 工作流会自动构建并发布网站。

## 写作规范

- 章节模板：概述 · 学习目标 · 符号说明 · 正文 · 本章回顾（小结、常见错误） · 参考文献。算例章节以一句话指明对应的理论章节开头；代码章节包含“环境准备”和“小结”两节。
- 例题使用 `{prf:example}`（题目展开显示），其后紧跟默认折叠的 `{dropdown} 解答`（`:class-container: solution`）；证明使用折叠的 `{dropdown} 证明`（`:class-container: proof`）。标题描述题目的主题，而不是其出处。
- 各章在全书范围内连续编号（1–36）；第 7 章的图、表、例题和公式编号为 7.1、7.2、……
- 标签包含章号：`eq-13-beckmann`、`ex-24-tg-zonal`、`fig-13-six-node-network`、`sec-06-zoning-rules`。
- 行间公式每行一个等式；长公式在 `=` 处拆分对齐；被引用的公式都有标签。
- Python 代码用 `black -l 79` 格式化，注释单独成行、写在所注释代码的上方，`# Expected:` 的数值与算例一致。两个版本中的代码均保持英文。
- 中文使用全角标点，每段一行；中文与行内公式、拉丁字母或带单位的数字之间加空格。参考文献条目保持原文。
- 共用的 LaTeX 宏（`\bx`、`\bT`、`\Prob`、`\E`、`\Var`、`\T` 等）及其含义定义在 `docs/_shared/conf_common.py` 中。
- 数字按三位分组，用空格分隔（12 500）。

## 作者与许可证

作者 **Better W.Z.**。本笔记于 2026 年 11 月在 Claude Opus 5.5（Anthropic）的协助下完成内容审阅、修订与整理，译为简体中文，并构建了网站。以 [MIT 许可证](LICENSE)发布：再利用时请保留版权声明“Copyright (c) 2026 Better W.Z.”和许可证全文。

## 引用方式

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
