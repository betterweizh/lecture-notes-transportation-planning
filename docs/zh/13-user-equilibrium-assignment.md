# 交通分配（一）：确定性用户均衡

## 概述

交通分配（traffic assignment）是四阶段法的最后一步。其输入是某种交通方式的 O-D 出行矩阵（例如早高峰小时的小汽车出行），输出是网络中每条路段的流量和行程时间。每个出行者选择的路径取决于行程时间，而行程时间又取决于每条路段上有多少出行者，因此交通分配是一个均衡问题。本章阐述 Wardrop 第一原理（Wardrop's first principle），将由此得到的**确定性用户均衡**（deterministic user equilibrium，DUE）写成关于路径流量的一组条件，证明它是 Beckmann 凸规划的解，并介绍实践中使用的算法：全有全无分配（all-or-nothing assignment）、Frank–Wolfe 算法和相继平均法（method of successive averages，MSA）。

:::{admonition} 学习目标
:class: objectives
学完本章后，读者应能够：

- 描述路段阻抗函数的性质；
- 阐述 Wardrop 第一原理及其行为假设；
- 用路段–路径关联表示网络，并写出路径流量和路段流量的可行性条件；
- 写出用户均衡条件，并对小型网络求解；
- 建立 Beckmann 模型，证明其与均衡条件等价，并解释为什么路段流量唯一而路径流量不唯一；
- 用全有全无分配、Frank–Wolfe 算法和相继平均法求解用户均衡，并判断收敛性。
:::

## 符号说明

| 符号 | 含义 |
|---|---|
| $G = (N, A)$ | 节点集为 $N$、路段集为 $A$ 的网络 |
| $R$, $S$ | 起点集和终点集（形心） |
| $K_{rs}$ | 从起点 $r$ 到终点 $s$ 的路径集 |
| $q_{rs}$ | 从 $r$ 到 $s$ 的 O-D 需求（单位时间出行量） |
| $x_a$, $t_a(x_a)$ | 路段 $a$ 的流量和行程时间 |
| $f_k^{rs}$, $c_k^{rs}$ | 路径 $k \in K_{rs}$ 的流量和行程时间 |
| $\delta_{a,k}^{rs}$ | 若路段 $a$ 在 $rs$ 对的路径 $k$ 上则为 1，否则为 0 |
| $\bDelta$ | 以 $\delta_{a,k}^{rs}$ 为元素的路段–路径关联矩阵 |
| $u_{rs}$ | 从 $r$ 到 $s$ 的最短路径行程时间 |
| $\by$ | 辅助（全有全无）路段流量 |

## 四阶段法中的交通分配

经过出行生成、出行分布和交通方式划分之后，所建模时段内每对小区之间的小汽车出行量就已知了。交通分配将这些出行加载到道路网络上。它回答两个问题：出行者使用哪些路径，以及由此产生什么样的流量和行程时间？这些答案用于评价项目（哪里会出现拥堵，新路段能节省多少时间？），把行程时间反馈给前面各步（需求与供给的均衡，见{doc}`05-transportation-planning-process`），并为环境和经济评价提供输入。

交通分配模型有三个组成部分：带有路段阻抗函数的**网络**、**O-D 矩阵**，以及说明出行者如何在每个 O-D 对的路径之间进行选择的**路径选择原则**。本章使用 Wardrop 第一原理；{doc}`15-stochastic-user-equilibrium`放松了其完全信息假设。

## 路段阻抗函数

路段 $a$ 的平均行程时间 $t_a(x_a)$（路段阻抗函数，link performance function）取决于路段流量 $x_a$（单位时间的车辆数）和通行能力（capacity）$c_a$（单位时间内能够通过该路段的最大车辆数）。它关于流量单调不减，关于通行能力单调不增：

$$
\begin{aligned}
\frac{\partial t_a}{\partial x_a} &\ge 0, \\
\frac{\partial t_a}{\partial c_a} &\le 0 .
\end{aligned}
$$

