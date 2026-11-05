# 交通分配（二）：系统最优、弹性需求与组合模型

## 概述

用户均衡描述出行者的行为方式；它并不使网络中的总耗时最小。本章介绍 Wardrop 第二原理（Wardrop's second principle），即**系统最优**（system optimum，SO），将其与用户均衡进行比较，并说明边际成本定价如何把用户均衡转化为系统最优。Braess 悖论表明二者的差别对规划很重要。然后，本章从两个方面放松 O-D 矩阵固定的假设：随行程时间增加而减少的**弹性需求**（elastic demand），以及同时确定出行矩阵和网络流量的**分布–分配组合模型**（combined distribution–assignment model）。

:::{admonition} 学习目标
:class: objectives
学完本章后，读者应能够：

- 阐述 Wardrop 第二原理，并将系统最优表述为凸规划；
- 解释路段的边际成本，并将系统最优作为以边际成本函数为阻抗的用户均衡来求解；
- 计算使用户均衡达到系统最优的边际成本收费；
- 解释 Braess 悖论；
- 建立并利用超额需求网络求解弹性需求下的用户均衡；
- 建立分布–分配组合模型，并说明其求解方法。
:::

## 符号说明

| 符号 | 含义 |
|---|---|
| $\mathrm{TSTT}$ | 系统总出行时间 $\sum_a x_at_a(x_a)$ |
| $\tilde t_a(x_a)$ | 路段 $a$ 的边际（社会）成本，$t_a + x_at_a'$ |
| $\tau_a$ | 路段 $a$ 的收费（以时间计） |
| $D_{rs}(u_{rs})$, $D_{rs}^{-1}(q_{rs})$ | $rs$ 对的需求函数及其反函数 |
| $\bar q_{rs}$ | 需求的上界，$D_{rs}(0)$ |
| $e_{rs}$, $W_{rs}(e_{rs})$ | 超额需求及其费用函数 |
| $O_r$, $D_s$ | 起点 $r$ 的出行产生量和终点 $s$ 的出行吸引量 |
| $\beta$ | 重力（熵）模型的离散参数 |

## 系统最优

### Wardrop 第二原理

Wardrop（1952）提出了第二原理：

> 平均出行时间最小。

平均出行时间等于总出行时间除以总需求，而总需求是固定的，因此最小化平均出行时间等价于最小化**系统总出行时间**（total system travel time）。对各路径时间求和，再按路段重新归组（每条路段出现在使用它的每条路径中），得到

$$
\begin{aligned}
\sum_{r, s}\sum_{k \in K_{rs}} f_k^{rs}c_k^{rs} &= \sum_{r, s}\sum_{k \in K_{rs}} f_k^{rs}\sum_a t_a(x_a)\,\delta_{a,k}^{rs} \\
&= \sum_{a \in A} x_a\,t_a(x_a) .
\end{aligned}
$$ (eq-14-tstt)

### 系统最优模型

**系统最优**在可行流量上最小化 {eq}`eq-14-tstt`：

$$
\begin{aligned}
\min_{\bff}\ \tilde z(\bx) &= \sum_{a \in A} x_a\,t_a(x_a) \\
\text{s.t.}\quad
\sum_{k \in K_{rs}} f_k^{rs} &= q_{rs}, \\
f_k^{rs} &\ge 0, \\
x_a &= \sum_{r, s}\sum_{k \in K_{rs}} f_k^{rs}\,\delta_{a,k}^{rs} .
\end{aligned}
$$ (eq-14-so)

约束与 Beckmann 模型 {eq}`eq-13-beckmann` 相同，只有目标函数不同。系统最优的流量模式一般**不是均衡**：只有当所有出行者共同行动以最小化总出行时间（而非各自的出行时间）时才能达到。在系统最优状态下，有些出行者可以通过单方面改变路径来减少自己的出行时间，因此这种模式无法自我维持，也不能用于预测实际的路径选择。不过，它是一个衡量标准：系统总出行时间是网络的关键绩效指标，而系统最优给出了任何路径诱导或收费政策所能达到的最佳值。

