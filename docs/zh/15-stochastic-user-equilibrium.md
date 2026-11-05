# 交通分配（三）：随机用户均衡

## 概述

Wardrop 第一原理假设每个出行者都确切知道每条路径的行程时间。实际出行者并非如此：他们对行程时间的感知存在误差，而且不同出行者的感知各不相同。**随机用户均衡**（stochastic user equilibrium，SUE）将感知的路径行程时间（perceived travel time）视为随机变量，并将{doc}`11-discrete-choice-models`中的随机效用理论应用于路径选择。本章定义随机用户均衡，推导基于 Logit 和基于 Probit 的形式，给出求解 Logit 随机用户均衡的 Fisk 凸规划，并介绍计算它所用的随机加载方法和相继平均法。

:::{admonition} 学习目标
:class: objectives
学完本章后，读者应能够：

- 解释确定性用户均衡与随机用户均衡的区别；
- 写出随机用户均衡条件及其 Logit 形式和 Probit 形式；
- 建立 Fisk 模型，并证明其最优性条件就是 Logit 随机用户均衡条件；
- 进行 Logit、Probit 和蒙特卡洛随机网络加载；
- 用相继平均法求解随机用户均衡。
:::

## 符号说明

| 符号 | 含义 |
|---|---|
| $C_k^{rs}$ | 路径 $k$ 的感知行程时间，是一个随机变量 |
| $c_k^{rs}(\bff)$ | 路径的平均（确定性）行程时间 |
| $\varepsilon_k^{rs}$ | 路径 $k$ 的感知误差 |
| $P_k^{rs}$ | 路径 $k$ 被感知为最短路径的概率 |
| $\theta$ | Logit 路径选择模型的离散参数 |
| $T_a$, $\zeta_a$ | 感知的路段行程时间及其随机误差 |
| $\bSigma$ | 路径感知误差的协方差矩阵 |

## 感知行程时间

$r$ 与 $s$ 之间路径 $k$ 的感知行程时间由确定性部分和随机部分组成：

$$
\begin{aligned}
C_k^{rs}(\bff) &= c_k^{rs}(\bff) + \varepsilon_k^{rs}, \\
\E\big[\varepsilon_k^{rs}\big] &= 0,
\end{aligned}
$$ (eq-15-perceived-cost)

其中 $c_k^{rs}(\bff) = \sum_a t_a(x_a)\,\delta_{a,k}^{rs}$ 是平均行程时间，与以前一样依赖于流量。随机项表示出行者之间感知的差异（从分析人员的角度看，还包括路径未被观测的属性）。每个出行者都选择他或她**感知**为最短的路径。因此，同一 O-D 对的出行者会分散到若干条路径上，平均行程时间最短的路径并不会吸引所有人。

在给定流量（因而给定平均行程时间）下，选择路径 $k$ 的出行者比例就是其感知时间最小的概率：

$$
P_k^{rs}(\bff) = \Prob\left(C_k^{rs} \le C_l^{rs},\ \forall l \in K_{rs}\right),
$$

这与效用为 $U_k = -C_k^{rs}$ 的随机效用最大化完全相同。

## 随机用户均衡

Daganzo 和 Sheffi（1977）将随机用户均衡定义为这样一种状态：没有出行者认为自己可以通过单方面改变路径来减少感知行程时间。此时每条路径上的流量等于需求乘以该路径被感知为最短路径的概率，概率在均衡流量下计算：

$$
f_k^{rs} = q_{rs}\,\Prob\left(c_k^{rs}(\bff) + \varepsilon_k^{rs}
\le c_l^{rs}(\bff) + \varepsilon_l^{rs},\ \forall l \in K_{rs}\right),
\qquad k \in K_{rs},\ r \in R,\ s \in S .
$$ (eq-15-sue)

这是不动点条件：概率通过行程时间依赖于流量，而流量又依赖于概率。当感知误差的方差趋于零时，随机用户均衡趋于确定性用户均衡；当方差增大时，行程时间的作用越来越小，出行者趋于均匀地分散到各条路径上。

