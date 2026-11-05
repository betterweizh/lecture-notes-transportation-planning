# 出行分布：增长系数法与重力模型

## 概述

出行生成告诉我们离开和到达每个小区的出行有多少；出行分布（trip distribution）则决定这些出行**去往何处**，即填充出行矩阵的各单元 $T_{ij}$。本章介绍两类经典的出行分布模型。**增长系数法**（growth-factor methods）将观测到的基年矩阵更新到未来的出行端总量：包括常增长系数法、平均增长系数法、底特律法、福莱特法和佛尼斯法。**重力模型**（gravity models）由出行端总量和小区间的出行费用合成矩阵；{doc}`04-biproportional-fitting`中的熵最大化（entropy maximization）原理用同一论证推导出这两类模型，并解释了每个参数的作用。重力模型必须根据观测的出行距离进行标定。本章最后讨论实际问题：部分矩阵、外部出行与小区内出行、出行目的以及 $K$ 系数。

:::{admonition} 学习目标
:class: objectives
学完本章后，读者应能够：

- 写出出行矩阵的平衡约束，并区分单约束模型和双约束模型；
- 定义广义费用；
- 应用常增长系数法、单约束增长系数法、平均增长系数法、底特律法、福莱特法和佛尼斯法，并对它们进行比较；
- 设定具有指数型、幂函数型、组合型和阶梯型阻抗函数的重力模型；
- 推导单约束和双约束重力模型的平衡系数；
- 用熵最大化推导增长系数模型和重力模型，并将乘子解释为平衡系数和阻抗参数；
- 用三比例拟合根据观测的出行距离分布标定重力模型，包括部分矩阵的情形；
- 处理外部小区、小区内出行、出行目的和 $K$ 系数。
:::

## 符号说明

| 符号 | 含义 |
|---|---|
| $i, j = 1, \ldots, z$ | 起点小区和终点小区 |
| $T_{ij}$, $O_i$, $D_j$, $T$ | 模型（未来）的出行量、出行端总量和出行总量 |
| $t_{ij}$, $o_i$, $d_j$, $t$ | 观测（基年或样本）的出行量、出行端总量和出行总量 |
| $c_{ij}$ | 从 $i$ 到 $j$ 的出行广义费用 |
| $f(c_{ij})$ | 阻抗函数 |
| $A_i$, $B_j$; $a_i$, $b_j$ | 平衡系数；$a_i = A_iO_i$，$b_j = B_jD_j$ |
| $\tau$, $\tau_i$, $\Gamma_j$ | 总增长系数、起点增长系数和终点增长系数 |
| $T_{ij}^{(m)}$ | 增长系数法第 $m$ 次迭代后的矩阵 |
| $\psi_{ij}^{(m)}$, $\epsilon$ | 单元的增长函数和迭代方法的终止容差 |
| $G^{(m)}$; $L_i^{O(m)}$, $L_j^{D(m)}$ | 总增长率（底特律法）；起点和终点位置系数（福莱特法） |
| $k = 1, \ldots, K$ | 费用区间；若 $c_{ij}$ 落在区间 $k$ 内，则 $\delta_{ijk} = 1$ |
| $F_k$, $S_k$ | 区间 $k$ 的分段阻抗系数和观测出行量 |

小写字母表示观测值，大写字母表示待建模的量。

## 出行矩阵及其约束

**出行矩阵** $[T_{ij}]_{z\times z}$ 记录某一时段内从各起点到各终点的出行量（O-D 矩阵，即起讫点矩阵），或全天从产生小区到吸引小区的出行量（产生–吸引矩阵，P–A matrix）。它可以按人员类型 $n$ 和交通方式 $k$ 细分，$T_{ij} = \sum_{n}\sum_{k} T_{ij}^{nk}$。其行和与列和必须等于出行端总量：

