# 交通方式划分：离散选择

本章求解{doc}`11-discrete-choice-models`中的例题与习题，包括估计和抽样问题。{doc}`35-python-mode-choice`中的代码可以复现这些数值。

## 二项 Logit

:::{prf:example} 两镇之间的小汽车或公共交通
:label: ex-26-dc-binary

两镇之间的通勤者在小汽车和公共交通之间选择，其效用为

$$
\begin{aligned}
U_{\mathrm{car}} &= 0.5 - 0.25\,T_{\mathrm{car}} - 0.42\,E_{\mathrm{car}} - 1.25\,C_{\mathrm{car}} + \varepsilon_{\mathrm{car}}, \\
U_{\mathrm{transit}} &= -0.25\,T_{\mathrm{transit}} - 0.42\,E_{\mathrm{transit}} - 1.25\,C_{\mathrm{transit}} + \varepsilon_{\mathrm{transit}},
\end{aligned}
$$

其中 $T$ 为车内时间（分钟），$E$ 为接驳时间（分钟），$C$ 为费用（新元），随机项独立同分布，服从 $\mu = 1$ 的耿贝尔分布（Gumbel distribution）。（小汽车，公共交通）的平均值为 $T = (25, 30)$，$E = (5, 8)$，$C = (3, 1)$。

(1) 计算方式分担率。(2) 若小汽车费用增加 1 新元的通行费，重新计算分担率。(3) 计算小汽车分担率对小汽车费用的直接弹性（direct elasticity），以及所隐含的车内时间价值（value of time）。
:::

:::{dropdown} 解答
:class-container: solution
:animate: fade-in

**(1)** 系统效用为

$$
\begin{aligned}
V_{\mathrm{car}} &= 0.5 - 0.25 \times 25 - 0.42 \times 5 - 1.25 \times 3 = -11.60, \\
V_{\mathrm{transit}} &= -0.25 \times 30 - 0.42 \times 8 - 1.25 \times 1 = -12.11,
\end{aligned}
$$

因此由 {eq}`eq-11-binary-logit`

$$
\begin{aligned}
P(\mathrm{car}) &= \frac{1}{1 + e^{V_{\mathrm{transit}} - V_{\mathrm{car}}}} \\
&= \frac{1}{1 + e^{-0.51}} \\
&= 0.625, \\
P(\mathrm{transit}) &= 0.375 .
\end{aligned}
$$

**(2)** 通行费使小汽车效用降低 $1.25 \times 1 = 1.25$：$V^*_{\mathrm{car}} = -12.85$，因此

$$
P^*(\mathrm{car}) = \frac{1}{1 + e^{-12.11 + 12.85}} = \frac{1}{1 + e^{0.74}} = 0.323,
$$

公共交通分担率升至 0.677。

**(3)** 由 {eq}`eq-11-direct-elasticity`，

$$
\begin{aligned}
E^{P(\mathrm{car})}_{C_{\mathrm{car}}} &= \beta_C\,C_{\mathrm{car}}\left[1 - P(\mathrm{car})\right] \\
&= -1.25 \times 3 \times 0.375 = -1.41 :
\end{aligned}
$$

小汽车费用每增加 1 %，小汽车分担率约下降 1.4 %。车内时间价值为 $\beta_T/\beta_C = 0.25/1.25 = $ 每分钟 0.20 新元（每小时 12 新元），而接驳时间的价值是车内时间的 $0.42/0.25 = 1.7$ 倍。
:::

## 极大似然

:::{prf:example} 似然函数与极大似然估计
:label: ex-26-dc-likelihood

六名出行者在两种公共交通方式 A 和 B 之间选择：

| 出行者 | 年龄 | A 的时间（分钟） | B 的时间（分钟） | 选择 |
|---|---|---|---|---|
| 1 | 35 | 15.4 | 58.2 | A |
| 2 | 45 | 14.2 | 31.0 | B |
| 3 | 37 | 19.6 | 43.6 | A |
| 4 | 42 | 50.8 | 59.9 | A |
| 5 | 32 | 55.5 | 33.8 | B |
| 6 | 15 | 不可用 | 48.4 | B |

效用为

