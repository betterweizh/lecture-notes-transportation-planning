# 术语表

本书使用的中英文术语对照。中文版在每章首次出现某术语时，会在括号中给出其英文名称。


## 概率与统计

| 中文 | English | 符号 / 说明 |
|---|---|---|
| 随机变量 | random variable | $X$ |
| 累积分布函数 | cumulative distribution function (CDF) | $F$ |
| 概率密度函数 | probability density function (PDF) | $f$ |
| 期望 / 方差 / 协方差 | expectation / variance / covariance | $\E$, $\Var$, $\Cov$ |
| 均匀分布 / 正态分布 | uniform / normal distribution | $\mathcal{N}(\mu, \sigma^2)$ |
| 标准正态分布函数 | standard normal CDF | $\Phi$ |
| 耿贝尔分布（第一类极值分布） | Gumbel (extreme value type I) distribution | $\mathrm{Gumbel}(\eta, \mu)$ |
| 逻辑斯谛分布 | logistic distribution |  |
| 位置参数 / 尺度参数 | location / scale parameter | $\eta$, $\mu$ |
| 二元 / 多元正态分布 | bivariate / multivariate normal distribution | $\rho$, $\bSigma$ |
| 线性回归 / 最小二乘法 | linear regression / least squares | $\hat\bbeta$ |
| 正规方程 | normal equations |  |
| 残差 | residual | $e_i$ |
| 总平方和 / 回归平方和 / 残差平方和 | total / regression / error sum of squares | $\mathit{SS}_T$, $\mathit{SS}_R$, $\mathit{SS}_E$ |
| 决定系数；调整 / 非中心化 | coefficient of determination; adjusted / uncentered | $R^2$, $\bar R^2$, $R_0^2$ |
| 假设检验；原假设 | hypothesis test; null hypothesis | $H_0$ |
| 显著性水平；$p$ 值 | significance level; $p$-value | $\alpha$ |
| 置信区间；自由度 | confidence interval; degrees of freedom | $\nu$ |
| 虚拟变量（哑变量） | dummy variable |  |
| 极大似然估计；对数似然 | maximum likelihood estimation; log-likelihood | $LL(\bbeta)$ |

## 最优化与矩阵平衡

| 中文 | English | 符号 / 说明 |
|---|---|---|
| 目标函数 / 可行域 | objective function / feasible set | $f$, $\Omega$ |
| 凸集 / 凸函数 | convex set / convex function |  |
| 梯度 / 黑塞矩阵 | gradient / Hessian matrix | $\nabla f$, $\nabla^2 f$ |
| 拉格朗日函数；拉格朗日乘子 | Lagrangian; Lagrange multiplier | $\mathcal{L}$, $\lambda$ |
| KKT 条件（卡罗需–库恩–塔克条件） | Karush–Kuhn–Tucker (KKT) conditions |  |
| 互补松弛条件 | complementary slackness |  |
| 线搜索；二分法；黄金分割法 | line search; bisection; golden-section search |  |
| Frank–Wolfe 算法（凸组合法） | Frank–Wolfe algorithm (convex combinations method) |  |
| 最短路径；Dijkstra 算法 | shortest path; Dijkstra's algorithm |  |
| 种子矩阵（先验矩阵） | seed (prior) matrix | $t_{ij}$ |
| 双比例拟合（迭代比例拟合、RAS 法） | bi-proportional fitting (iterative proportional fitting, RAS method) | $a_i$, $b_j$ |
| 平衡系数 | balancing factor | $A_i$, $B_j$ |
| 交叉乘积比 | cross-product ratio |  |
| 熵最大化（最大熵方法） | entropy maximization | $W\{T_{ij}\}$ |
| 微观状态 / 中观状态 / 宏观状态 | micro-state / meso-state / macro-state |  |
| 信息距离（KL 散度） | information distance (Kullback–Leibler divergence) | $I(\bT, \bt)$ |
| 三比例拟合；多维比例加权（raking） | tri-proportional fitting; raking | $F_k$ |

## 交通规划与数据

| 中文 | English | 符号 / 说明 |
|---|---|---|
| 交通规划过程 | transportation planning process |  |
| 四阶段法 | four-step model |  |
| 出行需求；服务水平 | travel demand; level of service | $F$, $L$ |
| 活动系统；交通系统 | activity system; transport system | $E$, $T$ |
| 需求–性能均衡（供需均衡） | demand–performance equilibrium | $(F^*, L^*)$ |
| 交通小区；交通小区划分 | traffic analysis zone; zoning system |  |
| 小区形心；形心连杆 | centroid; centroid connector |  |
| 外部小区；境界线；核查线 | external zone; cordon; screen line |  |
| 节点；路段；有向图（网络） | node; link; directed graph (network) | $G = (N, A)$ |
| 路段阻抗函数（路段行程时间函数） | link performance (travel time) function | $t_a(x_a)$ |
| BPR 函数 | BPR function |  |
| 通行能力；自由流行程时间 | capacity; free-flow travel time | $c_a$, $t_a^0$ |
| 饱和流率；绿灯时间；信号周期 | saturation flow; green time; cycle length | $s$, $g$, $C$ |
| 交叉口；转向交通 | junction (intersection); turning movement |  |
| 居民出行调查；路边询问调查 | household (travel) survey; roadside interview |  |
| 显示性偏好（RP）/ 陈述性偏好（SP） | revealed / stated preference |  |
| 简单随机抽样 / 分层抽样 / 基于选择的抽样 | simple random / stratified / choice-based sampling |  |
| 加权外生样本极大似然（WESML） | weighted exogenous sample maximum likelihood (WESML) | $w_Y$ |
| 移动观测法 | moving observer method |  |
| 诱增需求 | induced demand |  |
| 外部性（拥堵外部性） | externality (congestion externality) |  |
| 边际改进率 | marginal improvement rate |  |
| 有限总体校正 | finite population correction | $1 - n/N$ |
| 变异系数 | coefficient of variation | $\mathrm{CV}$ |
| 误差传播 | error propagation | $e_z$ |
| 测量误差 / 设定误差 / 抽样误差 | measurement / specification / sampling error | $e_m$, $e_s$ |

