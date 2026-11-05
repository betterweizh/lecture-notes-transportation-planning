# 交通方式划分：离散选择模型

## 概述

交通方式划分（modal split）是经典模型的第三步，它把每对小区之间的出行分配到各种可用的交通方式上。本章和下一章介绍两种方法。本章从个体出发：非集计（离散）选择模型（discrete choice model）描述单个出行者在有限个互斥方案中的选择——交通方式，同样也可以是路径、目的地或出发时间。这些模型建立在**随机效用最大化**（random utility maximization）的基础上：每个方案都有一个效用，其中系统部分取决于可观测的属性，随机部分则是分析人员无法观测的，出行者选择效用最高的方案。对随机部分的不同假设分别给出线性概率模型、Probit 模型和 Logit 模型。本章推导这些模型，研究多项 Logit 模型（multinomial logit）及其巢式扩展的性质，并说明如何用极大似然法估计和检验参数。Logit 模型所依据的耿贝尔分布和逻辑斯谛分布见{doc}`01-probability-distributions`，基于选择的抽样见{doc}`07-travel-surveys-and-sampling`。{doc}`12-aggregate-modal-split`随后将同样的 Logit 形式应用于小区平均值，并将其与出行分布结合。

:::{admonition} 学习目标
:class: objectives
学完本章后，读者应能够：

- 阐述随机效用最大化框架，并解释为什么只有效用差和效用的尺度才有意义；
- 用通用变量、方案特定变量、常数项和虚拟变量设定系统效用；
- 推导二项线性概率模型、Probit 模型、Logit 模型以及多项 Logit 模型；
- 解释 IIA 性质，计算弹性，并使用对数和；
- 计算巢式 Logit 模型的概率；
- 写出样本的对数似然函数，用极大似然法估计参数并进行检验；
- 校正用基于选择的样本估计的模型。
:::

## 符号说明

| 符号 | 含义 |
|---|---|
| $n = 1, \ldots, N$ | 样本中的决策者（出行者） |
| $C_n$, $J_n$ | 出行者 $n$ 的选择集及其包含的方案数 |
| $U_{in} = V_{in} + \varepsilon_{in}$ | 方案 $i$ 对 $n$ 的效用：系统部分加随机部分 |
| $\bx_{in}$ | 出行者 $n$ 面对的方案 $i$ 的解释变量向量 |
| $\bbeta$ | 系数向量，$V_{in} = \bbeta\T\bx_{in}$ |
| $P_n(i)$ | $n$ 选择 $i$ 的概率 |
| $\mu$ | 耿贝尔（逻辑斯谛）随机项的尺度参数 |
| $\phi_m$ | 巢 $m$ 的结构参数（巢式 Logit 模型） |
| $y_{in}$ | 若 $n$ 选择了 $i$ 则为 1，否则为 0 |
| $\mathcal{L}(\bbeta)$, $LL(\bbeta)$ | 似然函数和对数似然函数 |
| $H_i$, $Q_i$ | 方案 $i$ 的样本份额和总体份额（基于选择的样本） |

## 随机效用最大化

### 效用

在经济学中，**效用函数**（utility function）$u: X \to \R$ 对选择集（choice set）$X$ 中的方案进行排序：当 $u(x) \ge u(y)$ 时，消费者弱偏好 $x$ 胜于 $y$，并选择效用最高的方案。只有排序才有意义，因此 $u$ 的任何单调递增变换都表示相同的偏好。

应用于出行时，某种交通方式的效用概括了它对出行者的吸引力，是该方式属性和出行者属性的函数。分析人员无法观测所有相关因素——偏好因人而异，有些属性没有被测量，感知也各不相同——因此从分析人员的角度看，效用是一个**随机变量**：

$$
U_{in} = V_{in} + \varepsilon_{in},
$$ (eq-11-random-utility)