### 边际成本与系统最优条件

定义路段 $a$ 的**边际成本**（marginal cost）：

$$
\begin{aligned}
\tilde t_a(x_a) &= \frac{\diff\left[x_a t_a(x_a)\right]}{\diff x_a} \\
&= t_a(x_a) + x_a\,t_a'(x_a) .
\end{aligned}
$$ (eq-14-marginal-cost)

它是多一名出行者导致的路段 $a$ 上总出行时间的增量，由两部分组成：$t_a(x_a)$ 是这名新增出行者自己经历的行程时间，$x_at_a'(x_a)$ 是他或她给路段上已有的 $x_a$ 名出行者带来的额外延误。第二部分是一种**外部性**（externality）：为自己选择路径的出行者会忽略它。

由于 $x_at_a(x_a) = \int_0^{x_a}\tilde t_a(\omega)\,\diff\omega$，系统最优模型 {eq}`eq-14-so` 就是把 $t_a$ 换成 $\tilde t_a$ 的 Beckmann 模型。应用{prf:ref}`thm-13-beckmann-ue`得：

:::{prf:theorem} 作为用户均衡的系统最优
:label: thm-14-so-ue

系统最优流量就是将路段阻抗函数换成边际成本函数 $\tilde t_a(x_a)$ 后同一网络上的用户均衡流量。在系统最优状态下，一个 O-D 对的所有被使用路径具有相等且最小的**边际**路径费用 $\tilde c_k^{rs} = \sum_a \tilde t_a(x_a)\,\delta_{a,k}^{rs}$。
:::

因此，任何求解用户均衡的算法，只要输入边际成本函数，就能求解系统最优。$\tilde z$ 的黑塞矩阵是对角矩阵，其元素为 $\tilde t_a'(x_a) = 2t_a'(x_a) + x_a t_a''(x_a)$，因此若对所有路段都有 $2t_a'(x_a) + x_at_a''(x_a) > 0$，则**系统最优路段流量唯一**；所有严格递增的凸路段函数（包括 BPR 函数）都满足这一条件。

### 用户均衡与系统最优何时重合？

若行程时间不依赖于流量，$t_a(x_a) = t_a^0$，则 $\tilde t_a = t_a$，两个规划都化为 $\min \sum_a t_a^0x_a$：用户均衡与系统最优重合，二者都是以自由流时间进行的全有全无分配。这就是不拥堵网络的情形。存在拥堵时二者不同，而且用户均衡的总出行时间永远不小于系统最优的总出行时间。二者之比称为**无政府代价**（price of anarchy），对于线性路段函数的网络，它至多为 $4/3$（Roughgarden 和 Tardos，2002）；在{prf:ref}`ex-29-so-two-route`的两路径网络中，它为 $350/279.63 = 1.25$，而在实际网络中该比值通常更接近 1。

## 边际成本定价

设 $\{x_a^{\mathrm{SO}}\}$ 为系统最优流量。若对每条路段收取（以时间计的）通行费（toll）

$$
\tau_a = x_a^{\mathrm{SO}}\,t_a'\big(x_a^{\mathrm{SO}}\big), \qquad a \in A,
$$ (eq-14-mc-toll)

即等于系统最优状态下的外部性，则最小化自身广义时间 $\hat t_a(x_a) = t_a(x_a) + \tau_a$ 的出行者所达到的用户均衡就是系统最优。事实上，收费下的用户均衡最小化

$$
\sum_a \int_0^{x_a}\left[t_a(\omega) + \tau_a\right]\diff\omega,
$$

其 KKT 条件要求被使用的路径上费用 $\sum_a \big[t_a(x_a) + \tau_a\big]\delta_{a,k}^{rs}$ 相等。在 $\bx = \bx^{\mathrm{SO}}$ 处，$t_a + \tau_a = \tilde t_a$，因此系统最优流量满足这些条件，由唯一性，它就是收费下的均衡。

