# Nonlinear Optimization for Network Analysis

## Overview

The equilibrium models of traffic assignment
({doc}`13-user-equilibrium-assignment`), matrix balancing and entropy
maximization ({doc}`04-biproportional-fitting`), and the trip distribution
models built on them ({doc}`10-trip-distribution`) are solved by writing them as
convex optimization problems. This chapter collects the optimization theory
those chapters need: convex sets and functions, the Karush–Kuhn–Tucker
(KKT) optimality conditions, one-dimensional line searches, the Frank–Wolfe
method for problems with linear constraints, and the shortest-path algorithm
that turns Frank–Wolfe into a practical assignment method.

:::{admonition} Learning objectives
:class: objectives
After completing this chapter, readers should be able to:

- compute gradients and Hessians and check the convexity of a function;
- distinguish local and global minima and explain why convex programs have
  no spurious local minima;
- write and verify the KKT conditions of a constrained problem;
- carry out the bisection and Newton line searches;
- carry out the Frank–Wolfe method and interpret its stopping criterion as
  an optimality gap; and
- find shortest paths with a label-correcting algorithm.
:::

## Notation

| Symbol | Meaning |
|---|---|
| $\bx = (x_1, \ldots, x_n)\T$ | vector of decision variables |
| $f(\bx)$ | objective function |
| $\Omega \subseteq \R^n$ | feasible set |
| $\nabla f(\bx)$, $\nabla^2 f(\bx)$ | gradient vector and Hessian matrix |
| $g_i(\bx) \le 0$, $h_j(\bx) = 0$ | inequality and equality constraints |
| $u_i$, $\lambda_j$ | Lagrange (KKT) multipliers |
| $\alpha$ | step size in a line search |

## Optimization problems

A (nonlinear) program asks for values of the decision variables that
minimize an objective subject to constraints:

$$
\begin{aligned}
\min_{\bx}\quad & f(\bx) \\
\text{s.t.}\quad & g_i(\bx) \le 0, \qquad i = 1, \ldots, m_1, \\
& h_j(\bx) = 0, \qquad j = 1, \ldots, m_2 .
\end{aligned}
$$ (eq-03-nlp)

Writing $\Omega = \{\bx : g_i(\bx) \le 0\ \forall i,\ h_j(\bx) = 0\ \forall j\}$
for the **feasible set**, the problem is $\min_{\bx \in \Omega} f(\bx)$.
Maximizing $f$ is the same as minimizing $-f$.

:::{prf:definition} Global and local minima
:label: def-03-minimum

A point $\bx^* \in \Omega$ is a **global minimum** if
$f(\bx) \ge f(\bx^*)$ for every $\bx \in \Omega$, and a **local minimum** if
$f(\bx) \ge f(\bx^*)$ for every $\bx \in \Omega$ in some neighborhood of
$\bx^*$.
:::

A function can have several local minima, and on a bounded feasible set the
global minimum may lie on the boundary rather than at a stationary point.

## Gradients, Hessians, and convexity

### Gradient and Hessian

For a differentiable function $f: \R^n \to \R$, the **gradient** and the
**Hessian** at $\bx$ are

$$
\nabla f(\bx) = \begin{bmatrix}
\partial f/\partial x_1 \\ \vdots \\ \partial f/\partial x_n
\end{bmatrix},
\qquad
\nabla^2 f(\bx) = \left[\frac{\partial^2 f}{\partial x_i\,\partial x_j}\right]_{n\times n}.
$$

For example, $f_1(\bx) = (x_1 - 2)^2 + (x_2 - 2)^2$ has
$\nabla f_1 = (2(x_1 - 2),\ 2(x_2 - 2))\T$ and
$\nabla^2 f_1 = \diag(2, 2)$, while the linear function
$f_2(\bx) = 2x_1 + 3x_2 + 0.5x_3 - x_4$ has the constant gradient
$(2, 3, 0.5, -1)\T$ and a zero Hessian.

### Convex sets and functions

