# 矩阵平衡：双比例拟合

## 概述

建模中经常遇到这样的任务：调整一个非负矩阵，使其行和与列和等于已知的目标值，同时尽可能保留其内部结构。例如，旧的出行矩阵需要更新到新的出行端总量；样本交叉表需要扩样到已知的总体边际；阻抗值矩阵需要缩放，使每个起点发出和每个终点到达的出行量正确。标准做法是给每一行乘以一个系数、每一列乘以另一个系数，并通过交替缩放行和列求出这些系数。该方法在多个领域中被独立发现：统计学家称之为**迭代比例拟合**（iterative proportional fitting；Deming & Stephan, 1940），经济学家在更新投入产出表时称之为 **RAS 法**（Stone & Brown, 1962; Bacharach, 1970），数学家称之为**矩阵缩放**（matrix scaling；Sinkhorn, 1964），交通规划者则称之为**佛尼斯法**（Furness method；Furness, 1965）。本章给出这一**双比例拟合**（bi-proportional fitting）问题及两种标准算法，并给出收敛条件。然后解释*为什么*这种方法是正确的：根据**熵最大化**（entropy maximization）论证，平衡后的矩阵是与边际相容的最可能矩阵，也就是在信息距离意义下最接近种子矩阵的矩阵。最后介绍增加单元组总量约束的三比例扩展。

:::{admonition} 学习目标
:class: objectives
学完本章后，读者应能够：

- 写出双比例（矩阵平衡）问题及其目标值的一致性条件；
- 以适当的终止准则应用双比例算法 I（矩阵缩放）和算法 II（系数更新）；
- 解释迭代何时收敛，以及目标值不一致或与种子矩阵的零元不相容时会发生什么；
- 定义微观状态、中观状态、宏观状态和矩阵的熵，并推导线性约束下的最可能矩阵；
- 证明平衡矩阵在边际约束下使其与种子矩阵的 KL 散度（Kullback–Leibler divergence）最小；
- 将方法推广到含单元组总量的三比例拟合；
- 识别本书后续各部分模型中的双比例问题。
:::

## 符号说明

| 符号 | 含义 |
|---|---|
| $t_{ij} \ge 0$ | 种子（先验）矩阵，$i = 1, \ldots, m$，$j = 1, \ldots, n$ |
| $T_{ij}$ | 平衡后的矩阵 |
| $O_i$, $D_j$ | 行目标值和列目标值 |
| $a_i$, $b_j$ | 行平衡系数和列平衡系数 |
| $r$, $\epsilon$ | 迭代计数器和终止容差 |
| $I(\bT, \bt)$ | $\bT$ 相对于 $\bt$ 的信息（KL）距离 |
| $N$ | 矩阵总和（分配到各单元的个体数） |
| $W\{T_{ij}\}$ | 产生矩阵 $\{T_{ij}\}$ 的微观状态数 |
| $k = 1, \ldots, K$ | 单元组；若单元 $ij$ 属于组 $k$，则 $\delta_{ijk} = 1$ |
| $S_k$, $F_k$ | 组 $k$ 的目标总量和平衡系数 |

## 双比例问题

给定非负**种子矩阵**（seed matrix）$\bt = [t_{ij}]$ 以及正的行目标值 $O_i$ 和列目标值 $D_j$，求系数 $a_i$ 和 $b_j$，使得

$$
\begin{aligned}
T_{ij} &= a_i\,b_j\,t_{ij}, \\
\sum_{j} T_{ij} &= O_i, \qquad i = 1, \ldots, m, \\
\sum_{i} T_{ij} &= D_j, \qquad j = 1, \ldots, n .
\end{aligned}
$$ (eq-04-matrix-balancing)

平衡后的矩阵保持种子矩阵的**交叉乘积比**（cross-product ratio）：对任意两行 $i, k$ 和两列 $j, l$，

$$
\frac{T_{ij}T_{kl}}{T_{il}T_{kj}} = \frac{t_{ij}t_{kl}}{t_{il}t_{kj}},
$$

因为各系数相互抵消。种子矩阵中的关联模式得以保留，改变的只是边际。种子矩阵中为零的单元仍为零。

行目标值之和与列目标值之和都等于矩阵总和，因此只有当目标值**一致**时才可能有解：

