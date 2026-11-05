# Python 实现：交通方式选择

## 概述

本章实现{doc}`11-discrete-choice-models`和{doc}`12-aggregate-modal-split`中的离散选择模型和集计方式划分模型，并复现{doc}`26-examples-discrete-choice`和{doc}`27-examples-modal-split`中的算例。构建本书时不会运行这些代码；请将其复制到脚本或 notebook 中，并将打印结果与 `# Expected:` 注释（与算例一致）进行比较。

:::{admonition} 学习目标
:class: objectives
学完本章后，读者应能够：

- 计算 Logit 和巢式 Logit 概率、对数和以及弹性；
- 用牛顿–拉弗森法以极大似然估计 Logit 模型，并识别不可识别参数和完全分离；
- 用佛尼斯平衡求解出行分布–方式划分组合模型；
- 用线性回归标定集计的二项 Logit 划分；
- 用牛顿法求解不动点形式的方式划分问题。
:::

## 环境准备

代码使用 `numpy`、`pandas` 和 `scipy`（`optimize`、`stats`）；下面的代码块包含全部导入语句以及本章通用的两个 Logit 辅助函数。

```python
import numpy as np
import pandas as pd
from scipy import optimize, stats

np.set_printoptions(precision=3, suppress=True, linewidth=120)


def logit(V, mu=1.0):
    """Multinomial logit probabilities, equation (eq-11-mnl).

    Parameters
    ----------
    V : array_like
        Systematic utilities; the last axis indexes the alternatives.
    mu : float
        Scale parameter, mu > 0.

    Returns
    -------
    numpy.ndarray
        Choice probabilities, same shape as V.
    """
    if mu <= 0:
        raise ValueError("the scale parameter mu must be positive")
    V = mu * np.asarray(V, float)
    # subtract the maximum for numerical stability
    expV = np.exp(V - V.max(axis=-1, keepdims=True))
    return expV / expV.sum(axis=-1, keepdims=True)


def logsum(V, mu=1.0):
    """Log-sum (1/mu) ln sum_j exp(mu V_j), equation (eq-11-logsum).

    The constant gamma/mu of the expected maximum utility is omitted.

    Parameters
    ----------
    V : array_like
        Systematic utilities; the last axis indexes the alternatives.
    mu : float
        Scale parameter, mu > 0.
    """
    if mu <= 0:
        raise ValueError("the scale parameter mu must be positive")
    V = mu * np.asarray(V, float)
    m = V.max(axis=-1)
    return (m + np.log(np.exp(V - m[..., None]).sum(axis=-1))) / mu
```

## 非集计模型

### Logit 概率与弹性

```python
V_car = 0.5 - 0.25 * 25 - 0.42 * 5 - 1.25 * 3
V_tr = -0.25 * 30 - 0.42 * 8 - 1.25 * 1
P = logit([V_car, V_tr])
# S$1 toll
P_toll = logit([V_car - 1.25 * 1, V_tr])
# beta_C * C_car * (1 - P_car)
elasticity = -1.25 * 3 * (1 - P[0])
print(P.round(4), P_toll.round(4), round(elasticity, 3))
# Expected: [0.625 0.375] [0.323 0.677] -1.407
```

### 巢式 Logit

```python
V = {
    "c": -0.03 * 4.5 - 0.15 * 23 + 1.30,
    "st": -0.03 * 5.5 - 0.15 * 15 - 0.25,
    "b": -0.04 * 7.5 - 0.02 * 5.5 + 0.6,
    "u": -0.04 * 5.4 - 0.02 * 3.6,
}
# expected maximum utility of the nest
emu = logsum([V["b"], V["u"]])
# structural parameter 0.60
V["mt"] = 0.60 * emu
upper = logit([V["c"], V["st"], V["mt"]])
lower = logit([V["b"], V["u"]])
probs = {
    "car": upper[0],
    "shared taxi": upper[1],
    "bus": upper[2] * lower[0],
    "underground": upper[2] * lower[1],
}
print({k: round(float(v), 3) for k, v in probs.items()})
# Expected: car 0.061, shared taxi 0.042, bus 0.554, underground 0.343
```

### 修正基于选择的样本