$$
\begin{aligned}
\sum_{j} T_{ij} &= O_i \quad (i = 1, \ldots, z), \\
\sum_{i} T_{ij} &= D_j \quad (j = 1, \ldots, z),
\end{aligned}
$$ (eq-10-td-balance)

这要求 $\sum_i O_i = \sum_j D_j = T$（{doc}`09-trip-generation`对二者进行平衡）。同时满足两组约束的模型称为**双约束**（doubly constrained）模型；只满足起点（产生量）约束或只满足终点（吸引量）约束的模型称为**单约束**（singly constrained）模型。吸引量（就业岗位）已知程度较高的工作出行，通常用双约束模型建模；吸引量不确定的购物、社交和娱乐出行，则用起点约束模型建模。

### 广义费用

出行的**广义费用**（generalized cost）将抑制出行的各种属性按其感知重要程度加权组合：

$$
\begin{aligned}
c_{ij} ={}& a_1 t_{ij}^{v} + a_2 t_{ij}^{w} + a_3 t_{ij}^{t} + a_4 t_{ij}^{n} \\
          & + a_5 F_{ij} + a_6 \phi_j + \delta ,
\end{aligned}
$$ (eq-10-generalized-cost)

其中 $t^{v}$ 为车内时间，$t^{w}$ 为往返车站或停车场的步行时间，$t^{t}$ 为候车（或寻找车位）时间，$t^{n}$ 为换乘时间，$F_{ij}$ 为票价或车辆运行费用（含通行费），$\phi_j$ 为终端（停车）费用，$\delta$ 为反映舒适、安全等未计量属性的方式惩罚项。若以货币计量费用（$a_5 = 1$），则 $a_1$ 就是**车内时间价值**（value of in-vehicle time）；步行时间和候车时间的价值通常是 $a_1$ 的二至三倍。

## 增长系数法

设 $[t_{ij}]$ 为基年矩阵（来自近期调查或以往研究），$o_i = \sum_j t_{ij}$，$d_j = \sum_i t_{ij}$，$t = \sum_{ij} t_{ij}$。增长系数法将每个单元乘以一个反映其两端出行增长的系数。各种方法的区别在于对未来了解多少，以及如何组合这些系数。

### 常增长系数法

如果只知道未来的出行总量 $T$，则所有单元按同一比率增长：

$$
\begin{aligned}
T_{ij} &= \tau\, t_{ij}, \\
\tau &= \frac{T}{t} .
\end{aligned}
$$ (eq-10-uniform-growth)

该方法（uniform growth factor method）也称 **constant growth factor method**。它忽略了各小区增长的差异，因此未来的行和与列和几乎从来都不正确。

### 单约束增长系数法

如果已知从每个小区出发的未来出行量，则每一行按各自的系数缩放：

$$
\begin{aligned}
T_{ij} &= \tau_i\, t_{ij}, \\
\tau_i &= \frac{O_i}{o_i} \\
&= \frac{O_i}{\sum_j t_{ij}} .
\end{aligned}
$$ (eq-10-origin-growth)

终点增长系数 $\Gamma_j = D_j/d_j$ 以同样的方式缩放各列。此时另一组总量得不到满足（{prf:ref}`ex-25-td-singly-growth`）。

### 双约束增长：迭代方法

当 $O_i$ 和 $D_j$ 都已知时，任何单一的缩放都无法同时满足两组总量。因此经典方法采用迭代。从 $T_{ij}^{(0)} = t_{ij}$ 开始，在第 $m = 0, 1, 2, \ldots$ 次迭代时计算当前总量和增长系数

$$
\begin{aligned}
O_i^{(m)} &= \sum_j T_{ij}^{(m)}, \\
D_j^{(m)} &= \sum_i T_{ij}^{(m)}, \\
\tau_i^{(m)} &= \frac{O_i}{O_i^{(m)}}, \\
\Gamma_j^{(m)} &= \frac{D_j}{D_j^{(m)}},
\end{aligned}
$$

并用两个系数的增长函数 $\psi$ 更新每个单元：