通行费以时间表示；乘以时间价值即可换算为货币。实际的收费方案只能近似 {eq}`eq-14-mc-toll`，因为不可能对每条路段都收费；而随时段变化的收费，例如新加坡的电子道路收费（ERP），针对的是该问题的动态版本（{doc}`16-dynamic-assignment-and-simulation`）。

## Braess 悖论

在网络中增加一条路段不会增加系统最优的总出行时间——新路段总可以闲置不用。用户均衡则没有这样的保证。在{numref}`fig-14-braess-network`的网络中，每单位时间有 6 次出行从节点 1 到节点 4。没有路段 5 时，均衡把它们平均分配到两条路径上，每条路径的时间为 83。增加路段 5 后，六次出行中有两次转到新路径 1–3–2–4，三条路径各承担两次出行，每个出行者的时间都增加到 92，尽管其他一切都没有改变（{prf:ref}`ex-29-braess`）。这就是 **Braess 悖论**（Braess's paradox；Braess，1968；英译本见 Braess 等，2005）：在用户均衡下，额外的通行能力可能使每个人都变得更糟，因为每个出行者都忽略了自己给他人带来的延误。对规划的启示是：网络改善必须用交通分配模型评价，而不能凭直觉；收费（或取消某些路段）可以改善网络。

```{figure} figures/14-braess-network.svg
:name: fig-14-braess-network
:width: 420px
:class: dark-light

Braess 网络：从节点 1 到节点 4 有 6 次出行，图中标出了各路段的阻抗函数。虚线所示的路段 5 是新建道路。
```

## 弹性需求下的用户均衡

### 需求函数

到目前为止，O-D 矩阵都是固定的。实际上，拥堵会抑制部分出行：这些出行会改在其他时间、去往其他目的地、改用其他方式，或者干脆取消。假设 $rs$ 对的需求是均衡行程时间的递减函数：

$$
\begin{aligned}
q_{rs} &= D_{rs}(u_{rs}), \\
u_{rs} &= D_{rs}^{-1}(q_{rs}),
\end{aligned}
$$

例如 $q_{rs} = 10 - 0.2\,u_{rs}$（反函数 $u_{rs} = 50 - 5q_{rs}$）或 $q_{rs} = \bar q_{rs}\exp(-\beta u_{rs})$（反函数 $u_{rs} = -\ln(q_{rs}/\bar q_{rs})/\beta$）。反需求函数 $D_{rs}^{-1}(q_{rs})$ 是恰好有 $q_{rs}$ 次出行时的行程时间：即边际出行者的出行意愿。

### 模型表述与均衡条件

**弹性需求下的用户均衡**是下述问题的解：

$$
\begin{aligned}
\min_{\bff, \bq}\ z(\bx, \bq) &= \sum_{a}\int_0^{x_a} t_a(\omega)\,\diff\omega
- \sum_{r, s}\int_0^{q_{rs}} D_{rs}^{-1}(\omega)\,\diff\omega \\
\text{s.t.}\quad
\sum_{k \in K_{rs}} f_k^{rs} &= q_{rs}, \\
f_k^{rs} &\ge 0, \\
q_{rs} &\ge 0,
\end{aligned}
$$ (eq-14-elastic)

路段流量由 {eq}`eq-13-link-path-flow` 定义。对附加变量 $q_{rs}$ 重复{prf:ref}`thm-13-beckmann-ue`的证明，得到 KKT 条件

$$
\begin{aligned}
f_k^{rs}\left(c_k^{rs} - u_{rs}\right) &= 0, \\
c_k^{rs} - u_{rs} &\ge 0, \\
q_{rs}\left(u_{rs} - D_{rs}^{-1}(q_{rs})\right) &= 0, \\
u_{rs} - D_{rs}^{-1}(q_{rs}) &\ge 0 .
\end{aligned}
$$ (eq-14-elastic-conditions)