```python
def p_car(K=3.0, tc=25, ec=5, cc=140, tb=40, eb=8, cb=50):
    """Car probability of the binary logit model of ex-26-hw3-q5.

    K is the car constant; t, e, c are in-vehicle time, access time,
    and cost of car (c) and bus (b).
    """
    Vc = K - 0.25 * tc - 0.4 * ec - 0.1 * cc
    Vb = -0.25 * tb - 0.4 * eb - 0.1 * cb
    return logit([Vc, Vb])[0]


# car share in sample and population
H, Q = 220 / 850, 17_000 / 86_000
K_new = 3.0 - np.log(H / Q) + np.log((1 - H) / (1 - Q))
base = p_car(K_new)
print(
    f"uncorrected P = {p_car():.4f},"
    f" K' = {K_new:.4f}, corrected P = {base:.4f}"
)
print(
    f"bus fare +25%: P = {p_car(K_new, cb=62.5):.4f}"
    f" ({p_car(K_new, cb=62.5) / base - 1:+.1%})"
)
print(f"car cost x2:   P = {p_car(K_new, cc=280):.2e}")
# Expected: uncorrected 0.2592, K' = 2.6512, corrected 0.1980;
#           bus fare +25%: 0.4629 (+133.8%); car cost x2: 2.05e-07
```

### 用牛顿–拉弗森法进行极大似然估计

下面的函数利用 {eq}`eq-11-logit-gradient-hessian` 中的梯度和黑塞矩阵（Hessian matrix）最大化二项 Logit 对数似然函数，并由黑塞矩阵的逆给出标准误。

```python
def binary_logit_ml(X, y, names, tol=1e-10, max_iter=100):
    """Binary logit by maximum likelihood with Newton-Raphson.

    Parameters
    ----------
    X : array_like, shape (N, K)
        Rows x_n = x_in - x_jn (alternative i minus alternative j).
    y : array_like, shape (N,)
        1 if alternative i was chosen, 0 otherwise.
    names : list of str
        Names of the K coefficients.

    Returns
    -------
    table : pandas.DataFrame
        Estimates, standard errors, and t-statistics.
    info : dict
        LL, LL(0), rho2, and the number of iterations.
    """
    X, y = np.asarray(X, float), np.asarray(y, float)
    if X.ndim != 2 or X.shape[0] != y.shape[0] or X.shape[1] != len(names):
        raise ValueError("X must be N x K, y of length N, names of length K")
    if not np.all((y == 0) | (y == 1)):
        raise ValueError("y must contain only 0 and 1")
    beta = np.zeros(X.shape[1])
    for it in range(max_iter):
        P = 1 / (1 + np.exp(-X @ beta))
        grad = X.T @ (y - P)
        # Hessian (negative semidefinite)
        H = -(X * (P * (1 - P))[:, None]).T @ X
        step = np.linalg.solve(H, grad)
        beta = beta - step
        if np.abs(step).max() < tol:
            break
    P = 1 / (1 + np.exp(-X @ beta))
    LL = np.sum(y * np.log(P) + (1 - y) * np.log(1 - P))
    LL0 = len(y) * np.log(0.5)
    se = np.sqrt(np.diag(np.linalg.inv(-H)))
    table = pd.DataFrame(
        {"estimate": beta, "std.err": se, "t": beta / se}, index=names
    )
    return table, {
        "LL": LL,
        "LL(0)": LL0,
        "rho2": 1 - LL / LL0,
        "iterations": it + 1,
    }


# Traveler 6 (mode A unavailable) contributes nothing and is dropped;
# beta_2 (age < 20) is therefore not identified and is left out.
tA = np.array([15.4, 14.2, 19.6, 50.8, 55.5])
tB = np.array([58.2, 31.0, 43.6, 59.9, 33.8])
age_over_40 = np.array([0, 1, 0, 1, 0])
chose_A = np.array([1, 0, 1, 1, 0])
# constant, time difference, dummy
X = np.column_stack([np.ones(5), tA - tB, age_over_40])
table, info = binary_logit_ml(
    X, chose_A, ["beta0", "beta1 (time)", "beta3 (age>40)"]
)
print(table.round(4))
print({k: round(float(v), 4) for k, v in info.items()})
# Expected: beta0 -0.0369, beta1 -0.1020, beta3 -1.2846; LL -2.0165, rho2
#           0.4182
```

