# Python 实现：出行生成

## 概述

本章实现{doc}`09-trip-generation`中的出行生成模型，并复现{doc}`24-examples-trip-generation`中的算例：增长系数（growth factor）与出行率（trip rate）、小区回归模型和家庭回归模型、吸引模型的逐步比较、交叉分类法（cross-classification）模型和人员类别模型、贝叶斯更新以及出行端的平衡。构建本书时不会运行这些代码；请将其复制到脚本或 notebook 中，并将结果与 `# Expected:` 注释进行比较。

:::{admonition} 学习目标
:class: objectives
学完本章后，读者应能够：

- 估计含截距和不含截距的小区回归模型和家庭回归模型，并输出在二者之间进行选择所需的统计量；
- 对候选模型进行简单的逐步比较；
- 将交叉分类出行率和人员类别出行率应用于小区数据；
- 用贝叶斯公式更新出行率，并平衡出行端。
:::

## 环境准备

代码使用 `numpy`、`pandas` 和 `scipy`；此处重复给出{doc}`32-python-foundations`中的最小二乘函数 `ols`，使本章自成一体。

```python
import numpy as np
import pandas as pd
from scipy import stats

np.set_printoptions(precision=3, suppress=True, linewidth=120)


def ols(X, y, names, intercept=True):
    """Least squares with t-tests.

    R2 is the usual R^2 with an intercept and the uncentered R_0^2 without.
    """
    X, y = np.asarray(X, float), np.asarray(y, float)
    if X.ndim != 2 or X.shape[0] != y.shape[0]:
        raise ValueError("X must be a matrix with one row per observation")
    n, p = X.shape
    if n <= p:
        raise ValueError(f"need more observations ({n}) than parameters ({p})")
    # (X'X)^-1
    C = np.linalg.inv(X.T @ X)
    # estimates
    beta = C @ X.T @ y
    resid = y - X @ beta
    sse = resid @ resid
    sst = ((y - y.mean()) ** 2).sum() if intercept else y @ y
    # residual degrees of freedom
    df = n - p
    # estimate of the error variance
    s2 = sse / df
    se = np.sqrt(s2 * np.diag(C))
    table = pd.DataFrame(
        {"estimate": beta, "std.err": se, "t": beta / se}, index=names
    )
    info = {
        "sigma": np.sqrt(s2),
        "R2": 1 - sse / sst,
        "df": df,
        "t_crit": stats.t.ppf(0.975, df),
    }
    return table, info
```

## 增长系数与出行率

增长系数 {eq}`eq-09-growth-factor-tg` 与出行率模型（{prf:ref}`ex-24-tg-growth-factor`、{prf:ref}`ex-24-tg-trip-rate`）：

```python
# Growth factor for car ownership (one zone, 250 + 250 households)
# current HB trips per day
t_now = 250 * 2.5 + 250 * 6.0
# share of car-owning households: 0.5 -> 1.0
F = 1.0 / 0.5
print("growth factor:", t_now * F, " trip rates:", 500 * 6.0)
# Expected: growth factor: 4250.0  trip rates: 3000.0

# Trip-rate model: productions per resident applied to future residents
# thousand trips/day
prod = np.array([32, 40, 51, 45])
# thousand residents
res_now = np.array([12, 18, 20, 19])
res_future = np.array([15, 24, 35, 26])
rate = prod.sum() / res_now.sum()
print(
    f"rate = {rate:.3f} trips/resident;"
    f"  future production = {rate * res_future.sum():.1f} thousand"
)
# Expected: rate = 2.435 trips/resident;  future production = 243.5 thousand
```

## 回归模型

含截距和不含截距的小区回归模型和家庭回归模型（{prf:ref}`ex-24-tg-zonal`、{prf:ref}`ex-24-tg-household-regression`）：