$$
\sum_i O_i = \sum_j D_j .
$$ (eq-04-bp-consistency)

若目标值来自不同来源而不相等，通常在平衡前将它们缩放到同一个总量，例如两个总和的平均值，或较可靠来源的总量。

把行约束和列约束代入 $T_{ij} = a_ib_jt_{ij}$，得到关于系数的两组耦合方程：

$$
\begin{aligned}
a_i &= \frac{O_i}{\sum_j b_j\, t_{ij}}, \\
b_j &= \frac{D_j}{\sum_i a_i\, t_{ij}} .
\end{aligned}
$$ (eq-04-bp-factors)

这些系数只能确定到一个公共比例因子：将 $a_i$ 换成 $ca_i$、$b_j$ 换成 $b_j/c$，每个 $T_{ij}$ 都不变。只有乘积 $a_ib_j$ 是有意义的。

## 算法

方程 {eq}`eq-04-bp-factors` 用不动点迭代求解：先满足行目标值，再满足列目标值，如此反复。迭代既可以直接对矩阵进行，也可以对系数进行。

:::{prf:algorithm} 双比例算法 I（矩阵缩放）
:label: alg-04-biprop-1

1. 令 $T_{ij}^{(0)} = t_{ij}$，$r = 1$。
2. **行步：** 对所有 $i, j$，$T_{ij}' = T_{ij}^{(r-1)}\, O_i \big/ \sum_{l} T_{il}^{(r-1)}$。
3. **列步：** 对所有 $i, j$，$T_{ij}^{(r)} = T_{ij}'\, D_j \big/ \sum_{k} T_{kj}'$。
4. 若对所有 $i$ 都有 $\lvert\sum_j T_{ij}^{(r)} - O_i\rvert / O_i \le \epsilon$（第 3 步之后列和是精确的），则停止；否则令 $r \leftarrow r + 1$，返回第 2 步。
:::

:::{prf:algorithm} 双比例算法 II（系数更新）
:label: alg-04-biprop-2

1. 对所有 $j$ 令 $b_j^{(0)} = 1$，$r = 1$。
2. 对所有 $i$，$a_i^{(r)} = O_i \big/ \sum_j b_j^{(r-1)} t_{ij}$。
3. 对所有 $j$，$b_j^{(r)} = D_j \big/ \sum_i a_i^{(r)} t_{ij}$。
4. 若对所有 $j$ 都有 $\lvert b_j^{(r)} - b_j^{(r-1)}\rvert / b_j^{(r)} \le \epsilon$（等价于行和都在容差之内），则停止；否则令 $r \leftarrow r + 1$，返回第 2 步。
5. 输出 $T_{ij} = a_i^{(r)} b_j^{(r)} t_{ij}$。
:::

两种算法产生相同的矩阵序列。算法 II 只需存储 $m + n$ 个系数而不是 $mn$ 个单元，这对大矩阵很重要；而且它直接给出系数本身，某些模型需要这些系数（例如{doc}`10-trip-distribution`中重力模型的平衡系数）。也可以使用组合的相对变化准则

$$
\frac{\lVert \ba^{(r)} - \ba^{(r-1)}\rVert}{\sum_i a_i^{(r)}}
+ \frac{\lVert \bb^{(r)} - \bb^{(r-1)}\rVert}{\sum_j b_j^{(r)}}
\le \epsilon,
$$

容差应取得较小，例如相对值 $10^{-4}$ 或更小：5 % 这样宽松的容差可能使算法在远离解的地方就停止。收敛通常很快——对于性态良好的种子矩阵只需几次迭代（{prf:ref}`ex-20-bp-ras`）——但当目标值与种子矩阵的边际相差很大或种子矩阵含有许多零元时，收敛会变慢。

## 存在性、唯一性与收敛性

若目标值一致，并且存在某个与种子矩阵零元模式相同的矩阵具有所要求的边际，则平衡矩阵存在。当种子矩阵严格为正且目标值一致时，这一条件总是满足。在此条件下迭代收敛，且极限 $\bT$ 唯一。