$$
\begin{aligned}
V_A &= \beta_0 + \beta_1 t_A + \beta_2\,\mathrm{Age}_{<20} + \beta_3\,\mathrm{Age}_{>40}, \\
V_B &= \beta_1 t_B,
\end{aligned}
$$

其中两个年龄虚拟变量分别对年龄小于 20 岁和大于 40 岁的出行者取 1。(a) 写出选择概率，并计算 $(\beta_0, \beta_1, \beta_2, \beta_3) = (0.5, -0.1, 0.1, -0.1)$ 处的似然值。(b) 求极大似然估计（maximum likelihood estimation）值和似然比指数（likelihood ratio index）$\rho^2$。
:::

:::{dropdown} 解答
:class-container: solution
:animate: fade-in

**哪些观测值有用。** 出行者 6 只有方式 B 可用；其选择是确定的，对对数似然函数的贡献为 $\ln 1 = 0$。因此，唯一一名小于 20 岁的出行者没有被利用，**$\beta_2$ 无法**由这些数据估计。

**(a) 概率。** 由 $V_A - V_B = \beta_0 + \beta_1(t_A - t_B) + \beta_3\mathrm{Age}_{>40}$，

$$
\begin{aligned}
P_1(A) &= \frac{1}{1 + \exp\left(-\beta_0 + 42.8\beta_1\right)}, \\
P_2(B) &= \frac{1}{1 + \exp\left(\beta_0 - 16.8\beta_1 + \beta_3\right)}, \\
P_3(A) &= \frac{1}{1 + \exp\left(-\beta_0 + 24.0\beta_1\right)}, \\
P_4(A) &= \frac{1}{1 + \exp\left(-\beta_0 + 9.1\beta_1 - \beta_3\right)}, \\
P_5(B) &= \frac{1}{1 + \exp\left(\beta_0 + 21.7\beta_1\right)} .
\end{aligned}
$$

在 $(0.5, -0.1, 0.1, -0.1)$ 处：

$$
\begin{aligned}
P_1(A) &= 0.9917, \\
P_2(B) &= 0.1111, \\
P_3(A) &= 0.9478, \\
P_4(A) &= 0.7875, \\
P_5(B) &= 0.8416,
\end{aligned}
$$

似然值为它们的乘积，$\mathcal{L} = 0.0692$（$LL = -2.671$）。其他参数值给出的似然值为：在 $(0, -0.5, 0.5, -0.5)$ 处 $\mathcal{L} = 3.64\times 10^{-4}$，在 $(0, 1, 0.5, -0.5)$ 处为 $2.49\times 10^{-43}$：似然值衡量的是每组参数再现观测选择的程度。

**(b) 极大似然。** 从零出发，用牛顿–拉弗森法关于 $(\beta_0, \beta_1, \beta_3)$ 最大化 $LL = \ln P_1(A) + \ln P_2(B) + \ln P_3(A) + \ln P_4(A) + \ln P_5(B)$，得

$$
\begin{aligned}
\hat\beta_0 &= -0.037, \\
\hat\beta_1 &= -0.102~\text{每分钟}, \\
\hat\beta_3 &= -1.28, \\
LL(\hat\bbeta) &= -2.016 .
\end{aligned}
$$

等可能模型的 $LL(\bzero) = 5\ln 0.5 = -3.466$，因此

$$
\rho^2 = 1 - \frac{-2.016}{-3.466} = 0.418 .
$$

时间系数具有预期的负号。然而，由黑塞矩阵的逆得到的标准误分别为 2.41、0.094 和 2.95，因此只有五个观测值时，没有一个系数是显著的（$|t| < 1.1$）；本例只用于说明方法。
:::

## 选择模型的应用

:::{prf:example} 收入服从均匀分布时的选择
:label: ex-26-hw3-q3

出行者在方式 $a$ 和 $b$ 之间选择，出行时间为 $t_a$ 和 $t_b$，效用为

$$
\begin{aligned}
U_a &= \alpha t_a + \beta I, \\
U_b &= \alpha t_b,
\end{aligned}
$$

其中 $\alpha = -0.5$，$\beta = 1.5\times 10^{-4}$，收入 $I$ 在 5 000 至 25 000 之间均匀分布（密度为 $0.5\times 10^{-4}$）。(a) 求选择 $a$ 的概率关于 $t_b - t_a$ 的函数。(b) 画出其示意图。
:::