{prf:ref}`ex-26-hw3-q6`的似然函数没有有限的最大值。一个线性规划可以找到将每个观测值都正确分类的参数向量，从而证明存在完全分离：

```python
# t_A - t_B
dt = np.array([-5, -5, -15, -15, -10, -10])
# c_A - c_B
dc = np.array([0.8, 0.8, 3.2, 3.2, 2.1, 2.1])
# salary (enters V_A only)
s = np.array([3.0, 4.0, 3.5, 6.0, 4.5, 6.5])
chose_A = np.array([0, 1, 0, 1, 0, 1])
X = np.column_stack([np.ones(6), dt, dc, s])

sign = np.where(chose_A == 1, 1.0, -1.0)
# find b with sign * (X b) >= 1 for all n
res = optimize.linprog(
    np.zeros(4),
    A_ub=-(sign[:, None] * X),
    b_ub=-np.ones(6),
    bounds=[(None, None)] * 4,
)
print("separating vector found:", res.status == 0, res.x.round(3))
print("V_A - V_B:", (X @ res.x).round(2))
# Expected: True; V_A - V_B negative for persons 1, 3, 5 and positive for 2, 4,
#           6
```

## 集计方式划分

### 转移曲线与组合费用

```python
# Diversion curve: car S$6 + 20 min, bus S$1.85 + 30 min, value of time
# S$0.25/min (assumed)
C_car, C_bus = 6.0 + 0.25 * 20, 1.85 + 0.25 * 30
for beta in (0.2, 0.5, 1.0):
    # utilities are minus costs
    p_bus = logit([-C_car, -C_bus], mu=beta)[1]
    print(
        f"beta = {beta}: bus share = {p_bus:.3f},"
        f" bus users = {2000 * p_bus:.0f}"
    )
# Expected: 0.582 / 1164, 0.695 / 1391, 0.839 / 1678

# Composite cost of three modes (lambda = 0.1)
C = np.array([30.0, 20.0, 25.0])
P = logit(-C, mu=0.1)
# composite cost = minus the log-sum
K = -logsum(-C, mu=0.1)
print(
    "shares:",
    P.round(3),
    " composite cost:",
    round(K, 2),
    " weighted average:",
    round(P @ C, 2),
)
# Expected: shares [0.186 0.506 0.307], composite cost 13.2, weighted average
#           23.4
```

### 出行分布与方式划分的组合

```python
O = np.array([200.0, 150.0, 250.0])
D = np.array([280.0, 320.0])
# C[i, j, k]: k = 0 car, 1 bus
C = np.array(
    [[[30, 45], [46, 57]], [[40, 60], [43, 57]], [[20, 26], [25, 32]]],
    dtype=float,
)
# assumed dispersion parameter
beta = 0.05

# deterrence summed over modes
f = np.exp(-beta * C).sum(axis=2)
B = np.ones(len(D))
# Furness balancing
for _ in range(200):
    A = 1.0 / (f @ (B * D))
    B = 1.0 / ((A * O) @ f)
T_mode = (A * O)[:, None, None] * (B * D)[None, :, None] * np.exp(-beta * C)

print("T_ij:\n", T_mode.sum(axis=2).round(2))
print(
    "car trips:\n",
    T_mode[:, :, 0].round(2),
    "\nbus trips:\n",
    T_mode[:, :, 1].round(2),
)
print("total travel time:", round((T_mode * C).sum()))
# Expected: T_ij [[111.17 88.83] [58.51 91.49] [110.32 139.68]]
#           car  [[75.51 56.33] [42.78 61.13] [63.37 81.94]]; total travel time
#           21712
```

### 红巴士/蓝巴士问题的分层划分

