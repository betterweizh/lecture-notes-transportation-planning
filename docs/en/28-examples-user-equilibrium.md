# User Equilibrium Assignment

This chapter works through the examples and problems of
{doc}`13-user-equilibrium-assignment`. The code in
{doc}`36-python-traffic-assignment` reproduces the numbers.

## Equilibrium conditions on small networks

:::{prf:example} Two routes with different performance functions
:label: ex-28-ue-two-route

An O-D pair is connected by two links with

$$
\begin{aligned}
t_1(x_1) &= 40 + 0.5\,x_1, \\
t_2(x_2) &= 10 + 0.25\,x_2^2 .
\end{aligned}
$$

(1) Find the user equilibrium for $q = 10$. (2) Find it for any demand
$q \ge 0$, and the common travel time when both links are used.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**(1)** Suppose both links are used. Then $t_1 = t_2$ with
$x_1 = 10 - x_2$:

$$
\begin{aligned}
40 + 0.5\,(10 - x_2) &= 10 + 0.25\,x_2^2 \\
x_2^2 + 2x_2 - 140 &= 0 \\
x_2 &= -1 + \sqrt{141} = 10.874 .
\end{aligned}
$$

Then $x_1 = 10 - 10.874 = -0.874 < 0$, which is infeasible, so link 1 is
unused. With all the demand on link 2, $t_2(10) = 10 + 25 = 35$, which is
less than the free-flow time of link 1, $t_1(0) = 40$. The conditions
{eq}`eq-13-ue-conditions` hold, and the equilibrium is

$$
\begin{aligned}
x_1 &= 0, \\
x_2 &= 10, \\
u &= 35 .
\end{aligned}
$$

**(2)** Link 2 alone carries the demand as long as its time does not exceed
the free-flow time of link 1:

$$
10 + 0.25\,q^2 \le 40
\iff q^2 \le 120
\iff q \le \sqrt{120} = 10.95 .
$$

For $q \le 10.95$ the equilibrium is $x_1 = 0$, $x_2 = q$, with time
$u = 10 + 0.25q^2$. For $q > 10.95$ both links are used, and

$$
\begin{aligned}
40 + 0.5\,(q - x_2) &= 10 + 0.25\,x_2^2 \\
x_2^2 + 2x_2 - (120 + 2q) &= 0,
\end{aligned}
$$

so

$$
\begin{aligned}
x_2 &= \sqrt{2q + 121} - 1, \\
x_1 &= q + 1 - \sqrt{2q + 121}, \\
u &= 40.5 + 0.5\,q - 0.5\sqrt{2q + 121} .
\end{aligned}
$$

At $q = \sqrt{120}$, $\sqrt{2q + 121} = q + 1$, so $x_1 = 0$ and the two
branches join continuously. For $q = 20$, for example,
$x_1 = 8.31$, $x_2 = 11.69$, and $u = 44.16$. The steep link 2 is
attractive at low demand because its free-flow time is short, but its time
rises quickly. Once both links are used, link 2 takes only
$\diff x_2/\diff q = 1/\sqrt{2q + 121} < 0.09$ of each extra trip,
and link 1 takes the rest.
:::

:::{prf:example} Three parallel links
:label: ex-28-ue-three-link

Three parallel links join $r$ and $s$, with
$t_1 = 5 + x_1$, $t_2 = 2 + x_2$, $t_3 = 10 + x_3$. Find the equilibrium for
$q = 2$, for $q = 10$, and for any $q \ge 0$.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

The free-flow times are 5, 2, and 10, so link 2 is used first, link 1 joins
when $t_2$ reaches 5, and link 3 joins when the common time reaches 10.

**$q = 2$.** First guess: all three links used. Then
$5 + x_1 = 2 + x_2 = 10 + x_3 = u$ and $x_1 + x_2 + x_3 = 2$, so
$3u - 17 = 2$, $u = 19/3$, and $x_3 = u - 10 = -11/3 < 0$: link 3 is
unused. Second guess: links 1 and 2. Then $5 + x_1 = 2 + x_2$ and
$x_1 + x_2 = 2$ give $x_1 = -0.5 < 0$: link 1 is unused too. Third guess:
link 2 alone, $x_2 = 2$, $t_2 = 4$, which is less than $t_1(0) = 5$ and
$t_3(0) = 10$. The equilibrium is

