# Preliminaries and Foundations in Python

## Overview

This chapter implements the methods of Parts I and II
({doc}`01-probability-distributions` to {doc}`08-errors-and-uncertainty`)
with `numpy`, `scipy`, and `networkx` and reproduces the numbers of the
corresponding worked examples in Part IV. Each function is written from the
formulas of the theory chapters and uses their notation, so the code can be
read side by side with them. The code is not run when the book is built:
copy it into a script or notebook to run it, and compare the results with
the `# Expected:` comments.

:::{admonition} Learning objectives
:class: objectives
After completing this chapter, readers should be able to:

- evaluate Gumbel, logistic, and normal probabilities and simulate probit
  choice probabilities;
- estimate linear regression models and their tests from the matrix
  formulas;
- implement bisection, Newton's method, Frank–Wolfe, and a label-correcting
  shortest-path algorithm;
- balance a matrix to given margins by bi-proportional fitting;
- convert between population, stratified, and choice-based sample
  distributions and compute choice-based weights; and
- compute sample sizes and propagated errors programmatically.
:::

## Setup

The code was written for Python 3.10 or later with `numpy`, `scipy`,
`pandas`, and `networkx`; the block below holds all imports of the chapter.

```python
from collections import deque

import networkx as nx
import numpy as np
import pandas as pd
from scipy import optimize, stats

np.set_printoptions(precision=3, suppress=True, linewidth=120)
pd.set_option("display.precision", 4)
```

## Probability distributions

`scipy.stats` parameterizes distributions by location and *scale*, where the
scale is $1/\mu$ in the notation of {doc}`01-probability-distributions`.
The two helpers below build $\mathrm{Gumbel}(\eta, \mu)$ of
{eq}`eq-01-gumbel` and $\mathrm{Logistic}(\eta, \mu)$ of
{eq}`eq-01-logistic` from the book's parameters
({prf:ref}`ex-17-uniform`, {prf:ref}`ex-17-normal`,
{prf:ref}`ex-17-gumbel`, {prf:ref}`ex-17-gumbel-difference`,
{prf:ref}`ex-17-bivariate-normal`).

```python
def gumbel(eta, mu):
    """Gumbel(eta, mu) distribution of equation eq-01-gumbel.

    Parameters
    ----------
    eta : float
        Location parameter (the mode).
    mu : float
        Scale parameter of the book (an inverse scale), mu > 0.

    Returns
    -------
    scipy.stats frozen distribution
    """
    if mu <= 0:
        raise ValueError("the scale parameter mu must be positive")
    return stats.gumbel_r(loc=eta, scale=1 / mu)


def logistic(eta, mu):
    """Logistic(eta, mu) distribution of equation eq-01-logistic.

    Parameters
    ----------
    eta : float
        Location parameter (mode, median, and mean).
    mu : float
        Scale parameter of the book (an inverse scale), mu > 0.

    Returns
    -------
    scipy.stats frozen distribution
    """
    if mu <= 0:
        raise ValueError("the scale parameter mu must be positive")
    return stats.logistic(loc=eta, scale=1 / mu)


print("uniform   P(X > 22)  =", round(stats.uniform(15, 10).sf(22), 4))
# stats.norm takes the standard deviation, not the variance
print("normal    P(X <= 30) =", round(stats.norm(20, 10).cdf(30), 4))
G = gumbel(eta=0.5, mu=0.5)
print(
    "Gumbel    P(X <= 5), mean, sd =",
    round(G.cdf(5), 4),
    round(G.mean(), 4),
    round(G.std(), 4),
)
sd = np.sqrt(10 + 5 - 2 * 0.5 * np.sqrt(10 * 5))
print("bivariate P(X - Y <= 15) =", round(stats.norm.cdf((15 - 10) / sd), 4))
# Expected: 0.3, 0.8413, (0.9, 1.6544, 2.5651), 0.9621

# binary logit and log-sum of two Gumbel alternatives
mu = 0.5
V = np.array([-10.0, -12.0])
P1 = logistic(0, mu).cdf(V[0] - V[1])
eta_star = np.log(np.exp(mu * V).sum()) / mu
print(
    f"P(route 1) = {P1:.3f}; location of the maximum = {eta_star:.3f};"
    f" expected maximum = {gumbel(eta_star, mu).mean():.3f}"
)
# Expected: P(route 1) = 0.731; location -9.373; expected maximum -8.219
```

A simulation check that the difference of two independent Gumbel variables
with a common scale is logistic ({prf:ref}`prop-01-logistic`), and the probit
probabilities of {prf:ref}`ex-17-mvn-maximum` with an exact check through
the bivariate normal distribution of the utility differences:

```python
rng = np.random.default_rng(2024)
mu = 0.5
R = 1_000_000
d = gumbel(0, mu).rvs(R, random_state=rng) - gumbel(0, mu).rvs(
    R, random_state=rng
)
ks = stats.kstest(d, logistic(0, mu).cdf)
print(f"KS statistic = {ks.statistic:.4f}, p-value = {ks.pvalue:.2f}")
# Expected: a KS p-value well above 0.05 (no evidence against the logistic
#           law)

mean = np.array([2.0, 2.0, 3.0])
cov = np.array([[2.0, 0.0, 1.0], [0.0, 2.0, 1.0], [1.0, 1.0, 3.0]])
rng = np.random.default_rng(5205)
draws = rng.multivariate_normal(mean, cov, size=2_000_000)
P_hat = np.bincount(draws.argmax(axis=1), minlength=3) / len(draws)
print("P(alternative i is the largest):", P_hat)

# alternative 3 is the largest when X3 - X1 > 0 and X3 - X2 > 0
A = np.array([[-1.0, 0.0, 1.0], [0.0, -1.0, 1.0]])
diff = stats.multivariate_normal(-A @ mean, A @ cov @ A.T)
P3 = diff.cdf(np.zeros(2))
print(f"exact: P3 = {P3:.4f}, P1 = P2 = {(1 - P3) / 2:.4f}")
# Expected: simulated [0.222 0.222 0.556]; exact P3 = 0.5563,
#           P1 = P2 = 0.2218
```

## Linear regression

A single function implements {eq}`eq-02-ols`, the $t$-tests
{eq}`eq-02-t-test`, and the centered {eq}`eq-02-adjusted-r2` or uncentered
{eq}`eq-02-r2-uncentered-mlr` $R^2$, depending on whether the design matrix
contains an intercept ({prf:ref}`ex-18-slr-trips`,
{prf:ref}`ex-18-slr-origin`).

```python
def ols(X, y, names, intercept=True, alpha=0.05):
    """Least-squares estimates and t-tests of a linear regression.

    Parameters
    ----------
    X : array_like, shape (n, p)
        Design matrix; its first column is a column of ones if the model
        has an intercept.
    y : array_like, shape (n,)
        Response vector.
    names : list of str
        Names of the p coefficients.
    intercept : bool
        Whether X contains an intercept column (centered R2) or not
        (uncentered R2).
    alpha : float
        Significance level of the two-sided t-tests.

    Returns
    -------
    table : pandas.DataFrame
        Estimates, standard errors, t statistics, and p-values.
    info : dict
        SSE, sigma, R2, adjusted R2, residual degrees of freedom, and the
        critical t value.
    """
    X, y = np.asarray(X, float), np.asarray(y, float)
    n, p = X.shape
    if len(y) != n or len(names) != p:
        raise ValueError("X, y, and names have inconsistent sizes")
    if n <= p:
        raise ValueError("need more observations than coefficients")
    C = np.linalg.inv(X.T @ X)
    beta = C @ X.T @ y
    e = y - X @ beta
    SS_E = e @ e
    SS_T = ((y - y.mean()) ** 2).sum() if intercept else y @ y
    nu = n - p
    sigma2 = SS_E / nu
    se = np.sqrt(sigma2 * np.diag(C))
    T = beta / se
    table = pd.DataFrame(
        {
            "estimate": beta,
            "std.err": se,
            "t": T,
            "p-value": 2 * stats.t.sf(np.abs(T), nu),
        },
        index=names,
    )
    R2 = 1 - SS_E / SS_T
    R2_adj = 1 - (SS_E / nu) / (SS_T / (n - 1 if intercept else n))
    info = dict(
        SSE=SS_E,
        sigma=np.sqrt(sigma2),
        R2=R2,
        R2_adj=R2_adj,
        df=nu,
        t_crit=stats.t.ppf(1 - alpha / 2, nu),
    )
    return table, info


cars = np.array([200, 50, 500, 100, 100, 400, 300, 400])
trips = np.array([500, 300, 1300, 200, 400, 1200, 900, 1000])

for label, X, names, icpt in (
    (
        "with intercept",
        np.column_stack([np.ones(8), cars]),
        ["b0", "b1"],
        True,
    ),
    ("through origin", cars[:, None], ["b1"], False),
):
    table, info = ols(X, trips, names, intercept=icpt)
    print(f"--- {label}:", {k: round(float(v), 4) for k, v in info.items()})
    print(table.round(4), "\n")
# Expected: with intercept   b0 = 89.857 (t = 1.29), b1 = 2.4786 (t = 10.69),
#           R2 = 0.950, sigma = 102.94
#           through origin   b1 = 2.7336 (t = 21.57), uncentered R2 = 0.985,
#           sigma = 107.71
```

The freight model of {prf:ref}`ex-18-mlr-freight` shows how few residual
degrees of freedom inflate the critical value:

```python
Y = [100, 95, 106, 111, 90]
X = np.column_stack(
    [
        np.ones(5),
        [14, 11, 16, 18, 10],
        [1.6, 1.4, 1.8, 1.9, 1.2],
        [4.2, 4, 5, 5.9, 3.2],
    ]
)
table, info = ols(X, Y, ["b0", "population", "vehicles", "production"])
print({k: round(float(v), 5) for k, v in info.items()})
print(table.round(4))
# Expected: estimates 60.749, 0.811, 10.402, 2.697; t = 115.43, 8.09, 8.74,
#           13.20; t_crit = 12.706
```

The model without an intercept of {prf:ref}`ex-18-mlr-noint`:

```python
Y = [21, 17, 28, 18, 34, 38]
X = np.column_stack(
    [[0.4, 0.4, 3.1, 0.6, 1.7, 9.4], [15.8, 16.3, 3.7, 15.7, 12.3, 4.6]]
)
table, info = ols(X, Y, ["cars", "income"], intercept=False)
print({k: round(float(v), 3) for k, v in info.items()})
print(table.round(3))
# Expected: estimates 3.979, 1.264; t = 4.19, 4.07; uncentered R2 = 0.926,
#           adjusted 0.889; t_crit = 2.776
```

The model with dummy variables ({prf:ref}`ex-18-hw1-q5`):

```python
y = np.array([2, 4, 6, 3, 4, 5, 4, 5, 7, 7])
x1 = np.array([2, 4, 5, 1, 1, 3, 2, 2, 4, 3])
x2 = np.array([0, 0, 1, 1, 1, 1, 2, 2, 3, 2])
z1, z2 = (x2 == 1).astype(float), (x2 >= 2).astype(float)
one = np.ones(len(y))

models = {
    "Model 1": (
        np.column_stack([one, x1, x2]),
        ["b0", "workers", "cars"],
        True,
        [1, 2, 0.65],
    ),
    "Model 2": (
        np.column_stack([one, x1, z1, z2]),
        ["b0", "workers", "z1", "z2"],
        True,
        [1, 2, 0.35, 0.15],
    ),
    "Model 2, no b0": (
        np.column_stack([x1, z1, z2]),
        ["workers", "z1", "z2"],
        False,
        [2, 0.35, 0.15],
    ),
}
for name, (X, names, icpt, zone_means) in models.items():
    table, info = ols(X, y, names, intercept=icpt)
    O_i = 1000 * table["estimate"].values @ np.array(zone_means)
    print(
        f"--- {name}: R2 = {info['R2']:.3f}, adj. R2 = {info['R2_adj']:.3f}, "
        f"sigma = {info['sigma']:.3f},"
        f" t_crit = {info['t_crit']:.3f}, O_i = {O_i:,.0f}"
    )
    print(table.round(3), "\n")
# Expected: Model 1          adj. R2 0.763, sigma 0.796, O_i = 3,474
#           Model 2          adj. R2 0.787, sigma 0.756, O_i = 3,300
#           Model 2, no b0   sigma 0.730, all t > 2.365,  O_i = 3,087
```

### Two-sample test

The large-sample test {eq}`eq-02-two-sample-z` of
{prf:ref}`ex-18-two-means`:

```python
def two_sample_z(x1, x2):
    """Large-sample z statistic and two-sided p-value for mu_1 = mu_2.

    Parameters
    ----------
    x1, x2 : array_like
        The two independent samples.

    Returns
    -------
    z0 : float
        Test statistic of equation eq-02-two-sample-z.
    p : float
        Two-sided p-value 2[1 - Phi(|z0|)].
    """
    x1, x2 = np.asarray(x1, float), np.asarray(x2, float)
    if len(x1) < 2 or len(x2) < 2:
        raise ValueError("each sample needs at least two observations")
    se = np.sqrt(x1.var(ddof=1) / len(x1) + x2.var(ddof=1) / len(x2))
    z0 = (x1.mean() - x2.mean()) / se
    return z0, 2 * stats.norm.sf(abs(z0))


morning = np.array(
    (
        "6.491 7.253 6.604 7.131 6.779 6.863 6.622 7.843 7.903 7.166 "
        "8.420 7.941 6.789 6.601 8.287 5.741 7.433 6.995 7.822 6.712 "
        "7.359 7.075 7.456 6.386 6.683 8.229 6.918 7.895 7.050 6.145 "
        "7.248 8.104 7.157 7.163 6.403 7.211 8.080 5.536 6.361 7.091 "
        "8.614 6.004 6.930 6.624 7.028 7.012 5.579 6.644"
    ).split(),
    dtype=float,
)
afternoon = np.array(
    (
        "6.485 7.252 7.966 7.490 8.703 6.725 7.648 7.386 9.985 7.926 "
        "9.185 7.440 8.797 7.235 9.731 7.816 7.801 7.496 8.214 8.543 "
        "7.598 8.059 7.809 6.955 7.721 6.340 8.415 8.356 8.098 7.773 "
        "8.437 7.930 7.086 8.138 6.936 8.782 8.410 6.575 7.699 6.988 "
        "8.090 8.461 7.238"
    ).split(),
    dtype=float,
)
z0, p = two_sample_z(morning, afternoon)
print(
    f"means {morning.mean():.3f}, {afternoon.mean():.3f};"
    f"  z0 = {z0:.3f};  p = {p:.1e}"
)
# Welch test, for comparison
print(stats.ttest_ind(morning, afternoon, equal_var=False))
# Expected: means 7.070 and 7.854, z0 = -4.888, p = 1.0e-06
```

