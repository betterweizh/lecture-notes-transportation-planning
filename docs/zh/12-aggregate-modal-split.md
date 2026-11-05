# 集计与组合交通方式划分模型

## 概述

{doc}`11-discrete-choice-models`对单个出行者的方式选择进行了建模。本章介绍交通方式划分（modal split）的**集计**（aggregate）方法，其中每种方式在某个 O-D 对上的分担率是小区平均出行费用的函数。本章从早期研究中的经验转移曲线出发，由熵最大化的分布–方式划分组合模型推导出 Logit 方式划分公式，引入多于两种方式时所需的组合费用和分层（巢式）结构，说明如何用线性回归标定二项 Logit 划分，并将模型应用于两个政策问题：拥堵收费和公交专用道。集计模型使用{doc}`11-discrete-choice-models`中为个体推导的 Logit 形式，但将其应用于出行矩阵每个单元 $T_{ij}$ 中各方式的分担率。

:::{admonition} 学习目标
:class: objectives
学完本章后，读者应能够：

- 列出影响方式选择的因素，并区分集计模型和非集计模型；
- 由熵最大化推导出行分布与方式划分组合模型，并解释其参数的双重作用；
- 定义一组交通方式的组合费用，并说明为什么正确的定义是对数和而不是加权平均；
- 解释红巴士/蓝巴士问题以及解决该问题的分层（巢式）结构；
- 用线性回归标定带方式惩罚项的二项 Logit 划分；
- 将集计 Logit 划分与拥堵函数结合，评价拥堵收费和公交专用道方案。
:::

## 符号说明

| 符号 | 含义 |
|---|---|
| $k$, $m$ | 交通方式 |
| $n$ | 人员类型（例如有无小汽车可用） |
| $T_{ij}^k$ | 从 $i$ 到 $j$ 采用方式 $k$ 的出行量；$T_{ij} = \sum_k T_{ij}^k$ |
| $P_{ij}^k = T_{ij}^k/T_{ij}$ | 方式 $k$ 在 $ij$ 对上的分担率 |
| $C_{ij}^k$ | 从 $i$ 到 $j$ 采用方式 $k$ 的广义费用 |
| $K_{ij}$ | 从 $i$ 到 $j$ 所有方式的组合费用 |
| $\beta$ | 目的地选择的离散参数；也用于单一的二项划分（转移曲线、政策应用） |
| $\lambda$ | 方式选择的离散参数 |
| $\delta$ | 某种方式的方式惩罚项（常数） |
| $A_i$, $B_j$ | 重力模型的平衡系数 |

## 影响方式选择的因素

决定出行者使用哪种方式的因素分为三组。

出行者特征
: 小汽车的可用性和拥有情况、是否持有驾照、家庭结构（年轻夫妇、有子女的家庭、退休者、单身）、在其他场合已决定的义务（工作需要用车、需接送子女）、收入以及居住密度。

出行特征
: 出行目的（工作出行规律性强，比购物或社交出行更容易使用公共交通）、出行时段（深夜出行较难由公共交通服务），以及该出行是否为出行链的一部分。

交通方式特征
: 定量因素——车内时间、候车和步行时间、票价、燃油和停车费用、停车位可得性——以及定性因素——舒适性、便利性、可靠性、规律性和安全性。

时间和货币各组成部分组合为**广义费用**（generalized cost）

$$
C_{ij}^k = a_1 t_{ij}^{k,\mathrm{iv}} + a_2 t_{ij}^{k,\mathrm{wait}}
         + a_3 t_{ij}^{k,\mathrm{walk}} + a_4 F_{ij}^k + \cdots + \delta^k ,
$$ (eq-12-generalized-cost-mode)

其中权重 $a_\ell$ 将各组成部分换算为统一单位（通过时间价值（value of time）换算为货币，或通过其倒数换算为时间），**方式惩罚项**（modal penalty）$\delta^k$ 反映未明确纳入的属性（例如舒适性）的影响。候车和步行时间的权重通常约为车内时间的两倍。

**集计**模型根据这些变量的小区平均值预测各方式在某 O-D 对上的*分担率*；**非集计**（disaggregate）模型则根据个体自身的数据预测其选择各方式的*概率*（{doc}`11-discrete-choice-models`）。

## 转移曲线

早期研究将每个 O-D 对上观测到的公共交通分担率，对小汽车与公共交通费用之差（或之比）作图，得到 S 形的**转移曲线**（diversion curve）。逻辑斯谛函数可以再现这一形状：

