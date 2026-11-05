# 符号说明

下列符号在全书中统一使用。各章特有的符号在每章开头的符号说明表中定义。

## 主要符号

几乎每一章都会出现的十个符号：

| 符号 | 含义 | 首次出现 |
|---|---|---|
| $i, j$ | 起点小区和终点小区，$i, j = 1, \ldots, z$ | {doc}`04-biproportional-fitting` |
| $O_i$, $D_j$ | 小区 $i$ 产生（起始于小区 $i$）的出行量和小区 $j$ 吸引（终止于小区 $j$）的出行量 | {doc}`04-biproportional-fitting` |
| $T_{ij}$ | 从小区 $i$ 到小区 $j$ 的出行量（出行矩阵元素） | {doc}`04-biproportional-fitting` |
| $c_{ij}$ | 从 $i$ 到 $j$ 的广义出行费用 | {doc}`04-biproportional-fitting` |
| $G = (N, A)$ | 节点集为 $N$、路段集为 $A$ 的有向网络 | {doc}`06-zoning-and-networks` |
| $x_a$, $t_a(x_a)$ | 路段 $a$ 上的流量及其行程时间（路段阻抗函数） | {doc}`06-zoning-and-networks` |
| $q_{rs}$ | 从起点 $r$ 到终点 $s$ 的出行需求 | {doc}`13-user-equilibrium-assignment` |
| $f_k^{rs}$, $c_k^{rs}$ | $r$ 与 $s$ 之间路径 $k$ 上的流量和行程时间 | {doc}`13-user-equilibrium-assignment` |
| $\delta_{a,k}^{rs}$ | 路段–路径关联：若路段 $a$ 位于 O-D 对 $rs$ 的路径 $k$ 上则为 1 | {doc}`13-user-equilibrium-assignment` |
| $U_{in} = V_{in} + \varepsilon_{in}$ | 出行者 $n$ 对方案 $i$ 的随机效用 | {doc}`11-discrete-choice-models` |

以下各节按主题列出符号。

## 一般约定

| 约定 | 含义 | 首次出现 |
|---|---|---|
| $x$, $\bx$, $\bX$ | 标量用斜体；向量用粗体小写；矩阵用粗体大写 | {doc}`02-regression-and-hypothesis-tests` |
| $\bx\T$ | 转置 | {doc}`02-regression-and-hypothesis-tests` |
| $\R^n$ | $n$ 维实空间 | {doc}`02-regression-and-hypothesis-tests` |
| $\E[\cdot]$, $\Var[\cdot]$, $\Cov[\cdot,\cdot]$ | 期望、方差、协方差 | {doc}`01-probability-distributions` |
| $\Prob(\cdot)$, $\Pr(\cdot)$ | （总体中的）概率 | {doc}`01-probability-distributions` |
| $f(\cdot)$ | 密度函数，或样本中的概率（{doc}`07-travel-surveys-and-sampling`） | {doc}`01-probability-distributions` |
| $\mathcal{N}(\mu, \sigma^2)$ | 均值为 $\mu$、**方差**为 $\sigma^2$ 的正态分布 | {doc}`01-probability-distributions` |
| $\Phi(\cdot)$ | 标准正态分布函数 | {doc}`01-probability-distributions` |
| $\hat\theta$ | 参数 $\theta$ 的估计值 | {doc}`02-regression-and-hypothesis-tests` |
| $\mathbb{1}[\cdot]$ | 示性函数 | {doc}`17-examples-probability` |

## 空间与需求

| 符号 | 含义 | 首次出现 |
|---|---|---|
| $i, j$; $z$ | 起点小区和终点小区；小区数 | {doc}`04-biproportional-fitting` |
| $O_i$, $D_j$ | 小区 $i$ 产生 / 起始于小区 $i$ 的出行量；小区 $j$ 吸引 / 终止于小区 $j$ 的出行量 | {doc}`04-biproportional-fitting` |
| $T_{ij}$, $T$ | 从 $i$ 到 $j$ 的出行量；总出行量 | {doc}`04-biproportional-fitting` |
| $T_{ij}^k$ | 使用交通方式 $k$ 从 $i$ 到 $j$ 的出行量 | {doc}`12-aggregate-modal-split` |
| $c_{ij}$ | 从 $i$ 到 $j$ 的广义费用 | {doc}`04-biproportional-fitting` |
| $f(c_{ij})$ | 重力模型的阻抗函数 | {doc}`10-trip-distribution` |
| $\tau$, $\tau_i$, $\Gamma_j$ | 总体增长系数、起点增长系数和终点增长系数 | {doc}`10-trip-distribution` |
| $t_{ij}$ | 双比例拟合中的种子矩阵（先验矩阵或基年矩阵） | {doc}`04-biproportional-fitting` |
| $a_i$, $b_j$; $A_i$, $B_j$ | 双比例模型和重力模型的平衡系数 | {doc}`04-biproportional-fitting` |
| $W\{T_{ij}\}$ | 产生矩阵 $\{T_{ij}\}$ 的微观状态数（熵最大化） | {doc}`04-biproportional-fitting` |
| $E$, $L$, $F$ | 需求–供给框架中的活动系统、服务水平和流量 | {doc}`05-transportation-planning-process` |

## 网络与交通分配