若没有任何具有种子矩阵零元模式的矩阵能够满足目标值，迭代就不会收敛：行步和列步不断相互抵消，本应为零的单元趋向于零，而其他单元来回振荡（{prf:ref}`ex-20-bp-infeasible`）。因此，平衡计算不收敛本身就是一种诊断：说明目标值彼此不一致，或与种子矩阵的结构不一致。

## 熵最大化

为什么要缩放行和列，而不是以其他方式调整各单元？Wilson（1967, 1970）的熵最大化论证给出了答案：平衡矩阵是与已知总量相容的**最可能**矩阵。该论证适用于任何计数矩阵——小区之间的出行、按两个属性交叉分类的人口、部门之间的资金流动——因此这里以一般形式给出。

### 微观状态、中观状态与宏观状态

考虑 $N$ 个可区分的个体（出行、人、交易），每个个体落入矩阵的某个单元 $ij$。

- **微观状态**（micro-state）指明每个个体所在的单元。
- **中观状态**（meso-state）只指明每个单元中有多少个体——即矩阵 $\{T_{ij}\}$。
- **宏观状态**（macro-state）指明汇总量，如行和 $O_i$ 与列和 $D_j$，或各单元的其他线性函数。

已知的或能够预测的通常是宏观状态。与之相容的中观状态有很多，而每个中观状态又可以由许多微观状态实现。产生中观状态 $\{T_{ij}\}$ 的微观状态数是多项式系数

$$
W\{T_{ij}\} = \frac{N!}{\prod_{i}\prod_{j} T_{ij}!} .
$$ (eq-04-microstates)

例如，四个个体落入 H 和 W 两个单元时，可以分为 (4H, 0W)、(3H, 1W)、(2H, 2W)、(1H, 3W) 或 (0H, 4W)，分别由 $2^4 = 16$ 个微观状态中的 $1$、$4$、$6$、$4$ 和 $1$ 个实现。若所有微观状态等可能，则均分是最可能的中观状态；而且随着 $N$ 增大，$W$ 的分布越来越集中于其最大值附近（{prf:ref}`ex-20-bp-entropy`）。因此，**熵最大化**原理在已知宏观状态的约束下，取能以最多方式实现的中观状态作为估计。

### 熵函数

最大化 $W$ 等价于最大化 $\ln W$。利用斯特林近似 $\ln x! \approx x\ln x - x$，并去掉常数 $\ln N!$，得

$$
\ln W' = -\sum_{i}\sum_{j}\left(T_{ij}\ln T_{ij} - T_{ij}\right),
$$ (eq-04-entropy)

它关于 $\{T_{ij}\}$ 严格凹。（$\sum T_{ij} = N$ 一项是常数，但保留它可以简化导数：$\partial \ln W'/\partial T_{ij} = -\ln T_{ij}$。）该近似是渐近的：要求单元计数较大。

### 给定边际的最可能矩阵

在行和与列和约束下最大化 {eq}`eq-04-entropy`，乘子为 $\lambda_i$ 和 $\mu_j$：

$$
\begin{aligned}
\max_{T_{ij} \ge 0}\quad & -\sum_{i}\sum_{j}\left(T_{ij}\ln T_{ij} - T_{ij}\right) \\
\text{s.t.}\quad & \sum_j T_{ij} = O_i, \\
& \sum_i T_{ij} = D_j .
\end{aligned}
$$

由拉格朗日函数的平稳性条件得

$$
\begin{aligned}
-\ln T_{ij} - \lambda_i - \mu_j &= 0 \\
\Longrightarrow\quad T_{ij} &= e^{-\lambda_i}\, e^{-\mu_j} \\
&= a_i\, b_j .
\end{aligned}
$$

对数项迫使 $T_{ij} > 0$，因此非负约束不起作用，而乘子就是平衡系数的对数。代入边际条件得 $T_{ij} = O_iD_j/N$：没有其他信息时，最可能矩阵是**独立**矩阵，其中每一行都按列和的比例分配。

### 先验信息与信息距离

通常可以获得种子矩阵 $\{t_{ij}\}$——同一矩阵的早期观测，或由某个模型构造的矩阵。若每个个体以先验概率 $t_{ij}/t$ 落入单元 $ij$（$t = \sum_{ij} t_{ij}$），则中观状态的概率为多项分布概率 $W\{T_{ij}\}\prod_{ij}(t_{ij}/t)^{T_{ij}}$。取对数并应用斯特林近似，最大化该概率等价于**最小化**

