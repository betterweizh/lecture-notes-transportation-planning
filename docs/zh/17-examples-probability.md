# 概率分布

本章求解{doc}`01-probability-distributions`中的例题与习题。

## 均匀分布与正态分布

:::{prf:example} 均匀分布的出行时间
:label: ex-17-uniform

乘公共交通从校园到地铁站的出行时间 $X$ 在 15 至 25 分钟之间均匀分布。写出其概率密度函数、累积分布函数、均值和方差，并求出行时间超过 22 分钟的概率。
:::

:::{dropdown} 解答
:class-container: solution
:animate: fade-in

取 $a = 15$，$b = 25$，

$$
\begin{aligned}
f(x) &= \frac{1}{10}\ \ (15 \le x \le 25), \\
F(x) &= \frac{x - 15}{10}\ \ (15 \le x \le 25),
\end{aligned}
$$

区间外 $f = 0$；低于 15 时 $F = 0$，高于 25 时 $F = 1$。各阶矩为

$$
\begin{aligned}
\E[X] &= \frac{15 + 25}{2} = 20~\text{分钟}, \\
\Var[X] &= \frac{(25 - 15)^2}{12} = 8.33~\text{分钟}^2,
\end{aligned}
$$

因此标准差为 2.89 分钟。最后，$\Prob(X > 22) = 1 - F(22) = 1 - 0.7 = 0.3$。
:::

:::{prf:example} 正态分布的步行时间
:label: ex-17-normal

从校园步行到地铁站的时间 $X$ 服从均值为 20 分钟、标准差为 10 分钟的正态分布。步行时间不超过 30 分钟的概率是多少？
:::

:::{dropdown} 解答
:class-container: solution
:animate: fade-in

用 {eq}`eq-01-standardize` 标准化：

$$
\Prob(X \le 30) = \Phi\!\left(\frac{30 - 20}{10}\right) = \Phi(1.00) = 0.8413 .
$$

正态模型也给负的步行时间赋予了概率：$\Prob(X \le 0) = \Phi(-2) = 0.0228$。若只允许正的时间，则

$$
\Prob(0 < X \le 30) = \Phi(1) - \Phi(-2) = 0.8413 - 0.0228 = 0.8186 .
$$

变异系数较大（此处为 0.5）提示：用正态模型描述正值变量是粗略的；对数正态分布或伽马分布可能更合适。
:::

## 耿贝尔分布与逻辑斯谛分布

:::{prf:example} 耿贝尔分布的概率
:label: ex-17-gumbel

多个出行时间的最大值 $X$ 服从 $\eta = 0.5$、$\mu = 0.5$ 的耿贝尔分布。计算 $\Prob(X \le 5)$ 以及 $X$ 的均值和标准差。
:::

:::{dropdown} 解答
:class-container: solution
:animate: fade-in

由 {eq}`eq-01-gumbel`，

$$
\begin{aligned}
\Prob(X \le 5) &= \exp\!\left\{-e^{-0.5\,(5 - 0.5)}\right\} \\
&= \exp\!\left\{-e^{-2.25}\right\} = \exp(-0.1054) = 0.900 .
\end{aligned}
$$

由{prf:ref}`prop-01-gumbel`，均值为 $\eta + \gamma/\mu = 0.5 + 0.5772/0.5 = 1.654$，标准差为 $\pi/(\sqrt{6}\,\mu) = 2.565$。
:::

:::{prf:example} 两个耿贝尔方案之间的选择
:label: ex-17-gumbel-difference

两条路径的效用为 $U_1 = V_1 + \varepsilon_1$ 和 $U_2 = V_2 + \varepsilon_2$，其中 $V_1 = -10$，$V_2 = -12$（以分钟计的出行时间的相反数），$\varepsilon_1, \varepsilon_2$ 相互独立，服从 $\mu = 0.5$ 的 $\mathrm{Gumbel}(0, \mu)$。(a) 求选择路径 1 的概率。(b) 求最大效用的分布。
:::

:::{dropdown} 解答
:class-container: solution
:animate: fade-in

**(a)** 若 $U_1 > U_2$，即 $\varepsilon_2 - \varepsilon_1 < V_1 - V_2$，则选择路径 1。由{prf:ref}`prop-01-logistic`，$\varepsilon_2 - \varepsilon_1 \sim \mathrm{Logistic}(0, \mu)$，因此