```python
def red_blue(lam1, lam2, C=10.0):
    """Hierarchical split, car vs. (red bus, blue bus), equal costs C.

    lam1 and lam2 are the upper and lower dispersion parameters,
    0 < lam1 <= lam2. Returns P_car, P_red, P_blue.
    """
    if not 0 < lam1 <= lam2:
        raise ValueError("need 0 < lam1 <= lam2")
    # composite bus cost
    C_bus = -logsum([-C, -C], mu=lam2)
    p_car = logit([-C, -C_bus], mu=lam1)[0]
    return p_car, (1 - p_car) / 2, (1 - p_car) / 2


for lam2 in (0.5, 2.0, 50.0):
    print(f"lambda2 = {lam2}:", np.round(red_blue(0.5, lam2), 3))
# Expected: lambda2 = 0.5 -> 1/3 each (N-way logit); lambda2 -> infinity ->
#           (0.5, 0.25, 0.25)
```

### 用回归进行标定

```python
P1 = np.array([0.51, 0.57, 0.80, 0.71, 0.63])
C1 = np.array([21.0, 15.8, 15.9, 18.2, 11.0])
C2 = np.array([18.0, 13.1, 14.7, 16.4, 8.5])

# y = lambda (C2 - C1) + lambda delta
fit = stats.linregress(C2 - C1, np.log(P1 / (1 - P1)))
lam, lam_delta = fit.slope, fit.intercept
print(
    f"lambda = {lam:.4f}, lambda*delta = {lam_delta:.4f},"
    f" delta = {lam_delta / lam:.3f}, R2 = {fit.rvalue**2:.3f}"
)
# Expected: lambda = 0.7211, lambda*delta = 2.2423, delta = 3.110, R2 = 0.989
```

标定小汽车–轨道交通划分（{prf:ref}`ex-27-hw3-q1`）：

```python
# pairs A-U, B-U, ..., D-W
pairs = [f"{o}-{d}" for d in "UVW" for o in "ABCD"]
car = pd.DataFrame(
    {
        "X1": [23, 20, 18, 15, 26, 19, 14, 12, 30, 20, 15, 10],
        "X2": [3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5],
        "X3": [120, 96, 80, 68, 152, 96, 60, 56, 160, 100, 64, 52],
        "X4": [40, 40, 40, 40, 60, 60, 60, 60, 80, 80, 80, 80],
    },
    index=pairs,
)
rail = pd.DataFrame(
    {
        "X1": [19, 17, 14, 14, 23, 18, 11, 12, 25, 16, 12, 8],
        "X2": [10, 8, 10, 12, 10, 9, 9, 11, 10, 8, 9, 9],
        "X3": [72, 64, 28, 20, 104, 72, 36, 28, 120, 92, 36, 24],
    },
    index=pairs,
)
P_car = np.array(
    [0.80, 0.82, 0.85, 0.90, 0.70, 0.90, 0.75, 0.90, 0.50, 0.55, 0.58, 0.60]
)


def gen_cost(df, x3_factor=1.0, parking=True):
    """Generalized cost in S$ of ex-27-hw3-q1.

    In-vehicle time at S$10/h, excess time at S$20/h, running cost X3
    (times x3_factor) and parking cost X4 in cents / 100.
    """
    cost = df.X1 * 10 / 60 + df.X2 * 20 / 60 + x3_factor * df.X3 / 100
    return cost + (df.X4 / 100 if parking else 0)


Cc, Cr = gen_cost(car), gen_cost(rail, parking=False)
fit = stats.linregress(Cr - Cc, np.log(P_car / (1 - P_car)))
lam, delta = fit.slope, fit.intercept / fit.slope
model = lambda Cc, Cr: 1 / (1 + np.exp(-lam * (Cr + delta - Cc)))
print(f"lambda = {lam:.4f}, delta = {delta:.4f}, R2 = {fit.rvalue**2:.3f}")
# Expected: lambda = 1.0020, delta = 0.7102, R2 = 0.811

results = pd.DataFrame(
    {
        "base": model(Cc, Cr),
        "petrol x2": model(gen_cost(car, x3_factor=2.0), Cr),
        "free rail": model(Cc, gen_cost(rail, x3_factor=0.0, parking=False)),
    }
)
results["change (b)"] = results["petrol x2"] - results["base"]
results["change (c)"] = results["free rail"] - results["base"]
print(results.round(3).T.to_string())
# Expected: (A-U): base 0.818, petrol x2 0.574 (change -0.244), free rail 0.685
#           (change -0.132)
```

