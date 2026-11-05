# 需求建模中的概率分布

## 概述

出行时间、出行费用以及出行者偏好中无法观测的部分都是随机的。离散选择模型（{doc}`11-discrete-choice-models`）和随机交通分配（{doc}`15-stochastic-user-equilibrium`）都建立在对这些随机项分布的特定假设之上，而 Logit 模型简洁的闭式解正是来自**耿贝尔分布**（Gumbel distribution）和**逻辑斯谛分布**（logistic distribution）的特殊性质。本章回顾全书用到的概率分布，并证明后续各章所依赖的性质。

:::{admonition} 学习目标
:class: objectives
学完本章后，读者应能够：

- 计算均匀分布和正态分布的概率、均值和方差；
- 写出耿贝尔分布和逻辑斯谛分布及其矩，并说明它们如何由极值产生；
- 证明尺度参数相同的独立耿贝尔随机变量的最大值仍服从耿贝尔分布，而两个这样的变量之差服从逻辑斯谛分布；
- 计算联合正态随机变量线性组合的概率；
- 解释为什么“若干相关正态变量中某一个最大”的概率没有闭式解。
:::

## 符号说明

| 符号 | 含义 |
|---|---|
| $f(x)$, $F(x)$ | 概率密度函数（PDF）和累积分布函数（CDF） |
| $\E[X]$, $\Var[X]$ | 均值和方差 |
| $\Cov[X, Y]$, $\rho_{XY}$ | 协方差和相关系数 |
| $\Phi(z)$ | 标准正态分布的累积分布函数 |
| $\eta$, $\mu$ | 耿贝尔分布和逻辑斯谛分布的位置参数和尺度参数 |
| $\gamma \approx 0.5772$ | 欧拉–马斯刻罗尼常数 |

全书中，$\mathcal{N}(\mu, \sigma^2)$ 表示均值为 $\mu$、**方差**为 $\sigma^2$ 的正态分布。

## 基本定义

对密度为 $f$ 的连续随机变量 $X$，

$$
\begin{aligned}
F(x) &= \Prob(X \le x) \\
&= \int_{-\infty}^{x} f(t)\,\diff t, \\
\E[X] &= \int_{-\infty}^{\infty} x\,f(x)\,\diff x, \\
\Var[X] &= \E\!\left[(X - \E[X])^2\right] \\
&= \E[X^2] - (\E[X])^2 .
\end{aligned}
$$

对两个随机变量，$\Cov[X, Y] = \E[(X - \E[X])(Y - \E[Y])]$，$\rho_{XY} = \Cov[X, Y]/(\sigma_X\sigma_Y) \in [-1, 1]$。对常数 $a$、$b$，

$$
\Var[aX + bY] = a^2\Var[X] + b^2\Var[Y] + 2ab\,\Cov[X, Y].
$$ (eq-01-var-linear)

## 连续均匀分布

$X \sim \mathcal{U}(a, b)$ 在 $[a, b]$ 上具有常数密度：

$$
\begin{aligned}
f(x) &= \begin{cases} \dfrac{1}{b - a}, & a \le x \le b, \\[4pt] 0, & \text{其他}, \end{cases} \\[6pt]
F(x) &= \begin{cases} 0, & x < a, \\[2pt] \dfrac{x - a}{b - a}, & a \le x \le b, \\[4pt] 1, & x > b, \end{cases}
\end{aligned}
$$

且

$$
\begin{aligned}
\E[X] &= \frac{a + b}{2}, \\
\Var[X] &= \frac{(b - a)^2}{12}.
\end{aligned}
$$

它用于描述只知道落在某个区间内的量，例如公交车按固定车头时距到达、乘客随机到站时的候车时间。

## 正态分布

$X \sim \mathcal{N}(\mu, \sigma^2)$ 的密度为

$$
f(x) = \frac{1}{\sqrt{2\pi}\,\sigma}
\exp\!\left[-\frac{(x - \mu)^2}{2\sigma^2}\right],
\qquad -\infty < x < \infty,
$$

均值为 $\mu$，方差为 $\sigma^2$。其累积分布函数没有闭式表达，需借助**标准化**变量 $Z = (X - \mu)/\sigma$ 计算，$Z$ 服从标准正态分布 $\mathcal{N}(0, 1)$：