$$
\begin{aligned}
x_1 &= 0, \\
x_2 &= 2, \\
x_3 &= 0, \\
u &= 4 .
\end{aligned}
$$

**General $q$.** Repeating the argument with the thresholds $t_2 = 5$
($q = 3$) and $u = 10$ (links 1 and 2 at times 10: $x_1 = 5$, $x_2 = 8$,
$q = 13$):

| Demand | Used links | Flows | Time $u$ |
|---|---|---|---|
| $0 \le q \le 3$ | 2 | $x_2 = q$ | $2 + q$ |
| $3 < q \le 13$ | 1, 2 | $x_1 = \tfrac{q - 3}{2}$, $x_2 = \tfrac{q + 3}{2}$ | $\tfrac{q + 7}{2}$ |
| $q > 13$ | 1, 2, 3 | $x_1 = \tfrac{q + 2}{3}$, $x_2 = \tfrac{q + 11}{3}$, $x_3 = \tfrac{q - 13}{3}$ | $\tfrac{q + 17}{3}$ |

For $q = 10$: $x_1 = 3.5$, $x_2 = 6.5$, $x_3 = 0$, $u = 8.5 < t_3(0) = 10$.
:::

:::{prf:example} The six-node network
:label: ex-28-ue-six-node

In the network of {numref}`fig-13-six-node-network` the link performance
functions are

$$
\begin{aligned}
t_1 &= 3 + 0.5\,x_1, \\
t_2 &= 1 + 2\,x_2, \\
t_3 &= 0.5 + x_3, \\
t_4 &= 1 + 0.5\,x_4, \\
t_5 &= 2 + 0.5\,x_5, \\
t_6 &= 4 + x_6, \\
t_7 &= 1 + 0.5\,x_7,
\end{aligned}
$$

and the demands are $q_{12} = 100$ and $q_{56} = 50$ ($q_{16} = q_{52} = 0$).
Find the equilibrium path and link flows.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

The paths are $f_1$ (link 1) and $f_2$ (links 2–4–3) for pair $1 \to 2$, and
$g_1$ (link 6) and $g_2$ (links 5–4–7) for pair $5 \to 6$. The link flows
are

$$
\begin{aligned}
x_1 &= f_1, \\
x_2 &= x_3 = f_2, \\
x_4 &= f_2 + g_2, \\
x_5 &= x_7 = g_2, \\
x_6 &= g_1 .
\end{aligned}
$$

Assume that all four paths are used. For pair $1 \to 2$,

$$
\begin{aligned}
3 + 0.5\,f_1 &= (1 + 2f_2) + \left[1 + 0.5\,(f_2 + g_2)\right] + (0.5 + f_2) \\
&= 2.5 + 3.5\,f_2 + 0.5\,g_2 ,
\end{aligned}
$$

and with $f_1 = 100 - f_2$ this becomes $4f_2 + 0.5\,g_2 = 50.5$. For pair
$5 \to 6$,

$$
\begin{aligned}
4 + g_1 &= (2 + 0.5\,g_2) + \left[1 + 0.5\,(f_2 + g_2)\right] + (1 + 0.5\,g_2) \\
&= 4 + 1.5\,g_2 + 0.5\,f_2 ,
\end{aligned}
$$

and with $g_1 = 50 - g_2$ this becomes $0.5\,f_2 + 2.5\,g_2 = 50$. Solving
the two linear equations,

$$
\begin{aligned}
f_2 &= \frac{135}{13} = 10.385, \\
g_2 &= \frac{233}{13} = 17.923,
\end{aligned}
$$

so $f_1 = 89.615$ and $g_1 = 32.077$. All four flows are positive, so the
guess was right. The equilibrium link flows are

$$
\bx = (89.615,\ 10.385,\ 10.385,\ 28.308,\ 17.923,\ 32.077,\ 17.923),
$$

