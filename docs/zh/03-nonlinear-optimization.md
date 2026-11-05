# 网络分析中的非线性最优化

## 概述

交通分配的均衡模型（{doc}`13-user-equilibrium-assignment`）、矩阵平衡与熵最大化（{doc}`04-biproportional-fitting`），以及建立在它们之上的出行分布模型（{doc}`10-trip-distribution`），都是通过表述为凸优化问题来求解的。本章汇集这些章节所需的最优化理论：凸集与凸函数、Karush–Kuhn–Tucker（KKT）最优性条件、一维线搜索、求解线性约束问题的 Frank–Wolfe 算法，以及使 Frank–Wolfe 算法成为实用分配方法的最短路径算法。

:::{admonition} 学习目标
:class: objectives
学完本章后，读者应能够：

- 计算梯度和黑塞矩阵，并检验函数的凸性；
- 区分局部极小和全局极小，并解释为什么凸规划不存在虚假的局部极小；
- 写出并验证约束问题的 KKT 条件；
- 执行二分法和牛顿法线搜索；
- 执行 Frank–Wolfe 算法，并将其终止准则解释为最优性间隙；
- 用标号修正算法求最短路径。
:::

## 符号说明

| 符号 | 含义 |
|---|---|
| $\bx = (x_1, \ldots, x_n)\T$ | 决策变量向量 |
| $f(\bx)$ | 目标函数 |
| $\Omega \subseteq \R^n$ | 可行域 |
| $\nabla f(\bx)$, $\nabla^2 f(\bx)$ | 梯度向量和黑塞矩阵 |
| $g_i(\bx) \le 0$, $h_j(\bx) = 0$ | 不等式约束和等式约束 |
| $u_i$, $\lambda_j$ | 拉格朗日（KKT）乘子 |
| $\alpha$ | 线搜索中的步长 |

## 最优化问题

（非线性）规划问题要求在满足约束的条件下，求使目标函数最小的决策变量值：

$$
\begin{aligned}
\min_{\bx}\quad & f(\bx) \\
\text{s.t.}\quad & g_i(\bx) \le 0, \qquad i = 1, \ldots, m_1, \\
& h_j(\bx) = 0, \qquad j = 1, \ldots, m_2 .
\end{aligned}
$$ (eq-03-nlp)

记**可行域**（feasible set）为 $\Omega = \{\bx : g_i(\bx) \le 0\ \forall i,\ h_j(\bx) = 0\ \forall j\}$，则问题为 $\min_{\bx \in \Omega} f(\bx)$。最大化 $f$ 等价于最小化 $-f$。

:::{prf:definition} 全局极小与局部极小
:label: def-03-minimum

若对每个 $\bx \in \Omega$ 都有 $f(\bx) \ge f(\bx^*)$，则点 $\bx^* \in \Omega$ 是**全局极小点**；若对 $\bx^*$ 某邻域内的每个 $\bx \in \Omega$ 都有 $f(\bx) \ge f(\bx^*)$，则它是**局部极小点**。
:::

一个函数可以有多个局部极小点；在有界可行域上，全局极小点可能位于边界上，而不是在驻点处。

## 梯度、黑塞矩阵与凸性

### 梯度与黑塞矩阵

对可微函数 $f: \R^n \to \R$，其在 $\bx$ 处的**梯度**（gradient）和**黑塞矩阵**（Hessian）为

$$
\nabla f(\bx) = \begin{bmatrix}
\partial f/\partial x_1 \\ \vdots \\ \partial f/\partial x_n
\end{bmatrix},
\qquad
\nabla^2 f(\bx) = \left[\frac{\partial^2 f}{\partial x_i\,\partial x_j}\right]_{n\times n}.
$$

例如，$f_1(\bx) = (x_1 - 2)^2 + (x_2 - 2)^2$ 的梯度为 $\nabla f_1 = (2(x_1 - 2),\ 2(x_2 - 2))\T$，黑塞矩阵为 $\nabla^2 f_1 = \diag(2, 2)$；而线性函数 $f_2(\bx) = 2x_1 + 3x_2 + 0.5x_3 - x_4$ 的梯度为常向量 $(2, 3, 0.5, -1)\T$，黑塞矩阵为零。

### 凸集与凸函数

:::{prf:definition} 凸集
:label: def-03-convex-set