$$
\Prob(X \le x) = \Phi\!\left(\frac{x - \mu}{\sigma}\right).
$$ (eq-01-standardize)

正态分布的依据是**中心极限定理**：许多独立微小效应之和近似服从正态分布。它用于描述由许多微小延误累积而成的出行时间，以及样本均值、回归系数等估计量。

### 检验中用到的相关分布

若 $Z \sim \mathcal{N}(0, 1)$ 与 $W \sim \chi^2(\nu)$ 相互独立，则 $Z/\sqrt{W/\nu} \sim t(\nu)$；若 $W_1 \sim \chi^2(\nu_1)$ 与 $W_2 \sim \chi^2(\nu_2)$ 相互独立，则 $(W_1/\nu_1)/(W_2/\nu_2) \sim F(\nu_1, \nu_2)$。由此得到{doc}`02-regression-and-hypothesis-tests`中的 $t$ 检验和 $F$ 检验。当 $\nu \to \infty$ 时，$t(\nu)$ 趋于 $\mathcal{N}(0, 1)$，因此大样本时用 $z$ 代替 $t$。

## 耿贝尔分布

### 来源：多个随机变量中的最大值

设 $T_1, \ldots, T_n$ 独立同分布，累积分布函数为 $F_T$。其最大值 $M_n = \max\{T_1, \ldots, T_n\}$ 的累积分布函数为

$$
\begin{aligned}
\Prob(M_n \le x) &= \Prob(T_1 \le x, \ldots, T_n \le x) \\
&= [F_T(x)]^{n}.
\end{aligned}
$$

若 $F_T$ 具有指数型上尾（正态分布、指数分布和伽马分布均如此），则经过适当的中心化和标准化后，当 $n \to \infty$ 时 $M_n$ 的分布收敛于**耿贝尔分布**（第一类极值分布）。因此，耿贝尔分布是描述多个随机因素最大值的自然模型——例如某个方案效用中无法观测的部分。

### 定义与性质

位置参数为 $\eta$、尺度参数为 $\mu > 0$ 的 $X \sim \mathrm{Gumbel}(\eta, \mu)$ 满足

$$
\begin{aligned}
F(x) &= \exp\!\left\{-e^{-\mu(x - \eta)}\right\}, \\
f(x) &= \mu\,e^{-\mu(x - \eta)}\exp\!\left\{-e^{-\mu(x - \eta)}\right\}, \quad -\infty < x < \infty.
\end{aligned}
$$ (eq-01-gumbel)

注意 $\mu$ 是尺度的*倒数*：$\mu$ 越大，分布越集中（{numref}`fig-01-gumbel-logistic`）。

:::{prf:property} 耿贝尔分布的性质
:label: prop-01-gumbel

设 $X \sim \mathrm{Gumbel}(\eta, \mu)$。

1. 众数为 $\eta$。
2. 均值为 $\eta + \gamma/\mu$，其中 $\gamma \approx 0.5772$。
3. 方差为 $\pi^2/(6\mu^2)$。
4. 对常数 $V$ 和 $\alpha > 0$，$\alpha X + V \sim \mathrm{Gumbel}(\alpha\eta + V,\ \mu/\alpha)$。
5. 若 $X_1 \sim \mathrm{Gumbel}(\eta_1, \mu)$ 与 $X_2 \sim \mathrm{Gumbel}(\eta_2, \mu)$ 相互独立，则 $\max\{X_1, X_2\} \sim \mathrm{Gumbel}\!\left(\frac{1}{\mu}\ln\left(e^{\mu\eta_1} + e^{\mu\eta_2}\right),\ \mu\right)$。
6. 更一般地，若 $X_1, \ldots, X_J$ 相互独立且 $X_j \sim \mathrm{Gumbel}(\eta_j, \mu)$，则

   $$
   \max_{j = 1,\ldots,J} X_j \sim
   \mathrm{Gumbel}\!\left(\frac{1}{\mu}\ln\sum_{j=1}^{J} e^{\mu\eta_j},\ \mu\right).
   $$ (eq-01-gumbel-max)
