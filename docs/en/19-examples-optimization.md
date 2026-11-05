# Nonlinear Optimization

This chapter works through the examples and problems of
{doc}`03-nonlinear-optimization`. Several of them use the same small problem,

$$
\begin{aligned}
\min_{\bx}\quad & f(\bx) = (x_1 - 2)^2 + (x_2 - 3)^2 \\
\text{s.t.}\quad & x_1 + x_2 \le 2, \\
& x_1 \ge 0, \\
& x_2 \ge 0,
\end{aligned}
$$ (eq-19-example-qp)

whose feasible set is the triangle with vertices $(0,0)$, $(2,0)$, and
$(0,2)$ ({numref}`fig-19-frank-wolfe-example`).

## Convexity and optimality conditions

:::{prf:example} Checking convexity
:label: ex-19-convexity

Show that problem {eq}`eq-19-example-qp` is a convex program with a unique
solution, and classify $f_2(\bx) = 2x_1 + 3x_2 + 0.5x_3 - x_4$.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

The gradient and Hessian of $f$ are

$$
\nabla f(\bx) = \begin{bmatrix} 2(x_1 - 2) \\ 2(x_2 - 3) \end{bmatrix},
\qquad
\nabla^2 f(\bx) = \begin{bmatrix} 2 & 0 \\ 0 & 2 \end{bmatrix}.
$$

The Hessian has eigenvalues $2, 2 > 0$ (equivalently, its leading principal
minors are $2 > 0$ and $4 > 0$), so it is positive definite and $f$ is
strictly convex by {prf:ref}`thm-03-convexity-test`. The constraints are
linear, so the feasible set is a convex polyhedron. The problem is a convex
program with a strictly convex objective and a non-empty compact feasible
set, so by {prf:ref}`thm-03-convex-program` it has exactly one optimal
solution.

The linear function $f_2$ has a zero Hessian, which is positive
semidefinite but not positive definite: $f_2$ is convex but not strictly
convex (its graph is a hyperplane, so the convexity inequality of
{prf:ref}`def-03-convex-function` holds with equality for every pair of
points).
:::

:::{prf:example} Verifying the KKT conditions
:label: ex-19-kkt

Verify that $\bx^* = (0.5, 1.5)$ is the unique global minimum of problem
{eq}`eq-19-example-qp`.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

Write the constraints as
$g_1 = x_1 + x_2 - 2 \le 0$, $g_2 = -x_1 \le 0$, $g_3 = -x_2 \le 0$ with
multipliers $u_1, u_2, u_3$.

**Primal feasibility.** $x_1^* + x_2^* = 2$ (the first constraint is
binding), $x_1^* = 0.5 > 0$, and $x_2^* = 1.5 > 0$.

**Complementary slackness.** $u_2(-x_1^*) = 0$ and $u_3(-x_2^*) = 0$ with
$x_1^*, x_2^* > 0$ force $u_2 = u_3 = 0$; $u_1(x_1^* + x_2^* - 2) = 0$
holds for any $u_1$ because the constraint is binding.

**Stationarity.**

$$
\begin{bmatrix} 2(0.5 - 2) \\ 2(1.5 - 3) \end{bmatrix}
+ u_1 \begin{bmatrix} 1 \\ 1 \end{bmatrix}
+ u_2 \begin{bmatrix} -1 \\ 0 \end{bmatrix}
+ u_3 \begin{bmatrix} 0 \\ -1 \end{bmatrix}
= \begin{bmatrix} 0 \\ 0 \end{bmatrix} .
$$

With $u_2 = u_3 = 0$ both rows read $-3 + u_1 = 0$, so $u_1 = 3$.

**Dual feasibility.** $u_1 = 3 \ge 0$, $u_2 = u_3 = 0$.

All KKT conditions hold. Since the problem is a convex program, the KKT
conditions are sufficient, so $\bx^*$ is a global minimum, and by
{prf:ref}`ex-19-convexity` it is the only one. Geometrically, $\bx^*$ is the
projection of the unconstrained minimum $(2, 3)$ onto the line
$x_1 + x_2 = 2$. The multiplier $u_1 = 3$ says that relaxing the
constraint to $x_1 + x_2 \le 2 + \delta$ would lower the optimal objective
by about $3\delta$.
:::

## Line searches

:::{prf:example} Bisection
:label: ex-19-bisection

Minimize $z(x) = \sin x$ over $3 \le x \le 6$ by bisection.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

$z'(x) = \cos x$, with $z'(3) = -0.990 < 0$ and $z'(6) = 0.960 > 0$, so the
minimum lies inside the interval. Applying {prf:ref}`alg-03-bisection`:

