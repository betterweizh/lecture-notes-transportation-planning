# Python 实现：出行分布

## 概述

本章实现{doc}`04-biproportional-fitting`和{doc}`10-trip-distribution`中的增长系数法（growth factor method）、平衡算法和重力模型（gravity model），并复现{doc}`25-examples-trip-distribution`中的算例。构建本书时不会运行这些代码；请将其复制到脚本或 notebook 中，并将结果与 `# Expected:` 注释进行比较。

:::{admonition} 学习目标
:class: objectives
学完本章后，读者应能够：

- 实现常增长系数法、平均增长系数法、底特律法、福莱特法和佛尼斯法，并比较它们的收敛性；
- 实现带有恰当停止规则和结构性零元的佛尼斯（双比例）法；
- 运行单约束和双约束重力模型，并将 $\beta$ 标定到观测的平均出行费用；
- 在完整矩阵和部分矩阵上实现三比例拟合（tri-proportional fitting）；
- 用线性规划检验标定目标值的一致性。
:::

## 环境准备

代码使用 `numpy` 以及 `scipy.optimize` 中的求根函数和线性规划求解器。

```python
import numpy as np
from scipy import optimize

np.set_printoptions(precision=3, suppress=True, linewidth=120)
```

## 增长系数法

函数 `furness` 实现{prf:ref}`alg-04-biprop-2`；下面用它计算双约束增长系数模型，并以阻抗矩阵为种子矩阵计算重力模型（{prf:ref}`ex-25-td-singly-growth`、{prf:ref}`ex-25-td-furness`）。

```python
def furness(seed, O, D, tol=1e-4, max_iter=1000):
    """Bi-proportional algorithm II: T_ij = a_i b_j seed_ij.

    The row sums of T are O and the column sums are D.

    Zero cells of the seed (e.g. unobserved intra-zonal trips) stay zero.
    Stops when every b_j changes by less than tol in relative terms.
    """
    seed = np.asarray(seed, float)
    O, D = np.asarray(O, float), np.asarray(D, float)
    if seed.shape != (len(O), len(D)) or np.any(seed < 0):
        raise ValueError("seed must be a non-negative len(O) x len(D) matrix")
    if not np.isclose(O.sum(), D.sum()):
        raise ValueError(f"inconsistent totals: {O.sum()} vs {D.sum()}")
    b = np.ones(seed.shape[1])
    for n in range(1, max_iter + 1):
        # row step
        a = O / (seed @ b)
        # column step
        b_new = D / (a @ seed)
        converged = np.all(np.abs(b_new - b) <= tol * b_new)
        b = b_new
        if converged:
            break
    return a, b, a[:, None] * b[None, :] * seed, n


# Origin-constrained growth factors (only the rows are scaled)
t = np.array(
    [
        [5, 50, 100, 200],
        [50, 5, 100, 300],
        [50, 100, 5, 100],
        [100, 200, 250, 20],
    ],
    float,
)
O = np.array([400, 460, 400, 702])
tau = O / t.sum(axis=1)
print(tau.round(3), (tau[:, None] * t).sum(axis=0).round(1))
# Expected: [1.127 1.011 1.569 1.232] [257.8 464.6 529.5 710.1]

# Doubly constrained growth (Furness)
t = np.array([[3.0, 1.1, 1.1], [1.1, 3.0, 3.0], [1.8, 1.8, 3.0]])
a, b, T, n = furness(t, [100, 200, 250], [220, 165, 165])
print(n, a, b, "\n", T.round(1))
# Expected: 5 [16.148 30.377 38.512] [1.455 0.926 0.735]
#           T = [[70.5 16.4 13.1] [48.6 84.4 67.0] [100.9 64.2 84.9]]
```

### 迭代增长系数法的比较

下面的函数用平均增长系数法、底特律法、福莱特法和佛尼斯法的增长函数实现一般迭代式 {eq}`eq-10-growth-iteration`（{prf:ref}`ex-25-td-growth-methods`）。