常用形式是 BPR 函数 {eq}`eq-06-bpr`，$t_a(x_a) = t_a^0\left[1 + \alpha(x_a/c_a)^\beta\right]$。参数 $\alpha$ 确定达到通行能力时的行程时间 $t_a^0(1 + \alpha)$，$\beta$ 确定流量接近通行能力时行程时间上升的陡峭程度：$\beta = 1$ 时行程时间从一开始就线性增长，而 $\beta = 4$ 时低流量下几乎不变，超过通行能力的约 80 % 后急剧上升。对 $t_a^0 = 30$ 分钟、$c_a = 3\,600$ 辆/小时的路段，$x_a = 3\,600$ 辆/小时时的行程时间对任何 $\beta$ 都是 34.5 分钟，但 $x_a = 1\,800$ 辆/小时时，$\beta = 1$ 为 32.25 分钟，$\beta = 4$ 仅为 30.28 分钟。将 $\alpha$ 加倍到 0.30 会使每个流量下的延误 $t_a - t_a^0$ 加倍。各类道路的 $\alpha$ 和 $\beta$ 典型取值见 Cambridge Systematics 等（2012，第 4.11 节）。

下面的理论只要求每个 $t_a$ 连续且**严格递增**，且路段行程时间只取决于其自身的流量（**可分离**函数）。大多数手算例题使用线性函数 $t_a = A_a + B_ax_a$，因为它使代数运算保持简单。

## Wardrop 第一原理

熟悉网络的出行者会选择他们认为最快的路径。他们并不都走同一条路径，因为路径的行程时间随其上出行者数量的增加而增加：当最短路径变得拥挤时，另一条路径就变得同样有吸引力。经过一段时间的调整后，流量稳定在由 **Wardrop 第一原理**（Wardrop，1952）描述的状态：

> 所有被使用路径上的行程时间都相等，且小于任何未被使用路径上单辆车所经历的行程时间。

等价的表述有：

- 任何出行者都不能通过单方面改变路径来减少自己的行程时间；
- 对每个 O-D 对，所有被使用路径的行程时间相等，且没有任何未被使用的路径行程时间更短。

由此得到的流量模式就是**确定性用户均衡**（DUE），简称用户均衡（user equilibrium，UE）。该原理基于三个假设：

1. 出行者是理性的，选择行程时间最短的路径；
2. 出行者完全了解所有路径的行程时间；
3. 出行者的路径选择行为相同。

对于由两条平行路段连接的单个 O-D 对，均衡可以直接由该原理得到。若两条路段都被使用，则 $t_1(x_1) = t_2(x_2)$ 且 $x_1 + x_2 = q$。若这两个方程的解使某个流量为负，则该路段不被使用，全部需求走另一条路段，且其行程时间不大于未被使用路段的自由流行程时间。{prf:ref}`ex-28-ue-two-route`详细讨论了这两种情形，并说明被使用路径的集合如何随需求变化。

## 网络表示与可行流

网络是有向图 $G = (N, A)$。起点 $r \in R$ 和终点 $s \in S$ 是形心节点，$K_{rs}$ 是从 $r$ 到 $s$ 的路径（路段序列）集合。例如，在{numref}`fig-13-six-node-network`的网络中，$R = \{1, 5\}$，$S = \{2, 6\}$，O-D 对 $1 \to 2$ 有两条路径：路段 1，以及路段 2–4–3。

```{figure} figures/13-six-node-network.svg
:name: fig-13-six-node-network
:width: 460px
:class: dark-light

算例中使用的六节点网络。起点（绿色）为节点 1 和 5，终点（橙色）为节点 2 和 6；方括号内为路段编号。O-D 对 $1 \to 2$ 的路径为 [1] 和 [2]–[4]–[3]；O-D 对 $5 \to 6$ 的路径为 [6] 和 [5]–[4]–[7]。
```

路径的结构记录在**路段–路径关联**（link–path incidence）中：

$$
\delta_{a,k}^{rs} =
\begin{cases}
1 & \text{若路段 } a \text{ 在 } r \text{ 到 } s \text{ 的路径 } k \text{ 上}, \\
0 & \text{其他情况。}
\end{cases}
$$

它们构成矩阵 $\bDelta$，每条路段对应一行，每条路径对应一列。