## 出行需求模型

| 中文 | English | 符号 / 说明 |
|---|---|---|
| 出行生成；出行产生量 / 出行吸引量 | trip generation; trip production / attraction | $O_i$, $D_j$ |
| 出行端；出行目的；基于家的出行 | trip end; trip purpose; home-based trip |  |
| 出行率；交叉分类法（类别分析法） | trip rate; cross-classification (category analysis) | $t^{(p)}(h)$ |
| 人员类别；人员类别模型 | person category; person-category model |  |
| 小区回归 / 家庭回归 | zonal / household-based regression |  |
| 可达性 | accessibility | $A_i$ |
| 出行分布；O-D 矩阵（起讫点矩阵）；产生–吸引矩阵 | trip distribution; O-D matrix; P–A matrix | $T_{ij}$ |
| 广义费用；时间价值 | generalized cost; value of time | $c_{ij}$ |
| 增长系数法 | growth factor method | $\tau$, $\tau_i$, $\Gamma_j$ |
| 常增长系数法 | uniform (constant) growth factor method |  |
| 平均增长系数法 | average growth factor method |  |
| 底特律法 / 福莱特法 / 佛尼斯法 | Detroit / Fratar / Furness method |  |
| 位置系数（福莱特法） | location factor (Fratar) | $L_i^{O}$, $L_j^{D}$ |
| 单约束 / 双约束模型 | singly / doubly constrained model |  |
| 重力模型；阻抗函数 | gravity model; deterrence function | $f(c_{ij})$ |
| 分段阻抗系数；阶梯阻抗函数 | separation factor; stepwise deterrence function | $F_k$ |
| 出行距离分布 | trip length distribution | $S_k$ |
| 标定；验证 | calibration; validation |  |
| 交通方式划分 | modal split |  |
| 离散选择模型；随机效用 | discrete choice model; random utility | $U_{in} = V_{in} + \varepsilon_{in}$ |
| 系统效用（确定项）；选择集 | systematic utility; choice set | $V_{in}$, $C_n$ |
| 二项 / 多项 / 巢式 Logit 模型 | binary / multinomial / nested logit |  |
| 结构参数（巢式 Logit） | structural parameter (nested logit) | $\phi_m$ |
| 线性概率模型 | linear probability model |  |
| 通用变量 / 方案特定变量 | generic / alternative-specific variable |  |
| 完全分离 | perfect separation |  |
| Probit 模型 | probit model |  |
| 无关方案独立性（IIA） | independence of irrelevant alternatives (IIA) |  |
| 直接弹性 / 交叉弹性 | direct / cross elasticity |  |
| 对数和（期望最大效用） | logsum (expected maximum utility) | $\mathrm{EMU}$ |
| 方案特定常数 | alternative-specific constant | $K_i$ |
| 似然比指数 | likelihood ratio index | $\rho^2$ |
| 转移曲线 | diversion curve |  |
| 组合费用 | composite cost | $K_{ij}^n$ |
| 方式惩罚项 | modal penalty | $\delta$ |
| 市场细分（人群类别） | market segment |  |

## 交通分配

| 中文 | English | 符号 / 说明 |
|---|---|---|
| 交通分配；路径 | traffic assignment; path (route) | $k \in K_{rs}$ |
| 路段–路径关联 | link–path incidence | $\delta_{a,k}^{rs}$ |
| Wardrop 第一 / 第二原理 | Wardrop's first / second principle |  |
| （确定性）用户均衡 | (deterministic) user equilibrium (DUE) |  |
| 系统最优；系统总出行时间 | system optimum (SO); total system travel time | $\mathrm{TSTT}$ |
| Beckmann 等价极小化模型 | Beckmann's equivalent minimization program |  |
| 全有全无分配 | all-or-nothing assignment | $\by$ |
| 相继平均法（MSA） | method of successive averages (MSA) |  |
| 相对间隙 | relative gap | $\mathrm{RG}$ |
| 边际成本；边际成本定价；收费 | marginal cost; marginal-cost pricing; toll | $\tilde t_a$, $\tau_a$ |
| Braess 悖论 | Braess's paradox |  |
| 弹性需求；超额需求 | elastic demand; excess demand | $e_{rs}$ |
| 分布–分配组合模型 | combined distribution and assignment model |  |
| Hitchcock 运输问题 | Hitchcock transportation problem |  |
| 随机用户均衡 | stochastic user equilibrium (SUE) |  |
| 感知行程时间；随机网络加载 | perceived travel time; stochastic network loading | $C_k^{rs}$ |
| 松弛均衡 | relaxed equilibrium |  |
| 离散参数 | dispersion parameter | $\theta$ |
| 动态交通分配 | dynamic traffic assignment (DTA) |  |
| 瓶颈模型；出发时间选择 | bottleneck model; departure time choice |  |
| 计划延误；早到 / 晚到 | schedule delay; early / late arrival | $\beta$, $\gamma$ |
| 累计（到达与离开）曲线 | cumulative (arrival and departure) curves |  |
| 瞬时 / 实际经历行程时间 | instantaneous / experienced travel time | $\mathrm{ITT}$, $\mathrm{ETT}$ |
| 先进先出（FIFO） | first-in, first-out (FIFO) |  |
| 基于智能体的仿真 | agent-based simulation |  |