其中 $V_{in}$ 是**系统（确定性）部分**（systematic utility），$\varepsilon_{in}$ 是**随机部分（扰动项）**。出行者选择效用最高的方案，因此对分析人员而言

$$
\begin{aligned}
P_n(i) &= \Prob\left(U_{in} \ge U_{jn},\ \forall j \in C_n\right), \\
\sum_{i \in C_n} P_n(i) &= 1 .
\end{aligned}
$$ (eq-11-rum)

建立模型分三步：将效用分为系统部分和随机部分，设定系统部分，设定随机部分的分布。

### 只有效用差和尺度才有意义

对二项选择 $C_n = \{i, j\}$，

$$
\begin{aligned}
P_n(i) &= \Prob\left(V_{in} + \varepsilon_{in} \ge V_{jn} + \varepsilon_{jn}\right) \\
&= \Prob\left(\varepsilon_{jn} - \varepsilon_{in} \le V_{in} - V_{jn}\right).
\end{aligned}
$$ (eq-11-binary-rum)

由此得到两个结论，它们对任意多个方案都成立。

1. **给所有效用加上同一个常数不改变概率。** 只有差值 $V_{in} - V_{jn}$ 和 $\varepsilon_{jn} - \varepsilon_{in}$ 才有意义。因此至多能估计 $J - 1$ 个方案特定常数，而不随方案变化的变量（收入、年龄）至多只能进入 $J - 1$ 个方案的效用。
2. **将所有效用乘以同一个正常数不改变概率。** 效用的尺度是任意的，必须通过归一化加以固定，通常是固定扰动项的方差（例如 Logit 模型中 $\mu = 1$，Probit 模型中 $\sigma = 1$）。扰动项的非零均值被常数项吸收。

## 系统效用的设定

系统效用取决于出行者 $n$ 所面对的方案 $i$ 的属性 $\bz_{in}$（时间、费用、舒适性、可靠性），以及出行者的社会经济特征 $\mathbf{s}_n$（收入、小汽车拥有、家庭规模、年龄）。实际中它被设定为**参数的线性函数**：

$$
\begin{aligned}
V_{in} &= \beta_1 x_{in1} + \beta_2 x_{in2} + \cdots + \beta_K x_{inK} \\
&= \bbeta\T\bx_{in},
\end{aligned}
$$ (eq-11-linear-utility)

其中每个 $x_{ink}$ 都是 $\bz_{in}$ 和 $\mathbf{s}_n$ 的函数。变量可以是：

- **通用变量**（generic），在所有效用中具有相同的系数（例如车内时间在每种方式中的价值相同）；
- **方案特定变量**（alternative-specific），只进入一个效用（例如到达公共交通的步行时间的系数），包括**方案特定常数**（alternative-specific constant，ASC），其编码方式为该方案取 1、其他方案取 0 的变量；
- **社会经济变量**，至多进入 $J - 1$ 个效用，或与属性交互（费用除以收入、时间乘以年龄）；
- 表示类别（年龄组、性别、目的地是否在中央商务区）的**虚拟变量**（dummy variable），有 $L$ 个类别的变量至多使用 $L - 1$ 个虚拟变量。

对*参数*线性并不妨碍*变量*具有非线性效应（对数、分段项、交互项）。不过，将连续变量分组会丢失信息，通常不可取。

两个系数之比是**边际替代率**。若 $\beta_t$ 为时间的系数、$\beta_c$ 为费用的系数，则主观的**时间价值**（value of time）为 $\beta_t/\beta_c$（单位时间的货币量）。

## 二项选择模型

令 $\varepsilon_n = \varepsilon_{jn} - \varepsilon_{in}$，其密度为 $f$，则由 {eq}`eq-11-binary-rum`，$P_n(i) = \int_{-\infty}^{V_{in} - V_{jn}} f(y)\,\diff y$。对 $f$ 的每一种假设都给出一个模型。

### 线性概率模型