```python
# Zonal model: households vs. trips of five zones
hh = np.array([1000, 1500, 2500, 3000, 4000])
trips = np.array([7900, 11900, 20000, 23800, 31800])
for label, X, names, icpt in (
    ("with intercept", np.column_stack([np.ones(5), hh]), ["b0", "b1"], True),
    ("through origin", hh[:, None], ["b1"], False),
):
    table, info = ols(X, trips, names, icpt)
    print(
        label,
        {k: round(float(v), 3) for k, v in info.items()},
        "\n",
        table.round(4),
    )
# Expected: -31.6 + 7.963 x (t = -0.35, 231.3, sigma 82.2);  7.952 x (t =
#           643.3, sigma 72.6)

# Household model: average trips by household size, and the new-town forecast
size = np.array([2, 3, 4, 5, 6])
avg_trips = np.array([5, 7, 8, 10, 10])
t1, i1 = ols(np.column_stack([np.ones(5), size]), avg_trips, ["b0", "b1"])
t2, i2 = ols(size[:, None], avg_trips, ["b1"], intercept=False)
print(
    t1.round(3),
    round(i1["sigma"], 3),
    "\n",
    t2.round(3),
    round(i2["sigma"], 3),
)
# Expected: 2.80 + 1.30 x (t = 3.45, 6.79; sigma 0.606);  1.922 x (t = 15.6;
#           sigma 1.168)

households = np.array([1000, 2000, 1000, 500, 400])
sizes = np.array([2, 4, 6, 8, 10])
print(
    "new town, model through origin:",
    round(t2.loc["b1", "estimate"] * (households * sizes).sum()),
)
print(
    "new town, model with intercept:",
    round(
        t1["estimate"].values @ [households.sum(), (households * sizes).sum()]
    ),
)
# Expected: new town, model through origin: 46133
#           new town, model with intercept: 44920
```

### 比较候选吸引模型

下面的循环拟合 16 小区逐步回归算例中的每个候选模型，并汇总用于在它们之间进行选择的统计量（{prf:ref}`ex-24-tg-stepwise-attraction`）。

```python
# one row per zone: X1 (total), X2, X3, X4 (employment by sector), Y (trips)
data = pd.DataFrame(
    [
        [9482, 6820, 2547, 115, 9428],
        [2010, 111, 1899, 0, 2192],
        [574, 228, 87, 259, 330],
        [127, 0, 127, 0, 153],
        [3836, 2729, 813, 294, 3948],
        [953, 101, 773, 79, 1188],
        [223, 165, 58, 0, 240],
        [36, 6, 30, 0, 556],
        [2223, 1550, 499, 174, 2064],
        [272, 0, 166, 106, 280],
        [50, 0, 48, 2, 280],
        [209, 36, 173, 0, 230],
        [410, 140, 7, 263, 420],
        [11023, 10932, 63, 28, 9654],
        [527, 188, 325, 14, 450],
        [183, 123, 59, 1, 130],
    ],
    columns=["X1", "X2", "X3", "X4", "Y"],
)
# step 2: correlation matrix
print(data.corr().round(3))
# Expected: r(X1, Y) = 0.996, r(X2, Y) = 0.959, r(X1, X2) = 0.978

candidates = {
    "A": (["X1"], True),
    "B": (["X2"], True),
    "C": (["X2", "X3"], True),
    "D": (["X2", "X3"], False),
    "E": (["X2", "X3", "X4"], True),
    "F": (["X2", "X3", "X4"], False),
}
rows = []
for name, (cols, icpt) in candidates.items():
    X = data[cols].values
    names = cols
    if icpt:
        X = np.column_stack([np.ones(len(data)), X])
        names = ["const"] + cols
    table, info = ols(X, data["Y"], names, icpt)
    rows.append(
        {
            "model": name,
            "estimates (t)": ", ".join(
                f"{k} {v:.3f} ({t:.2f})"
                for k, v, t in zip(table.index, table["estimate"], table["t"])
            ),
            "sigma": round(info["sigma"], 1),
            "t_crit": round(info["t_crit"], 3),
        }
    )
print(pd.DataFrame(rows).to_string(index=False))
# Expected: F = 0.884 X2 + 1.234 X3 + 1.041 X4 with t = 49.36, 17.28, 2.43
#           and the smallest sigma (206.8)
```

## 类别模型

家庭交叉分类模型 {eq}`eq-09-cross-class-production` 与人员类别模型 {eq}`eq-09-person-category`（{prf:ref}`ex-24-tg-cross-class`、{prf:ref}`ex-24-tg-person-category`）：