$$
I(\bT, \bt) = \sum_{i}\sum_{j}\left[T_{ij}\ln\frac{T_{ij}}{t_{ij}} - T_{ij} + t_{ij}\right],
$$ (eq-04-bp-information)

求和遍及 $t_{ij} > 0$ 的单元。当 $T_{ij} = t_{ij}$ 时每一项为零，否则为正；$I$ 是 $\bT$ 相对于 $\bt$ 的（广义）**KL 散度**（Kullback & Leibler, 1951），度量了从种子矩阵到估计矩阵所增加的信息。在种子矩阵附近作二阶展开，得

$$
T_{ij}\ln\frac{T_{ij}}{t_{ij}} - T_{ij} + t_{ij}
\approx \frac{(T_{ij} - t_{ij})^2}{2\,t_{ij}},
$$

因此 $I$ 的性质类似于卡方距离。无种子矩阵的熵最大化是种子矩阵为均匀矩阵的特例。

在边际约束下最小化 $I$，恰好得到双比例矩阵：

:::{prf:theorem} 双比例拟合使信息距离最小
:label: thm-04-bp-information

平衡矩阵 {eq}`eq-04-matrix-balancing` 是下述问题的唯一解：

$$
\begin{aligned}
\min_{\bT \ge \bzero}\ & I(\bT, \bt) \\
\text{s.t.}\ & \sum_j T_{ij} = O_i, \qquad i = 1, \ldots, m, \\
& \sum_i T_{ij} = D_j, \qquad j = 1, \ldots, n .
\end{aligned}
$$ (eq-04-bp-program)
:::

:::{dropdown} 证明
:class-container: proof
:animate: fade-in

对行约束和列约束分别引入乘子 $\lambda_i$ 和 $\mu_j$，拉格朗日函数为

$$
\mathcal{L} = I(\bT, \bt)
+ \sum_i \lambda_i\Big(O_i - \sum_j T_{ij}\Big)
+ \sum_j \mu_j\Big(D_j - \sum_i T_{ij}\Big) .
$$

令其对 $T_{ij}$ 的导数为零，

$$
\ln\frac{T_{ij}}{t_{ij}} - \lambda_i - \mu_j = 0,
$$

因此 $T_{ij} = e^{\lambda_i}e^{\mu_j}\,t_{ij}$，即 $a_ib_jt_{ij}$ 的形式，其中 $a_i = e^{\lambda_i}$，$b_j = e^{\mu_j}$。凡 $t_{ij} > 0$ 处解均为正，因此非负约束不起作用。目标函数严格凸（其黑塞矩阵为 $\diag(1/T_{ij})$），约束是线性的，因此 KKT 条件是充分的，且解唯一（{prf:ref}`thm-03-convex-program`）。
:::

本章的算法是对 {eq}`eq-04-bp-program` 的对偶问题进行的**坐标上升**：行步在 $\mu_j$ 固定时选取恰好满足行约束的 $\lambda_i$，列步对 $\mu_j$ 做同样的事。每个半步都精确求解一个严格凸问题，这是收敛性证明的基础（Bregman, 1967）。

因此，平衡矩阵既是在给定种子矩阵和边际下的最可能矩阵，也是在信息意义下最接近种子矩阵的矩阵。它不会加入边际所不要求的结构：结果中的任何模式都来自种子矩阵或约束。

### 附加线性约束

这一论证可以推广到能写成单元线性约束 $\sum_{ij} g_{ij}T_{ij} = G$ 的任何附加信息。每个这样的约束（乘子为 $\nu$）都给解贡献一个因子 $e^{-\nu g_{ij}}$：

$$
T_{ij} = a_i\, b_j\, t_{ij}\, e^{-\nu g_{ij}} .
$$

目标函数仍严格凸，约束仍是线性的，因此只要约束可行，解就唯一（{prf:ref}`thm-03-convex-program`）。本书后面用到两种情形。若 $g_{ij}$ 是出行费用、$G$ 是总费用，则附加因子是指数型阻抗函数，结果就是{doc}`10-trip-distribution`中的重力模型。若 $g_{ij} = \delta_{ijk}$ 表示单元是否属于某个单元组，则每组一个约束给出每组一个因子：这就是下一节的三比例问题。