若对所有 $\bx_1, \bx_2 \in \Omega$ 和所有 $\alpha \in [0, 1]$ 都有 $\bx_1 + \alpha(\bx_2 - \bx_1) \in \Omega$，即集合中任意两点间的线段都在集合内，则称集合 $\Omega \subseteq \R^n$ 为**凸集**（convex set）。
:::

多面体 $\{\bx : \bA\bx \le \bb\}$ 和圆盘都是凸集。描述网络流量守恒的线性约束所定义的集合是多面体，因而是凸集。

:::{prf:definition} 凸函数与严格凸函数
:label: def-03-convex-function

若对所有 $\bx_1, \bx_2 \in \Omega$ 和所有 $\alpha \in [0, 1]$ 都有

$$
f\big(\bx_1 + \alpha(\bx_2 - \bx_1)\big) \le f(\bx_1) + \alpha\big[f(\bx_2) - f(\bx_1)\big],
$$

则称函数 $f$ 在凸集 $\Omega$ 上是**凸函数**（convex function）；若当 $\bx_1 \ne \bx_2$ 且 $\alpha \in (0, 1)$ 时不等式严格成立，则称其为**严格凸函数**。几何上，函数图像上任意两点间的弦位于图像上方。
:::

对二阶可微函数，可以用黑塞矩阵检验凸性。

:::{prf:theorem} 凸性的二阶判别法
:label: thm-03-convexity-test

设 $f$ 在开凸集 $\Omega$ 上二阶连续可微。

1. $f$ 在 $\Omega$ 上为凸函数，当且仅当对每个 $\bx \in \Omega$，$\nabla^2 f(\bx)$ 半正定。
2. 若对每个 $\bx \in \Omega$，$\nabla^2 f(\bx)$ 正定，则 $f$ 在 $\Omega$ 上严格凸。
:::

第二条只是*充分*条件：$f(x) = x^4$ 是严格凸的，但 $f''(0) = 0$。在上面的例子中，$f_1$ 严格凸（其黑塞矩阵正定），而 $f_2$ 是凸的但不是严格凸的；任何线性函数既是凸函数也是凹函数。

若对所有 $\bd \ne \bzero$ 都有 $\bd\T\bH\bd > 0$，则称对称矩阵 $\bH$ **正定**（positive definite）；若 $\bd\T\bH\bd \ge 0$，则称其**半正定**（positive semidefinite）。等价的判别方法有：

- $\bH$ 的所有特征值都为正（正定）或非负（半正定）；
- （Sylvester 判据）$\bH$ 的所有顺序主子式都为正——该判据适用于判别正定性；判别半正定性时，必须*所有*主子式（而不仅是顺序主子式）都非负。

对角元均为正的对角矩阵是正定的。交通分配中出现的正是这种简单情形：当每条路段的行程时间只取决于该路段自身的流量时，Beckmann 目标函数的黑塞矩阵是对角矩阵。

### 凸规划

:::{prf:definition} 凸规划
:label: def-03-convex-program

若可行域 $\Omega$ 是凸集，且目标函数 $f$ 在 $\Omega$ 上是凸函数，则问题 {eq}`eq-03-nlp` 是**凸规划**（convex program）。特别地，若每个 $g_i$ 都是凸函数、每个 $h_j$ 都是仿射函数（线性函数加常数），则上述条件成立。
:::

:::{prf:theorem} 凸规划的最优性
:label: thm-03-convex-program

1. 凸规划的每个局部极小点都是全局极小点。
2. 若目标函数严格凸，则全局极小点（若存在）唯一。
:::

这两个事实解释了为什么要把交通均衡表述为凸规划：任何找到局部极小点的算法都找到了*那个*均衡，而严格凸性意味着均衡路段流量唯一。

## Karush–Kuhn–Tucker 条件

定义 {eq}`eq-03-nlp` 的**拉格朗日函数**（Lagrangian）

$$
\begin{aligned}
\mathcal{L}(\bx, \bu, \blambda) &= f(\bx) + \sum_{i=1}^{m_1} u_i\, g_i(\bx) + \sum_{j=1}^{m_2}\lambda_j\, h_j(\bx).
\end{aligned}
$$

:::{prf:theorem} Karush–Kuhn–Tucker 条件
:label: thm-03-kkt

若 $\bx^*$ 是 {eq}`eq-03-nlp` 的局部极小点，且在 $\bx^*$ 处满足约束规范，则存在乘子 $u_1, \ldots, u_{m_1}$ 和 $\lambda_1, \ldots, \lambda_{m_2}$，使得