:::{prf:definition} Convex set
:label: def-03-convex-set

A set $\Omega \subseteq \R^n$ is **convex** if, for all
$\bx_1, \bx_2 \in \Omega$ and all $\alpha \in [0, 1]$,
$\bx_1 + \alpha(\bx_2 - \bx_1) \in \Omega$; that is, the segment between any
two points of the set lies in the set.
:::

Polyhedra $\{\bx : \bA\bx \le \bb\}$ and discs are convex.
The set defined by linear constraints that describe flow conservation in a
network is a polyhedron, hence convex.

:::{prf:definition} Convex and strictly convex functions
:label: def-03-convex-function

A function $f$ is **convex** on a convex set $\Omega$ if, for all
$\bx_1, \bx_2 \in \Omega$ and all $\alpha \in [0, 1]$,

$$
f\big(\bx_1 + \alpha(\bx_2 - \bx_1)\big) \le f(\bx_1) + \alpha\big[f(\bx_2) - f(\bx_1)\big],
$$

and **strictly convex** if the inequality is strict whenever
$\bx_1 \ne \bx_2$ and $\alpha \in (0, 1)$. Geometrically, the chord between
any two points of the graph lies above the graph.
:::

For twice-differentiable functions, convexity can be checked with the
Hessian.

:::{prf:theorem} Second-order test for convexity
:label: thm-03-convexity-test

Let $f$ be twice continuously differentiable on an open convex set
$\Omega$.

1. $f$ is convex on $\Omega$ if and only if $\nabla^2 f(\bx)$ is positive
   semidefinite for every $\bx \in \Omega$.
2. If $\nabla^2 f(\bx)$ is positive definite for every $\bx \in \Omega$,
   then $f$ is strictly convex on $\Omega$.
:::

The second statement is only *sufficient*: $f(x) = x^4$ is strictly convex
although $f''(0) = 0$. In the examples above, $f_1$ is strictly convex
(its Hessian is positive definite), while $f_2$ is convex but not strictly
convex; every linear function is both convex and concave.

A symmetric matrix $\bH$ is **positive definite** if
$\bd\T\bH\bd > 0$ for all $\bd \ne \bzero$, and **positive
semidefinite** if $\bd\T\bH\bd \ge 0$. Equivalent tests:

- all eigenvalues of $\bH$ are positive (definite) or non-negative
  (semidefinite);