## Optimization

### Line searches

{prf:ref}`alg-03-bisection` and {prf:ref}`alg-03-newton`, applied to
{prf:ref}`ex-19-bisection` and {prf:ref}`ex-19-newton`:

```python
def bisection(dz, a, b, eps=1e-3, max_iter=100):
    """Bisection line search on [a, b] (algorithm alg-03-bisection).

    Parameters
    ----------
    dz : callable
        Derivative z'(x) of the convex function to minimize.
    a, b : float
        Interval ends, with z'(a) < 0 < z'(b).
    eps : float
        Stop when the interval is shorter than eps.
    max_iter : int
        Maximum number of iterations.

    Returns
    -------
    x : float
        Midpoint of the final interval.
    history : pandas.DataFrame
        One row per iteration.
    """
    if not a < b:
        raise ValueError("need a < b")
    if eps <= 0:
        raise ValueError("eps must be positive")
    if not dz(a) < 0 < dz(b):
        raise ValueError("need z'(a) < 0 < z'(b)")
    history = []
    for k in range(max_iter):
        if b - a <= eps:
            break
        x = (a + b) / 2
        g = dz(x)
        history.append((k, a, b, x, g))
        if g > 0:
            b = x
        elif g < 0:
            a = x
        else:
            a = b = x
    columns = ["k", "a_k", "b_k", "x_k", "z'(x_k)"]
    return (a + b) / 2, pd.DataFrame(history, columns=columns)


def newton(dz, d2z, x0, eps=1e-8, max_iter=20):
    """Newton's method for z'(x) = 0 (algorithm alg-03-newton).

    Parameters
    ----------
    dz, d2z : callable
        First and second derivatives of z.
    x0 : float
        Starting point.
    eps : float
        Stop when |z'(x_k)| <= eps.
    max_iter : int
        Maximum number of iterations.

    Returns
    -------
    x : float
        Last iterate (a stationary point, not necessarily a minimum).
    history : pandas.DataFrame
        One row per iteration.
    """
    if eps <= 0:
        raise ValueError("eps must be positive")
    x, history = x0, []
    for k in range(max_iter):
        g, h = dz(x), d2z(x)
        history.append((k, x, g, h))
        if abs(g) <= eps:
            break
        if h == 0:
            raise ValueError(f"z''(x_k) = 0 at x_k = {x}")
        x = x - g / h
    columns = ["k", "x_k", "z'(x_k)", "z''(x_k)"]
    return x, pd.DataFrame(history, columns=columns)


x_bis, hist = bisection(np.cos, 3, 6, eps=0.03)
print(hist.round(6).to_string(index=False), "\n")
for x0 in (4.0, 3.0):
    x_newton, hist = newton(np.cos, lambda x: -np.sin(x), x0)
    print(
        f"Newton from {x0}: x* = {x_newton:.6f},"
        f" sin(x*) = {np.sin(x_newton):+.3f}"
    )
# Expected: the bisection table of the worked example, ending with
#           x_6 = 4.7109 and z'(x_6) = -0.0015;
#           Newton from 4.0 -> 4.712389 (a minimum, sin = -1),
#           Newton from 3.0 -> -4.712389 (a maximum, sin = +1)
```

### Frank–Wolfe

The linear subproblem of {prf:ref}`alg-03-frank-wolfe` is solved with
`scipy.optimize.linprog` and the line search with
`scipy.optimize.minimize_scalar` on $[0, 1]$ ({prf:ref}`ex-19-frank-wolfe`).