and the equilibrium O-D times are $u_{12} = 3 + 0.5 \times 89.615 = 47.81$
and $u_{56} = 4 + 32.077 = 36.08$. The Frank–Wolfe iterations of
{prf:ref}`ex-28-ue-fw-six-node` converge to the same flows.
:::

:::{prf:example} Unique link flows, non-unique path flows
:label: ex-28-ue-nonunique

In a network with link 1 ($1 \to 3$), link 2 ($2 \to 3$), link 3
($3 \to 4$), link 4 ($3 \to 4$, parallel to link 3), and link 5
($4 \to 5$), the demands are
$q_{15} = 2$ and $q_{25} = 3$ and the link times are

$$
\begin{aligned}
t_1 &= 1, \\
t_2 &= 2, \\
t_3 &= 2 + x_3, \\
t_4 &= 1 + 2x_4, \\
t_5 &= 1 .
\end{aligned}
$$

Find the equilibrium path and link flows.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

Each O-D pair has two paths, through link 3 or through link 4:
$f_1^{15}$ (1–3–5), $f_2^{15}$ (1–4–5), $f_1^{25}$ (2–3–5), $f_2^{25}$
(2–4–5). Links 1, 2, and 5 are common to both paths of a pair, so the
equilibrium conditions reduce to $t_3 = t_4$ for both pairs:

$$
\begin{aligned}
2 + \left(f_1^{15} + f_1^{25}\right) &= 1 + 2\left(f_2^{15} + f_2^{25}\right), \\
f_1^{15} + f_2^{15} &= 2, \\
f_1^{25} + f_2^{25} &= 3 .
\end{aligned}
$$

With $x_3 = f_1^{15} + f_1^{25}$ and $x_4 = f_2^{15} + f_2^{25} = 5 - x_3$,
the first equation gives $2 + x_3 = 11 - 2x_3$, so

$$
\begin{aligned}
x_1 &= 2, \\
x_2 &= 3, \\
x_3 &= 3, \\
x_4 &= 2, \\
x_5 &= 5,
\end{aligned}
$$

with $t_3 = t_4 = 5$. These link flows are unique. The path flows are not:
there are three equations for four unknowns, and every

$$
\begin{aligned}
f_1^{15} &= \phi, \\
f_2^{15} &= 2 - \phi, \\
f_1^{25} &= 3 - \phi, \\
f_2^{25} &= \phi, \quad 0 \le \phi \le 2,
\end{aligned}
$$

is an equilibrium. In terms of path flows the Hessian of Beckmann's
objective is
$\bDelta\T\diag(0, 0, 1, 2, 0)\bDelta$:

$$
\nabla^2_{\bff} z =
\begin{bmatrix}
1 & 0 & 1 & 0 \\
0 & 2 & 0 & 2 \\
1 & 0 & 1 & 0 \\
0 & 2 & 0 & 2
\end{bmatrix},
$$

which has two identical pairs of rows: it is positive semi-definite but
singular, so the objective is convex but not strictly convex in the path
flows.
:::

## All-or-nothing assignment

:::{prf:example} All-or-nothing loading
:label: ex-28-ue-aon

In the network of {prf:ref}`ex-28-ue-nonunique`, the current link flows are
$\bx = (2, 3, 1, 4, 5)$. Perform an all-or-nothing assignment with the
corresponding link times, and comment on the result.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

The link times are $t_1 = 1$, $t_2 = 2$, $t_3 = 2 + 1 = 3$,
$t_4 = 1 + 2 \times 4 = 9$, $t_5 = 1$. The path through link 3 is shorter
for both pairs: $1 + 3 + 1 = 5$ versus $1 + 9 + 1 = 11$ for $1 \to 5$, and
$6$ versus $12$ for $2 \to 5$. Loading each demand on its shortest path,

$$
\by = (2,\ 3,\ 5,\ 0,\ 5) .
$$

With these flows, $t_3 = 7$ and $t_4 = 1$, so the path through link 4 is
now the shorter one and a second AON assignment would move everybody there.
AON ignores the effect of flows on times and oscillates; it is not an
equilibrium. The equilibrium $\bx^* = (2, 3, 3, 2, 5)$ of
{prf:ref}`ex-28-ue-nonunique` lies between the two AON patterns, which is
exactly what the line search of Frank–Wolfe finds.
:::