:::{dropdown} 解答
:class-container: solution
:animate: fade-in

**(a)** 对某个个体，若 $U_a \ge U_b$ 则选择 $a$：

$$
\alpha t_a + \beta I \ge \alpha t_b
\iff I \ge \frac{\alpha(t_b - t_a)}{\beta} = -\frac{10^4}{3}\left(t_b - t_a\right) =: I^{*}.
$$

此处收入起着随机项的作用。由于 $I \sim \mathcal{U}(5\,000, 25\,000)$，

$$
P_a = \Prob(I \ge I^{*}) =
\begin{cases}
1, & I^{*} \le 5\,000, \\[2pt]
\dfrac{25\,000 - I^{*}}{20\,000}, & 5\,000 < I^{*} < 25\,000, \\[6pt]
0, & I^{*} \ge 25\,000 .
\end{cases}
$$

用 $\Delta = t_b - t_a$（分钟）表示，$I^{*} \le 5\,000 \iff \Delta \ge -1.5$，$I^{*} \ge 25\,000 \iff \Delta \le -7.5$，因此

$$
P_a(\Delta) =
\begin{cases}
1, & \Delta \ge -1.5, \\[2pt]
1.25 + \dfrac{\Delta}{6}, & -7.5 < \Delta < -1.5, \\[6pt]
0, & \Delta \le -7.5 .
\end{cases}
$$

**(b)** $P_a$ 关于 $\Delta$ 的图形是一个斜坡：在 $\Delta = -7.5$ 之前为零，然后以每分钟 $1/6$ 的斜率线性上升，从 $\Delta = -1.5$ 起等于一；在 $\Delta = -4.5$ 处 $P_a = 0.5$。由于收入带来的额外效用，除非 $a$ 慢 1.5 分钟以上，否则所有人都选择 $a$；若 $a$ 慢 7.5 分钟以上，则没有人选择它。

这就是**线性概率模型**（linear probability model） {eq}`eq-11-linear-probability`：均匀分布的随机项产生一个带折点的线性斜坡。
:::

:::{prf:example} 一个巢式 Logit 模型
:label: ex-26-hw3-q4

小汽车（c）、合乘出租车（st）和大运量公共交通（mt）构成巢式 Logit 模型（nested logit）的上层；大运量公共交通是一个包含公交（b）和地铁（u）的巢。效用为

$$
\begin{aligned}
V_c &= -0.03\,t_c - 0.15\,c_c + 1.30, \\
V_{st} &= -0.03\,t_{st} - 0.15\,c_{st} - 0.25, \\
V_b &= -0.04\,t_b - 0.02\,c_b + 0.6, \\
V_u &= -0.04\,t_u - 0.02\,c_u, \\
V_{mt} &= 0.60\,\mathrm{EMU}, \\
\mathrm{EMU} &= \ln\left(e^{V_b} + e^{V_u}\right),
\end{aligned}
$$

其中 $\mu = 1$，平均值为

| | 小汽车 | 合乘出租车 | 公交 | 地铁 |
|---|---|---|---|---|
| 时间 $t$ | 4.5 | 5.5 | 7.5 | 5.4 |
| 费用/收入 $c$ | 23.0 | 15.0 | 5.5 | 3.6 |

计算每种方式的概率。
:::

:::{dropdown} 解答
:class-container: solution
:animate: fade-in

**下层巢。**

$$
\begin{aligned}
V_b &= -0.04 \times 7.5 - 0.02 \times 5.5 + 0.6 = 0.190, \\
V_u &= -0.04 \times 5.4 - 0.02 \times 3.6 = -0.288,
\end{aligned}
$$

$$
\begin{aligned}
P(b \mid mt) &= \frac{e^{0.190}}{e^{0.190} + e^{-0.288}} = 0.617, \\
P(u \mid mt) &= 0.383,
\end{aligned}
$$

且 $\mathrm{EMU} = \ln(e^{0.190} + e^{-0.288}) = 0.672$。

**上层。**

$$
\begin{aligned}
V_c &= -0.03 \times 4.5 - 0.15 \times 23 + 1.30 = -2.285, \\
V_{st} &= -0.03 \times 5.5 - 0.15 \times 15 - 0.25 = -2.665, \\
V_{mt} &= 0.60 \times 0.672 = 0.403,
\end{aligned}
$$