- (Sylvester's criterion) all leading principal minors of $\bH$ are
  positive — this test is valid for definiteness; for semidefiniteness
  *all* principal minors, not only the leading ones, must be non-negative.

A diagonal matrix with positive diagonal entries is positive definite. This
simple case is the one that occurs in traffic assignment, where the Hessian
of Beckmann's objective is diagonal when each link travel time depends only
on the flow of that link.

### Convex programs

:::{prf:definition} Convex program
:label: def-03-convex-program

Problem {eq}`eq-03-nlp` is a **convex program** if the feasible set $\Omega$
is convex and the objective $f$ is convex on $\Omega$. This holds, in
particular, if every $g_i$ is convex and every $h_j$ is affine (linear plus
a constant).
:::

:::{prf:theorem} Optimality in convex programs
:label: thm-03-convex-program

1. Every local minimum of a convex program is a global minimum.
2. If the objective is strictly convex, the global minimum, if it exists, is
   unique.
:::

These two facts explain why traffic equilibrium is formulated as a convex
program: any algorithm that finds a local minimum has found *the*
equilibrium, and strict convexity implies the uniqueness of equilibrium
link flows.

## The Karush–Kuhn–Tucker conditions

Define the **Lagrangian** of {eq}`eq-03-nlp`,

$$
\begin{aligned}
\mathcal{L}(\bx, \bu, \blambda) &= f(\bx) + \sum_{i=1}^{m_1} u_i\, g_i(\bx) + \sum_{j=1}^{m_2}\lambda_j\, h_j(\bx).
\end{aligned}
$$

:::{prf:theorem} Karush–Kuhn–Tucker conditions
:label: thm-03-kkt

If $\bx^*$ is a local minimum of {eq}`eq-03-nlp` and a constraint
qualification holds at $\bx^*$, there exist multipliers
$u_1, \ldots, u_{m_1}$ and $\lambda_1, \ldots, \lambda_{m_2}$ such that

$$
\begin{aligned}
&\nabla f(\bx^*) + \sum_{i=1}^{m_1} u_i\nabla g_i(\bx^*)
   + \sum_{j=1}^{m_2}\lambda_j\nabla h_j(\bx^*) = \bzero
   && \text{(stationarity)} \\
&u_i \ge 0, \quad i = 1, \ldots, m_1
   && \text{(dual feasibility)} \\
&u_i\, g_i(\bx^*) = 0, \quad i = 1, \ldots, m_1
   && \text{(complementary slackness)} \\
&g_i(\bx^*) \le 0, \quad i = 1, \ldots, m_1
   && \text{(primal feasibility)} \\
&h_j(\bx^*) = 0, \quad j = 1, \ldots, m_2
   && \text{(primal feasibility)}
\end{aligned}
$$

For a convex program the KKT conditions are also **sufficient**: any point
satisfying them is a global minimum.
:::

Complementary slackness says that a multiplier can be positive only if its
constraint is binding. The multiplier $u_i$ is the rate at which the
optimal objective value would decrease if constraint $i$ were relaxed, that
is, approximately the improvement per unit of relaxation. Common
constraint qualifications are linear independence of the gradients of the
active constraints, or — for convex programs — Slater's condition (there is
a strictly feasible point). Linear constraints always satisfy a constraint
qualification, which covers all the network problems in this book.

For problems with non-negativity constraints $x_i \ge 0$, writing them as
$-x_i \le 0$ with multipliers $u_i$ and eliminating $u_i$ gives the compact
form used repeatedly in traffic assignment:

$$
\begin{aligned}
x_i^*\,\frac{\partial \mathcal{L}}{\partial x_i} &= 0, \\
\frac{\partial \mathcal{L}}{\partial x_i} &\ge 0, \\
x_i^* &\ge 0,
\end{aligned}
$$ (eq-03-kkt-nonneg)

where $\mathcal{L}$ now contains only the remaining constraints. In words:
at the optimum, a positive variable has zero reduced gradient and a variable
at zero has a non-negative one.

## Line search methods

Many algorithms reduce a multidimensional problem to a sequence of
one-dimensional problems $\min_{a \le x \le b} z(x)$. If $z$ is convex and
differentiable, the minimum is where $z'(x) = 0$, or at an end of the
interval.

### Bisection

:::{prf:algorithm} Bisection line search
:label: alg-03-bisection

**Inputs:** a convex function $z$ on $[a, b]$ with $z'(a) < 0 < z'(b)$, and a
tolerance $\epsilon > 0$.

1. Set $a_0 = a$, $b_0 = b$, $k = 0$.
2. If $b_k - a_k \le \epsilon$, stop: $x^* \approx (a_k + b_k)/2$.
3. Set $x_k = (a_k + b_k)/2$ and evaluate $z'(x_k)$.
   - If $z'(x_k) > 0$, set $a_{k+1} = a_k$, $b_{k+1} = x_k$.
   - If $z'(x_k) < 0$, set $a_{k+1} = x_k$, $b_{k+1} = b_k$.
   - If $z'(x_k) = 0$, stop: $x^* = x_k$.
4. Set $k \leftarrow k + 1$ and return to step 2.
:::

Each iteration halves the interval, so
$b_k - a_k = (b - a)/2^{k}$ and about $\log_2[(b - a)/\epsilon]$ iterations
are needed. Bisection uses only the sign of the derivative and always
converges, but slowly.

### Newton's method

:::{prf:algorithm} Newton's method for $z'(x) = 0$
:label: alg-03-newton

**Inputs:** a twice-differentiable $z$, a starting point $x_0$, and a
tolerance $\epsilon > 0$.