$$
\begin{aligned}
T_{ij}^{(m+1)} &= T_{ij}^{(m)}\, \psi_{ij}^{(m)}, \\
\psi_{ij}^{(m)} &= \psi\!\left(\tau_i^{(m)}, \Gamma_j^{(m)}\right) .
\end{aligned}
$$ (eq-10-growth-iteration)

当所有系数都接近 1，即 $\lvert\tau_i^{(m)} - 1\rvert \le \epsilon$ 且 $\lvert\Gamma_j^{(m)} - 1\rvert \le \epsilon$ 时停止迭代。教科书中的例题常取 $\epsilon = 0.03$；若结果还要进一步使用，宜取 $10^{-3}$ 或更小的容差。各方法的区别仅在于增长函数。

**平均增长系数法**（average growth factor method）。每个单元按其两端系数的平均值增长：

$$
\psi_{ij}^{(m)} = \frac{\tau_i^{(m)} + \Gamma_j^{(m)}}{2} .
$$ (eq-10-average-growth)

该方法简单，但取平均后两组约束都不能满足，因此收敛较慢，而且所收敛到的矩阵没有特定的最优性质。

**底特律法**（Detroit method）。该方法是为底特律都市区交通研究而提出的（Carroll，1957），它使每个单元按两端系数的乘积增长，再除以总增长率，以免总量被重复计入：

$$
\begin{aligned}
\psi_{ij}^{(m)} &= \frac{\tau_i^{(m)}\, \Gamma_j^{(m)}}{G^{(m)}}, \\
G^{(m)} &= \frac{T}{\sum_{ij} T_{ij}^{(m)}} .
\end{aligned}
$$ (eq-10-detroit)

**福莱特法**（Fratar method）。Fratar（1954）认为，小区 $i$ 的出行应按各终点的增长比例分配到各终点。仅以 $\Gamma_j$ 为权重分配第 $i$ 行的增长会改变行和，因此对每一端用一个**位置系数**（location factor）加以修正，再将两个修正取平均：