$$
\begin{aligned}
P_{ij}^{t} &= \frac{T_{ij}^{t}}{T_{ij}} \\
&= \frac{1}{1 + \exp\left[-\beta\left(C_{ij}^{c} - C_{ij}^{t}\right)\right]},
\end{aligned}
$$ (eq-12-diversion-curve)

其中 $c$ 表示小汽车，$t$ 表示公共交通。两种费用相等时，每种方式各占一半市场；离散参数（dispersion parameter）$\beta \ge 0$ 控制曲线的陡峭程度。当 $\beta \to 0$ 时，无论费用如何，划分都保持在 50 %；当 $\beta \to \infty$ 时，选择变为全有全无：费用较低的方式获得全部出行（{prf:ref}`ex-27-ms-diversion`）。

## 分布与方式划分组合模型

### 熵最大化模型

将重力模型的熵最大化推导（{doc}`10-trip-distribution`）推广到分方式的出行（Wilson, 1969）。给定出行端总量 $O_i$、$D_j$ 和出行总费用 $C$，按起点、终点和方式划分的最可能出行分布是下述问题的解：

$$
\begin{aligned}
\max_{T_{ij}^k \ge 0}\quad & H = -\sum_{i}\sum_{j}\sum_{k}\left(T_{ij}^k\ln T_{ij}^k - T_{ij}^k\right) \\
\text{s.t.}\quad & \sum_{j}\sum_{k} T_{ij}^k = O_i, \qquad \forall i, \\
& \sum_{i}\sum_{k} T_{ij}^k = D_j, \qquad \forall j, \\
& \sum_{i}\sum_{j}\sum_{k} T_{ij}^k C_{ij}^k = C .
\end{aligned}
$$ (eq-12-combined-dms)

目标函数严格凹，约束是线性的，因此解唯一。对三组约束分别引入拉格朗日乘子（Lagrange multiplier） $\alpha_i$、$\gamma_j$ 和 $\beta$，令拉格朗日函数对 $T_{ij}^k$ 的导数为零，得 $-\ln T_{ij}^k - \alpha_i - \gamma_j - \beta C_{ij}^k = 0$，即

$$
T_{ij}^k = A_i O_i B_j D_j \exp\left(-\beta C_{ij}^k\right),
$$ (eq-12-combined-solution)

其中 $A_i O_i = e^{-\alpha_i}$ 和 $B_j D_j = e^{-\gamma_j}$ 的取值使出行端约束成立：

$$
\begin{aligned}
A_i &= \frac{1}{\sum_j B_j D_j \sum_k e^{-\beta C_{ij}^k}}, \\
B_j &= \frac{1}{\sum_i A_i O_i \sum_k e^{-\beta C_{ij}^k}} .
\end{aligned}
$$

它们以 $\sum_k e^{-\beta C_{ij}^k}$ 为阻抗函数（deterrence function），用{doc}`10-trip-distribution`中的佛尼斯（Furness）迭代求得。

**方式划分是 Logit 形式。** 将 {eq}`eq-12-combined-solution` 除以其对各方式的和，平衡系数相互抵消：

$$
\begin{aligned}
P_{ij}^1 &= \frac{T_{ij}^1}{\sum_k T_{ij}^k} \\
&= \frac{\exp\left(-\beta C_{ij}^1\right)}{\sum_k \exp\left(-\beta C_{ij}^k\right)} .
\end{aligned}
$$ (eq-12-logit-split)

对两种方式，这就是转移曲线 {eq}`eq-12-diversion-curve`。Logit 划分具有实际中观测到的性质：曲线呈 S 形，费用相等时分担率相等，当竞争方式的费用增大时分担率趋于 1，并可直接推广到任意多种方式（{prf:ref}`ex-27-ms-combined`）。

### 分别设定离散参数

在 {eq}`eq-12-combined-solution` 中，单个参数 $\beta$ 起两种作用：它既控制在费用不同的*目的地*之间选择的离散程度，也控制在*方式*之间选择的离散程度。没有理由认为出行者在这两种选择中对费用同样敏感，因此更灵活的模型为方式选择单独设定参数 $\lambda$，并让目的地选择对概括所有方式的**组合费用**（composite cost）$K_{ij}$ 作出反应。再考虑不同的人员类型 $n$（例如有无小汽车可用），得