## 三比例拟合

有时不仅行和与列和已知，某些**单元组**的总量也已知——例如每个出行距离区间内的出行量，它与行和列交叉。若单元 $ij$ 属于组 $k$（$k = 1, \ldots, K$），令 $\delta_{ijk} = 1$，每个单元恰好属于一组，并记 $S_k$ 为组 $k$ 的目标总量。**三比例问题**（tri-proportional problem）求系数 $a_i$、$b_j$ 和 $F_k$，使得

$$
\begin{aligned}
T_{ij} &= a_i\, b_j\, t_{ij} \sum_{k} F_k\,\delta_{ijk}, \\
\sum_j T_{ij} &= O_i, \\
\sum_i T_{ij} &= D_j, \\
\sum_{i}\sum_{j} T_{ij}\,\delta_{ijk} &= S_k \quad (k = 1, \ldots, K).
\end{aligned}
$$ (eq-04-tri-proportional)

由于每个单元恰好属于一组，$\sum_k F_k\delta_{ijk}$ 只取出一个系数。由上一节，它是具有三组约束的熵问题的解，相应条件给出

$$
\begin{aligned}
a_i &= \frac{O_i}{\sum_j b_j\, t_{ij} \sum_k F_k\delta_{ijk}}, \\
b_j &= \frac{D_j}{\sum_i a_i\, t_{ij} \sum_k F_k\delta_{ijk}}, \\
F_k &= \frac{S_k}{\sum_i\sum_j a_i b_j\, t_{ij}\,\delta_{ijk}} .
\end{aligned}
$$ (eq-04-tri-factors)

:::{prf:algorithm} 三比例算法
:label: alg-04-triprop

1. 对所有 $j$ 和 $k$ 令 $b_j = 1$，$F_k = 1$。
2. 用 {eq}`eq-04-tri-factors` 依次更新 $a_i$、$b_j$ 和 $F_k$，每次都使用其他系数的最新值。
3. 当三组总量都满足容差时停止；否则返回第 2 步。
:::

有两点实际注意事项：

- 系数只能确定到比例因子（对任意 $c, d > 0$，$c\,a_i$、$d\,b_j$ 和 $F_k/(cd)$ 给出相同的 $T_{ij}$），因此需固定一个值（例如 $F_1 = 1$），或在每次迭代中对系数重新归一化；
- 目标值必须**相互一致**：除 $\sum_i O_i = \sum_j D_j = \sum_k S_k$ 外，行、列和组约束不能迫使某组单元之和等于两个不同的值。否则问题无解，算法不收敛（{prf:ref}`ex-25-td-tri-proportional`）。

更多组总量可以用同样的方法处理，只需为每组增加一个缩放步骤（**多比例拟合**）。另有两种常见变体：

- **固定单元或缺失单元。** 已知取值的单元从问题中移除（并从目标值中减去其值）；未观测的单元赋予零种子值，之后由拟合得到的系数估计（{prf:ref}`ex-25-hw2-q2`）。
- **样本权重。** 在调查加权中，同一算法称为**多维比例加权**（raking）：缩放样本权重，使加权计数同时与若干变量的已知总体总量一致。

## 本书中的应用

双比例问题出现在后续的许多模型中：

- **增长系数法出行分布。** 将基年出行矩阵更新到预测的出行端总量，就是{doc}`10-trip-distribution`中以基年矩阵为种子矩阵的佛尼斯法。
- **重力模型。** 双约束重力模型 $T_{ij} = A_iO_iB_jD_jf(c_{ij})$ 就是以阻抗矩阵 $[f(c_{ij})]$ 为种子矩阵的 {eq}`eq-04-matrix-balancing`；算法 II 计算其平衡系数。带费用约束的熵最大化推导出该模型，而阶梯阻抗函数的标定是以费用区间为单元组的三比例问题（{doc}`10-trip-distribution`）。
- **组合模型。** 分布–方式划分组合模型以对各方式求和的阻抗在起点和终点上进行平衡（{doc}`12-aggregate-modal-split`）；分布–分配组合模型在 Evans 算法的每次迭代中都用双比例拟合求解一个重力模型（{doc}`14-system-optimum-and-elastic-demand`）。
- **调查加权。** 基于选择的样本和分层样本通过加权与已知的总体比例相匹配（{doc}`07-travel-surveys-and-sampling`）；当需要同时匹配若干组总体总量时，用同一算法——多维比例加权——求权重。

