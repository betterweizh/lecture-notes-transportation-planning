# 线性回归与假设检验

## 概述

出行生成模型把小区或家庭的出行产生量或吸引量与土地利用和社会经济变量联系起来，最常用的工具就是线性回归。本章回顾含截距和不含截距的一元及多元线性回归模型的最小二乘估计、拟合优度指标，以及用于判断某个变量是否应纳入模型的 $t$ 检验。最后介绍检验两个总体均值是否相等的大样本检验，例如可用于比较两个时段或两个群体的交通流量或出行率。

:::{admonition} 学习目标
:class: objectives
学完本章后，读者应能够：

- 推导含截距和不含截距的一元线性回归的最小二乘估计量；
- 用矩阵形式估计多元线性回归；
- 计算并解释 $R^2$、调整 $R^2$ 和残差方差；
- 用 $t$ 检验检验单个系数，用 $F$ 检验检验整个模型；
- 用虚拟变量表示分类预测变量；
- 用大样本检验两个总体均值是否相等。
:::

## 符号说明

| 符号 | 含义 |
|---|---|
| $n$ | 观测数 |
| $k$ | 预测变量个数（不含截距） |
| $y_i$, $\by$ | 第 $i$ 个观测的响应值；$\R^n$ 中的响应向量 |
| $x_{ij}$, $\bX$ | 第 $i$ 个观测的第 $j$ 个预测变量值；设计矩阵 |
| $\beta_j$, $\hat\beta_j$ | 回归系数及其最小二乘估计 |
| $\hat{y}_i$, $e_i = y_i - \hat{y}_i$ | 拟合值和残差 |
| $\bar{x}$, $\bar{y}$ | 样本均值 |
| $S_{xx} = \sum_i (x_i - \bar{x})^2$ | $x$ 的离差平方和 |
| $S_{xy} = \sum_i (x_i - \bar{x})(y_i - \bar{y})$ | 离差交叉乘积和 |
| $\mathit{SS}_T, \mathit{SS}_R, \mathit{SS}_E$ | 总平方和、回归平方和与残差平方和 |
| $\hat\sigma^2 = \mathit{MS}_E$ | 误差方差的估计 |

## 线性回归模型

响应变量 $Y$（例如某小区的出行产生量）与预测变量 $X_1, \ldots, X_k$（家庭数、小汽车数、就业人数、建筑面积）的关系为

$$
\begin{aligned}
Y &= \beta_0 + \beta_1 X_1 + \beta_2 X_2 + \cdots + \beta_k X_k + \varepsilon, \\
\varepsilon &\sim \mathcal{N}(0, \sigma^2),
\end{aligned}
$$ (eq-02-mlr)

其中 $\beta_0$ 为截距，$\beta_1, \ldots, \beta_k$ 为**偏回归系数**（partial regression coefficient），不同观测的误差相互独立且具有相同的未知方差 $\sigma^2$。数据为 $n$ 个观测 $(y_i, x_{i1}, \ldots, x_{ik})$，$i = 1, \ldots, n$。

## 一元线性回归

### 最小二乘估计

只有一个预测变量时，$Y = \beta_0 + \beta_1 X + \varepsilon$。**最小二乘**（least squares）估计使误差平方和最小：

$$
L(\beta_0, \beta_1) = \sum_{i=1}^{n}\left(y_i - \beta_0 - \beta_1 x_i\right)^2 .
$$

其偏导数为

$$
\begin{aligned}
\frac{\partial L}{\partial \beta_0}
&= -2\sum_{i=1}^{n}\left(y_i - \beta_0 - \beta_1 x_i\right), \\
\frac{\partial L}{\partial \beta_1}
&= -2\sum_{i=1}^{n}\left(y_i - \beta_0 - \beta_1 x_i\right)x_i .
\end{aligned}
$$

令其为零，得到两个**正规方程**（normal equations），其解为

$$
\begin{aligned}
\hat\beta_1 &= \frac{S_{xy}}{S_{xx}} \\
&= \frac{\sum_i x_i y_i - \left(\sum_i x_i\right)\left(\sum_i y_i\right)/n}{\sum_i x_i^2 - \left(\sum_i x_i\right)^2/n}, \\
\hat\beta_0 &= \bar{y} - \hat\beta_1\bar{x}.
\end{aligned}
$$ (eq-02-slr-estimates)