$$
T_{ij}^{kn} = \underbrace{A_i^n O_i^n B_j^n D_j^n \exp\left(-\beta^n K_{ij}^n\right)}_{T_{ij}^{n}:\ \text{出行分布}}
\ \times\
\underbrace{\frac{\exp\left(-\lambda^n C_{ij}^{k}\right)}{\sum_{m}\exp\left(-\lambda^n C_{ij}^{m}\right)}}_{P_{ij}^{kn}:\ \text{方式划分}},
$$ (eq-12-distribution-modal-split)

其中方式划分中的求和遍及人员类型 $n$ 可用的方式。为保持一致，参数必须满足 $\lambda^n \ge \beta^n$：出行者在给定目的地的方式之间进行选择时，对费用的敏感程度至少与在目的地之间选择时相同。

### 组合费用

$K_{ij}$ 应如何定义？一个看似自然的选择是按方式分担率加权的平均费用 $K = \sum_k P^k C^k$。这是错误的。假设只有一种费用为 $C^1$ 的方式可用，则 $K = C^1$；现在引入第二种费用更高的方式（$C^2 > C^1$）。分担率为 $P^1$ 和 $P^2 = 1 - P^1$ 时，

$$
\begin{aligned}
K^{*} &= (1 - P^2)\,C^1 + P^2 C^2 \\
&= C^1 + P^2\left(C^2 - C^1\right) \\
&> C^1 = K .
\end{aligned}
$$

增加一个选项反而使前往该目的地的出行显得*更*昂贵，这是荒谬的：新方式只会有帮助，最坏也只是让出行者无所谓。加权平均之所以失败，是因为它忽略了每个改用新方式的出行者之所以改用，是因为新方式*对他或她而言*更好。

一致的定义（Williams, 1977）是**对数和**：

$$
K_{ij}^n = -\frac{1}{\lambda^n}\ln\left[\sum_k \exp\left(-\lambda^n C_{ij}^k\right)\right],
\qquad \lambda^n > 0 .
$$ (eq-12-composite-cost)

当感知费用等于真实费用减去独立的 $\mathrm{Gumbel}(0, \lambda^n)$ 误差时，它与期望最小感知费用只相差加性常数 $-\gamma/\lambda^n$（{prf:ref}`prop-01-gumbel`的性质 6 和 {eq}`eq-11-logsum`），并具有所需的性质：

1. $K_{ij}^n \le \min_k C_{ij}^k$：组合费用从不高于最便宜的方式，增加一种方式会降低组合费用；
2. $\lim_{\lambda^n \to \infty} K_{ij}^n = \min_k C_{ij}^k$，即全有全无的极限；
3. $\partial K_{ij}^n / \partial C_{ij}^k = P_{ij}^{kn}$：某种方式的费用增加一个单位，组合费用增加的量等于该方式的分担率（{prf:ref}`ex-27-ms-composite`）。

## 多方式划分

### 多项结构与红巴士/蓝巴士问题

有多于两种方式时，最简单的结构是对所有方式同时应用 {eq}`eq-12-logit-split`（*多项*划分）。当各方式明显不同时这是可行的，但当其中两种方式是相近的替代品时就会失效。

假设某城市一半出行者使用小汽车，一半使用公交，即 $C_C = C_B$。公交公司现在把一半的公交车漆成红色、一半漆成蓝色，服务不变。多项 Logit 模型看到三个费用相等的方案，预测

$$
P_C = P_{RB} = P_{BB} = \frac{1}{3},
$$

于是给公交车刷漆就能把小汽车使用者吸引到公共交通上来。实际上，出行者把两种颜色视为同一种方式，分担率仍为 $P_C = 1/2$ 和 $P_{RB} = P_{BB} = 1/4$。这一缺陷来自 Logit 模型的**无关方案独立性**（independence of irrelevant alternatives，IIA）：比值 $P_C/P_{RB}$ 与蓝巴士是否存在无关（{doc}`11-discrete-choice-models`）。因此，相似或相同的方式不能作为多项划分中的不同方案分别列入。

### 分层（巢式）结构

**分层**结构将具有共同要素的方式归为一个组合方式。**一级划分**利用该组的组合费用，在组合方式与其余方式之间分配出行；**二级划分**再将组合方式的出行分配给其组成方式。对红/蓝巴士的情形，

$$
\begin{aligned}
P_C &= \frac{1}{1 + \exp\left[-\lambda_1\left(C_B - C_C\right)\right]}, \\
P_B &= 1 - P_C, \\
P_{RB \mid B} &= \frac{1}{1 + \exp\left[-\lambda_2\left(C_{BB} - C_{RB}\right)\right]}, \\
P_{BB \mid B} &= 1 - P_{RB \mid B},
\end{aligned}
$$ (eq-12-hierarchical-split)