若 $\varepsilon_n$ 在 $[-L, L]$ 上服从均匀分布，则

$$
P_n(i) =
\begin{cases}
0, & V_{in} - V_{jn} < -L, \\[2pt]
\dfrac{V_{in} - V_{jn} + L}{2L}, & -L \le V_{in} - V_{jn} \le L, \\[6pt]
1, & V_{in} - V_{jn} > L .
\end{cases}
$$ (eq-11-linear-probability)

该模型简单，但在 $\pm L$ 处不可导，而且会预测出恰好为 0 或 1 的概率，而现实中总有一些出行者选择模型认为没有人会选的方案。

### 二项 Probit 模型

若 $\varepsilon_{in}$ 和 $\varepsilon_{jn}$ 服从均值为零、方差为 $\sigma_i^2$ 和 $\sigma_j^2$、协方差为 $\sigma_{ij}$ 的正态分布，则 $\varepsilon_n$ 服从方差为 $\sigma^2 = \sigma_i^2 + \sigma_j^2 - 2\sigma_{ij}$ 的正态分布，且

$$
\begin{aligned}
P_n(i) &= \Phi\!\left(\frac{V_{in} - V_{jn}}{\sigma}\right) \\
&= \Phi\!\left(\frac{\bbeta\T(\bx_{in} - \bx_{jn})}{\sigma}\right).
\end{aligned}
$$ (eq-11-binary-probit)

正态假设是自然的（扰动项是许多被遗漏效应之和），但 $\Phi$ 没有闭式表达；$1/\sigma$ 起尺度的作用，归一化为 1。

### 二项 Logit 模型

若 $\varepsilon_{in}$ 和 $\varepsilon_{jn}$ 独立且同服从尺度参数（scale parameter）为 $\mu$ 的耿贝尔分布（Gumbel distribution），则 $\varepsilon_n$ 服从逻辑斯谛分布（logistic distribution；{prf:ref}`prop-01-logistic`的性质 4），均值为 0，方差为 $\pi^2/(3\mu^2)$，且

$$
\begin{aligned}
P_n(i) &= \frac{1}{1 + e^{-\mu(V_{in} - V_{jn})}} \\
&= \frac{e^{\mu V_{in}}}{e^{\mu V_{in}} + e^{\mu V_{jn}}} .
\end{aligned}
$$ (eq-11-binary-logit)

对线性效用，$P_n(i) = 1/\{1 + \exp[-\mu\bbeta\T(\bx_{in} - \bx_{jn})]\}$；$\mu$ 归一化为 1。方差相等时，逻辑斯谛分布函数与正态分布函数非常接近，因此二项 Logit 模型和 Probit 模型的拟合几乎相同；由于方差归一化方式不同，Logit 系数约为 Probit 系数的 $\pi/\sqrt{3} \approx 1.8$ 倍。

### 极端情形

三种模型具有相同的两个极限。当扰动项方差趋于零（$\mu \to \infty$、$\sigma \to 0$、$L \to 0$）时，选择变为**确定性**的：若 $V_{in} > V_{jn}$，则 $P_n(i) = 1$；若 $V_{in} < V_{jn}$，则为 0。当方差趋于无穷（$\mu \to 0$、$\sigma \to \infty$、$L \to \infty$）时，模型不含任何信息，$P_n(i) = P_n(j) = 1/2$。

## 多项 Logit 模型

### 模型

当 $C_n$ 含有 $J_n > 2$ 个方案时，

$$
P_n(i) = \Prob\left(\varepsilon_{jn} \le V_{in} - V_{jn} + \varepsilon_{in},\ \forall j \in C_n,\ j \ne i\right),
$$

模型由扰动项的联合分布导出。

:::{prf:theorem} 多项 Logit 模型
:label: thm-11-mnl

若扰动项 $\varepsilon_{in}$（$i \in C_n$）独立同分布（i.i.d.）于 $\mathrm{Gumbel}(0, \mu)$，则