若一组路径流量 $\{f_k^{rs}\}$ 满足**流量守恒**和**非负性**，则称其为**可行**的：

$$
\begin{aligned}
\sum_{k \in K_{rs}} f_k^{rs} &= q_{rs}, && r \in R,\ s \in S, \\
f_k^{rs} &\ge 0, && k \in K_{rs},\ r \in R,\ s \in S.
\end{aligned}
$$ (eq-13-flow-conservation)

路段流量和路径费用通过关联矩阵由路径流量得到：

$$
x_a = \sum_{r \in R}\sum_{s \in S}\sum_{k \in K_{rs}} f_k^{rs}\,\delta_{a,k}^{rs},
\qquad a \in A,
$$ (eq-13-link-path-flow)

$$
c_k^{rs} = \sum_{a \in A} t_a(x_a)\,\delta_{a,k}^{rs},
\qquad k \in K_{rs}.
$$ (eq-13-path-cost)

写成矩阵形式，$\bx = \bDelta\bff$，$\bc = \bDelta\T\bt(\bx)$。式 {eq}`eq-13-path-cost` 假设路径费用是**可加**的：路径的行程时间等于其各路段行程时间之和。一个给定的 O-D 矩阵对应无穷多种可行的路径流量模式，因而也对应无穷多种可行的路段流量模式；路径选择原则从中选出一种。

## 均衡条件

设 $u_{rs}$ 为 $r$ 与 $s$ 之间的最短路径行程时间。Wardrop 第一原理表明，只有当路径的行程时间等于 $u_{rs}$ 时，该路径上才有流量。结合可行性条件，得到**用户均衡条件**：

$$
\begin{aligned}
f_k^{rs}\left(c_k^{rs} - u_{rs}\right) &= 0, && k \in K_{rs},\ r \in R,\ s \in S, \\
c_k^{rs} - u_{rs} &\ge 0, && k \in K_{rs},\ r \in R,\ s \in S, \\
\sum_{k \in K_{rs}} f_k^{rs} &= q_{rs}, && r \in R,\ s \in S, \\
f_k^{rs} &\ge 0, && k \in K_{rs},\ r \in R,\ s \in S.
\end{aligned}
$$ (eq-13-ue-conditions)

第一行表示被使用的路径（$f_k^{rs} > 0$）具有最短时间；第二行表示没有路径比 $u_{rs}$ 更快。由于路径费用通过 {eq}`eq-13-link-path-flow` 和 {eq}`eq-13-path-cost` 依赖于流量，{eq}`eq-13-ue-conditions` 是一组非线性方程和不等式，即一个**互补问题**（complementarity problem）。

对小型网络，可以手工求解这些条件：猜测哪些路径被使用，令它们的费用相等，将所得方程与流量守恒方程联立求解，然后检查每个流量是否非负、每条未被使用的路径是否不比被使用的路径更快。若检查不通过，就修改猜测。{prf:ref}`ex-28-ue-three-link`和{prf:ref}`ex-28-ue-six-node`应用了这一程序。对于有成千上万条路径的实际网络，可能的猜测组合是天文数字，因此需要最优化表述。

## Beckmann 模型

### 凸规划

Beckmann、McGuire 和 Winsten（1956）证明，均衡流量是下述规划的解：

$$
\begin{aligned}
\min_{\bff}\ z(\bx) &= \sum_{a \in A}\int_0^{x_a} t_a(\omega)\,\diff\omega \\
\text{s.t.}\quad
\sum_{k \in K_{rs}} f_k^{rs} &= q_{rs}, && r \in R,\ s \in S, \\
f_k^{rs} &\ge 0, && k \in K_{rs},\ r \in R,\ s \in S, \\
x_a &= \sum_{r, s}\sum_{k \in K_{rs}} f_k^{rs}\,\delta_{a,k}^{rs}, && a \in A.
\end{aligned}
$$ (eq-13-beckmann)

目标函数是各路段阻抗函数曲线下面积之和。它本身没有行为或经济上的解释；它是一个数学构造，其最优性条件恰好就是 Wardrop 条件。（不应把它与总行程时间 $\sum_a x_at_a(x_a)$ 混淆，后者是{doc}`14-system-optimum-and-elastic-demand`中系统最优的目标函数。）