1. Set $k = 0$.
2. If $\lvert z'(x_k)\rvert \le \epsilon$, stop.
3. Set $x_{k+1} = x_k - z'(x_k)/z''(x_k)$.
4. Set $k \leftarrow k + 1$ and return to step 2.
:::

Each step minimizes the quadratic approximation
$z(x_k) + z'(x_k)(x - x_k) + \tfrac{1}{2}z''(x_k)(x - x_k)^2$. If
$z''(x^*) \ne 0$ and $x_0$ is close enough to $x^*$, convergence is
quadratic: the number of correct digits roughly doubles at each iteration.
Newton's method is, however, a method for finding *stationary points*: far
from the solution it can diverge, leave the feasible interval, or converge
to a maximum if $z''(x_k) < 0$ ({prf:ref}`ex-19-newton`). In practice it is
safeguarded, for example by falling back to bisection.

## The Frank–Wolfe method

Consider a convex program with **linear** constraints,

$$
\min_{\bx \in \Omega} f(\bx),
\qquad
\Omega = \{\bx : \bA\bx \le \bb\}
$$ (eq-03-fw-problem)

(equalities may also be present). The **Frank–Wolfe** (conditional
gradient) method replaces $f$ at the current point by its linear
approximation, minimizes that linear function over $\Omega$ — a linear
program — and moves towards the solution.

:::{prf:algorithm} Frank–Wolfe method
:label: alg-03-frank-wolfe

**Inputs:** a convex differentiable $f$, a polyhedral feasible set $\Omega$,
a feasible starting point $\bx^{(0)}$, and a tolerance $\epsilon > 0$.

1. **Direction finding.** Solve the linear program
   $\by^{(k)} \in \argmin_{\by \in \Omega}\ \nabla f(\bx^{(k)})\T\by$
   and set the descent direction $\bd^{(k)} = \by^{(k)} - \bx^{(k)}$.
2. **Convergence test.** If
   $-\nabla f(\bx^{(k)})\T(\by^{(k)} - \bx^{(k)}) \le \epsilon$, stop.
3. **Line search.** Find
   $\alpha_k \in \argmin_{0 \le \alpha \le 1} f\big(\bx^{(k)} + \alpha\,\bd^{(k)}\big)$,
   for example by bisection.
4. **Update.** Set $\bx^{(k+1)} = \bx^{(k)} + \alpha_k\bd^{(k)}$,
   $k \leftarrow k + 1$, and return to step 1.
:::

Every iterate is a convex combination of feasible points, so it remains
feasible without any projection. The quantity in step 2 has a useful
interpretation. By convexity,
$f(\bx^*) \ge f(\bx^{(k)}) + \nabla f(\bx^{(k)})\T(\bx^* - \bx^{(k)})$, and
since $\by^{(k)}$ minimizes the linear term over $\Omega$,

$$
f(\bx^{(k)}) - f(\bx^*)
\ \le\ -\nabla f(\bx^{(k)})\T\big(\by^{(k)} - \bx^{(k)}\big)
\ =:\ \mathrm{gap}^{(k)} .
$$ (eq-03-fw-gap)

The **gap** is therefore an upper bound on the distance of the current
objective value from the optimum, and $f(\bx^{(k)}) - \mathrm{gap}^{(k)}$ is
a lower bound on $f(\bx^*)$. The gap is non-negative and is zero exactly at
an optimal solution.

Frank–Wolfe is attractive in traffic assignment because, there, the linear
program of step 1 decomposes into shortest-path problems — it is an
**all-or-nothing assignment** — and the line search is one-dimensional. Its
convergence is sublinear (the gap decreases roughly like $1/k$), which is
why many variants (conjugate Frank–Wolfe, path-based and bush-based
algorithms) have been developed.

## Shortest paths