由于 $\sum_i (x_i - \bar{x}) = 0$，分子也可写成 $S_{xy} = \sum_i y_i (x_i - \bar{x})$，便于手工计算。

### 方差分析与拟合优度

响应变量的总变差可分解为回归解释的部分和残差部分：

$$
\begin{aligned}
\underbrace{\sum_{i}(y_i - \bar{y})^2}_{\mathit{SS}_T,\ n-1\ \text{d.f.}} &= \underbrace{\sum_{i}(\hat{y}_i - \bar{y})^2}_{\mathit{SS}_R,\ 1\ \text{d.f.}}
+ \underbrace{\sum_{i}(y_i - \hat{y}_i)^2}_{\mathit{SS}_E,\ n-2\ \text{d.f.}} .
\end{aligned}
$$ (eq-02-anova-slr)

**决定系数**（coefficient of determination）

$$
\begin{aligned}
R^2 &= \frac{\mathit{SS}_R}{\mathit{SS}_T} \\
&= 1 - \frac{\mathit{SS}_E}{\mathit{SS}_T}
\end{aligned}
$$ (eq-02-r2)

是模型所解释的 $y$ 变差所占的比例，取值于 $[0, 1]$。误差方差由**残差均方**估计：

$$
\begin{aligned}
\hat\sigma^2 &= \mathit{MS}_E \\
&= \frac{\mathit{SS}_E}{n - 2}.
\end{aligned}
$$

### 系数的检验

在模型假设下，估计量服从正态分布：

$$
\begin{aligned}
\hat\beta_1 &\sim \mathcal{N}\!\left(\beta_1,\ \frac{\sigma^2}{S_{xx}}\right), \\
\hat\beta_0 &\sim \mathcal{N}\!\left(\beta_0,\ \sigma^2\left[\frac{1}{n} + \frac{\bar{x}^2}{S_{xx}}\right]\right).
\end{aligned}
$$ (eq-02-slr-distributions)

以 $\hat\sigma^2$ 代替 $\sigma^2$，得到标准误 $\se(\hat\beta_1) = \sqrt{\hat\sigma^2/S_{xx}}$ 和 $\se(\hat\beta_0) = \sqrt{\hat\sigma^2(1/n + \bar{x}^2/S_{xx})}$。检验 $H_0: \beta_j = \beta_{j,0}$ 时，将统计量

$$
T_j = \frac{\hat\beta_j - \beta_{j,0}}{\se(\hat\beta_j)}
\ \sim\ t(n - 2) \quad \text{在 } H_0 \text{ 下}
$$ (eq-02-t-test)

与 $t$ 分布的临界值比较：

| 备择假设 | 在水平 $\alpha$ 下拒绝 $H_0$ 的条件 |
|---|---|
| $H_1: \beta_j \ne \beta_{j,0}$ | $\lvert T_j\rvert > t_{\alpha/2,\,\nu}$ |
| $H_1: \beta_j > \beta_{j,0}$ | $T_j > t_{\alpha,\,\nu}$ |
| $H_1: \beta_j < \beta_{j,0}$ | $T_j < -t_{\alpha,\,\nu}$ |

其中 $\nu$ 为残差自由度（一元回归中 $\nu = n - 2$）。最常用的检验是对 $H_0: \beta_j = 0$ 作双侧检验：拒绝原假设意味着该预测变量具有统计显著的线性效应。

### 过原点回归

如果理论上要求预测变量为零时出行量为零，且数据与此不矛盾（截距与零没有显著差异），可以拟合模型 $Y = \beta_1 X + \varepsilon$。最小化 $\sum_i (y_i - \beta_1 x_i)^2$ 得到

$$
\begin{aligned}
\hat\beta_1 &= \frac{\sum_i x_i y_i}{\sum_i x_i^2}, \\
\hat\beta_1 &\sim \mathcal{N}\!\left(\beta_1,\ \frac{\sigma^2}{\sum_i x_i^2}\right), \\
\hat\sigma^2 &= \frac{\mathit{SS}_E}{n - 1}.
\end{aligned}
$$ (eq-02-slr-origin)