$$
\begin{aligned}
&\nabla f(\bx^*) + \sum_{i=1}^{m_1} u_i\nabla g_i(\bx^*)
   + \sum_{j=1}^{m_2}\lambda_j\nabla h_j(\bx^*) = \bzero
   && \text{（平稳性）} \\
&u_i \ge 0, \quad i = 1, \ldots, m_1
   && \text{（对偶可行性）} \\
&u_i\, g_i(\bx^*) = 0, \quad i = 1, \ldots, m_1
   && \text{（互补松弛性）} \\
&g_i(\bx^*) \le 0, \quad i = 1, \ldots, m_1
   && \text{（原始可行性）} \\
&h_j(\bx^*) = 0, \quad j = 1, \ldots, m_2
   && \text{（原始可行性）}
\end{aligned}
$$

对凸规划，KKT 条件也是**充分**的：满足这些条件的任何点都是全局极小点。
:::

互补松弛条件（complementary slackness）表明，只有当约束起作用（取等号）时，相应的乘子才可能为正。乘子 $u_i$ 是约束 $i$ 放松时最优目标值下降的速率，即近似为每放松一个单位所带来的改善量。常用的约束规范有：起作用约束的梯度线性无关，或者——对凸规划——Slater 条件（存在严格可行点）。线性约束总是满足约束规范，本书中的所有网络问题都属于这种情形。

对含非负约束 $x_i \ge 0$ 的问题，将其写成 $-x_i \le 0$、对应乘子 $u_i$，再消去 $u_i$，即得到交通分配中反复使用的紧凑形式：

$$
\begin{aligned}
x_i^*\,\frac{\partial \mathcal{L}}{\partial x_i} &= 0, \\
\frac{\partial \mathcal{L}}{\partial x_i} &\ge 0, \\
x_i^* &\ge 0,
\end{aligned}
$$ (eq-03-kkt-nonneg)

其中 $\mathcal{L}$ 只包含其余约束。用文字表述：在最优点，取正值的变量的约化梯度为零，取零值的变量的约化梯度非负。

## 线搜索方法

许多算法把多维问题化为一系列一维问题 $\min_{a \le x \le b} z(x)$，即**线搜索**（line search）。若 $z$ 是凸的且可微，则极小点位于 $z'(x) = 0$ 处或区间端点。

### 二分法

:::{prf:algorithm} 二分法线搜索
:label: alg-03-bisection

**输入：** $[a, b]$ 上满足 $z'(a) < 0 < z'(b)$ 的凸函数 $z$，以及容差 $\epsilon > 0$。

1. 令 $a_0 = a$，$b_0 = b$，$k = 0$。
2. 若 $b_k - a_k \le \epsilon$，停止：$x^* \approx (a_k + b_k)/2$。
3. 令 $x_k = (a_k + b_k)/2$，计算 $z'(x_k)$。
   - 若 $z'(x_k) > 0$，令 $a_{k+1} = a_k$，$b_{k+1} = x_k$。
   - 若 $z'(x_k) < 0$，令 $a_{k+1} = x_k$，$b_{k+1} = b_k$。
   - 若 $z'(x_k) = 0$，停止：$x^* = x_k$。
4. 令 $k \leftarrow k + 1$，返回第 2 步。
:::

每次迭代区间长度减半，因此 $b_k - a_k = (b - a)/2^{k}$，约需 $\log_2[(b - a)/\epsilon]$ 次迭代。二分法只用到导数的符号，总能收敛，但速度较慢。

### 牛顿法

:::{prf:algorithm} 求解 $z'(x) = 0$ 的牛顿法
:label: alg-03-newton

**输入：** 二阶可微函数 $z$、初始点 $x_0$ 和容差 $\epsilon > 0$。

1. 令 $k = 0$。
2. 若 $\lvert z'(x_k)\rvert \le \epsilon$，停止。
3. 令 $x_{k+1} = x_k - z'(x_k)/z''(x_k)$。
4. 令 $k \leftarrow k + 1$，返回第 2 步。
:::