```python
def frank_wolfe(f, grad, A_ub, b_ub, x0, eps=0.01, max_iter=100):
    """Frank-Wolfe method on {x >= 0 : A_ub x <= b_ub} (alg-03-frank-wolfe).

    Parameters
    ----------
    f, grad : callable
        Convex objective and its gradient.
    A_ub, b_ub : array_like
        Linear inequality constraints; x >= 0 is added.
    x0 : array_like
        Feasible starting point.
    eps : float
        Stop when the gap of equation eq-03-fw-gap is at most eps.
    max_iter : int
        Maximum number of iterations.

    Returns
    -------
    x : numpy.ndarray
        Last iterate.
    history : pandas.DataFrame
        Iterate, objective, LP solution, and gap of each iteration.
    """
    x = np.asarray(x0, float)
    A_ub, b_ub = np.asarray(A_ub, float), np.asarray(b_ub, float)
    if np.any(x < 0) or np.any(A_ub @ x > b_ub):
        raise ValueError("the starting point x0 is not feasible")
    rows = []
    for k in range(max_iter):
        g = grad(x)
        y = optimize.linprog(
            g, A_ub=A_ub, b_ub=b_ub, bounds=[(0, None)] * len(x)
        ).x
        gap = -g @ (y - x)
        rows.append((k, *x, f(x), *y, gap))
        if gap <= eps:
            break
        alpha = optimize.minimize_scalar(
            lambda a: f(x + a * (y - x)), bounds=(0, 1), method="bounded"
        ).x
        x = x + alpha * (y - x)
    columns = ["k", "x1", "x2", "f(x)", "y1", "y2", "gap"]
    return x, pd.DataFrame(rows, columns=columns)


def f(x):
    """Objective of equation eq-19-example-qp."""
    return (x[0] - 2) ** 2 + (x[1] - 3) ** 2


def grad_f(x):
    """Gradient of the objective of equation eq-19-example-qp."""
    return np.array([2 * (x[0] - 2), 2 * (x[1] - 3)])


x_star, hist = frank_wolfe(f, grad_f, A_ub=[[1, 1]], b_ub=[2], x0=[0, 0])
print(hist.round(4).to_string(index=False))
# Expected: iterates (0, 0) -> (0, 2) -> (0.5, 1.5); f = 13, 5, 4.5; gaps 12,
#           4, 0
```

When the LP has ties (iteration 3), `linprog` may return either vertex;
the gap is zero in both cases.

### Shortest paths

{prf:ref}`alg-03-label-correcting` with a first-in, first-out sequence list,
checked against Dijkstra's algorithm in `networkx`
({prf:ref}`ex-19-shortest-path`):

```python
def label_correcting(links, root):
    """Label-correcting shortest paths (algorithm alg-03-label-correcting).

    Parameters
    ----------
    links : dict
        {(i, j): t_ij} with non-negative link costs t_ij.
    root : hashable
        Root node r.

    Returns
    -------
    label : dict
        Shortest-path length l_i from r to every node i.
    pred : dict
        Predecessor p_i of every node on its shortest path (None for r and
        for unreachable nodes).
    """
    if any(t < 0 for t in links.values()):
        raise ValueError("link costs must be non-negative")
    nodes = {n for link in links for n in link}
    if root not in nodes:
        raise ValueError(f"root {root!r} is not a node of the network")
    out = {}
    for (i, j), t in links.items():
        out.setdefault(i, []).append((j, t))
    label = {n: np.inf for n in nodes}
    pred = {n: None for n in nodes}
    label[root] = 0.0
    Q = deque([root])
    while Q:
        i = Q.popleft()
        for j, t in out.get(i, []):
            if label[i] + t < label[j]:
                label[j], pred[j] = label[i] + t, i
                if j not in Q:
                    Q.append(j)
    return label, pred


def path_to(pred, node):
    """Path from the root to node, read backwards through the predecessors.

    Parameters
    ----------
    pred : dict
        Predecessors returned by label_correcting.
    node : hashable
        Destination node.

    Returns
    -------
    list
        Nodes of the path, from the root to node.
    """
    if node not in pred:
        raise ValueError(f"unknown node {node!r}")
    path = [node]
    while pred[path[-1]] is not None:
        path.append(pred[path[-1]])
    return path[::-1]


links = {(1, 4): 4, (1, 2): 1, (2, 3): 1, (3, 4): 1}
label, pred = label_correcting(links, root=1)
print("labels:", label, " path to 4:", path_to(pred, 4))

G = nx.DiGraph()
G.add_weighted_edges_from((i, j, t) for (i, j), t in links.items())
print(
    "networkx Dijkstra:",
    nx.dijkstra_path(G, 1, 4),
    nx.dijkstra_path_length(G, 1, 4),
)
# Expected: labels {1: 0, 2: 1, 3: 2, 4: 3}, path [1, 2, 3, 4], length 3
```

## Bi-proportional fitting

{prf:ref}`alg-04-biprop-1` alternately scales the rows and the columns, and
the information distance {eq}`eq-04-bp-information` checks
{prf:ref}`thm-04-bp-information` ({prf:ref}`ex-20-bp-ras`,
{prf:ref}`ex-20-bp-infeasible`).