$$
P_n(i) = \frac{\exp\left(\mu V_{in}\right)}{\sum_{j \in C_n}\exp\left(\mu V_{jn}\right)},
\qquad i \in C_n .
$$ (eq-11-mnl)

扰动项共同的标准差为 $\sigma = \pi/(\sqrt{6}\,\mu)$。
:::

:::{dropdown} 证明
:class-container: proof
:animate: fade-in

由{prf:ref}`prop-01-gumbel`的性质 4，$U_{jn} = V_{jn} + \varepsilon_{jn} \sim \mathrm{Gumbel}(V_{jn}, \mu)$。由性质 6，其余方案中的最优者 $U_n^{*} = \max_{j \ne i} U_{jn}$ 服从尺度参数为 $\mu$ 的耿贝尔分布，其位置参数为

$$
V_n^{*} = \frac{1}{\mu}\ln\sum_{j \ne i} e^{\mu V_{jn}} .
$$

于是 $P_n(i) = \Prob(U_{in} \ge U_n^{*})$ 是尺度参数相同的两个独立耿贝尔变量之间的二项选择，由 {eq}`eq-11-binary-logit`，

$$
\begin{aligned}
P_n(i) &= \frac{e^{\mu V_{in}}}{e^{\mu V_{in}} + e^{\mu V_n^{*}}} \\
&= \frac{e^{\mu V_{in}}}{e^{\mu V_{in}} + \sum_{j \ne i} e^{\mu V_{jn}}},
\end{aligned}
$$

这就是 {eq}`eq-11-mnl`。
:::

耿贝尔分布能很好地近似正态分布；选择它是为了解析上的方便。真正的限制在于独立同分布假设：它意味着所有扰动项方差相等，且方案之间不相关。

取 $\mu = 1$ 时，系数吸收了尺度：以 $\mu = 1$ 估计 $V_{jn}$ 得到的是 $\mu\bbeta$ 而不是 $\bbeta$。因此，只有时间价值这类比值，才能在用不同数据集（例如 RP 数据和 SP 数据）估计的模型之间进行有意义的比较。

当 $\mu \to 0$ 时，$P_n(i) \to 1/J_n$（所有方案等可能）；当 $\mu \to \infty$ 时，$V_{in}$ 最大的方案 $P_n(i) \to 1$，其他方案为 0。

### 无关方案独立性

对任意两个方案 $i$ 和 $l$，

$$
\begin{aligned}
\frac{P_n(i)}{P_n(l)} &= \frac{e^{\mu V_{in}}}{e^{\mu V_{ln}}} \\
&= e^{\mu(V_{in} - V_{ln})},
\end{aligned}
$$ (eq-11-iia)

与选择集中的其他方案无关。这一**无关方案独立性**（independence of irrelevant alternatives，IIA）性质（Luce, 1959）是独立同分布假设的直接结果。它简化了估计（模型可以在方案子集上估计）和预测（新方案按各已有方案的份额比例从中吸引出行者），但当方案相关时并不现实。在经典的**红巴士/蓝巴士**问题中，出行者在小汽车和红色巴士之间平分；把一半巴士漆成蓝色，就增加了一个与红巴士完全相同的方案，Logit 模型预测三者的份额各为 1/3，而常识告诉我们小汽车仍保持 1/2，两种巴士平分另一半（集计形式见{prf:ref}`ex-27-ms-red-blue`）。任何扰动项独立同分布的模型（不仅是 Logit 模型）在这种情形下都会失效。

### 弹性

对线性效用，$P_n(i)$ 对方案 $i$ 的属性 $x_{ink}$ 的**直接弹性**（direct elasticity），以及对另一方案 $j$ 的属性 $x_{jnk}$ 的**交叉弹性**（cross elasticity）分别为