### 与均衡条件的等价性

:::{prf:theorem} Beckmann 模型与用户均衡的等价性
:label: thm-13-beckmann-ue

若路段阻抗函数连续且单调不减，则一个可行的路径流量模式是 {eq}`eq-13-beckmann` 的解，当且仅当它满足用户均衡条件 {eq}`eq-13-ue-conditions`。
:::

:::{dropdown} 证明
:class-container: proof
:animate: fade-in

将 {eq}`eq-13-link-path-flow` 代入目标函数，$z$ 就只是路径流量的函数，且约束是线性的。对每个守恒约束引入乘子 $u_{rs}$，对每个非负约束引入 $v_k^{rs} \ge 0$。拉格朗日函数为

$$
\begin{aligned}
L(\bff, \bu, \bv) = z\big(\bx(\bff)\big)
&+ \sum_{r, s} u_{rs}\Big(q_{rs} - \sum_{k \in K_{rs}} f_k^{rs}\Big) \\
&- \sum_{r, s}\sum_{k \in K_{rs}} v_k^{rs} f_k^{rs}.
\end{aligned}
$$

由链式法则和微积分基本定理，

$$
\begin{aligned}
\frac{\partial z}{\partial f_k^{rs}} &= \sum_{a \in A} \frac{\partial z}{\partial x_a}\,\frac{\partial x_a}{\partial f_k^{rs}} \\
&= \sum_{a \in A} t_a(x_a)\,\delta_{a,k}^{rs} \\
&= c_k^{rs} .
\end{aligned}
$$

因此 KKT 条件（{prf:ref}`thm-03-kkt`）为

$$
\begin{aligned}
c_k^{rs} - u_{rs} - v_k^{rs} &= 0, \\
v_k^{rs} &\ge 0, \\
v_k^{rs} f_k^{rs} &= 0,
\end{aligned}
$$

再加上可行性条件。消去 $v_k^{rs} = c_k^{rs} - u_{rs}$，得到 $c_k^{rs} - u_{rs} \ge 0$ 和 $f_k^{rs}(c_k^{rs} - u_{rs}) = 0$，这正是 {eq}`eq-13-ue-conditions`。约束是线性的，因此 KKT 条件在极小点处是必要的；目标函数是凸的（见下文），因此它们也是充分的。乘子 $u_{rs}$ 就是均衡的 O-D 行程时间。
:::

### 路段流量的唯一性

$z$ 关于路段流量的黑塞矩阵是对角矩阵，因为目标函数的每一项只依赖于一条路段的流量：