```python
def growth_factor(seed, O, D, method, eps=1e-3, max_iter=500):
    """Iterative doubly constrained growth-factor methods.

    method: "average", "detroit", "fratar", or "furness".
    Stops when every growth factor is within eps of one.
    """
    if method not in ("average", "detroit", "fratar", "furness"):
        raise ValueError(f"unknown method: {method}")
    T = np.asarray(seed, float).copy()
    O, D = np.asarray(O, float), np.asarray(D, float)
    if not np.isclose(O.sum(), D.sum()):
        raise ValueError(f"inconsistent totals: {O.sum()} vs {D.sum()}")
    for m in range(max_iter):
        Om, Dm = T.sum(axis=1), T.sum(axis=0)
        tau, gam = O / Om, D / Dm
        if max(np.abs(tau - 1).max(), np.abs(gam - 1).max()) <= eps:
            return T, m
        if method == "average":
            T *= (tau[:, None] + gam[None, :]) / 2
        elif method == "detroit":
            G = O.sum() / T.sum()
            T *= tau[:, None] * gam[None, :] / G
        elif method == "fratar":
            # location factors of origins and destinations
            L_o = Om / (T @ gam)
            L_d = Dm / (tau @ T)
            L = (L_o[:, None] + L_d[None, :]) / 2
            T *= tau[:, None] * gam[None, :] * L
        elif method == "furness":
            # row step, then column step
            T *= tau[:, None]
            T *= (D / T.sum(axis=0))[None, :]
    raise RuntimeError(f"{method} did not converge in {max_iter} iterations")


t3 = np.array(
    [
        [17, 7, 4],
        [7, 38, 6],
        [4, 5, 17],
    ],
    float,
)
O3 = np.array([38.6, 91.9, 36.0])
D3 = np.array([39.3, 90.3, 36.9])

# uniform growth factor method
print("uniform:\n", (t3 * O3.sum() / t3.sum()).round(2))
for method in ("average", "detroit", "fratar", "furness"):
    T, m = growth_factor(t3, O3, D3, method)
    print(f"{method:8s} iterations {m}:", T.round(2).tolist())
# Expected: uniform [[26.96 11.1 6.34] [11.1 60.26 9.51] [6.34 7.93 26.96]]
#           average 8, detroit 9, fratar 3, furness 5 iterations;
#           furness [[22.58, 10.89, 5.13], [11.23, 71.39, 9.29],
#           [5.48, 8.02, 22.48]]
```

### 出行端不一致时的佛尼斯法

先将出行端缩放到同一总量；未观测的对角单元保持为零（{prf:ref}`ex-25-hw2-q1`）。

```python
# zeros on the diagonal: not observed
t = np.array(
    [
        [0, 60, 275, 571],
        [50, 0, 410, 443],
        [123, 61, 0, 47],
        [205, 265, 75, 0],
    ],
    float,
)
O = np.array([1200, 1050, 380, 770], float)
D = np.array([670, 730, 950, 995], float)
# 3400 vs 3345: cannot balance directly
print("totals:", O.sum(), D.sum())

# scale productions to the attraction total
O_adj = O * D.sum() / O.sum()
a, b, T, n = furness(t, O_adj, D, tol=1e-4)
print(n, "\n", T.round(1))
# Expected: 16 iterations;
#   [[  0.  204.4 395.3 580.9]
#    [140.    0.  506.  386.9]
#    [228.4 118.3   0.   27.2]
#    [301.6 407.3  48.6   0. ]]
```

## 重力模型

双约束重力模型就是以 $[f(c_{ij})]$ 为种子矩阵的佛尼斯法（{prf:ref}`ex-25-td-gravity`）。

```python
c = np.array(
    [[3, 11, 18, 22], [12, 3, 12, 19], [15.5, 13, 5, 7], [24, 18, 8, 5]], float
)
O = np.array([400, 460, 400, 702], float)
D = np.array([260, 400, 500, 802], float)


def gravity(c, O, D, beta, constraint="double"):
    """Gravity model with exponential deterrence f(c) = exp(-beta c).

    constraint: "origin" (singly constrained) or "double".
    """
    if constraint not in ("origin", "double"):
        raise ValueError(f"unknown constraint: {constraint}")
    f = np.exp(-beta * c)
    # T_ij = O_i D_j f / sum_j D_j f
    if constraint == "origin":
        return O[:, None] * D[None, :] * f / (f @ D)[:, None]
    _, _, T, _ = furness(f, O, D, tol=1e-8)
    return T


T = gravity(c, O, D, beta=0.1)
mean_cost = (T * c).sum() / T.sum()
print(T.round(1), f"\nmean trip cost = {mean_cost:.2f} min")
# Expected: first row [157.0 100.4 66.1 76.5]; mean trip cost = 8.65 min

# Calibrating beta: find the beta that reproduces an observed mean trip cost
# (say 9.0 min)
target = 9.0
beta_hat = optimize.brentq(
    lambda bt: (gravity(c, O, D, bt) * c).sum() / O.sum() - target, 0.001, 1.0
)
# a smaller beta than 0.1 gives longer trips
print(f"beta = {beta_hat:.4f}")
# Expected: beta = 0.0879
```

## 三比例拟合

系数 $a_i$、$b_j$ 和 $F_k$ 只能确定到一个比例因子；实现中在每次迭代时对 $b$ 重新归一化，使各系数不会漂移，并以单元值检验收敛。权重矩阵 `W` 标记参与计算的单元（1 = 观测值，0 = 缺失值或结构性零元），从而可以处理部分矩阵（{prf:ref}`ex-25-td-tri-proportional`）。