每一步都最小化二次近似 $z(x_k) + z'(x_k)(x - x_k) + \tfrac{1}{2}z''(x_k)(x - x_k)^2$。若 $z''(x^*) \ne 0$ 且 $x_0$ 足够接近 $x^*$，则收敛是二次的：每次迭代正确数字的位数大约翻倍。然而，牛顿法是求*驻点*的方法：远离解时它可能发散、跳出可行区间，或者在 $z''(x_k) < 0$ 时收敛到极大点（{prf:ref}`ex-19-newton`）。实际应用中需要加保护措施，例如在必要时退回到二分法。

## Frank–Wolfe 算法

考虑具有**线性**约束的凸规划

$$
\min_{\bx \in \Omega} f(\bx),
\qquad
\Omega = \{\bx : \bA\bx \le \bb\}
$$ (eq-03-fw-problem)

（也可以含等式约束）。**Frank–Wolfe 算法**（又称条件梯度法）在当前点用 $f$ 的线性近似代替 $f$，在 $\Omega$ 上最小化这个线性函数——这是一个线性规划——然后向其解移动。

:::{prf:algorithm} Frank–Wolfe 算法
:label: alg-03-frank-wolfe

**输入：** 可微凸函数 $f$、多面体可行域 $\Omega$、可行初始点 $\bx^{(0)}$ 和容差 $\epsilon > 0$。

1. **寻找方向。** 求解线性规划 $\by^{(k)} \in \argmin_{\by \in \Omega}\ \nabla f(\bx^{(k)})\T\by$，并令下降方向为 $\bd^{(k)} = \by^{(k)} - \bx^{(k)}$。
2. **收敛检验。** 若 $-\nabla f(\bx^{(k)})\T(\by^{(k)} - \bx^{(k)}) \le \epsilon$，停止。
3. **线搜索。** 求 $\alpha_k \in \argmin_{0 \le \alpha \le 1} f\big(\bx^{(k)} + \alpha\,\bd^{(k)}\big)$，例如用二分法。
4. **更新。** 令 $\bx^{(k+1)} = \bx^{(k)} + \alpha_k\bd^{(k)}$，$k \leftarrow k + 1$，返回第 1 步。
:::

每个迭代点都是可行点的凸组合，因此无需任何投影即保持可行。第 2 步中的量有一个有用的解释。由凸性，$f(\bx^*) \ge f(\bx^{(k)}) + \nabla f(\bx^{(k)})\T(\bx^* - \bx^{(k)})$；又因为 $\by^{(k)}$ 在 $\Omega$ 上最小化线性项，所以

$$
f(\bx^{(k)}) - f(\bx^*)
\ \le\ -\nabla f(\bx^{(k)})\T\big(\by^{(k)} - \bx^{(k)}\big)
\ =:\ \mathrm{gap}^{(k)} .
$$ (eq-03-fw-gap)

因此，**间隙**（gap）是当前目标值与最优值之差的上界，$f(\bx^{(k)}) - \mathrm{gap}^{(k)}$ 是 $f(\bx^*)$ 的下界。间隙非负，且恰在最优解处为零。

Frank–Wolfe 算法在交通分配中很有吸引力，因为第 1 步的线性规划可以分解为若干最短路径问题——即一次**全有全无分配**（all-or-nothing assignment）——而线搜索是一维的。它的收敛是次线性的（间隙大约按 $1/k$ 减小），因此人们发展了许多改进算法（共轭 Frank–Wolfe 算法、基于路径和基于丛的算法）。

## 最短路径

在交通分配中，Frank–Wolfe 算法的第 1 步需要求出每个起点到每个终点的**最短路径**（shortest path）。**标号修正算法**（label-correcting algorithm）在路段费用 $t_{ij}$ 非负的网络中，计算从一个根节点 $r$ 到所有其他节点的最短路径。每个节点 $i$ 带有一个**标号** $l_i$（迄今找到的从 $r$ 到 $i$ 的最佳路径长度）和一个**前驱** $p_i$（该路径上 $i$ 之前的节点）。

:::{prf:algorithm} 标号修正最短路径算法
:label: alg-03-label-correcting

1. 令 $l_r = 0$，对 $i \ne r$ 令 $l_i = \infty$，对所有 $i$ 令 $p_i = 0$，并将 $r$ 放入序列表 $Q$。
2. 若 $Q$ 为空，停止；否则从 $Q$ 中取出一个节点 $i$。
3. 对从 $i$ 出发的每条路段 $(i, j)$：若 $l_i + t_{ij} < l_j$，令 $l_j \leftarrow l_i + t_{ij}$，$p_j \leftarrow i$，并在 $j$ 不在 $Q$ 中时将其加入 $Q$。
4. 返回第 2 步。
:::

