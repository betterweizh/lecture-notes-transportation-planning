# 建模中的误差与不确定性

## 概述

任何预测都有不确定性。输入数据带有测量误差，模型由有限样本估计，迭代算法在精确收敛之前就停止，模型简化了行为，而规划年的解释变量本身也需要预测。本章对误差来源进行分类，说明输入中的误差如何传播到模型输出（误差传播，error propagation），并利用这一结果讨论两个实际问题：哪些数据值得改进，以及在给定数据质量下模型应当有多复杂。

:::{admonition} 学习目标
:class: objectives
学完本章后，读者应能够：

- 说出并描述出行需求建模中的主要误差类型；
- 推导并应用一阶误差传播公式（输入之间相关或不相关）；
- 比较和、差、积、商与幂的误差特性，并给出由此得到的建模经验规则；
- 计算边际改进率，判断提高哪个输入的测量精度最具成本效益；以及
- 解释模型复杂度与数据精度之间的权衡。
:::

## 符号说明

| 符号 | 含义 |
|---|---|
| $z = f(x_1, \ldots, x_k)$ | 模型输出，是其输入的函数 |
| $e_{x_i}$ | 输入 $x_i$ 的误差（标准差） |
| $e_z$ | 输出的误差（标准差） |
| $r_{ij}$ | $x_i$ 与 $x_j$ 的相关系数 |
| $e_s$, $e_m$, $e$ | 预测的设定误差、传播的测量误差和总误差 |

## 误差类型

把“即使模型正确也会导致错误预测的误差”与“导致估计出错误模型的误差”区分开来是有益的。

测量误差（measurement error）
: 基年数据测量中的不准确：受访者误解问题或调查员记录错误、网络测量误差、编码和数字化错误。其大小取决于数据采集的细致程度。

抽样误差（sampling error）
: 由于模型是用有限样本估计的而产生；它大致与观测数的平方根成反比（{doc}`07-travel-surveys-and-sampling`）。

计算误差（computational error）
: 由于模型用迭代数值方法求解，且在达到精确解之前就停止而产生。除拥堵网络上的交通分配和大型模型系统中的供需均衡外，它通常比其他误差小。

设定误差（specification error）
: 当现象未被充分理解或必须加以简化时产生：纳入无关变量、遗漏相关变量（可能是最常见的情形）、忽略个体之间的偏好差异，或使用不恰当的函数形式。遗漏的变量被模型的随机误差项吸收；只有当它们与已纳入的变量不相关，且在预测总体中与在估计样本中分布相同时，这才是无害的。可以通过使模型更复杂来减小设定误差，但要付出数据和估计工作量的代价。

移植误差（transfer error）
: 当在一种背景（地点或时间）下估计的模型被应用于另一种背景时产生。用当地数据重新估计模型的一部分可以减小空间移植误差；时间移植——每次预测都是如此——要到未来才能检验，因此它随预测期的延长而增大。

集计误差（aggregation error）
: 由于预测需要针对群体（交通小区、细分市场）进行，而行为最好在个体层面建模而产生。它包括*数据集计*（以小区平均值作为模型输入）、*方案集计*（把目的地归并为小区，或把路线归并为路径）以及*模型集计*（由非线性的个体模型得到集计预测）。只有对线性模型，模型集计才是平凡的。

每次预测还有一个误差来源：规划年解释变量（人口、收入、小汽车拥有量）取值的不确定性，因为它们本身就是预测值。

## 误差的传播

### 一般公式

设模型的输出为 $z = f(x_1, \ldots, x_k)$，每个输入 $x_i$ 的观测误差为 $e_{x_i}$（其标准差）。在观测值 $\bar{\bx} = (\bar{x}_1, \ldots, \bar{x}_k)$ 附近将 $f$ 作一阶泰勒展开，

$$
z \approx f(\bar{\bx})
  + \sum_{i=1}^{k} \frac{\partial f}{\partial x_i}\,(x_i - \bar{x}_i),