第一对条件是 Wardrop 原理。第二对条件表明：若 $r$ 与 $s$ 之间有出行，则其数量恰好等于均衡行程时间下的需求 $q_{rs} = D_{rs}(u_{rs})$；若没有出行，则行程时间超过了连第一名出行者都愿意承受的时间。由于 $-D_{rs}^{-1}$ 递增，目标函数关于 $(\bx, \bq)$ 严格凸，均衡路段流量和 O-D 需求都是唯一的。

### 超额需求网络

令 $\bar q_{rs} = D_{rs}(0)$ 为需求的上界（或任何足够大、需求永远达不到的数），并定义**超额需求**（excess demand）$e_{rs} = \bar q_{rs} - q_{rs}$：即没有发生的出行。在需求积分中作代换 $\omega = \bar q_{rs} - v$，得

$$
\begin{aligned}
-\int_0^{q_{rs}} D_{rs}^{-1}(\omega)\,\diff\omega
&= -\int_0^{\bar q_{rs}} D_{rs}^{-1}(\omega)\,\diff\omega
+ \int_{q_{rs}}^{\bar q_{rs}} D_{rs}^{-1}(\omega)\,\diff\omega \\
&= \text{常数} + \int_0^{e_{rs}} D_{rs}^{-1}(\bar q_{rs} - v)\,\diff v .
\end{aligned}
$$

利用**超额需求函数** $W_{rs}(e_{rs}) = D_{rs}^{-1}(\bar q_{rs} - e_{rs})$，模型 {eq}`eq-14-elastic` 变为

$$
\begin{aligned}
\min\ & \sum_a \int_0^{x_a} t_a(\omega)\,\diff\omega
+ \sum_{r, s}\int_0^{e_{rs}} W_{rs}(v)\,\diff v \\
\text{s.t.}\ & \sum_{k \in K_{rs}} f_k^{rs} + e_{rs} = \bar q_{rs}, \\
& f_k^{rs} \ge 0, \\
& e_{rs} \ge 0 .
\end{aligned}
$$ (eq-14-excess-demand)

这是扩展网络上的**固定需求**用户均衡：对每个 O-D 对，增加一条从 $r$ 直接到 $s$、阻抗函数为 $W_{rs}(e_{rs})$ 的虚拟路段，并分配固定需求 $\bar q_{rs}$。虚拟路段上的流量就是超额需求；均衡时虚拟路段的费用等于被使用路径的时间：“没有发生”的出行就是出行意愿低于均衡行程时间的那些出行。由于 $D_{rs}^{-1}$ 递减，$W_{rs}$ 递增，因此任何固定需求算法——Frank–Wolfe 算法、相继平均法——都可以不加修改地求解弹性需求问题（{prf:ref}`ex-29-elastic-demand`）。只要 $\bar q_{rs}$ 大于均衡需求，其取值就不影响解。

## 分布–分配组合模型

### 动机

{doc}`10-trip-distribution`中的重力模型把出行费用 $c_{rs}$ 视为给定，但这些费用本身是把出行矩阵分配到网络上的结果。只按顺序运行一遍四个阶段，会使二者相互矛盾：用于分布出行的费用并不是分配这些出行所产生的费用。**组合模型**同时确定出行矩阵和路段流量，使出行按均衡费用进行分布。

### 模型表述

Evans（1976）将 Beckmann 目标函数与双约束重力模型的熵项（{doc}`10-trip-distribution`）结合起来：

$$
\begin{aligned}
\min_{\bff, \bq}\ z(\bx, \bq) &= \sum_a\int_0^{x_a} t_a(\omega)\,\diff\omega
+ \frac{1}{\beta}\sum_{r, s} q_{rs}\left(\ln q_{rs} - 1\right) \\
\text{s.t.}\quad
\sum_{s} q_{rs} &= O_r, \\
\sum_{r} q_{rs} &= D_s, \\
\sum_{k \in K_{rs}} f_k^{rs} &= q_{rs}, \\
f_k^{rs} &\ge 0,
\end{aligned}
$$ (eq-14-combined-da)