Step 1 of Frank–Wolfe in traffic assignment requires the shortest path from
every origin to every destination. The **label-correcting** algorithm
computes the shortest paths from one root node $r$ to all other nodes of a
network with non-negative link costs $t_{ij}$. Every node $i$ carries a
**label** $l_i$ (the length of the best path found so far from $r$ to $i$)
and a **predecessor** $p_i$ (the node before $i$ on that path).

:::{prf:algorithm} Label-correcting shortest path
:label: alg-03-label-correcting

1. Set $l_r = 0$, $l_i = \infty$ for $i \ne r$, $p_i = 0$ for all $i$, and
   put $r$ on the sequence list $Q$.
2. If $Q$ is empty, stop. Otherwise remove a node $i$ from $Q$.
3. For every link $(i, j)$ leaving $i$: if $l_i + t_{ij} < l_j$, set
   $l_j \leftarrow l_i + t_{ij}$, $p_j \leftarrow i$, and add $j$ to $Q$ if
   it is not already there.
4. Return to step 2.
:::

At termination $l_j$ is the shortest-path length from $r$ to $j$, and the
path is read backwards through the predecessors $p_j, p_{p_j}, \ldots, r$;
the predecessors of all nodes form the **shortest-path tree** of $r$. If the
node removed in step 2 is always the one with the smallest label, each node
is removed only once and the method is **Dijkstra's (label-setting)
algorithm**, which requires non-negative costs
({prf:ref}`ex-19-shortest-path`).

## Solvers

Small problems can be solved with spreadsheet solvers (Excel Solver) and
general-purpose libraries such as `scipy.optimize`; modeling languages
(AMPL, Pyomo, JuMP) and commercial solvers (CPLEX, Gurobi, MATLAB's
Optimization Toolbox, LINDO) handle large linear, integer, and quadratic
programs. Traffic assignment on real networks is solved with specialized
algorithms implemented in planning software (PTV Visum, TransCAD, Emme,
AequilibraE). Part V implements the algorithms of this chapter from
scratch ({doc}`32-python-foundations`).

## Summary and Common Mistakes

### Summary

- Convexity of a twice-differentiable function is checked with its Hessian
  ({prf:ref}`thm-03-convexity-test`); convex programs have no spurious local
  minima, and strictly convex objectives give unique solutions
  ({prf:ref}`thm-03-convex-program`).
- The KKT conditions (stationarity, dual feasibility, complementary
  slackness, primal feasibility) characterize optima under a constraint
  qualification and are sufficient for convex programs
  ({prf:ref}`thm-03-kkt`); with non-negative variables they take the form
  {eq}`eq-03-kkt-nonneg`.
- Bisection ({prf:ref}`alg-03-bisection`) is robust but slow; Newton's
  method ({prf:ref}`alg-03-newton`) is fast near the solution but needs
  safeguards.
- Frank–Wolfe ({prf:ref}`alg-03-frank-wolfe`) solves convex programs with
  linear constraints through a sequence of linear programs and line
  searches; its gap {eq}`eq-03-fw-gap` bounds the error of the objective.
- Label-correcting and Dijkstra's algorithms
  ({prf:ref}`alg-03-label-correcting`) compute shortest-path trees.

### Common mistakes

- **Claiming that a strictly convex function must have a positive definite
  Hessian.** Positive definiteness is sufficient, not necessary: $x^4$ is
  strictly convex with $f''(0) = 0$.
- **Using leading principal minors to test for positive
  *semi*definiteness.** The leading minors test definiteness only; for
  semidefiniteness all principal minors, or the eigenvalues, must be
  checked.
- **Forgetting the sign condition $u_i \ge 0$ or complementary slackness
  when checking KKT conditions.** Stationarity alone is satisfied by maxima
  and saddle points as well; all four groups of conditions are needed.
- **Using Newton's method without safeguards on a non-convex function.** It
  finds stationary points and can move to a maximum or leave the interval;
  fall back to bisection when a step fails.
- **Stopping Frank–Wolfe when successive iterates are close.** Frank–Wolfe
  can take very small steps far from the optimum; stop when the gap
  {eq}`eq-03-fw-gap` is small.

## References

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