## Frank–Wolfe and MSA

:::{prf:example} Three links with BPR functions
:label: ex-28-ue-fw-three-link

Ten units of flow travel between $r$ and $s$ on three parallel links with
BPR functions $t_a = t_a^0\left[1 + 0.15\,(x_a/c_a)^4\right]$,

$$
\begin{aligned}
t_1^0 &= 10, \\
c_1 &= 2; \\
t_2^0 &= 20, \\
c_2 &= 4; \\
t_3^0 &= 25, \\
c_3 &= 3 .
\end{aligned}
$$

Solve the user equilibrium with Frank–Wolfe (bisection line search) and with
MSA, and compare (Sheffi, 1985, Sections 5.1–5.2).
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**Initialization.** At zero flow the times are $(10, 20, 25)$, so the AON
assignment puts everything on link 1: $\bx^{(1)} = (10, 0, 0)$, with
$z(\bx^{(1)}) = 1\,975.0$.

**Iteration 1.** The times are
$t_1 = 10(1 + 0.15 \times 5^4) = 947.5$, $t_2 = 20$, $t_3 = 25$. Link 2 is
now the shortest path, so $\by^{(1)} = (0, 10, 0)$, and the move transfers
flow from link 1 to link 2. The line search solves
{eq}`eq-13-fw-line-search`,

$$
t_1\big(10 - 10\alpha\big)(-10) + t_2\big(10\alpha\big)(10) = 0
\iff t_1(10 - 10\alpha) = t_2(10\alpha),
$$

whose root is $\alpha_1 = 0.5965$, giving $\bx^{(2)} = (4.03, 5.97, 0)$
with $t_1 = t_2 = 34.8$. Link 3 (25) is now the shortest, and so on:

| $n$ | $\bx^{(n)}$ | $\bt^{(n)}$ | $\by^{(n)}$ | $\alpha_n$ | $z(\bx^{(n+1)})$ | RG |
|---|---|---|---|---|---|---|
| 1 | (10.00, 0.00, 0.00) | (947.5, 20.0, 25.0) | (0, 10, 0) | 0.5965 | 197.40 | 0.979 |
| 2 | (4.03, 5.97, 0.00) | (34.8, 34.8, 25.0) | (0, 0, 10) | 0.1611 | 189.99 | 0.282 |
| 3 | (3.38, 5.00, 1.61) | (22.3, 27.3, 25.3) | (10, 0, 0) | 0.0356 | 189.45 | 0.119 |
| 4 | (3.62, 4.83, 1.55) | (26.1, 26.4, 25.3) | (0, 0, 10) | 0.0204 | 189.36 | 0.032 |
| 5 | (3.55, 4.73, 1.73) | (24.8, 25.9, 25.4) | (10, 0, 0) | 0.0072 | 189.34 | 0.023 |
| 6 | (3.59, 4.69, 1.71) | (25.6, 25.7, 25.4) | (0, 0, 10) | 0.0054 | 189.33 | 0.008 |

RG is the relative gap {eq}`eq-13-relative-gap` at $\bx^{(n)}$. The objective
decreases monotonically, and the iterations converge to

$$
\begin{aligned}
\bx^* &= (3.583,\ 4.645,\ 1.772), \\
t_1 &= t_2 = t_3 = 25.46, \\
z(\bx^*) &= 189.33 .
\end{aligned}
$$

**MSA.** With $\alpha_n = 1/n$ the first iterations are