| $k$ | $a_k$ | $b_k$ | $x_k$ | $z'(x_k)$ | next interval |
|---|---|---|---|---|---|
| 0 | 3 | 6 | 4.5 | −0.2108 | $[4.5,\ 6]$ |
| 1 | 4.5 | 6 | 5.25 | 0.5121 | $[4.5,\ 5.25]$ |
| 2 | 4.5 | 5.25 | 4.875 | 0.1619 | $[4.5,\ 4.875]$ |
| 3 | 4.5 | 4.875 | 4.6875 | −0.0249 | $[4.6875,\ 4.875]$ |
| 4 | 4.6875 | 4.875 | 4.78125 | 0.0688 | $[4.6875,\ 4.78125]$ |
| 5 | 4.6875 | 4.78125 | 4.734375 | 0.0220 | $[4.6875,\ 4.734375]$ |
| 6 | 4.6875 | 4.734375 | 4.710938 | −0.0015 | $[4.710938,\ 4.734375]$ |

After seven evaluations the interval has length $3/2^7 = 0.023$ and
contains the exact minimum $x^* = 3\pi/2 = 4.712389$.
:::

:::{prf:example} Newton's method
:label: ex-19-newton

Minimize $z(x) = \sin x$ over $3 \le x \le 6$ by Newton's method, starting
from (a) $x_0 = 4$ and (b) $x_0 = 3$.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

The iteration of {prf:ref}`alg-03-newton` is
$x_{k+1} = x_k - \cos x_k/(-\sin x_k) = x_k + \cot x_k$.

**(a) Start at $x_0 = 4$:**

| $k$ | $x_k$ | $z'(x_k)$ | $z''(x_k)$ | $x_{k+1}$ |
|---|---|---|---|---|
| 0 | 4.000000 | −0.653644 | 0.756802 | 4.863691 |
| 1 | 4.863691 | 0.150726 | 0.988576 | 4.711224 |
| 2 | 4.711224 | −0.001165 | 0.999999 | 4.712389 |
| 3 | 4.712389 | $\approx 0$ | 1.000000 | 4.712389 |

Convergence to $x^* = 3\pi/2$ is quadratic: the error falls from $0.15$ to
$1.2\times 10^{-3}$ to $5\times 10^{-10}$.

**(b) Start at $x_0 = 3$:**

| $k$ | $x_k$ | $z'(x_k)$ | $z''(x_k)$ | $x_{k+1}$ |
|---|---|---|---|---|
| 0 | 3.000000 | −0.989992 | −0.141120 | −4.015253 |
| 1 | −4.015253 | −0.642025 | −0.766684 | −4.852658 |
| 2 | −4.852658 | 0.139809 | −0.990178 | −4.711462 |
| 3 | −4.711462 | −0.000927 | −1.000000 | −4.712389 |

At $x_0 = 3$ the function is concave ($z'' < 0$), so the quadratic model
has a maximum, and the Newton step jumps far outside the interval. The
iterates converge to $x = -3\pi/2$, where $\sin x = 1$ — a **maximum**.
Newton's method finds stationary points, not minima; it must be safeguarded
(for example by checking $z'' > 0$ and keeping the iterate inside the
interval, falling back to bisection otherwise).
:::

## The Frank–Wolfe method

:::{prf:example} Frank–Wolfe method
:label: ex-19-frank-wolfe

Solve problem {eq}`eq-19-example-qp` with the Frank–Wolfe method from
$\bx^{(0)} = (0, 0)$ with tolerance $\epsilon = 0.01$.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

The gradient is $\nabla f(\bx) = (2x_1 - 4,\ 2x_2 - 6)\T$. Because the
feasible set is the triangle with vertices $(0,0)$, $(2,0)$, $(0,2)$, each
linear subproblem is solved at a vertex.

**Iteration 1** ($k = 0$, $\bx^{(0)} = (0, 0)$, $f = 13$).

1. $\nabla f(\bx^{(0)}) = (-4, -6)\T$. The LP
   $\min\ -4y_1 - 6y_2$ over the triangle has its minimum at the vertex
   $\by^{(0)} = (0, 2)$ (value $-12$ against $0$ and $-8$ at the other
   vertices).
2. Gap: $-\nabla f\T(\by^{(0)} - \bx^{(0)}) = -[(-4)(0) + (-6)(2)] = 12 > 0.01$.
3. Line search along $\bx^{(0)} + \alpha(\by^{(0)} - \bx^{(0)}) = (0, 2\alpha)$:
   $f = 4 + (2\alpha - 3)^2$ is minimized at $\alpha = 1.5$, outside
   $[0, 1]$, so $\alpha_0 = 1$.