$$
\begin{aligned}
\psi_{ij}^{(m)} &= \tau_i^{(m)}\, \Gamma_j^{(m)}\, \frac{L_i^{O(m)} + L_j^{D(m)}}{2}, \\
L_i^{O(m)} &= \frac{O_i^{(m)}}{\sum_{j'} T_{ij'}^{(m)}\,\Gamma_{j'}^{(m)}}, \\
L_j^{D(m)} &= \frac{D_j^{(m)}}{\sum_{i'} T_{i'j}^{(m)}\,\tau_{i'}^{(m)}} .
\end{aligned}
$$ (eq-10-fratar)

若只用 $L_i^{O}$，一步之后行和即可精确满足；若只用 $L_j^{D}$，则列和精确满足。取平均是一种折中，通常几次迭代即可收敛。

**佛尼斯法**（Furness method）。Furness（1965）完全避免了折中，采用交替进行的方式：在一个半步中每一行乘以 $\tau_i$，使行和精确满足；在下一个半步中每一列乘以 $\Gamma_j$，使列和精确满足。其极限具有如下形式：

$$
\begin{aligned}
T_{ij} &= a_i\, b_j\, t_{ij}, \\
\sum_j T_{ij} &= O_i, \\
\sum_i T_{ij} &= D_j .
\end{aligned}
$$ (eq-10-biproportional)

这就是{doc}`04-biproportional-fitting`中的**双比例问题**（该方法也称迭代比例拟合法或 RAS 法）。它是这些方法中唯一有收敛性证明并具有明确最优性质的方法：由熵最大化，其结果是在给定基年模式和新出行端总量下的最可能矩阵（{prf:ref}`ex-25-td-furness`、{prf:ref}`ex-25-hw2-q1`）。

**比较。** 对{prf:ref}`ex-25-td-growth-methods`中的三小区算例，取 $\epsilon = 10^{-3}$ 时，平均增长系数法需要 8 次迭代，底特律法 9 次，福莱特法 3 次，佛尼斯法 5 次；四个最终矩阵相差约 1 % 以内。平均增长系数法、底特律法和福莱特法主要具有历史意义，但仍出现在许多教科书和考试中；在实践中，佛尼斯法是标准方法。

**局限性。** 增长系数法简单，直接利用观测到的出行模式，并在新的出行端总量所允许的范围内保留这一模式。这也正是其局限：它们只适用于费用稳定的短期预测；需要代价高昂的基年矩阵并继承其误差（未观测到的单元仍为空）；而且无法反映出行费用的变化、新路段、新交通方式、收费或新增小区。

## 重力模型

### 从牛顿定律到阻抗函数

重力模型不依赖基年模式来合成矩阵。最初与牛顿定律的类比

$$
T_{ij} = \alpha\,\frac{P_i P_j}{d_{ij}^2},
$$

（$P_i$、$P_j$ 为小区人口，$d_{ij}$ 为距离）被推广为

$$
T_{ij} = \alpha\, O_i\, D_j\, f(c_{ij}),
$$ (eq-10-gravity-basic)

其中**阻抗函数**（deterrence function）$f$ 随广义费用递减。常用形式有

$$
\begin{aligned}
f(c) &= e^{-\beta c} \ \ \text{（指数型）}, \\
f(c) &= c^{-n} \ \ \text{（幂函数型）}, \\
f(c) &= c^{\,n} e^{-\beta c} \ \ \text{（组合型）},
\end{aligned}
$$

其中 $\beta, n > 0$；以及**阶梯型**函数

$$
f(c_{ij}) = \sum_{k=1}^{K} F_k\,\delta_{ijk},
$$ (eq-10-stepwise-deterrence)

其中费用被划分为 $K$ 个区间，若 $c_{ij}$ 落在区间 $k$ 内则 $\delta_{ijk} = 1$，否则为 0，$F_k$ 是区间 $k$ 的**分段阻抗系数**（separation factor）。指数函数适合短距离的城市出行；组合函数先升后降，能再现长距离出行中极短出行很少的特点。

### 单约束与双约束重力模型

用若干组平衡系数（balancing factor）代替单一常数 $\alpha$，即可使模型满足平衡约束：

$$
\begin{aligned}
T_{ij} &= A_i\, O_i\, B_j\, D_j\, f(c_{ij}) \\
&= a_i\, b_j\, f(c_{ij}) .
\end{aligned}
$$ (eq-10-gravity)

**起点约束**（$B_j = 1$）。对 $j$ 求和并令 $\sum_j T_{ij} = O_i$，得

$$
\begin{aligned}
A_i &= \frac{1}{\sum_j D_j\, f(c_{ij})}, \\
T_{ij} &= O_i\,\frac{D_j f(c_{ij})}{\sum_{j'} D_{j'} f(c_{ij'})} .
\end{aligned}
$$ (eq-10-origin-constrained)

每个起点的出行按各终点经费用折减后的吸引力成比例地分配到各终点——这是一个“目的地选择”模型。

**终点约束**（$A_i = 1$）：$B_j = 1/\sum_i O_i f(c_{ij})$。

**双约束。** 同时施加两组约束，得

$$
\begin{aligned}
A_i &= \frac{1}{\sum_j B_j D_j f(c_{ij})}, \\
B_j &= \frac{1}{\sum_i A_i O_i f(c_{ij})} .
\end{aligned}
$$ (eq-10-doubly-constrained)

两组系数相互依赖，需要迭代求解。令 $a_i = A_iO_i$，$b_j = B_jD_j$，该模型恰好就是以“种子”矩阵 $[f(c_{ij})]$ 代替 $[t_{ij}]$ 的双比例问题 {eq}`eq-10-biproportional`，因此佛尼斯法可以原样使用（{prf:ref}`ex-25-td-gravity`）。在第一次迭代前用 $\tau = \sum_i O_i / \sum_{ij} f(c_{ij})$ 缩放种子矩阵只会改变起始点。

## 熵最大化与出行分布模型

增长系数模型和重力模型看起来像两种不同的方法。熵最大化（Wilson, 1967；{doc}`04-biproportional-fitting`）表明，它们来自同一个原理：在已知出行信息的约束下，选择**最可能**的出行矩阵——即把单次出行分配到小区对时可以由最多种方式实现的矩阵。每一条写成线性约束的已知信息，都为模型增加一个因子。

### 只知道出行端总量

在平衡约束 {eq}`eq-10-td-balance` 下最大化熵 {eq}`eq-04-entropy`，得 $T_{ij} = a_ib_j$，从而 $T_{ij} = O_iD_j/T$：没有费用信息时，每个起点按各终点吸引量的比例分配其出行（{prf:ref}`ex-20-bp-entropy`）。这是阻抗为常数的重力模型。

### 已知基年矩阵：增长系数模型

若基年矩阵 $\{t_{ij}\}$ 提供了先验概率，则最可能矩阵在新的出行端总量约束下使信息距离 {eq}`eq-04-bp-information` 最小，由{prf:ref}`thm-04-bp-information`，

$$
\begin{aligned}
T_{ij} &= A_i O_i B_j D_j\, t_{ij} \\
&= a_i b_j t_{ij},
\end{aligned}
$$ (eq-10-entropy-growth)

这就是**双约束增长系数模型**：佛尼斯法求得的是在满足新出行端总量的矩阵中，在信息意义下最接近基年矩阵的那一个。

### 加入费用约束：指数型重力模型

假设出行总费用 $C = \sum_{ij} T_{ij}c_{ij}$ 也已知（或等价地，平均出行费用 $C/T$ 已知）。将这一约束（乘子为 $\beta$）加入熵问题，平稳性条件给出

$$
\frac{\partial\mathcal{L}}{\partial T_{ij}} = -\ln T_{ij} - \lambda_i - \mu_j - \beta\, c_{ij},
$$

它在最优点为零，因此

$$
T_{ij} = A_i O_i B_j D_j \exp(-\beta\, c_{ij}),
$$ (eq-10-entropy-gravity)

这就是具有**指数型**阻抗函数的双约束重力模型。平衡约束的乘子是平衡系数的对数，而阻抗参数 $\beta$ 是费用约束的乘子：其取值使模型再现观测的平均出行费用，这正是下文的标定规则。$\beta$ 越大，出行越短。

### 其他阻抗函数

阻抗函数的形式取决于费用约束的形式：

- 对 $\sum_{ij} T_{ij}\ln c_{ij}$ 施加约束（乘子为 $n$），得到**幂函数型** $T_{ij} = A_iO_iB_jD_j\, c_{ij}^{-n}$；
- 同时对 $\sum T_{ij}c_{ij}$ 和 $\sum T_{ij}\ln c_{ij}$ 施加约束，得到**组合型**函数 $c_{ij}^{\,n}e^{-\beta c_{ij}}$，其中 $-n$ 是第二个约束的乘子；
- 对每个费用区间的出行量各施加一个约束 $\sum_{ij} T_{ij}\delta_{ijk} = S_k$（乘子为 $\beta_k$），得到

  $$
  \begin{aligned}
  T_{ij} &= A_iO_iB_jD_j \sum_k e^{-\beta_k}\delta_{ijk} \\
  &= a_i b_j \sum_k F_k \delta_{ijk},
  \end{aligned}
  $$

  即 $F_k = e^{-\beta_k}$ 的**阶梯型**模型 {eq}`eq-10-stepwise-deterrence`，其标定是一个三比例问题。

Fotheringham（1983）的**竞争目的地**（competing destinations）模型增加了对 $\sum T_{ij}\ln S_{ij}$ 的约束，其中 $S_{ij}$ 度量终点 $j$ 到其他终点的可达性，得到 $T_{ij} = A_iO_iB_jD_j\,S_{ij}^{\rho}\exp(-\beta c_{ij})$。

目标函数严格凸，约束是线性的，因此这些问题都至多有一个解（{prf:ref}`thm-03-convex-program`）：计算这些模型的平衡算法具有唯一的极限。

### 解释与局限

熵最大化并不声称出行者随机选择目的地。它给出的是在作为约束使用的信息之下矩阵的*最小偏差*估计：结果中的任何结构都来自约束，而非隐含的假设。它在行为上的对应物是{doc}`11-discrete-choice-models`中的目的地选择 Logit 模型：具有指数型阻抗的起点约束重力模型，与效用为 $\ln D_j - \beta c_{ij}$ 的目的地选择多项 Logit 模型形式相同。

## 标定与验证

重力模型在使用之前，必须对其参数（$\beta$、$n$ 或 $F_k$）进行**标定**（calibration），使模型在其函数形式允许的范围内尽可能再现基年模式。**验证**（validation）是另一项任务：检验标定后的模型能否以适合所支持决策的精度，再现一个未用于标定的已知系统状态。

### 出行距离分布

自然的标定目标是观测的**出行距离（费用）分布**（trip length distribution，TLD）：由调查得到的、费用落在各区间 $k$ 内的出行量 $S_k$。对指数型阻抗函数，一个方便的目标是平均出行费用：调整 $\beta$，直到模型的平均值 $\sum_{ij}T_{ij}c_{ij}/T$ 等于观测值，这正是熵推导 {eq}`eq-10-entropy-gravity` 中确定 $\beta$ 的条件。

### 标定阶梯型阻抗函数

对阶梯型函数 {eq}`eq-10-stepwise-deterrence`，标定就是求 $a_i$、$b_j$ 和 $F_k$，使模型满足出行端总量，并再现每个费用区间的观测出行量 $S_k$。这就是{doc}`04-biproportional-fitting`中的三比例问题 {eq}`eq-04-tri-proportional`，其种子矩阵全为 1，单元组就是费用区间；用{prf:ref}`alg-04-triprop`求解。估计得到的 $F_k$ 无需假设函数形式即可描绘出阻抗函数的形状，然后可以用一个光滑函数对其进行拟合。与所有三比例问题一样，需要固定一个系数（例如 $F_1 = 1$），而且出行端总量与出行距离分布必须相互一致，否则算法无法收敛（{prf:ref}`ex-25-td-tri-proportional`）。

### 部分矩阵

调查数据很少覆盖每一个单元：路边询问调查只能观测到经过调查站点的出行。此时标定**只在观测到的单元上**进行，出行端总量和出行距离分布也由这些单元计算，然后用拟合的模型填充缺失的单元：对未观测的 $ij$，$\hat{T}_{ij} = a_i b_j \sum_k F_k \delta_{ijk}$（{prf:ref}`ex-25-hw2-q2`）。对增长系数模型，等价的做法是将未观测单元置零后进行平衡，再由所得系数估计缺失的单元。

## 实际考虑

外部小区
: 一端或两端在研究区域外的出行，在模型内没有有意义的费用。这类出行通常取自境界线路边询问调查，并用增长系数法（佛尼斯法）而不是重力模型进行预测。

小区内出行
: 小区内部出行的费用很难用形心连杆表示。小区内出行最好从合成模型中剔除，并按小区出行端总量的固定比例进行预测。

出行目的
: 对不同的出行目的和人员类型分别估计模型，并采用不同的阻抗参数：不同目的的出行对费用的敏感程度不同。

$K$ 系数
: 小区之间的特殊联系（例如企业城镇）可以用小区对调整系数表示，$T_{ij} = K_{ij} A_i O_i B_j D_j f(c_{ij})$。它们能改善基年的拟合，但没有行为依据，其未来取值也是未知的；应避免使用，或只用于理由明确的极少数小区对。

## 本章回顾

### 小结

- 出行矩阵必须与出行端总量一致 {eq}`eq-10-td-balance`；双约束模型同时满足行和与列和，这要求 $\sum_i O_i = \sum_j D_j$。
- 广义费用 {eq}`eq-10-generalized-cost` 将时间和货币费用按其感知重要程度加权组合。
- 增长系数法缩放观测矩阵：统一缩放 {eq}`eq-10-uniform-growth`、按行缩放 {eq}`eq-10-origin-growth`，或在两端总量均已知时，用平均增长系数法 {eq}`eq-10-average-growth`、底特律法 {eq}`eq-10-detroit`、福莱特法 {eq}`eq-10-fratar` 或佛尼斯法 {eq}`eq-10-biproportional` 的增长函数进行迭代 {eq}`eq-10-growth-iteration`；只有佛尼斯法有收敛性证明和最优性质。
- 重力模型 {eq}`eq-10-gravity` 由出行端总量和费用合成矩阵；起点约束形式 {eq}`eq-10-origin-constrained` 是一个目的地选择模型，双约束形式 {eq}`eq-10-doubly-constrained` 就是以 $f(c_{ij})$ 为种子矩阵的双比例问题。
- 熵最大化推导出增长系数模型 {eq}`eq-10-entropy-growth`（已知基年矩阵）和重力模型 {eq}`eq-10-entropy-gravity`（加入费用约束）；费用约束的乘子就是阻抗参数。
- 标定使阻抗函数拟合观测的出行距离分布；三比例拟合可以估计阶梯型函数 {eq}`eq-10-stepwise-deterrence`，并能处理部分矩阵。

### 常见错误

- **在 $\sum_i O_i \ne \sum_j D_j$ 时运行双约束方法。** 此时没有矩阵能同时满足两组约束，迭代会振荡；应先平衡出行端总量（{doc}`09-trip-generation`）。
- **对增长系数取平均后只迭代一次就停止。** 此时两组总量都得不到满足；应迭代到所有系数都接近 1。
- **用出行端总量的拟合来比较重力模型。** 每个平衡后的模型都能精确再现出行端总量；应比较出行距离分布和各单元。
- **用宽松的容差终止平衡算法。** 5 % 这样的容差可能使总量偏离目标若干个百分点；应取 $10^{-3}$ 或更小，并检查所报告矩阵的总量。
- **把分段阻抗系数 $F_k$ 当作费用。** 它们是各费用区间内出行的相对倾向，且只确定到一个比例因子。
- **推导阶梯型模型时，对每个区间内的*费用*施加约束。** 阶梯型模型来自对每个区间内*出行量*的约束。

## 参考文献

- Ortúzar, J. de D., & Willumsen, L. G. (2011). *Modelling Transport* (4th
  ed.), Chapter 5 (Trip distribution modelling). Wiley.
  <https://doi.org/10.1002/9781119993308>
- Fratar, T. J. (1954). Vehicular trip distribution by successive
  approximations. *Traffic Quarterly*, *8*(1), 53–65.
- Carroll, J. D., Jr. (1957). Future traffic predictions for the Detroit
  area. *Highway Research Board Proceedings*, 36.
- Furness, K. P. (1965). Time function iteration. *Traffic Engineering and
  Control*, 7(7), 458–460.
- Wilson, A. G. (1967). A statistical theory of spatial distribution
  models. *Transportation Research*, *1*(3), 253–269.
  <https://doi.org/10.1016/0041-1647(67)90035-4>
- Wilson, A. G. (1970). *Entropy in Urban and Regional Modelling*. Pion.
- Evans, A. W. (1970). Some properties of trip distribution methods.
  *Transportation Research*, *4*(1), 19–36.
  <https://doi.org/10.1016/0041-1647(70)90072-9>
- Fotheringham, A. S. (1983). A new set of spatial-interaction models: the
  theory of competing destinations. *Environment and Planning A*, *15*(1),
  15–36. <https://doi.org/10.1068/a150015>