$$
\begin{aligned}
E^{P_n(i)}_{x_{ink}} &= \frac{\partial P_n(i)}{\partial x_{ink}}\frac{x_{ink}}{P_n(i)} \\
&= \mu\beta_k\, x_{ink}\left[1 - P_n(i)\right],
\end{aligned}
$$ (eq-11-direct-elasticity)

$$
E^{P_n(i)}_{x_{jnk}} = -\mu\beta_k\, x_{jnk}\, P_n(j), \qquad j \ne i .
$$ (eq-11-cross-elasticity)

交叉弹性对所有方案 $i \ne j$ 都相同——这是 IIA 的另一种表现。集计弹性由个体弹性按选择概率加权得到。

### 期望最大效用

由{prf:ref}`prop-01-gumbel`的性质 6，选择集的最大效用服从位置参数为 $\mu^{-1}\ln\sum_j e^{\mu V_{jn}}$ 的耿贝尔分布，因此

$$
\E\left[\max_{j \in C_n} U_{jn}\right] = \frac{1}{\mu}\ln\sum_{j \in C_n} e^{\mu V_{jn}} + \frac{\gamma}{\mu},
$$ (eq-11-logsum)

其中 $\gamma \approx 0.5772$ 为欧拉常数。**对数和**（logsum）$\mu^{-1}\ln\sum_j e^{\mu V_{jn}}$（即期望最大效用 EMU，相差常数 $\gamma/\mu$）度量了选择集的总体吸引力。若效用取广义费用的相反数，且 $\mu$ 等于离散参数 $\lambda$，它就是 {eq}`eq-12-composite-cost` 中组合费用的相反数。它的变化除以货币的边际效用，给出政策引起的消费者剩余变化（Williams, 1977）。

## 多项 Probit 模型

若扰动项服从多元正态分布 $(\varepsilon_{1n}, \ldots, \varepsilon_{J_nn}) \sim \mathcal{N}(\bzero, \bSigma)$，则可以表示任意的方差和相关结构，IIA 不再成立。概率 $P_n(i)$ 是 $J_n$ 维正态积分 {eq}`eq-01-probit-probability`，当 $J_n > 2$ 时没有闭式解；需要用数值积分或蒙特卡洛模拟计算（{prf:ref}`ex-17-mvn-maximum`）。Probit 模型是存在路径重叠时路径选择的自然模型（{doc}`15-stochastic-user-equilibrium`）。

## 巢式 Logit 模型

**巢式 Logit 模型**（nested logit；Ben-Akiva, 1973；Williams, 1977；McFadden, 1978）对相似方案组（如红巴士和蓝巴士）放松了 IIA：具有共同未观测属性的方案归入同一个**巢**（nest）。对于巢为 $m$、方案为 $i \in C_m$ 的两层结构，$i$ 的概率是条件概率与边缘概率的乘积：

$$
\begin{aligned}
P_n(i) &= P_n(i \mid m)\,P_n(m), \\
P_n(i \mid m) &= \frac{e^{V_{in}}}{\sum_{l \in C_m} e^{V_{ln}}}, \\
P_n(m) &= \frac{e^{V_{mn}}}{\sum_{m'} e^{V_{m'n}}},
\end{aligned}
$$ (eq-11-nested-logit)

其中巢的效用等于其自身的系统效用（若有）加上 $\phi_m$ 乘以巢内方案的**期望最大效用**：

$$
\begin{aligned}
V_{mn} &= V_{mn}^0 + \phi_m\,\mathrm{EMU}_{mn}, \\
\mathrm{EMU}_{mn} &= \ln\sum_{l \in C_m} e^{V_{ln}} .
\end{aligned}
$$ (eq-11-emu)

**结构参数** $\phi_m$ 等于上层尺度参数与下层尺度参数之比。为与随机效用最大化相一致，它必须满足 $0 < \phi_m \le 1$：$\phi_m$ 越小，巢内方案的相关性越强；$\phi_m = 1$ 时模型退化为多项 Logit 模型。巢内 IIA 成立；巢之间则不成立（{prf:ref}`ex-26-hw3-q4`）。