:::

:::{dropdown} 证明
:class-container: proof
:animate: fade-in

性质 4：对 $\alpha > 0$，$\Prob(\alpha X + V \le x) = F\big((x - V)/\alpha\big)
= \exp\{-e^{-(\mu/\alpha)(x - V - \alpha\eta)}\}$，这正是位置参数为 $\alpha\eta + V$、尺度参数为 $\mu/\alpha$ 的耿贝尔累积分布函数。

性质 6（性质 5 是 $J = 2$ 的情形）：由独立性，

$$
\begin{aligned}
\Prob\!\left(\max_j X_j \le x\right)
&= \prod_{j=1}^{J}\exp\!\left\{-e^{-\mu(x - \eta_j)}\right\} \\
&= \exp\!\left\{-e^{-\mu x}\sum_{j=1}^{J} e^{\mu\eta_j}\right\} \\
&= \exp\!\left\{-e^{-\mu(x - \eta^{*})}\right\},
\end{aligned}
$$

其中

$$
\eta^{*} = \frac{1}{\mu}\ln\sum_{j=1}^{J} e^{\mu\eta_j},
$$

因为 $e^{\mu\eta^{*}} = \sum_j e^{\mu\eta_j}$。性质 1–3 可由 {eq}`eq-01-gumbel` 经求导和积分得到。
:::

性质 6 正是 Logit 模型具有闭式解的原因：若 $J$ 个方案的效用是尺度参数相同的独立耿贝尔变量，则最优方案的效用仍服从耿贝尔分布。其位置参数，即**对数和**（log-sum）$\eta^{*}$，决定了选择集的期望最大效用；由性质 2，期望最大效用等于 $\eta^{*} + \gamma/\mu$。

## 逻辑斯谛分布

位置参数为 $\eta$、尺度参数为 $\mu > 0$ 的 $X \sim \mathrm{Logistic}(\eta, \mu)$ 满足

$$
\begin{aligned}
F(x) &= \frac{1}{1 + e^{-\mu(x - \eta)}}, \\
f(x) &= \frac{\mu\,e^{-\mu(x - \eta)}}{\left[1 + e^{-\mu(x - \eta)}\right]^{2}}, \quad -\infty < x < \infty.
\end{aligned}
$$ (eq-01-logistic)

```{figure} figures/01-gumbel-logistic.svg
:name: fig-01-gumbel-logistic
:width: 640px
:class: dark-light

耿贝尔分布和逻辑斯谛分布的密度。耿贝尔密度右偏，众数为 $\eta$；逻辑斯谛密度关于 $\eta$ 对称。$\mu$ 减半时分布的离散程度加倍。
```

:::{prf:property} 逻辑斯谛分布的性质
:label: prop-01-logistic

设 $X \sim \mathrm{Logistic}(\eta, \mu)$。

1. 众数、中位数和均值都等于 $\eta$。
2. 方差为 $\pi^2/(3\mu^2)$。
3. 对常数 $V$ 和 $\alpha > 0$，$\alpha X + V \sim \mathrm{Logistic}(\alpha\eta + V,\ \mu/\alpha)$。
4. 若 $X_1 \sim \mathrm{Gumbel}(\eta_1, \mu)$ 与 $X_2 \sim \mathrm{Gumbel}(\eta_2, \mu)$ 相互独立，则 $X_1 - X_2 \sim \mathrm{Logistic}(\eta_1 - \eta_2,\ \mu)$。
:::

:::{dropdown} 证明
:class-container: proof
:animate: fade-in

性质 3 的证明与耿贝尔分布相同。对性质 4，令 $Y = X_1 - X_2$，并以 $X_2$ 为条件：

$$
\begin{aligned}
\Prob(Y \le y)
&= \int_{-\infty}^{\infty} F_1(x + y)\, f_2(x)\,\diff x \\
&= \int_{-\infty}^{\infty}
   \exp\!\left\{-e^{-\mu(x + y - \eta_1)}\right\}
   \mu e^{-\mu(x - \eta_2)}\exp\!\left\{-e^{-\mu(x - \eta_2)}\right\}\diff x .
