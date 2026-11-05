# 交通规划学习笔记

本学习笔记系统阐述交通规划的核心模型与方法：以交通小区和网络表示研究区域、出行调查与抽样、出行生成、出行分布、交通方式划分与离散选择模型，以及确定性、随机和动态交通分配。每种方法均先陈述其假设，再从基本原理出发加以推导。所需的概率、统计与最优化工具在预备知识部分复习。

部分方法配有附完整解答的例题与习题，全部数值均已通过代码重新计算核实。学习笔记的最后一部分以 Python 实现部分算法，并演示如何借助 NumPy、SciPy、pandas 和 NetworkX 求解同一模型。

本学习笔记以新加坡国立大学 CE5205 Transportation Planning（交通规划）课程讲义（主讲教师：孟强教授，作者于 2021/22 学年修读）为基础，并结合个人学习笔记与经典参考书，尤其是 Ortúzar 与 Willumsen 的 *Modelling Transport*，以及 Sheffi 的 *Urban Transportation Networks*，将全部材料重新组织为符号统一的学习笔记。

本笔记于 2026 年 11 月在 Claude Opus 5.5（Anthropic）的协助下完成内容审阅、修订与整理，译为简体中文，并构建了网站。

作者水平有限，书中难免存在疏漏与错误，恳请读者不吝指正。如发现任何问题，欢迎通过 [GitHub Issue](https://github.com/betterweizh/lecture-notes-transportation-planning/issues) 提交反馈，共同完善这份笔记。

:::{admonition} English edition
:class: tip
本书提供完整的英文版。点击任意页面右上角的翻译图标 {fas}`language`，即可打开另一种语言中的同一章节。
:::

## 本书结构

- **第一部分 预备知识** 回顾全书用到的数学工具：选择模型背后的概率分布、线性回归与假设检验、非线性最优化，以及双比例矩阵平衡及其熵最大化解释。
- **第二部分 交通建模基础** 介绍交通规划过程与四阶段法、交通小区划分与网络表示、出行调查与抽样，以及建模中的误差。
- **第三部分 出行需求与网络模型** 展开四阶段法：出行生成；增长系数法和重力模型的出行分布；离散选择与集计的交通方式划分；以及确定性、系统最优、弹性需求、随机和动态交通分配。
- **第四部分 算例与习题** 逐步求解第一至第三部分的例题与习题，每个主题对应一章。
- **第五部分 Python 实现** 用 NumPy 和 SciPy 从零实现上述模型，并复现第四部分的计算结果。

各章在全书范围内连续编号，第 7 章中的图、表、例题和公式依次编号为 7.1、7.2、…… 证明以及例题与习题的解答默认折叠：点击 **证明** 或 **解答** 栏即可展开，建议先自行尝试再查看解答。

{doc}`notation`汇总了全书符号，{doc}`glossary`给出了主要术语的中英文对照，{doc}`references`列出了各章引用的全部文献。

## 许可证

本学习笔记的文本、图和代码以 [MIT 许可证](https://opensource.org/license/mit)发布：在保留版权声明“Copyright (c) 2026 Better W.Z.”和许可证全文的前提下，可以使用、复制、修改和再分发，包括用于商业目的。本材料不附带任何担保。许可证仅适用于为本学习笔记撰写的内容；原始课程材料和所引用的著作仍归其作者和出版者所有。

## 引用方式

如使用本学习笔记，请按如下方式引用（APA 格式）：

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

引用某个具体模型或结论时，请考虑引用相应章节参考文献中给出的原始文献。

## 目录

```{toctree}
:caption: 第一部分 — 预备知识
:numbered:
:maxdepth: 1

01-probability-distributions
02-regression-and-hypothesis-tests
03-nonlinear-optimization
04-biproportional-fitting
```

```{toctree}
:caption: 第二部分 — 交通建模基础
:numbered:
:maxdepth: 1

05-transportation-planning-process
06-zoning-and-networks
07-travel-surveys-and-sampling
08-errors-and-uncertainty
```

```{toctree}
:caption: 第三部分 — 出行需求与网络模型
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
:caption: 第四部分 — 算例与习题
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
:caption: 第五部分 — Python 实现
:numbered:
:maxdepth: 1

32-python-foundations
33-python-trip-generation
34-python-trip-distribution
35-python-mode-choice
36-python-traffic-assignment
```

```{toctree}
:caption: 附录
:maxdepth: 1

notation
glossary
references
```