### 基于 Logit 的随机用户均衡

若误差 $\varepsilon_k^{rs}$ 是独立同分布的耿贝尔变量，则选择概率为多项 Logit 形式（{prf:ref}`thm-11-mnl`），**基于 Logit 的随机用户均衡**条件为

$$
f_k^{rs} = q_{rs}\,\frac{\exp\left[-\theta c_k^{rs}(\bff)\right]}
{\sum_{l \in K_{rs}}\exp\left[-\theta c_l^{rs}(\bff)\right]},
\qquad k \in K_{rs},\ r \in R,\ s \in S .
$$ (eq-15-logit-sue)

离散参数（dispersion parameter）$\theta > 0$ 与感知误差的标准差成反比（耿贝尔尺度参数 $\mu = \theta$，因此误差方差为 $\pi^2/(6\theta^2)$）。$\theta$ 越大，误差越小，解越接近确定性用户均衡。

由于 Logit 模型只依赖于路径时间之差，10 分钟的时间差在 15 分钟的出行和 2 小时的出行中产生相同的划分，这是不现实的。Logit 模型还继承了 IIA 性质 {eq}`eq-11-iia`：两条共用大部分路段的路径被当作相互独立的方案，合计分到的流量过多。C-Logit（Cascetta 等，1996）和路径规模 Logit（path-size logit；Ben-Akiva 和 Bierlaire，1999）等修正方法在路径效用中加入一个重叠项；下面的 Probit 模型则能自然地处理路径重叠。

### 基于 Probit 的随机用户均衡

若路径误差服从均值为零、协方差矩阵为 $\bSigma$ 的多元正态分布，则条件 {eq}`eq-15-sue` 是**基于 Probit** 的。构造 $\bSigma$ 的一种自然方法是给每条路段一个独立的感知误差 $\zeta_a$，方差为 $\sigma_a^2$，于是感知路段时间为 $T_a = t_a(x_a) + \zeta_a$，路径误差等于其各路段误差之和：

$$
\begin{aligned}
\varepsilon_k^{rs} &= \sum_a \zeta_a\,\delta_{a,k}^{rs}, \\
\Cov\big[\varepsilon_k^{rs}, \varepsilon_l^{rs}\big] &= \sum_a \sigma_a^2\,\delta_{a,k}^{rs}\delta_{a,l}^{rs} .
\end{aligned}
$$ (eq-15-probit-covariance)

写成矩阵形式，$\bSigma = \bDelta\T\diag(\sigma_a^2)\bDelta$。重叠的路径共用路段，因而正相关，这就消除了 Logit 模型的重叠问题。Daganzo 和 Sheffi（1977）建议方差与自由流路段时间成正比，$\sigma_a^2 = \xi\,t_a^0$，这也使路径方差随出行长度增大。代价是：多于两条路径时，Probit 概率没有闭式解，需要通过模拟计算。

## Logit 随机用户均衡的 Fisk 模型

Fisk（1980）证明，Logit 随机用户均衡是下述规划的解：

$$
\begin{aligned}
\min_{\bff}\ z(\bff) &= \frac{1}{\theta}\sum_{r, s}\sum_{k \in K_{rs}} f_k^{rs}\left(\ln f_k^{rs} - 1\right)
+ \sum_a \int_0^{x_a} t_a(\omega)\,\diff\omega \\
\text{s.t.}\quad
\sum_{k \in K_{rs}} f_k^{rs} &= q_{rs}, \\
f_k^{rs} &\ge 0,
\end{aligned}
$$ (eq-15-fisk)

其中 $x_a$ 由 {eq}`eq-13-link-path-flow` 给出。第一项是路径流量的熵的相反数，与重力模型的熵最大化推导相同；第二项是 Beckmann 目标函数。

:::{prf:theorem} Fisk 模型与 Logit 随机用户均衡
:label: thm-15-fisk