\end{aligned}
$$

作代换 $u = e^{-\mu(x - \eta_2)}$，则 $\diff u = -\mu u\,\diff x$，且 $e^{-\mu(x + y - \eta_1)} = u\,e^{-\mu(y - \eta_1 + \eta_2)} = u\,a$，其中 $a = e^{-\mu(y - (\eta_1 - \eta_2))}$：

$$
\begin{aligned}
\Prob(Y \le y) &= \int_{0}^{\infty} e^{-u(1 + a)}\,\diff u \\
&= \frac{1}{1 + a} \\
&= \frac{1}{1 + e^{-\mu[y - (\eta_1 - \eta_2)]}},
\end{aligned}
$$

这正是位置参数为 $\eta_1 - \eta_2$、尺度参数为 $\mu$ 的累积分布函数 {eq}`eq-01-logistic`。
:::

性质 4 给出了**二项 Logit 模型**（binary logit model）：若两个方案效用的误差项是尺度参数相同的独立耿贝尔变量，则误差之差服从逻辑斯谛分布，选择第一个方案的概率具有 {eq}`eq-01-logistic` 的闭式形式。相反，两个耿贝尔变量之*和*并不服从逻辑斯谛分布。

逻辑斯谛分布也可由极值产生：对于具有指数型尾部的对称母体分布，大样本的最大值与最小值渐近独立，二者的平均值（*中程数*）经适当中心化和标准化后收敛于逻辑斯谛分布。在实际应用中，逻辑斯谛分布是正态分布的良好近似：方差相同时，两个累积分布函数之差不超过约 0.02。

## 二元与多元正态分布

### 二元正态分布

同一次出行的出行时间 $X$ 与出行费用 $Y$ 通常是相关的。若 $(X, Y)$ 服从二元正态分布，均值为 $\mu_X, \mu_Y$，标准差为 $\sigma_X, \sigma_Y$，相关系数为 $\rho$，则联合密度为

$$
f(x, y) = \frac{1}{2\pi\sigma_X\sigma_Y\sqrt{1 - \rho^2}}
\exp\!\left\{-\frac{Q(x, y)}{2(1 - \rho^2)}\right\},
$$

其中

$$
Q(x, y) = \frac{(x - \mu_X)^2}{\sigma_X^2}
- \frac{2\rho(x - \mu_X)(y - \mu_Y)}{\sigma_X\sigma_Y}
+ \frac{(y - \mu_Y)^2}{\sigma_Y^2}.
$$

边缘分布为 $\mathcal{N}(\mu_X, \sigma_X^2)$ 和 $\mathcal{N}(\mu_Y, \sigma_Y^2)$，且 $\Cov[X, Y] = \rho\sigma_X\sigma_Y$。

**线性组合服从正态分布。** 对常数 $a$ 和 $b$，$aX + bY$ 服从正态分布，均值为 $a\mu_X + b\mu_Y$，由 {eq}`eq-01-var-linear`，方差为 $a^2\sigma_X^2 + b^2\sigma_Y^2 + 2ab\rho\sigma_X\sigma_Y$。特别地，

$$
X - Y \sim \mathcal{N}\!\left(\mu_X - \mu_Y,\
\sigma_X^2 + \sigma_Y^2 - 2\rho\sigma_X\sigma_Y\right),
$$ (eq-01-normal-difference)

因此 $\Prob(X - Y \le c)$ 之类的概率只需查标准正态分布表即可得到（{prf:ref}`ex-17-bivariate-normal`）。式 {eq}`eq-01-normal-difference` 是**二项 Probit 模型**（binary probit model）的基础。

### 多元正态分布

若随机向量 $\bX \in \R^m$ 的密度为

$$
\phi(\bx) = \frac{1}{(2\pi)^{m/2}\lvert\bSigma\rvert^{1/2}}
\exp\!\left[-\frac{1}{2}(\bx - \bmu)\T\bSigma^{-1}(\bx - \bmu)\right],
\qquad \bx \in \R^m.
$$