$$

其中导数在 $\bar{\bx}$ 处取值。由随机变量线性组合的方差公式得

$$
\begin{aligned}
e_z^2 &= \sum_{i=1}^{k}\left(\frac{\partial f}{\partial x_i}\right)^{2} e_{x_i}^2
  + \sum_{i=1}^{k}\sum_{j \ne i}
    \frac{\partial f}{\partial x_i}\,\frac{\partial f}{\partial x_j}\,
    r_{ij}\, e_{x_i}\, e_{x_j},
\end{aligned}
$$ (eq-08-error-propagation)

其中 $r_{ij}$ 是 $x_i$ 与 $x_j$ 的相关系数（二重求和中每一对计算两次）。公式 {eq}`eq-08-error-propagation` 对线性函数是精确的；对光滑的非线性函数，当误差相对于取值较小时也是很好的近似。当输入互不相关时，它化为

$$
e_z^2 = \sum_{i=1}^{k}\left(\frac{\partial f}{\partial x_i}\right)^{2} e_{x_i}^2 .
$$ (eq-08-error-propagation-indep)

### 基本运算

对两个独立输入 $x \pm e_x$ 和 $y \pm e_y$，由 {eq}`eq-08-error-propagation-indep` 得：

| 运算 | 绝对误差 $e_z$ | 相对误差 $e_z/z$ |
|---|---|---|
| $z = x + y$ | $\sqrt{e_x^2 + e_y^2}$ | $\sqrt{e_x^2 + e_y^2}\,/\,(x + y)$ |
| $z = x - y$ | $\sqrt{e_x^2 + e_y^2}$ | $\sqrt{e_x^2 + e_y^2}\,/\,(x - y)$ |
| $z = xy$ | $\sqrt{y^2e_x^2 + x^2e_y^2}$ | $\sqrt{(e_x/x)^2 + (e_y/y)^2}$ |
| $z = x/y$ | $\sqrt{e_x^2/y^2 + x^2e_y^2/y^4}$ | $\sqrt{(e_x/x)^2 + (e_y/y)^2}$ |
| $z = x^{m}$ | $\lvert m\,x^{m-1}\rvert\, e_x$ | $\lvert m\rvert\,e_x/\lvert x\rvert$ |

对于和与差，绝对误差按平方和开方合成；对于积与商，相对误差按平方和开方合成；取幂使相对误差乘以指数。两个相近量之差是最坏的情形：其绝对误差与和的相同，却要除以一个很小的数（{prf:ref}`ex-23-error-operations`）。

由这些结果可以得到在其他方面同样可接受的模型形式之间进行选择的**经验规则**：

1. 避免使用相互关联的变量（正相关会放大和与积的误差）；
2. 尽可能采用加法形式；
3. 若不能用加法，积与商是次优选择；以及
4. 尽量避免相近量之差和变量的乘方。

### 预测误差与设定误差

由模型得到的预测值 $\hat{z}$ 受两个独立误差来源的影响：由 {eq}`eq-08-error-propagation` 得到的传播输入误差 $e_{\hat{z}}$，以及模型本身的设定误差。将真值写成 $z = \hat{z} + D$，其中偏差 $D$ 的均值为零、标准差为 $e_s$（设定误差），且与输入误差相互独立，则

$$
e_z = \sqrt{e_{\hat{z}}^2 + e_s^2}.
$$ (eq-08-forecast-error)

{prf:ref}`ex-23-hw1-q3`说明了考虑设定误差后，两个预测模型之间的选择可能会颠倒。

## 更好数据的价值

### 边际改进率

在预算一定的情况下，应当提高哪个输入的测量精度？将 {eq}`eq-08-error-propagation-indep` 的平方根对 $e_{x_i}$ 求导，

$$
\begin{aligned}
\frac{\partial e_z}{\partial e_{x_i}} &= \left(\frac{\partial f}{\partial x_i}\right)^{2}\frac{e_{x_i}}{e_z}.
\end{aligned}
$$ (eq-08-marginal-improvement)