算法终止时，$l_j$ 就是从 $r$ 到 $j$ 的最短路径长度，路径可沿前驱 $p_j, p_{p_j}, \ldots, r$ 反向读出；所有节点的前驱构成 $r$ 的**最短路径树**。若第 2 步每次取出的都是标号最小的节点，则每个节点只被取出一次，此时该方法就是 **Dijkstra（标号设定）算法**，它要求费用非负（{prf:ref}`ex-19-shortest-path`）。

## 求解器

小规模问题可以用电子表格求解器（Excel Solver）和 `scipy.optimize` 等通用程序库求解；建模语言（AMPL、Pyomo、JuMP）和商业求解器（CPLEX、Gurobi、MATLAB 优化工具箱、LINDO）可处理大规模线性、整数和二次规划。实际网络上的交通分配由规划软件（PTV Visum、TransCAD、Emme、AequilibraE）中实现的专门算法求解。第五部分从零实现了本章的算法（{doc}`32-python-foundations`）。

## 本章回顾

### 小结

- 二阶可微函数的凸性可用其黑塞矩阵检验（{prf:ref}`thm-03-convexity-test`）；凸规划不存在虚假的局部极小点，严格凸的目标函数给出唯一解（{prf:ref}`thm-03-convex-program`）。
- 在满足约束规范时，KKT 条件（平稳性、对偶可行性、互补松弛性、原始可行性）刻画了最优点，对凸规划也是充分条件（{prf:ref}`thm-03-kkt`）；对非负变量，其形式为 {eq}`eq-03-kkt-nonneg`。
- 二分法（{prf:ref}`alg-03-bisection`）稳健但较慢；牛顿法（{prf:ref}`alg-03-newton`）在解附近收敛很快，但需要保护措施。
- Frank–Wolfe 算法（{prf:ref}`alg-03-frank-wolfe`）通过一系列线性规划和线搜索求解线性约束的凸规划；其间隙 {eq}`eq-03-fw-gap` 给出了目标值误差的上界。
- 标号修正算法和 Dijkstra 算法（{prf:ref}`alg-03-label-correcting`）计算最短路径树。

### 常见错误

- **认为严格凸函数的黑塞矩阵必定正定。** 正定只是充分条件，而非必要条件：$x^4$ 严格凸，但 $f''(0) = 0$。
- **用顺序主子式判别*半*正定性。** 顺序主子式只能判别正定性；判别半正定性必须检查所有主子式或特征值。
- **检验 KKT 条件时遗漏符号条件 $u_i \ge 0$ 或互补松弛条件。** 极大点和鞍点同样满足平稳性条件；四组条件缺一不可。
- **对非凸函数不加保护地使用牛顿法。** 牛顿法求的是驻点，可能走向极大点或跳出区间；某一步失败时应退回到二分法。
- **以相邻迭代点接近作为 Frank–Wolfe 算法的终止条件。** Frank–Wolfe 算法在远离最优点时也可能步长很小；应在间隙 {eq}`eq-03-fw-gap` 足够小时终止。

## 参考文献

- Sheffi, Y. (1985). *Urban Transportation Networks: Equilibrium Analysis
  with Mathematical Programming Methods*, Chapters 2, 4, and 5.
  Prentice-Hall. (Freely available from the author's MIT web page.)
- Bazaraa, M. S., Sherali, H. D., & Shetty, C. M. (2006). *Nonlinear
  Programming: Theory and Algorithms* (3rd ed.), Chapters 2–5, 8, and 10.
  Wiley.
- Frank, M., & Wolfe, P. (1956). An algorithm for quadratic programming.
  *Naval Research Logistics Quarterly*, *3*(1–2), 95–110.
  <https://doi.org/10.1002/nav.3800030109>
- Karush, W. (1939). *Minima of functions of several variables with
  inequalities as side constraints* [Master's thesis, University of
  Chicago].
- Kuhn, H. W., & Tucker, A. W. (1951). Nonlinear programming. In
  *Proceedings of the Second Berkeley Symposium on Mathematical Statistics
  and Probability* (pp. 481–492). University of California Press.
- Dijkstra, E. W. (1959). A note on two problems in connexion with graphs.
  *Numerische Mathematik*, *1*, 269–271. <https://doi.org/10.1007/BF01386390>