## 极大似然估计

### 似然函数

若出行者 $n$ 选择了 $i$，令 $y_{in} = 1$，否则为 0。对由 $N$ 个相互独立的出行者构成的随机样本，**似然函数**（likelihood）是模型再现全部观测选择的概率：

$$
\mathcal{L}(\bbeta) = \prod_{n=1}^{N}\prod_{i \in C_n} P_n(i)^{y_{in}},
$$ (eq-11-likelihood)

**对数似然函数**为

$$
LL(\bbeta) = \sum_{n=1}^{N}\sum_{i \in C_n} y_{in}\ln P_n(i) .
$$ (eq-11-log-likelihood)

对二项模型，记 $y_n = y_{in}$，则 $LL = \sum_n \{y_n\ln P_n(i) + (1 - y_n)\ln[1 - P_n(i)]\}$，即机器学习中二元交叉熵损失的相反数。由于每个 $P_n(i) \le 1$，$LL \le 0$。**极大似然（maximum likelihood，ML）**估计 $\hat\bbeta$ 使 $LL$ 最大：它给出使观测选择最可能出现的参数（{prf:ref}`ex-26-dc-likelihood`）。

### 梯度、黑塞矩阵与凹性

对 $\mu = 1$ 的二项 Logit 模型，记 $\bx_n = \bx_{in} - \bx_{jn}$，$P_n = P_n(i) = 1/(1 + e^{-\bbeta\T\bx_n})$。由于 $\partial P_n/\partial\bbeta = P_n(1 - P_n)\bx_n$，

$$
\begin{aligned}
\nabla LL(\bbeta) &= \sum_{n=1}^{N}\left(y_n - P_n\right)\bx_n, \\
\nabla^2 LL(\bbeta) &= -\sum_{n=1}^{N} P_n\left(1 - P_n\right)\bx_n\bx_n\T .
\end{aligned}
$$ (eq-11-logit-gradient-hessian)

黑塞矩阵半负定，因此对数似然函数是**凹函数**；若由 $\bx_n$ 构成的矩阵列满秩，则黑塞矩阵负定。因此，一阶条件 $\nabla LL = \bzero$——“观测值减预测值，以变量加权后求和为零”——确定的是全局极大点（如果极大点存在）。对多项 Logit 模型，梯度为 $\sum_n\sum_i (y_{in} - P_n(i))\bx_{in}$，对数似然函数同样是凹的。

极大点用**牛顿–拉弗森**（Newton–Raphson）法求得：

$$
\hat\bbeta^{(t+1)} = \hat\bbeta^{(t)} - \left[\nabla^2 LL\big(\hat\bbeta^{(t)}\big)\right]^{-1}\nabla LL\big(\hat\bbeta^{(t)}\big),
$$ (eq-11-newton-raphson)

例如从 $\hat\bbeta^{(0)} = \bzero$ 开始，直到 $\hat\bbeta$ 或 $LL$ 的变化可以忽略；电子表格求解器、`scipy` 以及专门的软件包（Biogeme、Apollo、`statsmodels`）都实现了这一方法。

:::{admonition} 极大值不存在的情形
:class: warning
有两种情形会使估计无法进行。

- **参数不可识别。** 若某个系数对应的变量在所有效用中取值相同，或该变量在所用的全部观测中都等于零，则该系数无法估计（似然函数在这个方向上是平的）。
- **完全分离。** 若变量的某种组合能准确预测每一个观测选择，则当系数无限增大时对数似然趋向于 0，不存在有限的极大值。这在很小的样本中很常见（{prf:ref}`ex-26-hw3-q6`）。
:::

### 标准误与检验

在通常的正则条件下，ML 估计量是一致的且渐近正态，其协方差矩阵等于 **Fisher 信息**矩阵的逆：