## 本章回顾

### 小结

- 双比例问题 {eq}`eq-04-matrix-balancing` 在给定行和与列和下求 $T_{ij} = a_ib_jt_{ij}$；它要求目标值一致 {eq}`eq-04-bp-consistency`，并保持种子矩阵的交叉乘积比。
- 算法 I（{prf:ref}`alg-04-biprop-1`）交替缩放矩阵的行和列；算法 II（{prf:ref}`alg-04-biprop-2`）更新系数 {eq}`eq-04-bp-factors`。当目标值一致且与零元相容时，两者都收敛到唯一的极限。
- 由熵最大化 {eq}`eq-04-entropy`，平衡矩阵是给定种子矩阵和边际下的最可能矩阵；等价地，它使与种子矩阵的 KL 距离 {eq}`eq-04-bp-information` 最小（{prf:ref}`thm-04-bp-information`），而算法是对偶问题上的坐标上升。
- 每增加一个线性约束就增加一个乘性因子；单元组总量给出三比例方法 {eq}`eq-04-tri-proportional`（{prf:ref}`alg-04-triprop`）。
- 同一算法在本书中以佛尼斯法、重力模型与组合模型的平衡，以及调查扩样等形式出现。

### 常见错误

- **对和不相等的目标值进行平衡。** 行和与列和不可能同时满足；应先把目标值缩放到同一个总量。
- **使用宽松的容差终止，或只检查最后拟合的边际。** 列步之后列和总是精确的；应以 $10^{-4}$ 或更小的容差检验行和。
- **解释单个系数 $a_i$ 或 $b_j$。** 它们只能确定到一个公共比例因子；只有乘积 $a_ib_j$ 是可识别的。
- **期望种子矩阵中的零元变为正值。** 双比例拟合不能创造种子矩阵中没有的结构。
- **忽视不收敛。** 它表明目标值彼此不一致，或与种子矩阵的零元模式不一致。
- **忘记熵最大化的推导依赖斯特林近似。** 该近似要求单元计数较大；计数较小时，最可能矩阵可能与平衡矩阵不同。

## 参考文献

- Deming, W. E., & Stephan, F. F. (1940). On a least squares adjustment of
  a sampled frequency table when the expected marginal totals are known.
  *Annals of Mathematical Statistics*, *11*(4), 427–444.
  <https://doi.org/10.1214/aoms/1177731829>
- Sinkhorn, R. (1964). A relationship between arbitrary positive matrices
  and doubly stochastic matrices. *Annals of Mathematical Statistics,
  35*(2), 876–879. <https://doi.org/10.1214/aoms/1177703591>
- Bregman, L. M. (1967). Proof of the convergence of Sheleikhovskii's
  method for a problem with transportation constraints. *USSR Computational
  Mathematics and Mathematical Physics, 7*(1), 191–204.
  <https://doi.org/10.1016/0041-5553(67)90069-9>
- Stone, R., & Brown, A. (1962). *A Computable Model of Economic Growth*.
  Chapman and Hall.
- Bacharach, M. (1970). *Biproportional Matrices and Input–Output Change*.
  Cambridge University Press.
- Kullback, S., & Leibler, R. A. (1951). On information and sufficiency.
  *Annals of Mathematical Statistics*, *22*(1), 79–86.
  <https://doi.org/10.1214/aoms/1177729694>
- Wilson, A. G. (1967). A statistical theory of spatial distribution
  models. *Transportation Research*, *1*(3), 253–269.
  <https://doi.org/10.1016/0041-1647(67)90035-4>
- Wilson, A. G. (1970). *Entropy in Urban and Regional Modelling*. Pion.
- Furness, K. P. (1965). Time function iteration. *Traffic Engineering and
  Control, 7*(7), 458–460.
- Ortúzar, J. de D., & Willumsen, L. G. (2011). *Modelling Transport* (4th
  ed.), Sections 5.2, 5.4, and 5.6. Wiley.