这就是输出误差关于输入 $i$ 误差的**边际改进率**（marginal improvement rate）：$e_{x_i}$ 每减小一个单位所带来的 $e_z$ 的减小量。将改进各输入的边际成本除以其边际改进率，就得到通过该输入使 $e_z$ 减小一个单位的成本；应首先采用最便宜的选项（{prf:ref}`ex-23-value-better-data`）。

实际中存在收益递减规律——变量误差每进一步减小，成本都会成比例地增加——因此误差变化后必须重新计算。由 {eq}`eq-08-marginal-improvement` 可以直接得到两条规则：

- 集中精力于**误差大**的变量（$e_{x_i}$ 大）；以及
- 集中精力于**最相关**的变量，即 $\lvert\partial f/\partial x_i\rvert$ 大的变量。

### 模型复杂度与数据精度

较复杂的模型通常设定误差 $e_s$ 较小，但它使用的变量更多，每个变量都带有测量误差，因此其传播的测量误差 $e_m$ 更大。若二者相互独立，则与 {eq}`eq-08-forecast-error` 一样，总误差为

$$
e = \sqrt{e_s^2 + e_m^2}.
$$ (eq-08-total-error)

随着复杂度增加，$e_s$ 下降而 $e_m$ 上升，因此总误差在某个中等复杂度处取得最小值（{numref}`fig-08-error-vs-complexity`）。因此最优模型取决于数据质量：数据较差时，较简单的模型可能比“完美”但需要大量数据的模型预测得更好（{prf:ref}`ex-23-simple-vs-complex`）。

```{figure} figures/08-error-vs-complexity.svg
:name: fig-08-error-vs-complexity
:width: 460px
:class: dark-light

随着模型复杂度增加，设定误差下降，传播的测量误差上升；二者合成的总预测误差在中等复杂度处最小。
```

## 本章回顾

### 小结

- 误差来自测量、抽样、计算、设定、移植和集计，此外还有规划年输入的不确定性。
- 一阶误差传播公式 {eq}`eq-08-error-propagation` 对相关输入含协方差项；对独立输入化为 $e_z^2 = \sum_i (\partial f/\partial x_i)^2 e_{x_i}^2$ {eq}`eq-08-error-propagation-indep`。
- 和与差的绝对误差、积与商的相对误差按平方和开方合成；相近量之差和乘方会放大误差。
- 预测误差由传播的输入误差和设定误差合成 {eq}`eq-08-forecast-error`。
- 边际改进率 {eq}`eq-08-marginal-improvement` 指出哪些数据值得改进：误差大且敏感度高的输入。
- 总误差 {eq}`eq-08-total-error` 在取决于数据质量的某个中等模型复杂度处最小（{numref}`fig-08-error-vs-complexity`）。

### 常见错误

- **把独立误差线性相加。** 独立误差应按平方和开方合成；线性相加会高估误差，而对强正相关的误差按平方和开方合成则会低估误差（应计入 {eq}`eq-08-error-propagation` 中的协方差项）。
- **把一阶公式用于大误差。** 泰勒线性化假设相对误差较小；对于大误差或高度非线性的模型，应改用模拟求输出的分布。
- **不考虑数据能否支撑，就选择最详细的模型。** 每增加一个变量都会带来测量误差；数据较差时，较简单的模型总误差可能更小。

## 参考文献

- Ortúzar, J. de D., & Willumsen, L. G. (2011). *Modelling Transport* (4th
  ed.), Section 3.2 (Errors in modelling and forecasting). Wiley.
  <https://doi.org/10.1002/9781119993308>
- Alonso, W. (1968). Predicting best with imperfect data. *Journal of the
  American Institute of Planners*, *34*(4), 248–255.
  <https://doi.org/10.1080/01944366808977813>
- Taylor, J. R. (1997). *An Introduction to Error Analysis* (2nd ed.),
  Chapter 3. University Science Books.