{eq}`eq-15-fisk` 的路径流量解满足 Logit 随机用户均衡条件 {eq}`eq-15-logit-sue`，且路径流量解唯一。
:::

:::{dropdown} 证明
:class-container: proof
:animate: fade-in

与{prf:ref}`thm-13-beckmann-ue`一样引入乘子 $u_{rs}$ 和 $v_k^{rs} \ge 0$，由于

$$
\frac{\partial z}{\partial f_k^{rs}} = \frac{1}{\theta}\ln f_k^{rs} + c_k^{rs},
$$

KKT 条件为

$$
\begin{aligned}
\frac{1}{\theta}\ln f_k^{rs} + c_k^{rs} - u_{rs} - v_k^{rs} &= 0, \\
v_k^{rs}f_k^{rs} &= 0, \\
v_k^{rs} &\ge 0 .
\end{aligned}
$$

当 $f_k^{rs} \to 0$ 时，$\ln f_k^{rs} \to -\infty$，因此零路径流量不可能满足第一个条件：每条路径都有正流量，且 $v_k^{rs} = 0$。于是 $f_k^{rs} = \exp(\theta u_{rs})\exp(-\theta c_k^{rs})$，对 $k \in K_{rs}$ 求和并利用守恒条件，得

$$
\begin{aligned}
\exp(\theta u_{rs}) &= \frac{q_{rs}}{\sum_{l \in K_{rs}}\exp(-\theta c_l^{rs})}, \\
f_k^{rs} &= q_{rs}\,\frac{\exp(-\theta c_k^{rs})}{\sum_{l \in K_{rs}}\exp(-\theta c_l^{rs})} .
\end{aligned}
$$

这就是 {eq}`eq-15-logit-sue`。关于唯一性，$z$ 关于路径流量的黑塞矩阵为