| $n$ | $\bx^{(n)}$ | $\bt^{(n)}$ | $\by^{(n)}$ | $z(\bx^{(n)})$ |
|---|---|---|---|---|
| 1 | (10.00, 0.00, 0.00) | (947.5, 20.0, 25.0) | (0, 10, 0) | 1975.00 |
| 2 | (0.00, 10.00, 0.00) | (10.0, 137.2, 25.0) | (10, 0, 0) | 434.38 |
| 3 | (5.00, 5.00, 0.00) | (68.6, 27.3, 25.0) | (0, 0, 10) | 215.92 |
| 4 | (3.33, 3.33, 3.33) | (21.6, 21.4, 30.7) | (0, 10, 0) | 195.82 |
| 5 | (2.50, 5.00, 2.50) | (13.7, 27.3, 26.8) | (10, 0, 0) | 197.56 |
| 6 | (4.00, 4.00, 2.00) | (34.0, 23.0, 25.7) | (0, 10, 0) | 191.90 |
| 7 | (3.33, 5.00, 1.67) | (21.6, 27.3, 25.4) | (10, 0, 0) | 190.16 |
| 8 | (4.29, 4.29, 1.43) | (41.6, 24.0, 25.2) | (0, 10, 0) | 194.84 |

The first step ($\alpha_1 = 1$) overshoots, the objective goes up and down,
and after 12 iterations the flows are still $(3.33, 5.00, 1.67)$. MSA
reaches $(3.58, 4.65, 1.77)$ only after about 1 000 iterations, because
every AON direction gets the same weight regardless of its quality.
:::

:::{prf:example} Frank–Wolfe on the six-node network
:label: ex-28-ue-fw-six-node

Solve the equilibrium of {prf:ref}`ex-28-ue-six-node` with Frank–Wolfe.
Perform the first iteration by hand, evaluate the three stopping criteria of
{doc}`13-user-equilibrium-assignment`, and tabulate the following iterations.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**Initialization.** The free-flow path times are $3$ and
$1 + 1 + 0.5 = 2.5$ for $1 \to 2$, and $4$ and $2 + 1 + 1 = 4$ for
$5 \to 6$. Path 2–4–3 is the shortest for $1 \to 2$; for $5 \to 6$ the two
paths tie, and the direct link 6 is chosen. Hence

$$
\begin{aligned}
\bx^{(1)} &= (0,\ 100,\ 100,\ 100,\ 0,\ 50,\ 0), \\
z(\bx^{(1)}) &= 19\,200 .
\end{aligned}
$$

**Iteration 1.** *Update:*
$\bt^{(1)} = (3,\ 201,\ 100.5,\ 51,\ 2,\ 54,\ 1)$.

*Direction:* for $1 \to 2$, link 1 (3) beats path 2–4–3 (352.5); for
$5 \to 6$, link 6 (54) and path 5–4–7 ($2 + 51 + 1 = 54$) tie again, and the
direct link is kept. So $\by^{(1)} = (100, 0, 0, 0, 0, 50, 0)$ and

$$
\by^{(1)} - \bx^{(1)} = (100,\ -100,\ -100,\ -100,\ 0,\ 0,\ 0) .
$$

*Line search:* along this direction only links 1–4 change, and
{eq}`eq-13-fw-line-search` becomes

$$
\begin{aligned}
h'(\alpha) &= (3 + 50\alpha)(100) + (201 - 200\alpha)(-100) \\
&\quad + (100.5 - 100\alpha)(-100) + (51 - 50\alpha)(-100) \\
&= -34\,950 + 40\,000\,\alpha = 0,
\end{aligned}
$$

so $\alpha_1 = 34\,950/40\,000 = 0.87375$.

*Move:* $\bx^{(2)} = (87.38,\ 12.63,\ 12.63,\ 12.63,\ 0,\ 50,\ 0)$, with
$z(\bx^{(2)}) = 3\,931.22$.

*Convergence tests.* (1) The objective fell by
$19\,200 - 3\,931.22 = 15\,268.78$. (2) The shortest-path times were
$\bu^{(1)} = (3, 54)$; with $\bt^{(2)} = (46.69, 26.25, 13.13, 7.31, 2, 54, 1)$
they are $\bu^{(2)} = (46.69, 10.31)$, so
$\sum \lvert u^{(2)} - u^{(1)}\rvert/u^{(1)} = 43.69/3 + 43.69/54 = 15.37$.
(3) The flows changed by
$\sqrt{\sum_a (x_a^{(2)} - x_a^{(1)})^2}/\sum_a x_a^{(1)} = 174.75/350 = 0.50$.
All three are far from zero.

**Further iterations.**