$$
\begin{aligned}
P_c &= \frac{e^{-2.285}}{e^{-2.285} + e^{-2.665} + e^{0.403}} = 0.061, \\
P_{st} &= 0.042, \\
P_{mt} &= 0.897 .
\end{aligned}
$$

**无条件概率。**

$$
\begin{aligned}
P_b &= 0.897 \times 0.617 = 0.554, \\
P_u &= 0.897 \times 0.383 = 0.343 .
\end{aligned}
$$

| 交通方式 | 小汽车 | 合乘出租车 | 公交 | 地铁 |
|---|---|---|---|---|
| 概率 | 0.061 | 0.042 | 0.554 | 0.343 |

结构参数（structural parameter）0.60 如所要求的那样位于 $(0, 1]$ 中：公交和地铁共享未观测属性（二者都是大运量公共交通），因此公交的改善从地铁吸引的份额按比例大于从小汽车吸引的份额。
:::

:::{prf:example} 修正在基于选择的样本上估计的模型
:label: ex-26-hw3-q5

在城市某一区域的样本上估计了一个小汽车与公交的二项 Logit 模型（$\mu = 1$）：

$$
\begin{aligned}
V_c &= 3.0 - 0.25\,t_c - 0.4\,e_c - 0.1\,c_c, \\
V_b &= -0.25\,t_b - 0.4\,e_b - 0.1\,c_b,
\end{aligned}
$$

其中 $t$ 为车内时间（分钟），$e$ 为接驳时间（分钟），$c$ 为费用；（小汽车，公交）的平均值为 $t = (25, 40)$，$e = (5, 8)$，$c = (140, 50)$。样本中有 220 人选择小汽车、630 人选择公交；在整个总体中，有 17 000 人选择小汽车、69 000 人选择公交。

(a) 应对模型进行何种修正？(b) 若公交票价上涨 25 %，选择小汽车的概率变化多少百分比？(c) 若小汽车费用上涨 100 % 呢？
:::

:::{dropdown} 解答
:class-container: solution
:animate: fade-in

**诊断。** 采用平均数据，

$$
\begin{aligned}
V_c &= 3.0 - 6.25 - 2.0 - 14.0 = -19.25, \\
V_b &= -10.0 - 3.2 - 5.0 = -18.20,
\end{aligned}
$$

因此 $P_c = 1/(1 + e^{1.05}) = 0.259$。这等于*样本*中的小汽车分担率 $H_c = 220/850 = 0.259$，但总体分担率为 $Q_c = 17\,000/86\,000 = 0.198$。样本中小汽车使用者的比例过高——这是一个基于选择的样本——模型也继承了这一偏差。

**(a) 修正。** 对于在基于选择的样本（choice-based sample）上估计的、含方案特定常数（alternative-specific constant）的 Logit 模型，只有常数是有偏的。由 {eq}`eq-11-asc-correction`，将公交常数归一化为零，

$$
\begin{aligned}
K_c' &= K_c - \ln\frac{H_c}{Q_c} + \ln\frac{H_b}{Q_b} \\
&= 3.0 - \ln\frac{0.2588}{0.1977} + \ln\frac{0.7412}{0.8023} \\
&= 3.0 - 0.2695 - 0.0793 = 2.651,
\end{aligned}
$$

修正后的模型为

$$
\begin{aligned}
V_c &= 2.651 - 0.25\,t_c - 0.4\,e_c - 0.1\,c_c, \\
V_b &= -0.25\,t_b - 0.4\,e_b - 0.1\,c_b .
\end{aligned}
$$

检验：此时 $V_c = -19.599$，$P_c = 1/(1 + e^{1.399}) = 0.198 = Q_c$。

**(b) 公交票价上涨 25 %。** $c_b = 62.5$，因此 $V_b = -19.45$，且

$$
P_c = \frac{1}{1 + e^{-19.45 + 19.599}} = \frac{1}{1 + e^{0.149}} = 0.463,
$$

增加了 $0.463/0.198 - 1 = 134\,\%$。响应之所以很大，是因为票价上涨使公交效用降低 1.25，而两种方式的效用原本只相差 1.4 个单位。