$$
\nabla^2_{\bff} z = \frac{1}{\theta}\diag\left(\frac{1}{f_k^{rs}}\right)
+ \bDelta\T\diag\big(t_a'(x_a)\big)\bDelta,
$$

即一个正定对角矩阵与一个半正定矩阵之和。它是正定的，因此 $z$ 关于路径流量严格凸，解唯一——这与确定性用户均衡不同，后者只有路段流量是唯一的。
:::

在随机用户均衡下，每条路径都会分到一些流量，无论它有多长：Logit 模型给每个方案都赋予正的概率。实践中，路径集合被限制为“合理”的路径，例如逐步远离起点、接近终点的路径（Dial 的 STOCH 算法，Dial，1971），或由反复的最短路径搜索生成的路径。

## 随机网络加载

**随机网络加载**（stochastic network loading）在**固定的**路段行程时间 $\{t_a\}$ 下计算路径流量和路段流量：即计算一次 {eq}`eq-15-sue` 的右端。它所起的作用相当于全有全无分配对确定性用户均衡所起的作用。常用的方法有三种。

**Logit 加载。** 利用路径时间 $c_k^{rs} = \sum_a t_a\,\delta_{a,k}^{rs}$，直接应用 {eq}`eq-15-logit-sue`。对小型网络，通过枚举路径即可直接计算；Dial 算法则无需枚举路径就能在大型网络上完成同样的加载（{prf:ref}`ex-30-sue-logit-loading`）。

**解析 Probit 加载。** 对两条路径，路径 1 被感知为较短的概率是一个正态分布函数值：

$$
\begin{aligned}
\Prob\big(C_1 \le C_2\big) &= \Prob\big(\varepsilon_1 - \varepsilon_2 \le c_2 - c_1\big) \\
&= \Phi\left(\frac{c_2 - c_1}{\sqrt{\Var[\varepsilon_1 - \varepsilon_2]}}\right),
\end{aligned}
$$ (eq-15-probit-two-paths)

其中，在路段误差独立时，$\Var[\varepsilon_1 - \varepsilon_2]$ 等于恰好只属于两条路径之一的各路段的方差之和；共用路段的误差相互抵消（{prf:ref}`ex-30-sue-probit-loading`）。

**蒙特卡洛加载。** 对于更多的路径，Probit 概率通过模拟估计（Sheffi，1985，第 11.2 节）：

:::{prf:algorithm} 蒙特卡洛（模拟）随机加载
:label: alg-15-monte-carlo-loading

**输入：** 平均路段时间 $\{t_a\}$、误差分布、O-D 矩阵和容差 $\varepsilon$。

1. 令 $n = 1$，$\bx^{(0)} = \bzero$。
2. **抽样。** 为每条路段从其分布中抽取一个感知时间 $T_a^{(n)}$。
3. **全有全无分配。** 以路段时间 $T_a^{(n)}$ 将每个 O-D 流量分配到其最短路径上，得到路段流量 $\bX^{(n)}$。
4. **平均。** 对所有 $a$，令 $x_a^{(n)} = \big[(n - 1)\,x_a^{(n-1)} + X_a^{(n)}\big]/n$。
5. **终止检验。** 若 $n > 1$，且平均流量的变化（例如在流量为正的路段上的 $\max_a \lvert x_a^{(n)} - x_a^{(n-1)}\rvert/x_a^{(n-1)}$）不超过 $\varepsilon$，则停止；否则令 $n \leftarrow n + 1$，返回第 2 步。
:::

每次抽样代表一个对网络有特定感知的出行者（或一组出行者）。与所有模拟一样，平均流量以 $1/\sqrt{n}$ 的缓慢速度收敛到 Probit 加载结果，因此相邻平均值变化小只是一个较弱的终止准则；实践中采用固定的、较大的抽样次数（{prf:ref}`ex-30-sue-monte-carlo`）。

## 求解随机用户均衡的相继平均法

随机用户均衡将随机加载与确定性用户均衡中的拥堵反馈结合起来。Fisk 目标函数可以用 Frank–Wolfe 类方法最小化，但 Probit 模型的加载是一种模拟，其目标函数（Sheffi 和 Powell，1982）计算代价高，而且加载得到的流量带有噪声。**相继平均法**避免了线搜索，并能容忍噪声（Sheffi 和 Powell，1982）：

:::{prf:algorithm} 求解随机用户均衡的相继平均法
:label: alg-15-msa-sue

1. **初始化。** 以自由流时间 $t_a(0)$ 进行一次随机加载，得到 $\bx^{(1)}$。令 $n = 1$。
2. **更新。** 对所有 $a$，令 $t_a^{(n)} = t_a\big(x_a^{(n)}\big)$。
3. **寻找方向。** 以时间 $t_a^{(n)}$ 进行一次随机加载，得到辅助流量 $\by^{(n)}$。
4. **移动。** 令 $\bx^{(n+1)} = \bx^{(n)} + \frac{1}{n}\big(\by^{(n)} - \bx^{(n)}\big)$。
5. **收敛检验。** 若 $\sqrt{\sum_a\big(x_a^{(n+1)} - x_a^{(n)}\big)^2}\big/\sum_a x_a^{(n)} \le \varepsilon$，则停止；否则令 $n \leftarrow n + 1$，返回第 2 步。
:::

该算法就是把全有全无分配换成随机加载的{prf:ref}`alg-13-msa-ue`。由于步长按 $1/n$ 缩小，蒙特卡洛加载的噪声在迭代过程中被平均掉；原则上每次迭代只抽样一次就足够了。这里的终止准则同样较弱，因为步长本身越来越小；更好的检验是将当前流量与在当前时间下重新进行的一次加载结果相比较（{prf:ref}`ex-30-sue-msa`）。

### 确定性用户均衡与随机用户均衡的比较

| | 确定性用户均衡（DUE） | 随机用户均衡（SUE） |
|---|---|---|
| 信息 | 完全信息 | 感知有误差 |
| 路径选择 | 只使用时间最短的路径 | 每条路径都有正的概率 |
| 条件 | {eq}`eq-13-ue-conditions` | {eq}`eq-15-sue` |
| 数学规划 | Beckmann {eq}`eq-13-beckmann` | Fisk {eq}`eq-15-fisk`（Logit） |
| 唯一性 | 路段流量 | 路段流量和路径流量（Logit） |
| 加载 | 全有全无 | Logit、Probit、蒙特卡洛 |
| 算法 | Frank–Wolfe、MSA、基于路径或基于丛的算法 | MSA |

在有许多相似路径的网络上，随机用户均衡更接近观测到的行为；即使拥堵较轻，它也会把流量分散到平行路径上。其参数（$\theta$ 或误差方差）必须标定，例如根据观测的路径选择或路段计数。

## 本章回顾

### 小结

- 随机用户均衡假设出行者最小化感知行程时间 {eq}`eq-15-perceived-cost`；路径流量等于需求乘以被感知为最短路径的概率 {eq}`eq-15-sue`。
- 耿贝尔误差给出 Logit 随机用户均衡 {eq}`eq-15-logit-sue`；由路段误差构造的正态误差 {eq}`eq-15-probit-covariance` 给出 Probit 随机用户均衡，重叠路径之间是相关的。
- Fisk 模型 {eq}`eq-15-fisk` 在 Beckmann 目标函数上加了熵项；其唯一解就是 Logit 随机用户均衡（{prf:ref}`thm-15-fisk`）。
- 随机加载——Logit、解析 Probit {eq}`eq-15-probit-two-paths` 和蒙特卡洛（{prf:ref}`alg-15-monte-carlo-loading`）——取代全有全无分配，相继平均法（{prf:ref}`alg-15-msa-sue`）求解均衡。

### 常见错误

- **期望随机用户均衡下长路径上的流量为零。** Logit 模型给每条被枚举的路径赋予正的概率，因此每条路径都会被使用；应当限制路径集合。
- **不加修正地将 Logit 模型应用于高度重叠的路径。** IIA 性质把它们当作相互独立的方案，从而分给它们过多的流量；应使用修正项或 Probit 模型。
- **混淆随机加载与随机用户均衡。** 加载使用固定的时间；均衡时时间依赖于流量。
- **蒙特卡洛抽样次数太少，或只根据相邻平均值的变化判断收敛。** 模拟误差按 $1/\sqrt{n}$ 减小，步长小并不意味着误差小。
- **忘记 $\theta$ 是有单位的。** 它以时间单位的倒数计：其取值取决于时间以分钟还是小时计。

## 参考文献

- Ben-Akiva, M., & Bierlaire, M. (1999). Discrete choice methods and their
  applications to short term travel decisions. In R. W. Hall (Ed.),
  *Handbook of Transportation Science* (pp. 5–33). Kluwer.
- Cascetta, E., Nuzzolo, A., Russo, F., & Vitetta, A. (1996). A modified
  logit route choice model overcoming path overlapping problems:
  Specification and some calibration results for interurban networks. In
  J.-B. Lesort (Ed.), *Transportation and Traffic Theory* (pp. 697–711).
  Pergamon.
- Daganzo, C. F., & Sheffi, Y. (1977). On stochastic models of traffic
  assignment. *Transportation Science*, *11*(3), 253–274.
- Dial, R. B. (1971). A probabilistic multipath traffic assignment model
  which obviates path enumeration. *Transportation Research*, *5*(2), 83–111.
- Fisk, C. (1980). Some developments in equilibrium traffic assignment.
  *Transportation Research Part B*, *14*(3), 243–255.
- Ortúzar, J. de D., & Willumsen, L. G. (2011). *Modelling Transport* (4th
  ed.), Chapters 10 and 11. Wiley.
- Sheffi, Y. (1985). *Urban Transportation Networks: Equilibrium Analysis
  with Mathematical Programming Methods*, Sections 10.1–10.2 and Chapters
  11–12. Prentice-Hall.
- Sheffi, Y., & Powell, W. B. (1982). An algorithm for the equilibrium
  assignment problem with random link times. *Networks*, *12*(2), 191–207.