其中公交的组合费用为

$$
C_B = -\frac{1}{\lambda_2}\ln\left[\exp\left(-\lambda_2 C_{RB}\right) + \exp\left(-\lambda_2 C_{BB}\right)\right],
$$

无条件分担率为 $P_{RB} = P_B\,P_{RB \mid B}$ 和 $P_{BB} = P_B\,P_{BB \mid B}$。为与效用最大化保持一致，下层划分的离散参数必须不小于上层，即 $\lambda_2 \ge \lambda_1$。在极限 $\lambda_2 \to \infty$（两种巴士完全可替代）时，$C_B = C_{RB} = C_C$，模型给出 $P_C = 1/2$ 和 $P_{RB} = P_{BB} = 1/4$，正如所期望的那样（{prf:ref}`ex-27-ms-red-blue`）。这一结构是{doc}`11-discrete-choice-models`中**巢式 Logit** 模型的集计对应形式。

## 标定二项 Logit 划分

为了反映实测费用中未包含的因素，给第二种方式加上方式惩罚项 $\delta$：

$$
\begin{aligned}
P_1 &= \frac{1}{1 + \exp\left[-\lambda\left(C_2 + \delta - C_1\right)\right]}, \\
P_2 &= 1 - P_1 .
\end{aligned}
$$ (eq-12-binary-split-penalty)

需要标定两个参数：离散参数 $\lambda$ 和惩罚项 $\delta$。取分担率之比再取对数，

$$
\begin{aligned}
\frac{P_1}{1 - P_1} &= \exp\left[\lambda\left(C_2 + \delta - C_1\right)\right] \\
\Longrightarrow\quad \ln\frac{P_1}{1 - P_1} &= \lambda\left(C_2 - C_1\right) + \lambda\delta .
\end{aligned}
$$ (eq-12-logit-linearization)

若已知若干 O-D 对的观测分担率 $P_1$ 和费用，则将 $y = \ln[P_1/(1 - P_1)]$ 对 $x = C_2 - C_1$ 作一元线性回归，得到斜率 $\hat\lambda$ 和截距 $\widehat{\lambda\delta}$，从而 $\hat\delta = \widehat{\lambda\delta}/\hat\lambda$（{prf:ref}`ex-27-ms-calibration`、{prf:ref}`ex-27-hw3-q1`）。这种线性化要求每个 O-D 对上都有 $0 < P_1 < 1$，并且不论出行量多少都给每个 O-D 对相同的权重；有非集计数据时，宜采用极大似然法（{doc}`11-discrete-choice-models`）。

## 政策应用

集计 Logit 划分与拥堵函数相结合，可用于评价交通政策。由于道路使用者的出行时间取决于小汽车数量，方式划分和出行时间必须作为一个不动点方程的解同时求出。

### 拥堵收费

考虑连接居住区和工作地的一条走廊，由一条快速轨道线路和一条公路服务，每小时有 $Q$ 名通勤者，每辆小汽车载一人。公共交通和小汽车的广义费用分别为

$$
\begin{aligned}
C_T &= \alpha T_T + P_T, \\
C_A &= \alpha T_A(Q_A) + P_A,
\end{aligned}
$$ (eq-12-pricing-costs)

其中 $\alpha$ 为时间价值，$T_T$ 为乘公共交通的（恒定的）门到门时间，$P_T$ 为统一票价，$P_A$ 为道路收费，$T_A(Q_A)$ 是小汽车流量 $Q_A$ 的增函数。采用 Logit 划分，

$$
\begin{aligned}
Q_A &= \frac{Q}{1 + \exp\left[-\beta\left(C_T - C_A(Q_A)\right)\right]}, \\
Q_T &= Q - Q_A .
\end{aligned}
$$ (eq-12-pricing-equilibrium)

方程 {eq}`eq-12-pricing-equilibrium` 两边都含有 $Q_A$；其唯一解（右端随 $Q_A$ 递减，左端递增）用牛顿法求得。反之，达到目标小汽车流量 $\bar{Q}_A$ 所需的收费，可以通过从 {eq}`eq-12-pricing-equilibrium` 中解出 $P_A$ 以闭式得到（{prf:ref}`ex-27-ms-pricing`）。

### 公交专用道