```python
def tri_proportional(bins, O, D, S, W=None, tol=1e-8, max_iter=10_000):
    """Fit T_ij = a_i b_j F_k(ij) W_ij by tri-proportional fitting.

    Targets: row totals O, column totals D, and bin totals S.
    """
    if not np.isclose(np.sum(O), np.sum(D)) or not np.isclose(
        np.sum(O), np.sum(S)
    ):
        raise ValueError("the totals of O, D, and S must be equal")
    z, K = len(O), len(S)
    W = np.ones((z, z)) if W is None else np.asarray(W, float)
    b, F, T_old = np.ones(z), np.ones(K), None
    for n in range(1, max_iter + 1):
        G = F[bins] * W
        a = O / (G @ b)
        b = D / (a @ G)
        # remove the scale freedom
        b /= b.max()
        AB = a[:, None] * b[None, :] * W
        F = S / np.array([AB[bins == k].sum() for k in range(K)])
        T = AB * F[bins]
        if T_old is not None and np.abs(T - T_old).max() < tol * T.max():
            break
        T_old = T
    return a, b, F, T, n


def is_feasible(bins, O, D, S):
    """Check with an LP whether a positive matrix fits all totals."""
    z, K = len(O), len(S)
    # row sums
    rows = [np.kron(np.eye(z)[i], np.ones(z)) for i in range(z)]
    # column sums
    cols = [np.kron(np.ones(z), np.eye(z)[j]) for j in range(z)]
    # bin sums
    bin_rows = [(bins.ravel() == k).astype(float) for k in range(K)]
    A_eq = np.column_stack(
        [np.array(rows + cols + bin_rows), np.zeros(2 * z + K)]
    )
    # T_ij >= s
    A_ub = np.column_stack([-np.eye(z * z), np.ones(z * z)])
    res = optimize.linprog(
        np.r_[np.zeros(z * z), -1],
        A_ub=A_ub,
        b_ub=np.zeros(z * z),
        A_eq=A_eq,
        b_eq=np.r_[O, D, S],
        bounds=[(0, None)] * (z * z + 1),
    )
    return res.status == 0 and -res.fun > 0


c2 = np.array(
    [[3, 11, 18, 22], [10, 3, 13, 19], [15, 13, 5, 7], [24, 18, 6, 5]], float
)
# bins 0..5 for 0-4, 4-8, ..., 20-24
bins = np.digitize(c2, [4, 8, 12, 16, 20])
S_survey = np.array([365, 962, 160, 150, 230, 95], float)
S_fixed = np.array([365, 962, 155, 150, 230, 100], float)
print(is_feasible(bins, O, D, S_survey), is_feasible(bins, O, D, S_fixed))
# Expected: False True  (the survey TLD contradicts the trip ends)

a, b, F, T, n = tri_proportional(bins, O, D, S_fixed)
print(n, F / F[0], "\n", T.round(1))
# Expected: 24 [1.    0.459 0.414 0.246 0.177 0.113]
#           first row [155.2 98.1 68.8 77.9]
```

### 在部分矩阵上标定

只有观测到的单元进入目标值和迭代；然后用拟合的系数填充缺失的单元（{prf:ref}`ex-25-hw2-q2`）。

```python
cost = np.array(
    [
        [0, 1.23, 1.85, 2.67],
        [1.23, 0, 2.48, 1.21],
        [1.85, 2.48, 0, 1.44],
        [2.67, 1.21, 1.44, 0],
    ]
)
counts = np.array(
    [[0, 6, np.nan, 2], [np.nan, 0, 1, 4], [8, np.nan, 0, 8], [6, 18, 6, 0]]
)
# off-diagonal, observed cells
observed = ~np.isnan(counts) & ~np.eye(4, dtype=bool)
x = np.where(observed, counts, 0.0)
# bin 0: cost <= 1.9, bin 1: > 1.9
bins = (cost > 1.9).astype(int)
O, D = x.sum(axis=1), x.sum(axis=0)
S = np.array([x[bins == 0].sum(), x[bins == 1].sum()])
# [8 5 16 30] [14 24 7 14] [50 9]
print(O, D, S)

a, b, F, T, n = tri_proportional(bins, O, D, S, W=observed, tol=1e-10)
# normalize to F_1 = 1
scale = F[0]
a, F = a * scale, F / scale
# model value for every cell
full = a[:, None] * b[None, :] * F[bins]
print(n, a, b, F)
print(
    "A->C, B->A, C->B:",
    full[0, 2].round(3),
    full[1, 0].round(3),
    full[2, 1].round(3),
)
# Expected: 108 [ 6.  6. 12. 18.] [0.667 1.    0.333 0.667] [1.  0.5]
#           A->C, B->A, C->B: 2.0 4.0 6.0
```

## 小结

- `furness` 实现带相对停止规则的双比例算法 II；种子矩阵中的零单元保持为零，出行端总量不一致时报错，而不是让迭代振荡。
- `growth_factor` 用平均增长系数法、底特律法、福莱特法和佛尼斯法的增长函数实现一般迭代式 {eq}`eq-10-growth-iteration`；在三小区算例中，它们分别需要 8、9、3 和 5 次迭代。
- `gravity` 计算单约束和双约束重力模型 {eq}`eq-10-gravity`，用求根函数可将 $\beta$ 标定到观测的平均出行费用。
- `tri_proportional` 在完整矩阵或部分矩阵上标定阶梯型阻抗函数 {eq}`eq-10-stepwise-deterrence`，`is_feasible` 则在迭代开始之前用线性规划检验目标值是否一致。