路段流量由 {eq}`eq-13-link-path-flow` 给出。目标函数关于 $(\bx, \bq)$ 严格凸，因此路段流量和出行矩阵的解都唯一。

### 最优性条件

对路径守恒约束引入乘子 $u_{rs}$，对出行端约束引入乘子 $\mu_r$、$\lambda_s$，路径流量的条件就是 Wardrop 条件 {eq}`eq-13-ue-conditions`：$u_{rs}$ 是均衡行程时间。对（正的）O-D 流量，

$$
\frac{\partial L}{\partial q_{rs}} = \frac{1}{\beta}\ln q_{rs} + u_{rs} - \mu_r - \lambda_s,
$$

它在最优点为零，因此 $q_{rs} = \exp(\beta\mu_r)\exp(\beta\lambda_s)\exp(-\beta u_{rs})$。由 $\sum_s q_{rs} = O_r$ 和 $\sum_r q_{rs} = D_s$ 确定两个指数因子，得

$$
\begin{aligned}
q_{rs} &= A_r O_r B_s D_s \exp(-\beta u_{rs}), \\
A_r &= \frac{1}{\sum_s B_s D_s \exp(-\beta u_{rs})}, \\
B_s &= \frac{1}{\sum_r A_r O_r \exp(-\beta u_{rs})} .
\end{aligned}
$$ (eq-14-combined-da-solution)

出行矩阵是**以均衡行程时间计算**的双约束重力模型，而路段流量是该出行矩阵下的用户均衡：分布与分配相互一致。

### 求解算法

将 Frank–Wolfe 算法应用于 {eq}`eq-14-combined-da`，会同时对 $\bx$ 和 $\bq$ 线性化目标函数。O-D 流量的线性化费用为 $u_{rs}^{(n)} + \tfrac{1}{\beta}\ln q_{rs}^{(n)}$，因此寻找方向的步骤是一个 **Hitchcock 运输问题**——以最小线性化费用分配出行端总量的线性规划——再对所得矩阵进行全有全无分配（Sheffi，1985，第 7.3–7.4 节）。Evans（1976）的**部分线性化**方法精确保留熵项，只对网络部分线性化，效率更高：

:::{prf:algorithm} 分布–分配组合模型的 Evans 算法
:label: alg-14-evans

1. **初始化。** 用自由流路段时间计算最短路径时间，以这些时间求解重力模型 {eq}`eq-14-combined-da-solution`，并对所得矩阵进行全有全无分配，得到 $\bq^{(1)}$ 和 $\bx^{(1)}$。令 $n = 1$。
2. **更新。** 令 $t_a^{(n)} = t_a\big(x_a^{(n)}\big)$，并计算最短路径时间 $u_{rs}^{(n)}$。
3. **寻找方向。** 以费用 $u_{rs}^{(n)}$ 求解双约束重力模型（双比例拟合），得到辅助矩阵 $\bv^{(n)}$。将 $\bv^{(n)}$ 按最短路径进行全有全无分配，得到辅助路段流量 $\by^{(n)}$。
4. **线搜索。** 求 $\alpha_n \in [0, 1]$，使 $z\big(\bx^{(n)} + \alpha(\by^{(n)} - \bx^{(n)}),\ \bq^{(n)} + \alpha(\bv^{(n)} - \bq^{(n)})\big)$ 最小。
5. **移动。** 以步长 $\alpha_n$ 更新 $\bx$ 和 $\bq$。
6. **收敛检验。** 若流量和矩阵不再变化，则停止；否则令 $n \leftarrow n + 1$，返回第 2 步。
:::