```python
# Household cross-classification: rates (trips/household) and households of
# one zone
rates = pd.DataFrame(
    [
        [3.4, 4.9, 3.7, 5.0, 3.8, 5.1],
        [5.2, 6.9, 7.3, 8.3, 8.0, 10.2],
        [5.8, 7.2, 8.1, 11.8, 10.0, 12.9],
    ],
    index=["no car", "1 car", "2+ cars"],
    columns=["low 1-3", "low 4+", "med 1-3", "med 4+", "high 1-3", "high 4+"],
)
households = pd.DataFrame(0, index=rates.index, columns=rates.columns)
households.loc["no car", "low 1-3"] = 100
households.loc["no car", "low 4+"] = 200
households.loc["1 car", "med 4+"] = 300
households.loc["2+ cars", "high 4+"] = 50
print("HB work trips:", (rates * households).to_numpy().sum())
# Expected: HB work trips: 4455.0

# Person-category vehicle trip rates (HB work/education, HB other, NHB) and
# persons by category
person_rates = np.array(
    [
        [0.63, 0.48, 0.15],
        [0.98, 0.28, 0.27],
        [1.57, 0.83, 0.52],
        [1.61, 0.82, 0.63],
        [0.06, 0.31, 0.11],
        [0.16, 1.04, 0.32],
        [0.21, 1.50, 0.39],
        [0.12, 0.60, 0.28],
    ]
)
persons = np.array([200, 300, 400, 500, 600, 700, 800, 900])
by_purpose = persons @ person_rates
print("by purpose:", by_purpose, " total:", by_purpose.sum())
# Expected: by purpose: [2277. 3576. 1488.]  total: 7341.0
```

## 贝叶斯更新与平衡

贝叶斯更新 {eq}`eq-09-bayes-update` 与出行端的平衡 {eq}`eq-09-balance-attractions`（{prf:ref}`ex-24-tg-bayes`、{prf:ref}`ex-24-tg-balancing`）：

```python
def bayes_update(t1, var1, n1, ts, vars_, ns):
    """Posterior mean and variance of a trip rate.

    Prior: mean t1, trip-rate variance var1, n1 observations; new sample:
    ts, vars_, ns.
    """
    if min(var1, vars_) <= 0 or min(n1, ns) <= 0:
        raise ValueError("variances and sample sizes must be positive")
    # variances of the two means
    s1, ss = var1 / n1, vars_ / ns
    # precisions
    w1, ws = 1 / s1, 1 / ss
    return (w1 * t1 + ws * ts) / (w1 + ws), 1 / (w1 + ws)


for prior, sample in (
    ((8, 64, 65), (12, 144, 30)),
    ((5, 15, 300), (6, 36, 30)),
):
    t2, var2 = bayes_update(*prior, *sample)
    print(f"updated rate {t2:.3f}, variance {var2:.3f}")
# Expected: updated rate 8.681, variance 0.817
#           updated rate 5.040, variance 0.048


def balance_attractions(O, D):
    """Scale the attractions D to the total of the productions O."""
    O, D = np.asarray(O, float), np.asarray(D, float)
    if D.sum() <= 0:
        raise ValueError("the attractions must have a positive total")
    return D * O.sum() / D.sum()


D_balanced = balance_attractions([200, 300, 250], [280, 320, 200])
print(D_balanced, D_balanced.sum())
# Expected: [262.5 300.  187.5] 750.0
```

## 小结

- `ols` 估计含截距和不含截距的回归模型，并返回在二者之间进行选择所用的 $t$ 统计量、$\hat\sigma$ 和 $R^2$（不含截距时为 $R_0^2$）。
- 对候选模型设定进行循环，即可复现吸引模型的逐步选择；{doc}`09-trip-generation`中的逻辑检验仍须由分析人员完成。
- 交叉分类模型和人员类别模型都是出行率与家庭数或人数的矩阵乘积。
- `bayes_update` 实现按精度加权的更新 {eq}`eq-09-bayes-update`，`balance_attractions` 实现缩放 {eq}`eq-09-balance-attractions`。