```python
def biproportional(t, O, D, eps=1e-4, max_iter=1000):
    """Bi-proportional algorithm I (matrix scaling, alg-04-biprop-1).

    Parameters
    ----------
    t : array_like, shape (m, n)
        Non-negative seed matrix t_ij.
    O, D : array_like
        Positive row targets O_i and column targets D_j.
    eps : float
        Stop when every row total is within eps (relative) of its target.
    max_iter : int
        Maximum number of iterations.

    Returns
    -------
    T : numpy.ndarray
        Balanced matrix after the last column step.
    r : int
        Number of iterations.
    err : float
        Largest relative error of the row totals.
    """
    T = np.asarray(t, float).copy()
    O, D = np.asarray(O, float), np.asarray(D, float)
    if T.shape != (len(O), len(D)):
        raise ValueError("the seed does not match the numbers of targets")
    if np.any(T < 0) or np.any(O <= 0) or np.any(D <= 0):
        raise ValueError("need a non-negative seed and positive targets")
    if not np.isclose(O.sum(), D.sum()):
        raise ValueError("inconsistent targets: sum(O) != sum(D)")
    for r in range(1, max_iter + 1):
        # row step, then column step (the column totals are then exact)
        T *= (O / T.sum(axis=1))[:, None]
        T *= (D / T.sum(axis=0))[None, :]
        err = np.max(np.abs(T.sum(axis=1) - O) / O)
        if err <= eps:
            break
    return T, r, err


def information(T, t):
    """Information (Kullback-Leibler) distance I(T, t), eq-04-bp-information.

    Parameters
    ----------
    T, t : array_like
        Estimated and seed matrices of equal shape; the sum runs over the
        cells with t_ij > 0.

    Returns
    -------
    float
    """
    T, t = np.asarray(T, float), np.asarray(t, float)
    if T.shape != t.shape:
        raise ValueError("T and t must have the same shape")
    k = t > 0
    return np.sum(T[k] * np.log(T[k] / t[k]) - T[k] + t[k])


t = np.array([[20, 10, 10], [10, 30, 10], [10, 10, 40]], float)
T, r, err = biproportional(t, O=[50, 60, 70], D=[40, 60, 80])
print(T.round(2), "\niterations:", r, " largest row error:", f"{err:.1e}")

# the cross-product ratio is preserved
print("ratio:", T[0, 0] * T[1, 1] / (T[0, 1] * T[1, 0]))

# a margin-preserving perturbation increases the information distance
P = np.array([[1, -1, 0], [-1, 1, 0], [0, 0, 0]], float)
print([round(float(information(M, t)), 3) for M in (T, T + P, T - P)])
# Expected: [[21.43 13.15 15.42] [ 9.8 36.09 14.11] [ 8.77 10.76 50.48]]
#           iterations: 5; ratio: 6.0; distances [4.46, 4.588, 4.584]

# targets incompatible with the zero cell (1, 2): no convergence
T, r, err = biproportional([[5, 0], [3, 2]], O=[6, 4], D=[3, 7], max_iter=50)
print(T.round(3), "row totals:", T.sum(axis=1).round(3), "error:", err)
# Expected: [[3. 0.] [0. 7.]], row totals [3. 7.], error 0.75 after 50 steps
```

## Sampling

### Joint distributions under three sampling methods

The functions below implement {eq}`eq-07-stratified-joint` and
{eq}`eq-07-choice-based-joint` for a population table with choices in rows and
strata in columns ({prf:ref}`ex-22-three-samples`).

```python
def stratified_sample(pop, f_x):
    """Joint sample distribution f(Y, X) = f(X) Pr(Y | X).

    Parameters
    ----------
    pop : array_like
        Population distribution Pr(Y, X): rows = choices Y, columns =
        strata X.
    f_x : array_like
        Sample shares f(X) of the strata.

    Returns
    -------
    numpy.ndarray
    """
    pop, f_x = np.asarray(pop, float), np.asarray(f_x, float)
    if len(f_x) != pop.shape[1] or not np.isclose(f_x.sum(), 1):
        raise ValueError("f_x must give one share per stratum, summing to 1")
    return pop / pop.sum(axis=0) * f_x


def choice_based_sample(pop, f_y):
    """Joint sample distribution f(Y, X) = f(Y) Pr(X | Y).

    Parameters
    ----------
    pop : array_like
        Population distribution Pr(Y, X): rows = choices Y, columns =
        strata X.
    f_y : array_like
        Sample shares f(Y) of the choices.

    Returns
    -------
    numpy.ndarray
    """
    pop, f_y = np.asarray(pop, float), np.asarray(f_y, float)
    if len(f_y) != pop.shape[0] or not np.isclose(f_y.sum(), 1):
        raise ValueError("f_y must give one share per choice, summing to 1")
    return pop / pop.sum(axis=1, keepdims=True) * f_y[:, None]


pop = pd.DataFrame(
    [[0.45, 0.15], [0.20, 0.20]], index=["bus", "car"], columns=["LI", "HI"]
)
strat = pd.DataFrame(
    stratified_sample(pop.values, [0.75, 0.25]),
    index=pop.index,
    columns=pop.columns,
)
cb = pd.DataFrame(
    choice_based_sample(pop.values, [0.75, 0.25]),
    index=pop.index,
    columns=pop.columns,
)
print(
    "stratified sample:\n",
    strat.round(4),
    "\n\nchoice-based sample:\n",
    cb.round(4),
)
# Expected: stratified   bus 0.5192 0.1071 / car 0.2308 0.1429
#           choice-based bus 0.5625 0.1875 / car 0.1250 0.1250
```