$$
\begin{aligned}
\Prob(U_1 > U_2) &= \frac{1}{1 + e^{-\mu(V_1 - V_2)}} \\
&= \frac{e^{\mu V_1}}{e^{\mu V_1} + e^{\mu V_2}} \\
&= \frac{1}{1 + e^{-0.5 \times 2}} = 0.731 .
\end{aligned}
$$

这就是二项 Logit 公式。

**(b)** 由{prf:ref}`prop-01-gumbel`的性质 4，$U_j = V_j + \varepsilon_j \sim \mathrm{Gumbel}(V_j, \mu)$。由性质 6，

$$
\max\{U_1, U_2\} \sim \mathrm{Gumbel}\!\left(\frac{1}{\mu}\ln\left(e^{\mu V_1} + e^{\mu V_2}\right),\ \mu\right),
$$

其位置参数为 $2\ln(e^{-5} + e^{-6}) = -9.373$。期望最大效用为 $-9.373 + \gamma/\mu = -8.219$，高于 $V_1$ 和 $V_2$，因为出行者可以选择结果更好的那条路径。
:::

## 二元与多元正态分布

:::{prf:example} 出行的时间与费用
:label: ex-17-bivariate-normal

某次出行的出行时间 $X$ 和出行费用 $Y$ 服从联合正态分布，$X \sim \mathcal{N}(20, 10)$，$Y \sim \mathcal{N}(10, 5)$（第二个参数为方差），相关系数 $\rho = 0.5$。计算 $\Prob(X - Y \le 15)$。
:::

:::{dropdown} 解答
:class-container: solution
:animate: fade-in

由 {eq}`eq-01-normal-difference`，$X - Y$ 服从正态分布，均值为 $20 - 10 = 10$，方差为

$$
\begin{aligned}
\sigma_X^2 + \sigma_Y^2 - 2\rho\sigma_X\sigma_Y &= 10 + 5 - 2 \times 0.5 \times \sqrt{10}\sqrt{5} = 15 - 7.071 = 7.929,
\end{aligned}
$$

因此其标准差为 2.816。于是

$$
\begin{aligned}
\Prob(X - Y \le 15) &= \Phi\!\left(\frac{15 - 10}{2.816}\right) \\
&= \Phi(1.776) = 0.962 .
\end{aligned}
$$

在半平面 $x - y \le 15$ 上对二元密度进行数值积分，得到相同的值。
:::

:::{prf:example} 成为最大者的概率
:label: ex-17-mvn-maximum

三个方案的感知效用服从多元正态分布，

$$
\bmu = \begin{bmatrix} 2 \\ 2 \\ 3 \end{bmatrix},
\qquad
\bSigma = \begin{bmatrix} 2 & 0 & 1 \\ 0 & 2 & 1 \\ 1 & 1 & 3 \end{bmatrix}.
$$

计算每个方案效用最大的概率 $P_i = \Prob(X_i > \max_{j \ne i} X_j)$。
:::

:::{dropdown} 解答
:class-container: solution
:animate: fade-in

对三个方案，积分 {eq}`eq-01-probit-probability` 没有闭式解，因此用**蒙特卡洛模拟**计算：抽取大量（$R$ 个）向量 $\bx^{(r)} \sim \mathcal{N}(\bmu, \bSigma)$，统计每个分量为最大的次数：

$$
\hat{P}_i = \frac{1}{R}\sum_{r=1}^{R}\mathbb{1}\!\left[x_i^{(r)} > \max_{j \ne i} x_j^{(r)}\right].
$$

取 $R = 2\,000\,000$ 次抽样（{doc}`32-python-foundations`），

$$
\begin{aligned}
\hat{P}_1 &= 0.222, \\
\hat{P}_2 &= 0.222, \\
\hat{P}_3 &= 0.556 .
\end{aligned}
$$

方案 1 和方案 2 是对称的，因此 $P_1 = P_2$。每个估计值的标准误 $\sqrt{\hat{P}(1 - \hat{P})/R}$ 至多为 0.0004。作为检验：当且仅当两个差 $X_3 - X_1$ 和 $X_3 - X_2$ 都为正时，方案 3 最大；这两个差服从二元正态分布，均值均为 1，方差均为 3，协方差为 1，对其二元正态累积分布函数作数值计算得 $P_3 = 0.5563$，$P_1 = P_2 = (1 - P_3)/2 = 0.2218$。

对一对方案，概率有闭式解。例如，$X_3 - X_1 \sim \mathcal{N}(1,\ 3 + 2 - 2 \times 1) = \mathcal{N}(1, 3)$，因此 $\Prob(X_3 > X_1) = \Phi(1/\sqrt{3}) = 0.718$。
:::