此时 $t$ 检验 {eq}`eq-02-t-test` 的自由度为 $n - 1$。不含截距时，分解式 {eq}`eq-02-anova-slr` 只对*非中心化*平方和成立，即 $\sum_i y_i^2 = \sum_i \hat{y}_i^2 + \sum_i e_i^2$，因此拟合优度用**非中心化**决定系数（uncentered coefficient of determination）度量：

$$
\begin{aligned}
R_0^2 &= \frac{\sum_i \hat{y}_i^2}{\sum_i y_i^2} \\
&= 1 - \frac{\mathit{SS}_E}{\sum_i y_i^2}.
\end{aligned}
$$ (eq-02-r2-uncentered)

:::{admonition} 非中心化 $R^2$ 不能与 $R^2$ 比较
:class: warning
由于 $\sum_i y_i^2 \ge \sum_i (y_i - \bar{y})^2$，即使不含截距的模型拟合更差，其非中心化 $R_0^2$ 也几乎总是大于含截距模型的普通 $R^2$。应通过残差平方和或残差标准误来比较两个模型，而不是比较 $R^2$（{prf:ref}`ex-18-slr-origin`）。
:::

## 多元线性回归

### 矩阵形式与估计

将 {eq}`eq-02-mlr` 的 $n$ 个观测堆叠起来，得到 $\by = \bX\bbeta + \bvarepsilon$，其中

$$
\by = \begin{bmatrix} y_1 \\ y_2 \\ \vdots \\ y_n \end{bmatrix},
\quad
\bX = \begin{bmatrix}
1 & x_{11} & \cdots & x_{1k} \\
1 & x_{21} & \cdots & x_{2k} \\
\vdots & \vdots & \ddots & \vdots \\
1 & x_{n1} & \cdots & x_{nk}
\end{bmatrix},
\quad
\bbeta = \begin{bmatrix} \beta_0 \\ \beta_1 \\ \vdots \\ \beta_k \end{bmatrix}.
$$

最小二乘准则及其梯度为

$$
\begin{aligned}
L(\bbeta) &= (\by - \bX\bbeta)\T(\by - \bX\bbeta), \\
\nabla L(\bbeta) &= -2\bX\T(\by - \bX\bbeta).
\end{aligned}
$$

令梯度为零，得到正规方程 $\bX\T\bX\,\bbeta = \bX\T\by$；当 $\bX$ 列满秩时，

$$
\begin{aligned}
\hat\bbeta &= (\bX\T\bX)^{-1}\bX\T\by, \\
\hat{\by} &= \bX\hat\bbeta.
\end{aligned}
$$ (eq-02-ols)

### 拟合优度

分解式 $\mathit{SS}_T = \mathit{SS}_R + \mathit{SS}_E$ 仍然成立，相应自由度分别为 $n - 1$、$k$ 和 $n - k - 1$。增加预测变量永远不会使 $R^2$ 减小，即使该变量毫无关系；因此，比较预测变量个数不同的模型时应使用**调整** $R^2$（adjusted $R^2$），它将各平方和除以相应的自由度：

$$
\begin{aligned}
\bar{R}^2
&= 1 - \frac{\mathit{SS}_E/(n - k - 1)}{\mathit{SS}_T/(n - 1)} \\
&= 1 - (1 - R^2)\,\frac{n - 1}{n - k - 1}.
\end{aligned}
$$ (eq-02-adjusted-r2)

加入不必要的预测变量时 $\bar{R}^2$ 会减小，且可能为负。

### 单个系数的检验

每个 $\hat\beta_j$ 都是 $y_1, \ldots, y_n$ 的线性组合，因而服从正态分布：

$$
\hat\beta_j \sim \mathcal{N}\!\left(\beta_j,\ \sigma^2 c_{jj}\right),
\qquad j = 0, 1, \ldots, k,
$$

其中 $c_{jj}$ 是 $(\bX\T\bX)^{-1}$ 的第 $(j+1)$ 个对角元（行和列从 1 开始编号，因此 $c_{00}$ 是第一个）。取

$$
\begin{aligned}
\hat\sigma^2 &= \mathit{MS}_E \\
&= \frac{\mathit{SS}_E}{n - k - 1}
\end{aligned}
$$ (eq-02-mse)