The conditional probability of car use among high-income travelers in each
sample, and the weighted correction of {eq}`eq-07-choice-based-weights`:

```python
def p_car_given_hi(table):
    """Share of car users among the high-income travelers of a table."""
    return table.loc["car", "HI"] / table["HI"].sum()


# w_Y = Pr(Y) / f(Y)
w = pop.sum(axis=1) / cb.sum(axis=1)
weighted = cb.mul(w, axis=0)
print(
    {
        name: round(float(p_car_given_hi(table)), 4)
        for name, table in [
            ("population", pop),
            ("stratified", strat),
            ("choice-based", cb),
            ("weighted", weighted),
        ]
    }
)
print("weights:", w.round(3).to_dict())
# Expected: population 0.5714, stratified 0.5714, choice-based 0.4, weighted
#           0.5714
#           weights {"bus": 0.8, "car": 1.6}
```

### Population shares from two samples

```python
modes = ["car", "bus", "underground"]
incomes = ["low", "medium", "high"]
f_strat = (
    pd.DataFrame(
        [[3.33, 18.00, 20.00], [33.34, 7.20, 4.00], [3.33, 4.80, 6.00]],
        index=modes,
        columns=incomes,
    )
    / 100
)
f_cb = (
    pd.DataFrame(
        [[6.67, 20.00, 13.33], [17.24, 2.07, 0.69], [16.67, 13.33, 10.00]],
        index=modes,
        columns=incomes,
    )
    / 100
)
p_income = pd.Series([0.60, 0.25, 0.15], index=incomes)

# Pr(Y, X) = Pr(X) f(Y, X) / f(X)
population = f_strat / f_strat.sum(axis=0) * p_income
print((100 * population).round(2))
print("mode shares (%):", (100 * population.sum(axis=1)).round(2).to_dict())
print(
    "weights:", (population.sum(axis=1) / f_cb.sum(axis=1)).round(3).to_dict()
)
# Expected: mode shares car 30.0, bus 58.01, underground 12.0 (%)
#           weights car 0.75, bus 2.90, underground 0.30
```

The low-income entries are 4.995 % and 50.01 % only because the data were
rounded to 3.33 % and 33.34 %; the exact values are 5 % and 50 %
({prf:ref}`ex-22-hw1-q4`).

### Subpopulation shares and sample sizes

```python
A = np.array([[78_000, 14_400, 38_400], [1.15, 0.05, 0.85], [1, 1, 1]])
b = np.array([33_600, 0.44, 1])
F = np.linalg.solve(A, b)
print("shares F:", F.round(4), " users:", (180_000 * F).round(-2))
# Expected: shares [0.245 0.604 0.15 ], users [44100 108800 27100]
```

```python
def n_mean(cv, rel_error, conf=0.95):
    """Sample size for a mean with relative error E: n = z^2 CV^2 / E^2.

    Parameters
    ----------
    cv : float
        Coefficient of variation of the variable.
    rel_error : float
        Admissible relative error E > 0.
    conf : float
        Confidence level, 0 < conf < 1.

    Returns
    -------
    float
    """
    if rel_error <= 0 or not 0 < conf < 1:
        raise ValueError("need rel_error > 0 and 0 < conf < 1")
    z = stats.norm.ppf(1 - (1 - conf) / 2)
    return (z * cv / rel_error) ** 2


def n_proportion(N, e=0.1, conf=0.95, p=0.5):
    """Sample size for a proportion with finite population correction.

    Parameters
    ----------
    N : int
        Population size.
    e : float
        Admissible absolute error.
    conf : float
        Confidence level, 0 < conf < 1.
    p : float
        Assumed proportion (0.5 gives the largest sample).

    Returns
    -------
    float
    """
    if N <= 0 or e <= 0 or not 0 < conf < 1:
        raise ValueError("need N > 0, e > 0, and 0 < conf < 1")
    z = stats.norm.ppf(1 - (1 - conf) / 2)
    return p * (1 - p) / ((e / z) ** 2 + p * (1 - p) / N)


print("household survey:", round(n_mean(cv=1.0, rel_error=0.05, conf=0.90), 1))
print("384 CV^2 rule   :", round(n_mean(cv=1.0, rel_error=0.10, conf=0.95), 1))
flows = [100, 500, 1_000, 2_000, 5_000, 10_000]
print("roadside n*     :", {N: int(np.ceil(n_proportion(N))) for N in flows})
# Expected: 1082.2, 384.1, and {100: 49, 500: 81, 1000: 88, 2000: 92, 5000: 95,
#           10000: 96}
```