| $n$ | $\bx^{(n)}$ | $\by^{(n)}$ | $\alpha_n$ | $z(\bx^{(n)})$ |
|---|---|---|---|---|
| 1 | (0, 100, 100, 100, 0, 50, 0) | (100, 0, 0, 0, 0, 50, 0) | 0.87375 | 19 200.00 |
| 2 | (87.38, 12.63, 12.63, 12.63, 0, 50, 0) | (100, 0, 0, 50, 50, 0, 50) | 0.3491 | 3 931.22 |
| 3 | (91.78, 8.22, 8.22, 25.67, 17.46, 32.54, 17.46) | (0, 100, 100, 150, 50, 0, 50) | 0.0226 | 3 549.88 |
| 4 | (89.71, 10.29, 10.29, 28.49, 18.19, 31.81, 18.19) | (0, 100, 100, 100, 0, 50, 0) | 0.0010 | 3 539.81 |
| 5 | (89.61, 10.39, 10.39, 28.56, 18.18, 31.82, 18.18) | | | 3 539.79 |

After 19 iterations the relative gap is below $10^{-6}$ and the flows equal
the exact solution of {prf:ref}`ex-28-ue-six-node`,
$(89.615, 10.385, 10.385, 28.308, 17.923, 32.077, 17.923)$, with
$z = 3\,539.71$. MSA from the same start gives
$(89.6, 10.4, 10.4, 28.3, 17.9, 32.1, 17.9)$ after 1 000 iterations.
:::

## A network with two O-D pairs

:::{prf:example} Beckmann's program and Frank–Wolfe on a five-link network
:label: ex-28-hw4-q2-due

The network of {numref}`fig-28-two-origin-network` has five links — link 1
($1 \to 2$), link 2 ($3 \to 2$), link 3 ($1 \to 3$), link 4 ($3 \to 4$), and
link 5 ($4 \to 2$) — and two O-D pairs with $q_{12} = 20$ and $q_{32} = 60$ trips per hour. The link
times are $t_a = 1 + 0.15\,x_a/a$, where $a$ is the link number.

(1) Formulate the DUE as a convex program in path flows and show with the
KKT conditions that its solution satisfies the DUE conditions.
(2) Solve the DUE with Frank–Wolfe.

```{figure} figures/28-two-origin-network.svg
:name: fig-28-two-origin-network
:width: 420px
:class: dark-light

The five-link network with two O-D pairs: origins 1 and 3 (green),
destination 2 (orange).
```
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**(1)** Pair $1 \to 2$ has three paths: $f_1$ (link 1), $f_2$ (links 3–2),
and $f_3$ (links 3–4–5). Pair $3 \to 2$ has two: $g_1$ (link 2) and $g_2$
(links 4–5). The link flows are

$$
\begin{aligned}
x_1 &= f_1, \\
x_2 &= f_2 + g_1, \\
x_3 &= f_2 + f_3, \\
x_4 &= x_5 = f_3 + g_2,
\end{aligned}
$$

and the link functions are
$t_1 = 1 + 0.15x_1$, $t_2 = 1 + 0.075x_2$, $t_3 = 1 + 0.05x_3$,
$t_4 = 1 + 0.0375x_4$, $t_5 = 1 + 0.03x_5$. Beckmann's program is

$$
\begin{aligned}
\min_{\bff, \bg}\ z
&= \int_0^{f_1} t_1\,\diff\omega + \int_0^{f_2 + g_1} t_2\,\diff\omega
+ \int_0^{f_2 + f_3} t_3\,\diff\omega \\
&\quad + \int_0^{f_3 + g_2} t_4\,\diff\omega + \int_0^{f_3 + g_2} t_5\,\diff\omega \\
\text{s.t.}\quad & f_1 + f_2 + f_3 = 20, \\
& g_1 + g_2 = 60, \\
& \bff, \bg \ge \bzero .
\end{aligned}
$$

With multipliers $u_{12}$, $u_{32}$ for the conservation constraints and
$v_k \ge 0$ for the non-negativity constraints, the Lagrangian is

$$
L = z + u_{12}\,(20 - f_1 - f_2 - f_3) + u_{32}\,(60 - g_1 - g_2) - \sum_k v_k\,(\text{path flow } k) .
$$