线搜索函数的导数等于 Frank–Wolfe 导数 {eq}`eq-13-fw-line-search` 加上 $\tfrac{1}{\beta}\sum_{r,s}\ln\big(q_{rs} + \alpha(v_{rs} - q_{rs})\big)(v_{rs} - q_{rs})$。{prf:ref}`ex-29-combined-da`将该算法应用于六节点网络。同样的思路可以推广到包含方式选择的组合模型，此时用{doc}`12-aggregate-modal-split`中的对数和代替行程时间。

## 本章回顾

### 小结

- 系统最优 {eq}`eq-14-so` 使系统总出行时间 {eq}`eq-14-tstt` 最小；它就是以边际成本 $\tilde t_a = t_a + x_at_a'$ {eq}`eq-14-marginal-cost` 为阻抗的用户均衡（{prf:ref}`thm-14-so-ue`）。
- 边际成本收费 {eq}`eq-14-mc-toll` 使用户均衡达到系统最优；Braess 悖论（{numref}`fig-14-braess-network`）表明，增加通行能力可能使用户均衡变差。
- 弹性需求在 Beckmann 目标函数中增加了 $-\sum\int D^{-1}$ 项 {eq}`eq-14-elastic`，其条件为 {eq}`eq-14-elastic-conditions`；超额需求网络 {eq}`eq-14-excess-demand` 将其转化为固定需求问题。
- 组合模型 {eq}`eq-14-combined-da` 增加了熵项；其解是以均衡行程时间计算的重力模型 {eq}`eq-14-combined-da-solution`，用 Evans 算法（{prf:ref}`alg-14-evans`）求解。

### 常见错误

- **把系统最优当作路径选择的预测。** 在系统最优状态下，有些出行者改变路径可以获益；系统最优是一个基准，而不是行为模型。
- **用路段行程时间而不是边际成本求解系统最优。** 系统最优是以 $\tilde t_a$ 为阻抗的用户均衡；对线性函数，不要忘记 $\tilde t_a = A_a + 2B_ax_a$ 中的系数 2。
- **用用户均衡流量计算收费。** 收费 {eq}`eq-14-mc-toll` 应在系统最优流量处计算。
- **认为额外的通行能力总能减少出行时间。** 在用户均衡下，它可能使每个人的出行时间都增加（Braess 悖论）。
- **选取小于均衡需求的上界 $\bar q_{rs}$。** 这样超额需求 $e_{rs}$ 就必须为负；$\bar q_{rs}$ 必须大于需求，例如取 $\bar q_{rs} = D_{rs}(0)$。
- **只按顺序运行一遍四个阶段就把结果称为均衡。** 此时用于分布的费用与分配得到的费用不同；要保持一致性，需要反馈或组合模型。

## 参考文献

- Braess, D. (1968). Über ein Paradoxon aus der Verkehrsplanung.
  *Unternehmensforschung*, *12*, 258–268.
- Braess, D., Nagurney, A., & Wakolbinger, T. (2005). On a paradox of
  traffic planning [English translation of Braess, 1968]. *Transportation
  Science*, 39(4), 446–450. <https://doi.org/10.1287/trsc.1050.0127>
- Evans, S. P. (1976). Derivation and analysis of some models for combining
  trip distribution and assignment. *Transportation Research*, *10*(1), 37–57.
- Ortúzar, J. de D., & Willumsen, L. G. (2011). *Modelling Transport* (4th
  ed.), Chapters 10 and 11. Wiley.
- Roughgarden, T., & Tardos, É. (2002). How bad is selfish routing?
  *Journal of the ACM*, *49*(2), 236–259.
- Sheffi, Y. (1985). *Urban Transportation Networks: Equilibrium Analysis
  with Mathematical Programming Methods*, Sections 3.4–3.5, 6.1–6.3, and
  7.3–7.4. Prentice-Hall.
- Wardrop, J. G. (1952). Some theoretical aspects of road traffic research.
  *Proceedings of the Institution of Civil Engineers, Part II*, *1*(3),
  325–378. <https://doi.org/10.1680/ipeds.1952.11259>
