"""Generate the bilingual glossary pages docs/en/glossary.md and docs/zh/glossary.md.

Run from the repository root:  python scripts/glossary.py

Each entry: (English, 中文, symbol or note). This table is also the reference
terminology for the Chinese translation.
"""
from pathlib import Path

DOCS = Path(__file__).resolve().parents[1] / "docs"

SECTIONS = [
    ("Probability and statistics", "概率与统计", [
        ("random variable", "随机变量", "$X$"),
        ("cumulative distribution function (CDF)", "累积分布函数", "$F$"),
        ("probability density function (PDF)", "概率密度函数", "$f$"),
        ("expectation / variance / covariance", "期望 / 方差 / 协方差", r"$\E$, $\Var$, $\Cov$"),
        ("uniform / normal distribution", "均匀分布 / 正态分布", r"$\mathcal{N}(\mu, \sigma^2)$"),
        ("standard normal CDF", "标准正态分布函数", r"$\Phi$"),
        ("Gumbel (extreme value type I) distribution", "耿贝尔分布（第一类极值分布）", r"$\mathrm{Gumbel}(\eta, \mu)$"),
        ("logistic distribution", "逻辑斯谛分布", ""),
        ("location / scale parameter", "位置参数 / 尺度参数", r"$\eta$, $\mu$"),
        ("bivariate / multivariate normal distribution", "二元 / 多元正态分布", r"$\rho$, $\bSigma$"),
        ("linear regression / least squares", "线性回归 / 最小二乘法", r"$\hat\bbeta$"),
        ("normal equations", "正规方程", ""),
        ("residual", "残差", r"$e_i$"),
        ("total / regression / error sum of squares", "总平方和 / 回归平方和 / 残差平方和", r"$\mathit{SS}_T$, $\mathit{SS}_R$, $\mathit{SS}_E$"),
        ("coefficient of determination; adjusted / uncentered", "决定系数；调整 / 非中心化", r"$R^2$, $\bar R^2$, $R_0^2$"),
        ("hypothesis test; null hypothesis", "假设检验；原假设", r"$H_0$"),
        ("significance level; $p$-value", "显著性水平；$p$ 值", r"$\alpha$"),
        ("confidence interval; degrees of freedom", "置信区间；自由度", r"$\nu$"),
        ("dummy variable", "虚拟变量（哑变量）", ""),
        ("maximum likelihood estimation; log-likelihood", "极大似然估计；对数似然", r"$LL(\bbeta)$"),
    ]),
    ("Optimization and matrix balancing", "最优化与矩阵平衡", [
        ("objective function / feasible set", "目标函数 / 可行域", r"$f$, $\Omega$"),
        ("convex set / convex function", "凸集 / 凸函数", ""),
        ("gradient / Hessian matrix", "梯度 / 黑塞矩阵", r"$\nabla f$, $\nabla^2 f$"),
        ("Lagrangian; Lagrange multiplier", "拉格朗日函数；拉格朗日乘子", r"$\mathcal{L}$, $\lambda$"),
        ("Karush–Kuhn–Tucker (KKT) conditions", "KKT 条件（卡罗需–库恩–塔克条件）", ""),
        ("complementary slackness", "互补松弛条件", ""),
        ("line search; bisection; golden-section search", "线搜索；二分法；黄金分割法", ""),
        ("Frank–Wolfe algorithm (convex combinations method)", "Frank–Wolfe 算法（凸组合法）", ""),
        ("shortest path; Dijkstra's algorithm", "最短路径；Dijkstra 算法", ""),
        ("seed (prior) matrix", "种子矩阵（先验矩阵）", r"$t_{ij}$"),
        ("bi-proportional fitting (iterative proportional fitting, RAS method)", "双比例拟合（迭代比例拟合、RAS 法）", r"$a_i$, $b_j$"),
        ("balancing factor", "平衡系数", r"$A_i$, $B_j$"),
        ("cross-product ratio", "交叉乘积比", ""),
        ("entropy maximization", "熵最大化（最大熵方法）", r"$W\{T_{ij}\}$"),
        ("micro-state / meso-state / macro-state", "微观状态 / 中观状态 / 宏观状态", ""),
        ("information distance (Kullback–Leibler divergence)", "信息距离（KL 散度）", r"$I(\bT, \bt)$"),
        ("tri-proportional fitting; raking", "三比例拟合；多维比例加权（raking）", r"$F_k$"),
    ]),
    ("Transport planning and data", "交通规划与数据", [
        ("transportation planning process", "交通规划过程", ""),
        ("four-step model", "四阶段法", ""),
        ("travel demand; level of service", "出行需求；服务水平", r"$F$, $L$"),
        ("activity system; transport system", "活动系统；交通系统", r"$E$, $T$"),
        ("demand–performance equilibrium", "需求–性能均衡（供需均衡）", r"$(F^*, L^*)$"),
        ("traffic analysis zone; zoning system", "交通小区；交通小区划分", ""),
        ("centroid; centroid connector", "小区形心；形心连杆", ""),
        ("external zone; cordon; screen line", "外部小区；境界线；核查线", ""),
        ("node; link; directed graph (network)", "节点；路段；有向图（网络）", r"$G = (N, A)$"),
        ("link performance (travel time) function", "路段阻抗函数（路段行程时间函数）", r"$t_a(x_a)$"),
        ("BPR function", "BPR 函数", ""),
        ("capacity; free-flow travel time", "通行能力；自由流行程时间", r"$c_a$, $t_a^0$"),
        ("saturation flow; green time; cycle length", "饱和流率；绿灯时间；信号周期", r"$s$, $g$, $C$"),
        ("junction (intersection); turning movement", "交叉口；转向交通", ""),
        ("household (travel) survey; roadside interview", "居民出行调查；路边询问调查", ""),
        ("revealed / stated preference", "显示性偏好（RP）/ 陈述性偏好（SP）", ""),
        ("simple random / stratified / choice-based sampling", "简单随机抽样 / 分层抽样 / 基于选择的抽样", ""),
        ("weighted exogenous sample maximum likelihood (WESML)", "加权外生样本极大似然（WESML）", r"$w_Y$"),
        ("moving observer method", "移动观测法", ""),
        ("induced demand", "诱增需求", ""),
        ("externality (congestion externality)", "外部性（拥堵外部性）", ""),
        ("marginal improvement rate", "边际改进率", ""),
        ("finite population correction", "有限总体校正", r"$1 - n/N$"),
        ("coefficient of variation", "变异系数", r"$\mathrm{CV}$"),
        ("error propagation", "误差传播", r"$e_z$"),
        ("measurement / specification / sampling error", "测量误差 / 设定误差 / 抽样误差", r"$e_m$, $e_s$"),
    ]),
    ("Travel demand models", "出行需求模型", [
        ("trip generation; trip production / attraction", "出行生成；出行产生量 / 出行吸引量", r"$O_i$, $D_j$"),
        ("trip end; trip purpose; home-based trip", "出行端；出行目的；基于家的出行", ""),
        ("trip rate; cross-classification (category analysis)", "出行率；交叉分类法（类别分析法）", r"$t^{(p)}(h)$"),
        ("person category; person-category model", "人员类别；人员类别模型", ""),
        ("zonal / household-based regression", "小区回归 / 家庭回归", ""),
        ("accessibility", "可达性", r"$A_i$"),
        ("trip distribution; O-D matrix; P–A matrix", "出行分布；O-D 矩阵（起讫点矩阵）；产生–吸引矩阵", r"$T_{ij}$"),
        ("generalized cost; value of time", "广义费用；时间价值", r"$c_{ij}$"),
        ("growth factor method", "增长系数法", r"$\tau$, $\tau_i$, $\Gamma_j$"),
        ("uniform (constant) growth factor method", "常增长系数法", ""),
        ("average growth factor method", "平均增长系数法", ""),
        ("Detroit / Fratar / Furness method", "底特律法 / 福莱特法 / 佛尼斯法", ""),
        ("location factor (Fratar)", "位置系数（福莱特法）", r"$L_i^{O}$, $L_j^{D}$"),
        ("singly / doubly constrained model", "单约束 / 双约束模型", ""),
        ("gravity model; deterrence function", "重力模型；阻抗函数", r"$f(c_{ij})$"),
        ("separation factor; stepwise deterrence function", "分段阻抗系数；阶梯阻抗函数", r"$F_k$"),
        ("trip length distribution", "出行距离分布", r"$S_k$"),
        ("calibration; validation", "标定；验证", ""),
        ("modal split", "交通方式划分", ""),
        ("discrete choice model; random utility", "离散选择模型；随机效用", r"$U_{in} = V_{in} + \varepsilon_{in}$"),
        ("systematic utility; choice set", "系统效用（确定项）；选择集", r"$V_{in}$, $C_n$"),
        ("binary / multinomial / nested logit", "二项 / 多项 / 巢式 Logit 模型", ""),
        ("structural parameter (nested logit)", "结构参数（巢式 Logit）", r"$\phi_m$"),
        ("linear probability model", "线性概率模型", ""),
        ("generic / alternative-specific variable", "通用变量 / 方案特定变量", ""),
        ("perfect separation", "完全分离", ""),
        ("probit model", "Probit 模型", ""),
        ("independence of irrelevant alternatives (IIA)", "无关方案独立性（IIA）", ""),
        ("direct / cross elasticity", "直接弹性 / 交叉弹性", ""),
        ("logsum (expected maximum utility)", "对数和（期望最大效用）", r"$\mathrm{EMU}$"),
        ("alternative-specific constant", "方案特定常数", r"$K_i$"),
        ("likelihood ratio index", "似然比指数", r"$\rho^2$"),
        ("diversion curve", "转移曲线", ""),
        ("composite cost", "组合费用", r"$K_{ij}^n$"),
        ("modal penalty", "方式惩罚项", r"$\delta$"),
        ("market segment", "市场细分（人群类别）", ""),
    ]),
    ("Traffic assignment", "交通分配", [
        ("traffic assignment; path (route)", "交通分配；路径", r"$k \in K_{rs}$"),
        ("link–path incidence", "路段–路径关联", r"$\delta_{a,k}^{rs}$"),
        ("Wardrop's first / second principle", "Wardrop 第一 / 第二原理", ""),
        ("(deterministic) user equilibrium (DUE)", "（确定性）用户均衡", ""),
        ("system optimum (SO); total system travel time", "系统最优；系统总出行时间", r"$\mathrm{TSTT}$"),
        ("Beckmann's equivalent minimization program", "Beckmann 等价极小化模型", ""),
        ("all-or-nothing assignment", "全有全无分配", r"$\by$"),
        ("method of successive averages (MSA)", "相继平均法（MSA）", ""),
        ("relative gap", "相对间隙", r"$\mathrm{RG}$"),
        ("marginal cost; marginal-cost pricing; toll", "边际成本；边际成本定价；收费", r"$\tilde t_a$, $\tau_a$"),
        ("Braess's paradox", "Braess 悖论", ""),
        ("elastic demand; excess demand", "弹性需求；超额需求", r"$e_{rs}$"),
        ("combined distribution and assignment model", "分布–分配组合模型", ""),
        ("Hitchcock transportation problem", "Hitchcock 运输问题", ""),
        ("stochastic user equilibrium (SUE)", "随机用户均衡", ""),
        ("perceived travel time; stochastic network loading", "感知行程时间；随机网络加载", r"$C_k^{rs}$"),
        ("relaxed equilibrium", "松弛均衡", ""),
        ("dispersion parameter", "离散参数", r"$\theta$"),
        ("dynamic traffic assignment (DTA)", "动态交通分配", ""),
        ("bottleneck model; departure time choice", "瓶颈模型；出发时间选择", ""),
        ("schedule delay; early / late arrival", "计划延误；早到 / 晚到", r"$\beta$, $\gamma$"),
        ("cumulative (arrival and departure) curves", "累计（到达与离开）曲线", ""),
        ("instantaneous / experienced travel time", "瞬时 / 实际经历行程时间", r"$\mathrm{ITT}$, $\mathrm{ETT}$"),
        ("first-in, first-out (FIFO)", "先进先出（FIFO）", ""),
        ("agent-based simulation", "基于智能体的仿真", ""),
    ]),
]

EN_HEAD = """# Glossary

English and Chinese terms used in this book. The Chinese edition uses the
Chinese term and gives the English term in parentheses at its first use in
each chapter.
"""
ZH_HEAD = """# 术语表

本书使用的中英文术语对照。中文版在每章首次出现某术语时，会在括号中给出其英文名称。
"""


def write():
    en, zh = [EN_HEAD], [ZH_HEAD]
    for e_title, z_title, rows in SECTIONS:
        en += [f"\n## {e_title}\n", "| English | 中文 | Symbol / note |", "|---|---|---|"]
        zh += [f"\n## {z_title}\n", "| 中文 | English | 符号 / 说明 |", "|---|---|---|"]
        for e, z, sym in rows:
            en.append(f"| {e} | {z} | {sym} |")
            zh.append(f"| {z} | {e} | {sym} |")
    (DOCS / "en" / "glossary.md").write_text("\n".join(en) + "\n")
    (DOCS / "zh" / "glossary.md").write_text("\n".join(zh) + "\n")


if __name__ == "__main__":
    write()