| 符号 | 含义 | 首次出现 |
|---|---|---|
| $G = (N, A)$ | 有向网络：节点集 $N$，路段集 $A$ | {doc}`06-zoning-and-networks` |
| $a \in A$ | 一条路段 | {doc}`06-zoning-and-networks` |
| $x_a$, $\bx$ | 路段 $a$ 上的流量；路段流量向量 | {doc}`06-zoning-and-networks` |
| $t_a(x_a)$ | 路段阻抗（行程时间）函数 | {doc}`06-zoning-and-networks` |
| $t_a^0$, $c_a$ | 路段 $a$ 的自由流行程时间和通行能力 | {doc}`06-zoning-and-networks` |
| $r, s$; $q_{rs}$ | 起点节点和终点节点；二者之间的需求 | {doc}`13-user-equilibrium-assignment` |
| $K_{rs}$ | 从 $r$ 到 $s$ 的路径集合 | {doc}`13-user-equilibrium-assignment` |
| $f_k^{rs}$, $c_k^{rs}$ | 路径 $k \in K_{rs}$ 上的流量和行程时间 | {doc}`13-user-equilibrium-assignment` |
| $\delta_{a,k}^{rs}$ | 若路段 $a$ 位于 O-D 对 $rs$ 的路径 $k$ 上则为 1，否则为 0 | {doc}`13-user-equilibrium-assignment` |
| $u_{rs}$ | $r$ 与 $s$ 之间的最小（均衡）行程时间 | {doc}`13-user-equilibrium-assignment` |
| $\by$ | 辅助路段流量（全有全无分配或随机加载） | {doc}`13-user-equilibrium-assignment` |
| $\tilde t_a(x_a)$ | 边际成本 $t_a + x_at_a'(x_a)$（系统最优） | {doc}`14-system-optimum-and-elastic-demand` |
| $\tau_a$ | 以时间单位计的路段收费（不要与增长系数 $\tau_i$ 混淆） | {doc}`14-system-optimum-and-elastic-demand` |
| $e_{rs}$, $\bar q_{rs}$ | 超额需求和需求上界（弹性需求） | {doc}`14-system-optimum-and-elastic-demand` |
| $\theta$ | Logit 路径选择的离散参数（随机用户均衡） | {doc}`15-stochastic-user-equilibrium` |
| $s$, $t^*$ | 瓶颈通行能力和期望到达时刻（动态模型） | {doc}`16-dynamic-assignment-and-simulation` |

## 选择模型

| 符号 | 含义 | 首次出现 |
|---|---|---|
| $C_n$ | 决策者 $n$ 的选择集 | {doc}`11-discrete-choice-models` |
| $U_{in} = V_{in} + \varepsilon_{in}$ | $n$ 对方案 $i$ 的效用：系统项加随机项 | {doc}`11-discrete-choice-models` |
| $P_n(i)$ | $n$ 选择 $i$ 的概率 | {doc}`11-discrete-choice-models` |
| $\mu$ | 耿贝尔随机项和逻辑斯谛随机项的尺度参数 | {doc}`01-probability-distributions` |
| $\btheta$, $\bbeta$ | 选择模型或回归模型的参数 | {doc}`02-regression-and-hypothesis-tests` |

## 统计

| 符号 | 含义 | 首次出现 |
|---|---|---|
| $N$, $n$ | 总体规模和样本量 | {doc}`07-travel-surveys-and-sampling` |
| $\bar{x}$, $s^2$ | 样本均值和样本方差 | {doc}`02-regression-and-hypothesis-tests` |
| $\mathrm{CV}$ | 变异系数 $\sigma/\mu$ | {doc}`07-travel-surveys-and-sampling` |
| $z_{\alpha}$, $t_{\alpha,\nu}$ | 标准正态分布和 $t(\nu)$ 分布的上 $\alpha$ 分位数 | {doc}`02-regression-and-hypothesis-tests` |
| $\mathit{SS}_T$, $\mathit{SS}_R$, $\mathit{SS}_E$ | 总平方和、回归平方和与误差平方和 | {doc}`02-regression-and-hypothesis-tests` |
| $R^2$, $\bar{R}^2$, $R_0^2$ | 决定系数、调整决定系数和非中心化决定系数 | {doc}`02-regression-and-hypothesis-tests` |
| $e_x$ | 测量量 $x$ 的误差（标准差） | {doc}`08-errors-and-uncertainty` |
| $e_s$, $e_m$ | 模型的设定误差和传播的测量误差 | {doc}`08-errors-and-uncertainty` |
| $w_Y$ | 基于选择的抽样中层 $Y$ 的权重（WESML） | {doc}`07-travel-surveys-and-sampling` |

## 最优化

| 符号 | 含义 | 首次出现 |
|---|---|---|
| $f(\bx)$, $\Omega$ | 目标函数和可行集 | {doc}`03-nonlinear-optimization` |
| $\nabla f$, $\nabla^2 f$ | 梯度和 Hessian 矩阵 | {doc}`03-nonlinear-optimization` |
| $g_i \le 0$, $h_j = 0$ | 不等式约束和等式约束 | {doc}`03-nonlinear-optimization` |
| $u_i$, $\lambda_j$ | KKT 乘子 | {doc}`03-nonlinear-optimization` |
| $\mathcal{L}$ | 拉格朗日函数（在选择模型各章中表示似然函数） | {doc}`03-nonlinear-optimization` |
| $\alpha$ | 步长 | {doc}`03-nonlinear-optimization` |