The household value differs slightly from the 1 082.4 of
{prf:ref}`ex-22-household-sample-size` because `scipy` uses the exact quantile
$z_{0.05} = 1.6449$ rather than 1.645.

## Error propagation

The function below implements {eq}`eq-08-error-propagation` with numerical
derivatives (central differences), so it works for any model written as a
Python function.

```python
def propagate(f, x, e, corr=None, h=1e-6):
    """First-order error of f at x (equation eq-08-error-propagation).

    Parameters
    ----------
    f : callable
        Model z = f(x_1, ..., x_k).
    x : array_like
        Values of the inputs.
    e : array_like
        Errors (standard deviations) of the inputs.
    corr : array_like, optional
        Correlation matrix of the inputs (default: independent).
    h : float
        Step of the central differences.

    Returns
    -------
    z : float
        Value of the model.
    e_z : float
        Propagated error.
    grad : numpy.ndarray
        Partial derivatives of f at x.
    """
    x, e = np.asarray(x, float), np.asarray(e, float)
    if x.shape != e.shape:
        raise ValueError("x and e must have the same length")
    I = np.eye(len(x))
    grad = np.array(
        [
            (f(*(x + h * I[i])) - f(*(x - h * I[i]))) / (2 * h)
            for i in range(len(x))
        ]
    )
    corr = I if corr is None else np.asarray(corr, float)
    cov = np.outer(e, e) * corr
    return f(*x), float(np.sqrt(grad @ cov @ grad)), grad


ops = {
    "x + y": lambda x, y: x + y,
    "x - y": lambda x, y: x - y,
    "x * y": lambda x, y: x * y,
    "x / y": lambda x, y: x / y,
    "x ** 2": lambda x, y: x**2,
}
rows = []
for name, model in ops.items():
    z, e_z, _ = propagate(model, [10, 8], [1, 1])
    rows.append((name, z, e_z, 100 * e_z / z))
print(pd.DataFrame(rows, columns=["model", "z", "e_z", "e_z/z (%)"]).round(3))
# Expected relative errors: 7.86, 70.71, 16.01, 16.01, 20.00 %
```

The value of better data ({prf:ref}`ex-23-value-better-data`):

```python
def model(x, y, w):
    """Model z = xy + w of the worked example."""
    return x * y + w


z, e_z, grad = propagate(model, [100, 50, 200], [10, 5, 50])
# marginal rate (df/dx_i)^2 e_i / e_z
rates = grad**2 * np.array([10, 5, 50]) / e_z
cost = np.array([5.00, 6.00, 0.02])
print(f"e_z = {e_z:.2f}")
print(
    pd.DataFrame(
        {"marginal rate": rates, "cost per unit of e_z": cost / rates},
        index=["x", "y", "w"],
    ).round(4)
)
# Expected: e_z = 708.87; rates 35.27, 70.53, 0.0705; cost per unit 0.142,
#           0.085, 0.284
```

Forecasting population ({prf:ref}`ex-23-hw1-q3`):

```python
P2020_a, e_a, _ = propagate(
    lambda p90, p00: p00**3 / p90**2, [25_000, 26_000], [500, 300]
)
P2020_b, e_b, _ = propagate(
    lambda p00, p10: p10**2 / p00, [26_000, 27_500], [300, 850]
)
for label, P, e, d in (
    ("(a) base 2000", P2020_a, e_a, 2),
    ("(b) base 2010", P2020_b, e_b, 1),
):
    # add a specification error of 10 % per decade forecast ahead
    total = np.hypot(e, 0.10 * d * P)
    print(
        f"{label}: P = {P:,.1f} ± {e:,.1f} ({100 * e / P:.2f} %);"
        f" with specification error ± {total:,.0f} ({100 * total / P:.1f} %)"
    )
# Expected: (a) 28,121.6 ± 1,487.6 (5.29 %), with specification error ± 5,818
#           (20.7 %)
#           (b) 29,086.5 ± 1,829.1 (6.29 %), with specification error ± 3,436
#           (11.8 %)
```

## Summary

- `scipy.stats` uses scale $= 1/\mu$ for the Gumbel and logistic
  distributions; the helpers `gumbel` and `logistic` take the book's
  parameters $(\eta, \mu)$.
- Linear regression and its tests follow directly from
  $(\bX\T\bX)^{-1}\bX\T\by$; libraries such as `statsmodels` give the same
  results with more diagnostics.
- Frank–Wolfe needs only an LP solver and a line search; in traffic
  assignment the LP becomes a shortest-path computation
  ({doc}`36-python-traffic-assignment`).
- Bi-proportional fitting is two lines of `numpy` per iteration; check the
  margin that was not fitted last, and treat non-convergence as a sign of
  infeasible targets.
- Sampling tables, weights, and sample sizes are a few lines of `numpy`, and
  a generic error-propagation function with numerical derivatives handles
  any model.