4. $\bx^{(1)} = (0, 2)$, $f = 5$.

**Iteration 2** ($k = 1$).

1. $\nabla f(\bx^{(1)}) = (-4, -2)\T$. The LP $\min\ -4y_1 - 2y_2$ gives
   $\by^{(1)} = (2, 0)$ (value $-8$).
2. Gap: $-[(-4)(2 - 0) + (-2)(0 - 2)] = -(-8 + 4) = 4 > 0.01$.
3. Along $(2\alpha,\ 2 - 2\alpha)$:
   $f(\alpha) = (2\alpha - 2)^2 + (-2\alpha - 1)^2$, so
   $f'(\alpha) = 4(2\alpha - 2) + 4(2\alpha + 1) = 16\alpha - 4 = 0$ and
   $\alpha_1 = 0.25$.
4. $\bx^{(2)} = (0, 2) + 0.25\,(2, -2) = (0.5, 1.5)$, $f = 4.5$.

**Iteration 3** ($k = 2$).

1. $\nabla f(\bx^{(2)}) = (-3, -3)\T$. The LP $\min\ -3y_1 - 3y_2$ has
   the same value $-6$ at $(2, 0)$ and $(0, 2)$; take $\by^{(2)} = (2, 0)$.
2. Gap: $-[(-3)(2 - 0.5) + (-3)(0 - 1.5)] = -(-4.5 + 4.5) = 0 \le 0.01$.
   Stop.

The solution is $\bx^* = (0.5, 1.5)$ with $f^* = 4.5$, in agreement with
{prf:ref}`ex-19-kkt`. By {eq}`eq-03-fw-gap`, the lower bounds on $f^*$ were
$13 - 12 = 1$, $5 - 4 = 1$, and $4.5 - 0 = 4.5$.

```{figure} figures/19-frank-wolfe-example.svg
:name: fig-19-frank-wolfe-example
:width: 380px
:class: dark-light

Frank–Wolfe iterates for problem {eq}`eq-19-example-qp`. The feasible set is
shaded; grey curves are contours of $f$. Each step moves towards a vertex
of the feasible set.
```

Here Frank–Wolfe reaches the exact solution in two steps because the
optimum lies on an edge between two vertices. In general it approaches the
optimum gradually, with a zig-zag between vertices.
:::

## Shortest paths

:::{prf:example} Shortest path by label correcting
:label: ex-19-shortest-path

Find the shortest path from node 1 to node 4 in the network of
{numref}`fig-19-shortest-path-network`.

```{figure} figures/19-shortest-path-network.svg
:name: fig-19-shortest-path-network
:width: 330px
:class: dark-light

A network with four links; the numbers are link travel times.
```
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

Apply {prf:ref}`alg-03-label-correcting` with root $r = 1$, processing the
sequence list $Q$ first in, first out, and scanning link $(1,4)$ before
$(1,2)$.

| Step | Node scanned | Label updates | Labels $(l_1, l_2, l_3, l_4)$ | Predecessors $(p_2, p_3, p_4)$ | $Q$ after |
|---|---|---|---|---|---|
| 0 | — | initialize | $(0, \infty, \infty, \infty)$ | $(0, 0, 0)$ | $\{1\}$ |
| 1 | 1 | $l_4 = 0 + 4$, $l_2 = 0 + 1$ | $(0, 1, \infty, 4)$ | $(1, 0, 1)$ | $\{4, 2\}$ |
| 2 | 4 | none (no outgoing links) | $(0, 1, \infty, 4)$ | $(1, 0, 1)$ | $\{2\}$ |
| 3 | 2 | $l_3 = 1 + 1$ | $(0, 1, 2, 4)$ | $(1, 2, 1)$ | $\{3\}$ |
| 4 | 3 | $l_4 = 2 + 1 = 3 < 4$ | $(0, 1, 2, 3)$ | $(1, 2, 3)$ | $\{4\}$ |
| 5 | 4 | none | $(0, 1, 2, 3)$ | $(1, 2, 3)$ | $\emptyset$ |

The list is empty, so the labels are final. The shortest distance to node 4
is $l_4 = 3$, and tracing predecessors $p_4 = 3$, $p_3 = 2$, $p_2 = 1$ gives
the path $1 \to 2 \to 3 \to 4$. Node 4 was scanned twice, the first time
with a label that was not yet final: the label-correcting method may scan a
node again after revising its label. Dijkstra's algorithm, which always
scans the node with the smallest label (here node 2, then node 3, before
node 4), scans every node exactly once, when its label is already final.
:::