$$
\Var\big[\hat\bbeta\big] \approx \left(-\E\left[\nabla^2 LL(\bbeta)\right]\right)^{-1},
$$ (eq-11-ml-covariance)

用 $[-\nabla^2 LL(\hat\bbeta)]^{-1}$ 估计。常用的检验有三种。

渐近 $t$ 检验
: 在 $H_0: \beta_k = 0$ 下，$t_k = \hat\beta_k/\se(\hat\beta_k)$ 近似服从标准正态分布；$|t_k| > 1.96$ 时在 5 % 水平下拒绝 $H_0$。

似然比检验
: 对于嵌套在无约束模型 $U$ 中、参数少 $r$ 个的约束模型 $R$，在约束成立时 $-2[LL(\hat\bbeta_R) - LL(\hat\bbeta_U)] \;\dot\sim\; \chi^2(r)$。它可以同时检验多个约束——例如检验某个系数是通用的而不是方案特定的。

拟合优度
: **似然比指数**（likelihood ratio index）$\rho^2 = 1 - LL(\hat\bbeta)/LL(\bzero)$，其中 $LL(\bzero)$ 是等概率模型的对数似然（$LL(\bzero) = \sum_n \ln(1/J_n)$）。它介于 0 和 1 之间，但 0.2–0.4 的值就已经表示拟合良好，而且它不能与回归的 $R^2$ 相比。调整后的形式 $\bar\rho^2 = 1 - [LL(\hat\bbeta) - K]/LL(\bzero)$ 对参数个数 $K$ 进行了惩罚。以只含常数项的模型 $LL(\bc)$ 为基准度量拟合度，得到 $\rho^2(\bc)$，当各方式市场份额不相等时它更有参考价值。

与回归一样，还应检查系数的**符号和大小是否合理**（费用和时间系数为负，时间价值合理）。

### 基于选择的样本

若模型是用基于选择的样本（choice-based sample）估计的，其中方案 $i$ 的样本份额为 $H_i$，而其总体份额为 $Q_i$（{doc}`07-travel-surveys-and-sampling`），则含全套方案特定常数的多项 Logit 模型对除常数项外的全部系数仍是一致的。常数项按下式校正：

$$
K_i' = K_i - \ln\frac{H_i}{Q_i},
$$ (eq-11-asc-correction)

至多相差一个对所有方案相同的加性常数（{prf:ref}`ex-26-hw3-q5`）。另一种方法是以 $Q_i/H_i$ 为权重，用加权似然（WESML）估计模型。

### 用非集计模型进行预测

非集计模型预测的是个体的概率。集计预测可以通过**样本枚举**得到——将模型应用于一个有代表性的样本（可重新加权到预测年）中的每个个体，再用扩样系数对概率求和——也可以通过将个体划分为同质组得到。将模型应用于变量的小区平均值（“朴素”方法）会引入集计误差，因为 Logit 函数是非线性的。

## 本章回顾

### 小结

- 随机效用 {eq}`eq-11-random-utility`：出行者选择效用最大的方案 {eq}`eq-11-rum`；只有效用差和效用尺度是可识别的 {eq}`eq-11-binary-rum`。
- 均匀、正态和耿贝尔扰动项分别给出线性概率模型 {eq}`eq-11-linear-probability`、Probit 模型 {eq}`eq-11-binary-probit` 和 Logit 模型 {eq}`eq-11-binary-logit`。
- 多项 Logit 模型（{prf:ref}`thm-11-mnl`）：$P_n(i) = e^{\mu V_{in}}/\sum_j e^{\mu V_{jn}}$ {eq}`eq-11-mnl`，具有 IIA 性质 {eq}`eq-11-iia`，直接弹性为 $\mu\beta_k x_{ink}[1 - P_n(i)]$ {eq}`eq-11-direct-elasticity`，交叉弹性对各方案相同 {eq}`eq-11-cross-elasticity`，对数和即期望最大效用 {eq}`eq-11-logsum`。
- 巢式 Logit 模型 {eq}`eq-11-nested-logit` 将相关的方案分组；巢的效用含 $\phi_m$ 乘以巢内方案的对数和 {eq}`eq-11-emu`，且 $0 < \phi_m \le 1$。
- 参数通过最大化对数似然函数 {eq}`eq-11-log-likelihood` 估计，Logit 模型的对数似然函数是凹的 {eq}`eq-11-logit-gradient-hessian`，可用牛顿–拉弗森法 {eq}`eq-11-newton-raphson` 求解；推断使用协方差矩阵 {eq}`eq-11-ml-covariance`、$t$ 检验、似然比检验和 $\rho^2$。
- 用基于选择的样本估计时，只有方案特定常数有偏，按 {eq}`eq-11-asc-correction` 校正。