**(c) 小汽车费用上涨 100 %。** $c_c = 280$，因此 $V_c = 2.651 - 6.25 - 2.0 - 28.0 = -33.60$，$P_c = 1/(1 + e^{15.40}) = 2.1\times 10^{-7}$：几乎所有人都会选择公交。
:::

:::{prf:example} 由陈述偏好数据建立似然函数
:label: ex-26-hw3-q6

一项陈述偏好（stated preference，SP）调查得到了在方式 A 和 B 之间的六个选择：

| 受访者 | A 的时间（分钟） | A 的费用（新元） | B 的时间（分钟） | B 的费用（新元） | 月薪 $s$（千新元/月） | 选择 |
|---|---|---|---|---|---|---|
| 1 | 10 | 1.8 | 15 | 1.0 | 3.0 | B |
| 2 | 10 | 1.8 | 15 | 1.0 | 4.0 | A |
| 3 | 5 | 4.0 | 20 | 0.8 | 3.5 | B |
| 4 | 5 | 4.0 | 20 | 0.8 | 6.0 | A |
| 5 | 8 | 3.0 | 18 | 0.9 | 4.5 | B |
| 6 | 8 | 3.0 | 18 | 0.9 | 6.5 | A |

(a) 定义线性效用函数。(b) 写出用极大似然法估计它们时的对数似然函数。
:::

:::{dropdown} 解答
:class-container: solution
:animate: fade-in

**(a) 效用。** 时间和费用是两种方式都有的属性，采用通用系数（generic coefficient）；月薪不随方式变化，因此只能与一个常数一起进入其中一个效用：

$$
\begin{aligned}
V_A^n &= \beta_0 + \beta_t\,t_A^n + \beta_c\,c_A^n + \beta_s\,s^n, \\
V_B^n &= \beta_t\,t_B^n + \beta_c\,c_B^n .
\end{aligned}
$$

**(b) 对数似然函数。** 对二项 Logit，$P_A^n = 1/[1 + \exp(V_B^n - V_A^n)]$，$P_B^n = 1 - P_A^n$，其中

$$
V_A^n - V_B^n = \beta_0 + \beta_t\left(t_A^n - t_B^n\right) + \beta_c\left(c_A^n - c_B^n\right) + \beta_s s^n .
$$

受访者 1–2 的差值为 $(t_A - t_B, c_A - c_B) = (-5, 0.8)$，受访者 3–4 为 $(-15, 3.2)$，受访者 5–6 为 $(-10, 2.1)$。观测到的选择依次为 B、A、B、A、B、A，因此

$$
\begin{aligned}
LL(\beta_0, \beta_t, \beta_c, \beta_s)
&= \ln P_B^1 + \ln P_A^2 + \ln P_B^3 + \ln P_A^4 + \ln P_B^5 + \ln P_A^6 \\
&= -\ln\left(1 + e^{\beta_0 - 5\beta_t + 0.8\beta_c + 3.0\beta_s}\right)
   - \ln\left(1 + e^{-\beta_0 + 5\beta_t - 0.8\beta_c - 4.0\beta_s}\right) \\
&\quad - \ln\left(1 + e^{\beta_0 - 15\beta_t + 3.2\beta_c + 3.5\beta_s}\right)
   - \ln\left(1 + e^{-\beta_0 + 15\beta_t - 3.2\beta_c - 6.0\beta_s}\right) \\
&\quad - \ln\left(1 + e^{\beta_0 - 10\beta_t + 2.1\beta_c + 4.5\beta_s}\right)
   - \ln\left(1 + e^{-\beta_0 + 10\beta_t - 2.1\beta_c - 6.5\beta_s}\right).
\end{aligned}
$$

**能否求出最大值？** 用这些数据不能。在每对受访者中，属性完全相同，而收入较高者选择 A，因此存在某个参数向量能将六个选择全部正确分类——例如 $(\beta_0, \beta_t, \beta_c, \beta_s) = (-10.43, 0, -2.86, 3.43)$ 使受访者 1、3、5 的 $V_A - V_B$ 为负，而 2、4、6 的为正。将这样的向量乘以越来越大的因子，会使每个观测选择的概率趋向于一，$LL$ 趋向于 0，因此最大值无法达到（**完全分离**，perfect separation）。估计需要更多、更多样化的回答——在 SP 实践中，每位受访者要回答多个选择任务——或者减少参数个数。
:::