则称其服从均值向量为 $\bmu$、协方差矩阵为 $\bSigma$（对称正定）的多元正态分布，记为 $\bX \sim \mathcal{N}(\bmu, \bSigma)$。任一线性变换 $\bA\bX$ 仍服从多元正态分布，均值为 $\bA\bmu$，协方差为 $\bA\bSigma\bA\T$。

在效用服从正态分布的路径选择或方式选择中，方案 $i$ 取最大值的概率

$$
\begin{aligned}
P_i(\bmu, \bSigma) &= \Prob\!\left(X_i > \max_{j \ne i} X_j\right) \\
&= \int_{\{\bx:\ x_i > x_j\ \forall j \ne i\}} \phi(\bx)\,\diff\bx,
\end{aligned}
$$ (eq-01-probit-probability)

是在由超平面 $x_i = x_j$ 所围区域上的 $m$ 维积分。当 $m > 2$ 时它没有闭式解，需要数值计算，通常采用蒙特卡洛模拟（{prf:ref}`ex-17-mvn-maximum`）。这就是**多项 Probit 模型**（multinomial probit model）：由于 $\bSigma$ 可以表示方案之间的相关性（例如共用路段的路径），它比 Logit 模型更灵活，但计算代价更高。

## 本章回顾

### 小结

- 均匀分布：均值为 $(a + b)/2$，方差为 $(b - a)^2/12$。正态分布的概率通过标准化求得，见式 {eq}`eq-01-standardize`。
- Gumbel$(\eta, \mu)$，式 {eq}`eq-01-gumbel`：均值为 $\eta + \gamma/\mu$，方差为 $\pi^2/(6\mu^2)$；尺度参数相同的独立耿贝尔变量的最大值仍服从耿贝尔分布，位置参数为 $\mu^{-1}\ln\sum_j e^{\mu\eta_j}$（{prf:ref}`prop-01-gumbel`，式 {eq}`eq-01-gumbel-max`）。
- Logistic$(\eta, \mu)$，式 {eq}`eq-01-logistic`：均值为 $\eta$，方差为 $\pi^2/(3\mu^2)$；尺度参数相同的两个独立耿贝尔变量之差服从逻辑斯谛分布（{prf:ref}`prop-01-logistic`），由此得到二项 Logit 模型。
- 联合正态变量的线性组合服从正态分布，见式 {eq}`eq-01-normal-difference`（二项 Probit）；若干相关正态变量中某一个为最大的概率，即式 {eq}`eq-01-probit-probability`，需要数值积分（多项 Probit）。

### 常见错误

- **混淆 $\mathcal{N}(\mu, \sigma^2)$ 中的方差与标准差。** 第二个参数是方差；标准化时应除以其平方根 $\sigma$。
- **把耿贝尔分布和逻辑斯谛分布中的 $\mu$ 当作标准差。** 它是尺度的倒数：两者的方差分别为 $\pi^2/(6\mu^2)$ 和 $\pi^2/(3\mu^2)$，$\mu$ 越大，分布越集中。
- **把耿贝尔分布限制在 $x \ge 0$ 上。** 它定义在整个实数轴上。
- **把耿贝尔分布的位置参数 $\eta$ 当作均值。** 位置参数是众数；均值为 $\eta + \gamma/\mu$。
- **把最大值稳定性 {eq}`eq-01-gumbel-max` 用于尺度参数*不同*的耿贝尔变量。** 只有当所有变量的 $\mu$ 相同时，最大值才服从耿贝尔分布。

## 参考文献

- Ben-Akiva, M., & Lerman, S. R. (1985). *Discrete Choice Analysis:
  Theory and Application to Travel Demand*, Chapter 5. MIT Press.
- Sheffi, Y. (1985). *Urban Transportation Networks*, Appendix (Normal
  distribution and probit analysis). Prentice-Hall.
- Train, K. E. (2009). *Discrete Choice Methods with Simulation* (2nd ed.),
  Chapter 3. Cambridge University Press.
  <https://eml.berkeley.edu/books/choice2.html>
- Gumbel, E. J. (1958). *Statistics of Extremes*. Columbia University
  Press.
- Montgomery, D. C., & Runger, G. C. (2018). *Applied Statistics and
  Probability for Engineers* (7th ed.), Chapters 4–5. Wiley.