按出行者类型的分布–方式划分模型（{prf:ref}`ex-27-hw3-q2`）：

```python
# mode-choice dispersion parameters lambda^n of the two person types
lam = {1: 0.20, 2: 0.15}
beta = 0.05
# car, public transport
C = np.array([20.0, 40.0])
# person type 1: both modes available
K1 = -logsum(-C, mu=lam[1])
# person type 2: public transport only
K2 = C[1]
AOBD = 2000 / (np.exp(-beta * K1) + np.exp(-beta * K2))
T1, T2 = AOBD * np.exp(-beta * K1), AOBD * np.exp(-beta * K2)
p_car = logit(-C, mu=lam[1])[0]
print(
    f"K1 = {K1:.2f}; T1 = {T1:.1f}, T2 = {T2:.1f};"
    f" car = {T1 * p_car:.1f}, PT = {T1 * (1 - p_car) + T2:.1f}"
)
# Expected: K1 = 19.91; T1 = 1463.9, T2 = 536.1; car = 1437.6, PT = 562.4
```

### 政策应用：用牛顿法求不动点

```python
def newton(f, df, x0, tol=1e-8, max_iter=50):
    """Solve f(x) = 0 by Newton's method from x0.

    Stops when the step is below tol; raises if it does not converge.
    """
    if tol <= 0 or max_iter < 1:
        raise ValueError("tol must be positive and max_iter at least 1")
    x = x0
    for _ in range(max_iter):
        step = f(x) / df(x)
        x -= step
        if abs(step) < tol:
            return x
    raise RuntimeError("Newton's method did not converge")


# Congestion pricing: x = Q_A / 1000 solves x = 20 / (1 + exp(0.4 x^2 - 2.3))
e = lambda x: np.exp(0.4 * x**2 - 2.3)
x = newton(
    lambda x: x - 20 / (1 + e(x)),
    lambda x: 1 + 16 * x * e(x) / (1 + e(x)) ** 2,
    x0=2.0,
)
print(f"Q_A = {1000 * x:.0f} veh/h, Q_T = {20000 - 1000 * x:.0f}")
print(f"toll for Q_A = 2500: {10 * np.log(7) + 8:.2f} HK$")
# Expected: Q_A = 3153, Q_T = 16847; toll 27.46 HK$

# Bus lane (N = 5000, 3 lanes, 110 buses/h, beta = 0.5, Delta = 5)
N, buses, beta, Delta = 5000, 110, 0.5, 5.0
# minutes, q in veh/h/lane
t_lane = lambda q: 9.0 + 0.012 * q

# no bus lane: equal travel times
n_bus0 = N / (1 + np.exp(beta * Delta))
t0 = t_lane((N - n_bus0 + buses) / 3)
TC0 = n_bus0 * (t0 + Delta) + (N - n_bus0) * t0

# one bus lane
c_bus = t_lane(buses) + Delta
g = lambda n: np.exp(-beta * (c_bus - t_lane(n / 2)))
n_car = newton(
    lambda n: n - N / (1 + g(n)),
    lambda n: 1 + N * g(n) * beta * 0.006 / (1 + g(n)) ** 2,
    x0=2000.0,
)
TC1 = (N - n_car) * c_bus + n_car * t_lane(n_car / 2)
print(
    f"TC0 = {TC0:,.0f}, N_car = {n_car:.0f},"
    f" TC1 = {TC1:,.0f}, CE = {TC1 / TC0:.3f}"
)
# Expected: TC0 = 141,511, N_car = 1376, TC1 = 79,265, CE = 0.560
```

## 小结

- `logit` 和 `logsum` 是本章每个模型的两个基本构件；减去最大效用可以避免数值溢出。
- 二项 Logit 的极大似然估计只需要梯度 $\sum_n (y_n - P_n)\bx_n$ 和黑塞矩阵 $-\sum_n P_n(1 - P_n)\bx_n\bx_n\T$；在相信估计值之前，应先检查可识别性和分离问题。`statsmodels`（`Logit`、`MNLogit`）和 Biogeme 等软件包给出相同的估计值，并提供更多诊断信息。
- 集计模型将 Logit 划分与佛尼斯平衡、线性回归以及求不动点的牛顿法结合起来。
