# Trip Distribution in Python

## Overview

This chapter implements the growth-factor methods, balancing algorithms,
and gravity models of {doc}`04-biproportional-fitting` and
{doc}`10-trip-distribution`, and
reproduces the worked examples of {doc}`25-examples-trip-distribution`. The
code is not run when the book is built; copy it into a script or notebook
and compare the results with the `# Expected:` comments.

:::{admonition} Learning objectives
:class: objectives
After completing this chapter, readers should be able to:

- implement the uniform, average, Detroit, Fratar, and Furness
  growth-factor methods and compare their convergence;
- implement the Furness (bi-proportional) method with a proper stopping
  rule and structural zeros;
- run singly and doubly constrained gravity models and calibrate $\beta$ to
  an observed mean trip cost;
- implement the tri-proportional method on full and partial matrices; and
- check the consistency of calibration targets with linear programming.
:::

## Setup

The code uses `numpy` and the root finder and linear-programming solver of
`scipy.optimize`.

```python
import numpy as np
from scipy import optimize

np.set_printoptions(precision=3, suppress=True, linewidth=120)
```

## Growth-factor methods

The function `furness` implements {prf:ref}`alg-04-biprop-2`; it is used
below for the doubly constrained growth-factor model and, with the
deterrence matrix as seed, for the gravity model
({prf:ref}`ex-25-td-singly-growth`, {prf:ref}`ex-25-td-furness`).

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

### Comparing the iterative growth-factor methods

The function below implements the general iteration
{eq}`eq-10-growth-iteration` with the growth functions of the average,
Detroit, Fratar, and Furness methods ({prf:ref}`ex-25-td-growth-methods`).

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

### Furness method with inconsistent trip ends

The trip ends are first scaled to a common total; the diagonal cells,
which were not observed, stay zero ({prf:ref}`ex-25-hw2-q1`).

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

## Gravity models

The doubly constrained gravity model is the Furness method applied to the
seed $[f(c_{ij})]$ ({prf:ref}`ex-25-td-gravity`).

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

## Tri-proportional method

The factors $a_i$, $b_j$, and $F_k$ are only determined up to scale; the
implementation renormalizes $b$ in every iteration so that the factors do
not drift, and tests convergence on the cell values. A weight matrix `W`
marks the cells that take part (1 = observed, 0 = missing or structural
zero), which handles partial matrices ({prf:ref}`ex-25-td-tri-proportional`).

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

### Calibration on a partial matrix

Only the observed cells enter the targets and the iterations; the fitted
factors then fill the missing cells ({prf:ref}`ex-25-hw2-q2`).

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

## Summary

- `furness` implements bi-proportional algorithm II with a relative
  stopping rule; zero cells of the seed stay zero, and inconsistent totals
  raise an error instead of making the iterations oscillate.
- `growth_factor` implements the general iteration
  {eq}`eq-10-growth-iteration` with the average, Detroit, Fratar, and
  Furness growth functions; on the three-zone example they need 8, 9, 3,
  and 5 iterations.
- `gravity` computes singly and doubly constrained gravity models
  {eq}`eq-10-gravity`, and a root finder calibrates $\beta$ to an observed
  mean trip cost.
- `tri_proportional` calibrates a stepwise deterrence function
  {eq}`eq-10-stepwise-deterrence` on full or partial matrices, and
  `is_feasible` checks with a linear program that the targets are
  consistent before the iterations start.