### 常见错误

- **在全部 $J$ 个效用中都加入常数项或社会经济变量。** 只有效用差才有意义，因此这样的参数不可识别；应将一个方案归一化（至多 $J - 1$ 个常数，社会经济变量至多进入 $J - 1$ 个效用）。
- **直接跨数据集比较系数。** 估计得到的系数是 $\mu\bbeta$，而尺度 $\mu$ 在不同数据集之间（例如 RP 数据和 SP 数据）不同；应比较时间价值这类比值。
- **对具有共同未观测属性的方案使用多项 Logit 模型。** 此时 IIA 会给出荒谬的替代关系（红巴士/蓝巴士）；应使用巢式 Logit 模型或 Probit 模型。
- **允许巢式 Logit 的结构参数取 $(0, 1]$ 以外的值。** 大于 1 的值与随机效用最大化不一致；小于或等于 0 的值没有意义。
- **像解释回归 $R^2$ 那样解释 $\rho^2$。** 似然比指数的量纲不同：0.2–0.4 的值就已表示拟合良好。
- **用基于选择的样本估计的模型进行预测时不校正常数项。** 这些常数再现的是样本份额而不是总体份额；应先按 {eq}`eq-11-asc-correction` 校正。

## 参考文献

- Ben-Akiva, M. (1973). *Structure of passenger travel demand models*
  [Doctoral dissertation, Massachusetts Institute of Technology].
- Ben-Akiva, M., & Lerman, S. R. (1985). *Discrete Choice Analysis: Theory
  and Application to Travel Demand*, Chapters 3–8 and 10. MIT Press.
- Ortúzar, J. de D., & Willumsen, L. G. (2011). *Modelling Transport* (4th
  ed.), Chapters 7 and 8. Wiley.
- Train, K. E. (2009). *Discrete Choice Methods with Simulation* (2nd ed.),
  Chapters 2–5 and 8. Cambridge University Press.
  <https://eml.berkeley.edu/books/choice2.html>
- McFadden, D. (1974). Conditional logit analysis of qualitative choice
  behavior. In P. Zarembka (Ed.), *Frontiers in Econometrics* (pp. 105–142).
  Academic Press.
- McFadden, D. (1978). Modelling the choice of residential location. In
  A. Karlqvist, L. Lundqvist, F. Snickars, & J. W. Weibull (Eds.),
  *Spatial Interaction Theory and Planning Models* (pp. 75–96).
  North-Holland.
- Luce, R. D. (1959). *Individual Choice Behavior: A Theoretical Analysis*.
  Wiley.
- Williams, H. C. W. L. (1977). On the formation of travel demand models
  and economic evaluation measures of user benefit. *Environment and
  Planning A*, 9(3), 285–344. <https://doi.org/10.1068/a090285>
- Manski, C. F., & Lerman, S. R. (1977). The estimation of choice
  probabilities from choice based samples. *Econometrica*, *45*(8),
  1977–1988. <https://doi.org/10.2307/1914121>