$$
\nabla^2_{\bx} z(\bx) = \diag\left(t_1'(x_1),\ t_2'(x_2),\ \ldots,\ t_{|A|}'(x_{|A|})\right).
$$

若每个 $t_a$ 都严格递增，则黑塞矩阵正定，$z$ 关于 $\bx$ 严格凸，且可行域（多面体的线性像）是凸集。因此**均衡路段流量是唯一的**（{prf:ref}`thm-03-convex-program`）。

### 路径流量的非唯一性

关于路径流量的黑塞矩阵为 $\nabla^2_{\bff} z = \bDelta\T\diag(t_a')\bDelta$；只要 $\bDelta$ 的列线性相关，它就只是**半**正定的（奇异）——路径数多于路段数时必然如此，路径相互重叠时也常常如此。此时不同的路径流量模式可以产生相同的唯一路段流量，因此**均衡路径流量一般不唯一**（{prf:ref}`ex-28-ue-nonunique`）。这在实践中很重要：需要路径流量的分析，例如选定路段分析或由计数反推 O-D 矩阵，必须在均衡路径流量中作出选择，例如取熵最大的那一个。

## 求解算法

### 全有全无分配

:::{prf:algorithm} 全有全无（AON）分配
:label: alg-13-aon

**输入：** 固定的路段行程时间 $\{t_a\}$ 和 O-D 矩阵。

1. 对每个起点 $r$，求出到所有终点的最短路径（{prf:ref}`alg-03-label-correcting`）。
2. 将全部需求 $q_{rs}$ 加载到从 $r$ 到 $s$ 的最短路径上。
3. 每条路段上的流量等于使用该路段的各路径流量之和。
:::

全有全无分配（all-or-nothing assignment）忽略了拥堵：它是行程时间不依赖于流量时的分配结果（或是之后再修正时间的模型的第一步）。它适用于不拥堵的网络，也是下面各均衡算法的基本构件。存在拥堵时，全有全无分配的流量不是均衡：最短路径会过载，其行程时间超过被闲置路径的行程时间（{prf:ref}`ex-28-ue-aon`）。

### Frank–Wolfe 算法

Beckmann 模型的目标函数是凸的，约束是线性的，因此可以应用 Frank–Wolfe 算法（{prf:ref}`alg-03-frank-wolfe`）。其寻找方向的步骤在可行路段流量上最小化线性化的目标函数：

$$
\min_{\by}\ \nabla z(\bx^{(n)})\T\by = \sum_{a} t_a\big(x_a^{(n)}\big)\,y_a,
$$

当路段时间固定为 $t_a^{(n)} = t_a(x_a^{(n)})$ 时，输送每个 O-D 流量的最便宜方式就是把它放到其最短路径上：这个线性子问题就是一次**全有全无分配**。LeBlanc、Morlok 和 Pierskalla（1975）将这一算法引入交通分配；Visum、EMME 和 TransCAD 等规划软件都提供该算法，如今它们也提供本节末尾介绍的更快的方法。

:::{prf:algorithm} 求解用户均衡的 Frank–Wolfe 算法
:label: alg-13-fw-ue

1. **初始化。** 以自由流行程时间 $t_a(0)$ 进行一次全有全无分配，得到 $\bx^{(1)}$。令 $n = 1$。
2. **更新。** 对所有 $a$，令 $t_a^{(n)} = t_a\big(x_a^{(n)}\big)$。
3. **寻找方向。** 以时间 $t_a^{(n)}$ 进行一次全有全无分配，得到辅助流量 $\by^{(n)}$。
4. **线搜索。** 求 $\alpha_n \in [0, 1]$，使 $z\big(\bx^{(n)} + \alpha(\by^{(n)} - \bx^{(n)})\big)$ 最小。
5. **移动。** 令 $\bx^{(n+1)} = \bx^{(n)} + \alpha_n\big(\by^{(n)} - \bx^{(n)}\big)$。
6. **收敛检验。** 若满足终止准则，则停止；否则令 $n \leftarrow n + 1$，返回第 2 步。
:::

第 4 步的线搜索是一维的。其目标函数关于 $\alpha$ 是凸的，导数为

$$
\frac{\diff}{\diff\alpha}\,
z\big(\bx^{(n)} + \alpha(\by^{(n)} - \bx^{(n)})\big)
= \sum_{a \in A} t_a\big(x_a^{(n)} + \alpha(y_a^{(n)} - x_a^{(n)})\big)\big(y_a^{(n)} - x_a^{(n)}\big),
$$ (eq-13-fw-line-search)

因此 $\alpha_n$ 是 {eq}`eq-13-fw-line-search` 在 $[0, 1]$ 上的根，可用二分法（{prf:ref}`alg-03-bisection`）求得，函数为线性时也可得到闭式解；若导数在 $\alpha = 1$ 处仍为负，则 $\alpha_n = 1$。

### 终止准则

常用的终止准则比较相邻两次迭代：

$$
\begin{aligned}
&\text{(1)}\quad z\big(\bx^{(n)}\big) - z\big(\bx^{(n+1)}\big) \le \varepsilon, \\
&\text{(2)}\quad \sum_{r, s}\frac{\big|u_{rs}^{(n+1)} - u_{rs}^{(n)}\big|}{u_{rs}^{(n)}} \le \varepsilon, \\
&\text{(3)}\quad \frac{\sqrt{\sum_a\big(x_a^{(n+1)} - x_a^{(n)}\big)^2}}{\sum_a x_a^{(n)}} \le \varepsilon .
\end{aligned}
$$

它们衡量的是进展，而不是与均衡的距离；一个移动缓慢的算法可能在远离解的地方就满足这些准则。更好的度量来自 Frank–Wolfe 间隙 {eq}`eq-03-fw-gap`：由于 $\nabla z = \bt(\bx)$，

$$
\begin{aligned}
\mathrm{RG}^{(n)} &= \frac{\sum_a t_a^{(n)}\big(x_a^{(n)} - y_a^{(n)}\big)}{\sum_a t_a^{(n)}x_a^{(n)}} \\
&= \frac{\sum_a t_a^{(n)}x_a^{(n)} - \sum_{r,s} q_{rs}u_{rs}^{(n)}}{\sum_a t_a^{(n)}x_a^{(n)}} .
\end{aligned}
$$ (eq-13-relative-gap)

分子等于当前流量下的总行程时间，减去每个人都能以当前最短路径时间出行时的总行程时间；它只在均衡时为零，并且是 $z(\bx^{(n)}) - z(\bx^*)$ 的上界。**相对间隙**（relative gap，RG）{eq}`eq-13-relative-gap` 是规划软件的标准收敛指标，典型目标值为 $10^{-4}$ 或更小。

### 相继平均法

**相继平均法**（method of successive averages，MSA）用预先确定的步长代替线搜索：

:::{prf:algorithm} 相继平均法（MSA）
:label: alg-13-msa-ue

第 1–3 步和第 6 步同{prf:ref}`alg-13-fw-ue`；第 4、5 步换成

$$
\bx^{(n+1)} = \bx^{(n)} + \frac{1}{n}\big(\by^{(n)} - \bx^{(n)}\big).
$$
:::

第一步（$\alpha_1 = 1$）抛弃了初始流量，由归纳法得

$$
\bx^{(n+1)} = \frac{1}{n}\sum_{m=1}^{n}\by^{(m)} :
$$

即当前流量是所有辅助全有全无流量的简单平均，该方法因此得名。只要步长 $\alpha_n$ 满足 $\sum_n \alpha_n = \infty$ 和 $\sum_n \alpha_n^2 < \infty$，就能保证收敛（Robbins 和 Monro，1951；Blum，1954；Powell 和 Sheffi，1982），而 $1/n$ 是最简单的选择。相继平均法不需要目标函数，因此是随机分配的首选方法（{doc}`15-stochastic-user-equilibrium`）。对确定性用户均衡，它比 Frank–Wolfe 算法慢：早期步长过大，后期步长过小，目标函数甚至可能在相邻迭代之间增大（{prf:ref}`ex-28-ue-fw-three-link`）。

### Frank–Wolfe 之后

Frank–Wolfe 算法在接近解时会变慢，因为相继的全有全无方向在少数几个极点之间来回曲折（{prf:ref}`ex-28-hw4-q2-due`）。更快的方法在迭代之间保留更多信息：**基于路径**的算法（梯度投影法，Jayakrishnan 等，1994）在每个 O-D 对的被使用路径之间转移流量，**基于起点或基于丛**的算法（Bar-Gera，2002；Dial，2006）则以每个起点为根的无环子网络为工作对象。它们能达到 $10^{-8}$ 或更小的相对间隙，还能给出一致的路径流量。TNTP 基准网络（<https://github.com/bstabler/TransportationNetworks>）被广泛用于比较这些算法。

## 本章回顾

### 小结

- Wardrop 第一原理：在用户均衡状态下，一个 O-D 对的所有被使用路径具有相等且最短的行程时间，且没有任何未被使用的路径更快。
- 可行路径流量满足守恒与非负条件 {eq}`eq-13-flow-conservation`；路段流量和路径费用通过路段–路径关联 {eq}`eq-13-link-path-flow` 和 {eq}`eq-13-path-cost` 得到。
- 均衡条件 {eq}`eq-13-ue-conditions` 是路径流量与路径超额费用 $c_k^{rs} - u_{rs}$ 之间的互补条件。
- Beckmann 模型 {eq}`eq-13-beckmann` 的 KKT 条件就是均衡条件（{prf:ref}`thm-13-beckmann-ue`）；路段函数严格递增时路段流量唯一，而路径流量一般不唯一。
- Frank–Wolfe 算法（{prf:ref}`alg-13-fw-ue`）通过全有全无分配（{prf:ref}`alg-13-aon`）和线搜索 {eq}`eq-13-fw-line-search` 求解该模型；相继平均法（{prf:ref}`alg-13-msa-ue`）使用步长 $1/n$。相对间隙 {eq}`eq-13-relative-gap` 衡量收敛程度。

### 常见错误

- **令路径时间相等后不检验结果。** 对被使用路径的猜测可能是错的：应检查每个流量是否非负、是否没有未被使用的路径更快，否则就修改猜测。
- **把 Beckmann 目标函数当作总行程时间。** 积分 {eq}`eq-13-beckmann` 没有行为含义；总行程时间 $\sum_a x_at_a(x_a)$ 是系统最优的目标函数。
- **期望路径流量唯一。** 只有路段流量是唯一的；许多路径流量模式都能产生同样的路段流量（{prf:ref}`ex-28-ue-nonunique`）。
- **从零流量开始 Frank–Wolfe 算法。** 零流量不满足流量守恒；初始点必须可行，因此要先进行一次全有全无分配。
- **以固定迭代次数或流量变化作为终止规则。** 它们衡量的是进展，而不是与均衡的距离；应报告相对间隙 {eq}`eq-13-relative-gap`。
- **线搜索时忘记端点。** 若导数 {eq}`eq-13-fw-line-search` 在 $\alpha = 1$ 处仍为负，则步长为 $\alpha_n = 1$，而不是 $[0, 1]$ 上（并不存在的）根。

## 参考文献

- Bar-Gera, H. (2002). Origin-based algorithm for the traffic assignment
  problem. *Transportation Science*, *36*(4), 398–417.
- Beckmann, M., McGuire, C. B., & Winsten, C. B. (1956). *Studies in the
  Economics of Transportation*. Yale University Press.
- Blum, J. R. (1954). Multidimensional stochastic approximation methods.
  *Annals of Mathematical Statistics*, *25*(4), 737–744.
  <https://doi.org/10.1214/aoms/1177728659>
- Cambridge Systematics et al. (2012). *Travel Demand Forecasting:
  Parameters and Techniques* (NCHRP Report 716), Section 4.11.
  Transportation Research Board. <https://doi.org/10.17226/14665>
- Dial, R. B. (2006). A path-based user-equilibrium traffic assignment
  algorithm that obviates path storage and enumeration. *Transportation
  Research Part B*, 40(10), 917–936.
- Jayakrishnan, R., Tsai, W. K., Prashker, J. N., & Rajadhyaksha, S.
  (1994). A faster path-based algorithm for traffic assignment.
  *Transportation Research Record*, *1443*, 75–83.
- LeBlanc, L. J., Morlok, E. K., & Pierskalla, W. P. (1975). An efficient
  approach to solving the road network equilibrium traffic assignment
  problem. *Transportation Research*, *9*(5), 309–318.
- Ortúzar, J. de D., & Willumsen, L. G. (2011). *Modelling Transport* (4th
  ed.), Chapters 10 and 11. Wiley.
- Powell, W. B., & Sheffi, Y. (1982). The convergence of equilibrium
  algorithms with predetermined step sizes. *Transportation Science*, *16*(1),
  45–55.
- Robbins, H., & Monro, S. (1951). A stochastic approximation method.
  *Annals of Mathematical Statistics*, *22*(3), 400–407.
  <https://doi.org/10.1214/aoms/1177729586>
- Sheffi, Y. (1985). *Urban Transportation Networks: Equilibrium Analysis
  with Mathematical Programming Methods*, Sections 1.3, 3.1–3.3, 4.3, and
  5.1–5.3. Prentice-Hall.
- Wardrop, J. G. (1952). Some theoretical aspects of road traffic research.
  *Proceedings of the Institution of Civil Engineers, Part II*, *1*(3),
  325–378. <https://doi.org/10.1680/ipeds.1952.11259>