Differentiating, for example,
$\partial z/\partial f_3 = t_3 + t_4 + t_5 = c_3^{12}$, and in general
$\partial z/\partial(\text{path flow}) = $ path time. The KKT conditions are
$c_k - u_{rs} - v_k = 0$, $v_k \ge 0$, $v_k \cdot (\text{flow}_k) = 0$, plus
feasibility; eliminating $v_k$ gives $c_k \ge u_{rs}$ and
$(c_k - u_{rs})\cdot\text{flow}_k = 0$, which are the DUE conditions
({prf:ref}`thm-13-beckmann-ue`).

**(2) Initialization.** All free-flow link times are 1, so the shortest
paths are link 1 (time 1) for $1 \to 2$ and link 2 (time 1) for $3 \to 2$:
$\bx^{(1)} = (20, 60, 0, 0, 0)$.

*Iteration 1.* $\bt^{(1)} = (4.00, 5.50, 1.00, 1.00, 1.00)$. For $1 \to 2$
the path times are 4.00, $1 + 5.5 = 6.50$, and $1 + 1 + 1 = 3.00$; for
$3 \to 2$, 5.50 and 2.00. The AON flows are $\by^{(1)} = (0, 0, 20, 80, 80)$
and the direction is $(-20, -60, 20, 80, 80)$. The line search derivative
is

$$
\begin{aligned}
h'(\alpha) &= (4 - 3\alpha)(-20) + (5.5 - 4.5\alpha)(-60) + (1 + \alpha)(20) \\
&\quad + (1 + 3\alpha)(80) + (1 + 2.4\alpha)(80) \\
&= -230 + 782\,\alpha = 0,
\end{aligned}
$$

so $\alpha_1 = 0.2941$ and $\bx^{(2)} = (14.12, 42.35, 5.88, 23.53, 23.53)$.
The change criterion is
$\sqrt{\sum_a (x_a^{(2)} - x_a^{(1)})^2}/\sum_a x_a^{(1)} = 38.57/80 = 0.482$.

*Iteration 2.* $\bt^{(2)} = (3.12, 4.18, 1.29, 1.88, 1.71)$. Path times
$1 \to 2$: 3.12, 5.47, 4.88; $3 \to 2$: 4.18, 3.59. So
$\by^{(2)} = (20, 0, 0, 60, 60)$ and $\alpha_2 = 0.1526$, giving
$\bx^{(3)} = (15.02, 35.89, 4.98, 29.10, 29.10)$.

*Iteration 3.* Now link 2 (3.69) is quicker than links 4–5 (3.96) for
$3 \to 2$, so $\by^{(3)} = (20, 60, 0, 0, 0)$ and $\alpha_3 = 0.1546$.

From here the AON directions alternate between $(20, 0, 0, 60, 60)$ and
$(20, 60, 0, 0, 0)$, the classic **zigzagging** of Frank–Wolfe: the step
sizes shrink, and more than 3 000 iterations are needed to reach a relative
gap of $10^{-4}$.

**The exact equilibrium.** The iterations show that link 3 is being
emptied: path 1 of $1 \to 2$ stays the shortest. Guess that $1 \to 2$ uses
link 1 only ($x_1 = 20$, $t_1 = 4$) and that $3 \to 2$ uses both its paths.
Then

$$
\begin{aligned}
1 + 0.075\,(60 - y) &= 2 + (0.0375 + 0.03)\,y \\
3.5 &= 0.1425\,y \\
y &= 24.561,
\end{aligned}
$$

where $y = x_4 = x_5$. The equilibrium is

$$
\begin{aligned}
\bx^* &= (20,\ 35.439,\ 0,\ 24.561,\ 24.561), \\
u_{12} &= 4.000, \\
u_{32} &= 3.658 .
\end{aligned}
$$

Check: the unused paths of $1 \to 2$ take
$t_3(0) + t_2 = 1 + 3.658 = 4.658$ and
$t_3(0) + t_4 + t_5 = 4.658$, both more than $u_{12} = 4$. All
conditions hold.
:::