则在 $H_0: \beta_j = \beta_{j,0}$ 下，统计量 $T_j = (\hat\beta_j - \beta_{j,0})/\sqrt{\hat\sigma^2 c_{jj}}$ 服从 $t(n - k - 1)$，并按 $\nu = n - k - 1$ 使用上表中的拒绝规则。

### 整体显著性

“所有预测变量均不起作用”的假设 $H_0: \beta_1 = \cdots = \beta_k = 0$ 用

$$
F_0 = \frac{\mathit{SS}_R/k}{\mathit{SS}_E/(n - k - 1)}
\ \sim\ F(k,\ n - k - 1) \quad \text{在 } H_0 \text{ 下},
$$ (eq-02-f-test)

检验，当 $F_0 > F_{\alpha;\,k,\,n-k-1}$ 时拒绝 $H_0$。

### 不含截距的模型

若省略截距，$\bX$ 中不再有全 1 列，只包含 $k$ 个预测变量。估计量 {eq}`eq-02-ols` 的形式不变，残差自由度变为 $n - k$，因此 $\hat\sigma^2 = \mathit{SS}_E/(n - k)$，$t$ 检验的自由度为 $n - k$。拟合优度同样用非中心化平方和度量：

$$
\begin{aligned}
R_0^2 &= 1 - \frac{\mathit{SS}_E}{\sum_i y_i^2}, \\
\bar{R}_0^2 &= 1 - \frac{\mathit{SS}_E/(n - k)}{\sum_i y_i^2/n}.
\end{aligned}
$$ (eq-02-r2-uncentered-mlr)

### 分类预测变量：虚拟变量

有 $m$ 个类别的分类预测变量（例如拥有 0 辆、1 辆、2 辆及以上小汽车）用 $m - 1$ 个**虚拟变量**（dummy variable）表示，每个虚拟变量在某一类别时取 1、否则取 0；被省略的类别作为参照类别，其效应由截距吸收。若同时使用全部 $m$ 个虚拟变量和截距，$\bX$ 将不满秩（即*虚拟变量陷阱*）。虚拟变量允许变量的效应是非线性的：在{prf:ref}`ex-18-hw1-q5`中，第一辆小汽车对出行的影响与第二辆不同。

### 模型选择

统计检验只是模型选择的依据之一，还需考虑：

- **合理性**——每个系数都应有预期的符号和合理的大小（小汽车越多，小汽车出行不应越少）；
- **显著性**——除非理论要求，每个预测变量都应显著；
- **拟合度**——比较预测变量个数不同的模型时，比较 $\bar{R}^2$ 或 $\hat\sigma$，而不是 $R^2$；
- **简约性与可预测性**——每个预测变量本身都需要在规划年进行预测，因此较少且易于预测的预测变量更可取。

观测较少时 $t$ 临界值很大：残差自由度为 1 时 $t_{0.025,1} = 12.71$。此时看起来高度显著的系数也可能通不过检验（{prf:ref}`ex-18-mlr-freight`）。

## 两个总体均值相等的检验

设两个总体的均值为 $\mu_1$、$\mu_2$，方差为 $\sigma_1^2$、$\sigma_2^2$，容量为 $n_1$ 和 $n_2$ 的独立随机样本给出样本均值 $\bar{x}_1$、$\bar{x}_2$ 和样本方差

$$
s_\ell^2 = \frac{1}{n_\ell - 1}\sum_{j=1}^{n_\ell}\left(x_{\ell j} - \bar{x}_\ell\right)^2,
\qquad \ell = 1, 2.
$$

样本均值之差近似服从正态分布：

$$
\bar{x}_1 - \bar{x}_2 \ \dot\sim\
\mathcal{N}\!\left(\mu_1 - \mu_2,\ \frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}\right).
$$

对于**大样本**（例如 $n_1, n_2 > 40$），可用方差的估计值代替方差；在 $H_0: \mu_1 = \mu_2$ 下，统计量

$$
z_0 = \frac{\bar{x}_1 - \bar{x}_2}{\sqrt{s_1^2/n_1 + s_2^2/n_2}}
$$ (eq-02-two-sample-z)