在一条有 $n$ 条车道、承载 $N$ 名独自驾车或乘坐公交的通勤者的公路上，划出 $n_{\mathrm{bus}}$ 条公交专用道会提高公交速度，吸引部分驾车者改乘公交，并使剩下的小汽车可用的车道减少。广义时间为 $C_{\mathrm{car}} = t_{\mathrm{car}}$ 和 $C_{\mathrm{bus}} = t_{\mathrm{bus}} + \Delta$，其中 $\Delta$ 汇总了公交的接驳、候车和不适惩罚，Logit 划分为

$$
\begin{aligned}
N_{\mathrm{car}} &= \frac{N}{1 + \exp\left[-\beta\left(C_{\mathrm{bus}} - C_{\mathrm{car}}\right)\right]}, \\
N_{\mathrm{bus}} &= N - N_{\mathrm{car}},
\end{aligned}
$$

总出行费用为

$$
TC = N_{\mathrm{bus}}\left(t_{\mathrm{bus}} + \Delta\right) + N_{\mathrm{car}}\,t_{\mathrm{car}} .
$$ (eq-12-bus-lane-tc)

若**成本效果比** $CE = TC_n^{n_{\mathrm{bus}}}/TC_n^{0}$ 小于 1，则该方案值得实施（{prf:ref}`ex-27-ms-bus-lane`）。

## 本章回顾

### 小结

- 交通方式的广义费用 {eq}`eq-12-generalized-cost-mode` 综合了时间、货币费用和方式惩罚项；经验转移曲线是逻辑斯谛曲线 {eq}`eq-12-diversion-curve`。
- 对分方式出行进行熵最大化 {eq}`eq-12-combined-dms`，得到 $T_{ij}^k = A_iO_iB_jD_j e^{-\beta C_{ij}^k}$ {eq}`eq-12-combined-solution`，其方式划分为 Logit 形式 {eq}`eq-12-logit-split`。
- 单独的方式选择参数 $\lambda^n \ge \beta^n$ {eq}`eq-12-distribution-modal-split` 需要引入组合费用；一致的组合费用是对数和 {eq}`eq-12-composite-cost`，它从不高于最便宜的方式。
- 相似的方式在分层结构中归为一组，进行一级划分和二级划分 {eq}`eq-12-hierarchical-split`，且 $\lambda_2 \ge \lambda_1$。
- 带方式惩罚项的二项 Logit 划分 {eq}`eq-12-binary-split-penalty` 通过将 $\ln[P_1/(1-P_1)]$ 对 $C_2 - C_1$ 回归进行标定 {eq}`eq-12-logit-linearization`。
- 政策评价将 Logit 划分与拥堵函数耦合，并求解均衡的方式划分（{eq}`eq-12-pricing-equilibrium`、{eq}`eq-12-bus-lane-tc`）。

### 常见错误

- **用按分担率加权的平均费用作为组合费用。** 增加一种更贵的方式时它反而增大，仿佛新选项使出行变差；应使用对数和 {eq}`eq-12-composite-cost`。
- **对相近的替代方式使用多项 Logit 划分。** 此时 IIA 使单纯的重新标记（红巴士/蓝巴士）也能吸引出行者；应将这些方式归入分层划分。
- **在组合模型中取 $\lambda < \beta$，或在分层划分中取 $\lambda_2 < \lambda_1$。** 这意味着出行者在目的地（或主要方式）之间比在相近方案之间对费用更敏感，与效用最大化不一致。
- **用*现状*出行时间下的方式划分评价政策。** 拥堵时间随方式划分而变化，因此方式划分与出行时间必须作为不动点一起求解。

## 参考文献

- Ortúzar, J. de D., & Willumsen, L. G. (2011). *Modelling Transport* (4th
  ed.), Chapter 6 (Modal split and direct demand models). Wiley.
- Williams, H. C. W. L. (1977). On the formation of travel demand models
  and economic evaluation measures of user benefit. *Environment and
  Planning A*, 9(3), 285–344. <https://doi.org/10.1068/a090285>
- Wilson, A. G. (1969). The use of entropy maximising models in the theory
  of trip distribution, mode split and route split. *Journal of Transport
  Economics and Policy*, 3(1), 108–126.
- Wilson, A. G. (1970). *Entropy in Urban and Regional Modelling*. Pion.
- Cambridge Systematics et al. (2012). *Travel Demand Forecasting:
  Parameters and Techniques* (NCHRP Report 716), Section 4.7.
  Transportation Research Board.