近似服从标准正态分布。记 $\Phi$ 为标准正态分布函数：

| 备择假设 | 拒绝 $H_0$ 的条件 | $p$ 值 |
|---|---|---|
| $H_1: \mu_1 \ne \mu_2$ | $\lvert z_0\rvert > z_{\alpha/2}$ | $2[1 - \Phi(\lvert z_0\rvert)]$ |
| $H_1: \mu_1 > \mu_2$ | $z_0 > z_\alpha$ | $1 - \Phi(z_0)$ |
| $H_1: \mu_1 < \mu_2$ | $z_0 < -z_\alpha$ | $\Phi(z_0)$ |

对于来自正态总体的小样本，同一统计量近似服从自由度由 Welch–Satterthwaite 公式确定的 $t$ 分布（Satterthwaite, 1946; Welch, 1947）。

## 本章回顾

### 小结

- 最小二乘估计为 $\hat\bbeta = (\bX\T\bX)^{-1}\bX\T\by$，见式 {eq}`eq-02-ols`；一元回归中 $\hat\beta_1 = S_{xy}/S_{xx}$，$\hat\beta_0 = \bar{y} - \hat\beta_1\bar{x}$，见式 {eq}`eq-02-slr-estimates`；过原点回归中 $\hat\beta_1 = \sum_i x_iy_i/\sum_i x_i^2$，见式 {eq}`eq-02-slr-origin`。
- $R^2 = 1 - \mathit{SS}_E/\mathit{SS}_T$，见式 {eq}`eq-02-r2`；$\bar{R}^2$ 对预测变量个数进行了修正，见式 {eq}`eq-02-adjusted-r2`；不含截距时使用非中心化平方和，见式 {eq}`eq-02-r2-uncentered` 和 {eq}`eq-02-r2-uncentered-mlr`。
- 单个系数的 $t$ 检验（式 {eq}`eq-02-t-test`）使用 $\hat\sigma^2 c_{jj}$ 和 $n - p$ 个自由度，其中 $p$ 为估计的系数个数（含截距时 $p = k + 1$，不含截距时 $p = k$）；$F$ 检验 {eq}`eq-02-f-test` 对全部斜率进行联合检验。
- 两个大样本均值用 $z_0 = (\bar{x}_1 - \bar{x}_2)/\sqrt{s_1^2/n_1 + s_2^2/n_2}$ 比较，见式 {eq}`eq-02-two-sample-z`。

### 常见错误

- **将不含截距模型的 $R^2$ 与含截距模型的 $R^2$ 相比较。** 前者是非中心化的，几乎总是更大；应改为比较残差标准误 $\hat\sigma$。
- **所有检验都使用 $n - 2$ 个自由度。** 残差自由度为 $n - p$，其中 $p$ 为估计的系数个数。
- **仅因截距的 $t$ 检验不显著就去掉截距。** 这会迫使拟合直线通过原点，若真实关系的截距不为零，斜率估计会产生偏差；只有理论上也要求截距为零时才应去掉截距。
- **在含截距的同时为每个类别都设置一个虚拟变量。** 此时 $\bX$ 的列线性相关，$\bX\T\bX$ 不可逆；$m$ 个类别应使用 $m - 1$ 个虚拟变量。

## 参考文献

- Montgomery, D. C., & Runger, G. C. (2018). *Applied Statistics and
  Probability for Engineers* (7th ed.), Chapters 10–12. Wiley.
- Montgomery, D. C., Peck, E. A., & Vining, G. G. (2021). *Introduction to
  Linear Regression Analysis* (6th ed.), Chapters 2–3 and 8. Wiley.
- Satterthwaite, F. E. (1946). An approximate distribution of estimates of
  variance components. *Biometrics Bulletin*, *2*(6), 110–114.
  <https://doi.org/10.2307/3002019>
- Welch, B. L. (1947). The generalization of "Student's" problem when
  several different population variances are involved. *Biometrika,
  34*(1–2), 28–35. <https://doi.org/10.1093/biomet/34.1-2.28>
- Ortúzar, J. de D., & Willumsen, L. G. (2011). *Modelling Transport* (4th
  ed.), Section 4.2 (Regression analysis). Wiley.
