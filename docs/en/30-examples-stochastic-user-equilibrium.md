# Stochastic User Equilibrium

This chapter works through the examples and problems of
{doc}`15-stochastic-user-equilibrium`. The code in
{doc}`36-python-traffic-assignment` reproduces the numbers.

## Logit-based SUE on two routes

:::{prf:example} Two routes solved by Newton's method
:label: ex-30-sue-two-route

Thirty travelers per unit time choose between two routes with perceived
times

$$
\begin{aligned}
C_1 &= 30 + f_1 + \varepsilon_1, \\
C_2 &= 40 + f_2 + \varepsilon_2,
\end{aligned}
$$

where $\varepsilon_1$ and $\varepsilon_2$ are i.i.d. Gumbel with
$\theta = 0.1$. Find the logit-based SUE with Newton's method, starting from
$f_1 = 10$, and compare it with the DUE.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

By {eq}`eq-15-logit-sue` with $f_2 = 30 - f_1$,

$$
\begin{aligned}
f_1 &= \frac{30}{1 + \exp\left[\theta\,(c_1 - c_2)\right]} \\
&= \frac{30}{1 + \exp\left[0.1\,(2f_1 - 40)\right]},
\end{aligned}
$$

since $c_1 - c_2 = (30 + f_1) - (40 + 30 - f_1) = 2f_1 - 40$. Write
$x = f_1$ and solve $F(x) = 0$ with

$$
\begin{aligned}
F(x) &= x - \frac{30}{1 + e(x)}, \\
e(x) &= \exp\left[0.1\,(2x - 40)\right], \\
F'(x) &= 1 + \frac{6\,e(x)}{\left[1 + e(x)\right]^2},
\end{aligned}
$$

and Newton's iteration $x_{k+1} = x_k - F(x_k)/F'(x_k)$
({prf:ref}`alg-03-newton`):

| $k$ | $x_k$ | $F(x_k)$ | $F'(x_k)$ | $x_{k+1}$ |
|---|---|---|---|---|
| 0 | 10.00000 | −16.42391 | 1.62996 | 20.07626 |
| 1 | 20.07626 | 5.19064 | 2.49991 | 17.99993 |
| 2 | 17.99993 | 0.03920 | 2.44156 | 17.98387 |
| 3 | 17.98387 | 0.00001 | 2.44064 | 17.98387 |

The SUE is $f_1 = 17.984$ and $f_2 = 12.016$, with mean times
$c_1 = 47.98$ and $c_2 = 52.02$. At the DUE, $30 + f_1 = 40 + 30 - f_1$
gives $f_1 = 20$, $f_2 = 10$, and equal times of 50. Because some
travelers misperceive the times, the SUE sends more flow to route 2 than
the DUE does, and the used routes no longer have equal mean times.
:::

## Stochastic network loading

:::{prf:example} Logit loading on the six-node network
:label: ex-30-sue-logit-loading

In the network of {prf:ref}`ex-28-ue-six-node`, with $q_{12} = 10$,
$q_{56} = 5$, and $\theta = 1$, perform a logit loading at free-flow link
times.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

The free-flow link times are $\bt^0 = (3, 1, 0.5, 1, 2, 4, 1)$. The path
times are $c_1^{12} = 3$ and $c_2^{12} = 1 + 1 + 0.5 = 2.5$ for $1 \to 2$,
and $c_1^{56} = 4$ and $c_2^{56} = 2 + 1 + 1 = 4$ for $5 \to 6$. By
{eq}`eq-15-logit-sue`,

$$
\begin{aligned}
f_1^{12} &= 10\,\frac{e^{-3}}{e^{-3} + e^{-2.5}} = \frac{10}{1 + e^{0.5}} = 3.775, \\
f_2^{12} &= 6.225,
\end{aligned}
$$

and $f_1^{56} = f_2^{56} = 2.5$. The link flows are

$$
\bx = (3.775,\ 6.225,\ 6.225,\ 8.725,\ 2.5,\ 2.5,\ 2.5) .
$$

Even though path 2 is 0.5 shorter, more than a third of the travelers
take path 1: with $\theta = 1$ the perception errors have standard
deviation $\pi/\sqrt{6} = 1.28$, large compared with the time difference.
:::

:::{prf:example} Probit loading with link errors
:label: ex-30-sue-probit-loading

In the same network, the perceived link times at zero flow are
$T_a = t_a^0 + \zeta_a$ with independent errors
$\zeta_a \sim \mathcal{N}(0, \sigma_a^2)$,
$\boldsymbol{\sigma} = (0.3, 0.1, 0.1, 0.2, 0.4, 0.6, 0.1)$. Compute the
probit loading for $q_{12} = 10$ and $q_{56} = 5$.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

For $1 \to 2$, $C_1 = 3 + \zeta_1$ and
$C_2 = 2.5 + \zeta_2 + \zeta_4 + \zeta_3$. The paths share no link, so by
{eq}`eq-15-probit-two-paths`

$$
\begin{aligned}
\Prob(C_1 \le C_2) &= \Prob\left(\zeta_1 - \zeta_2 - \zeta_3 - \zeta_4 \le -0.5\right) \\
&= \Phi\left(\frac{-0.5}{\sqrt{0.3^2 + 0.1^2 + 0.1^2 + 0.2^2}}\right)
= \Phi(-1.291) = 0.0984 ,
\end{aligned}
$$

so $f_1^{12} = 0.984$ and $f_2^{12} = 9.016$. For $5 \to 6$, both paths
have mean time 4, so the probability is $\Phi(0) = 0.5$ whatever the
variances, and $f_1^{56} = f_2^{56} = 2.5$. The link flows are

$$
\bx = (0.984,\ 9.016,\ 9.016,\ 11.516,\ 2.5,\ 2.5,\ 2.5) .
$$

The probit errors here are much smaller than the logit errors of
{prf:ref}`ex-30-sue-logit-loading` (standard deviation 0.39 for the difference
of the path times, against $\pi/\sqrt{3} = 1.81$ for the logit model with
$\theta = 1$), so the loading is much closer to all-or-nothing.
:::

:::{prf:example} Monte Carlo loading
:label: ex-30-sue-monte-carlo

Estimate the probit loading of {prf:ref}`ex-30-sue-probit-loading` by Monte
Carlo simulation ({prf:ref}`alg-15-monte-carlo-loading`). The first two draws
of the link errors are

$$
\begin{aligned}
\boldsymbol{\zeta}^{(1)} &= (-0.04,\ 0.10,\ 0.06,\ 0.03,\ 0.88,\ 0.05,\ 0.04), \\
\boldsymbol{\zeta}^{(2)} &= (-0.19,\ -0.11,\ 0.06,\ 0.16,\ -0.13,\ 0.23,\ 0.04) .
\end{aligned}
$$
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**Draw 1.** $\bT^{(1)} = (2.96, 1.10, 0.56, 1.03, 2.88, 4.05, 1.04)$.
Path times: $1 \to 2$: $2.96$ versus $1.10 + 1.03 + 0.56 = 2.69$, so path 2;
$5 \to 6$: $4.05$ versus $2.88 + 1.03 + 1.04 = 4.95$, so path 1. The AON
flows are $\bX^{(1)} = (0, 10, 10, 10, 0, 5, 0)$, and
$\bx^{(1)} = \bX^{(1)}$.

**Draw 2.** $\bT^{(2)} = (2.81, 0.89, 0.56, 1.16, 1.87, 4.23, 1.04)$.
Path times: $2.81$ versus $2.61$ (path 2); $4.23$ versus $4.07$ (path 2).
So $\bX^{(2)} = (0, 10, 10, 15, 5, 0, 5)$ and

$$
\begin{aligned}
\bx^{(2)} &= \tfrac{1}{2}\left(\bx^{(1)} + \bX^{(2)}\right) \\
&= (0,\ 10,\ 10,\ 12.5,\ 2.5,\ 2.5,\ 2.5) .
\end{aligned}
$$

The largest relative change over the links with positive flow is that of
link 6, $\lvert 2.5 - 5\rvert/5 = 0.5$.

**Continuing.** With more draws the averages approach the exact probit
loading $(0.984, 9.016, 9.016, 11.516, 2.5, 2.5, 2.5)$; one run of the code
gives

| Draws | $\bx$ |
|---|---|
| 100 | (1.10, 8.90, 8.90, 11.25, 2.35, 2.65, 2.35) |
| 1 000 | (0.94, 9.06, 9.06, 11.62, 2.56, 2.44, 2.56) |
| 10 000 | (0.984, 9.016, 9.016, 11.503, 2.487, 2.513, 2.487) |

The error decreases like $1/\sqrt{n}$: about 0.3 vehicles on link 1 after
100 draws and 0.03 after 10 000. A loose tolerance on the change between
successive averages (for example 0.2) stops the simulation after a handful
of draws, far from the probit flows; a fixed, large number of draws is
safer.
:::

## SUE by the method of successive averages

:::{prf:example} Logit SUE on the six-node network
:label: ex-30-sue-msa

Solve the logit-based SUE of the network of {prf:ref}`ex-28-ue-six-node`
($q_{12} = 100$, $q_{56} = 50$) with $\theta = 1$ by MSA, and compare it
with the DUE.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**Initialization.** The logit loading at free-flow times gives the path
flows $(37.75, 62.25)$ and $(25, 25)$, so

$$
\bx^{(1)} = (37.75,\ 62.25,\ 62.25,\ 87.25,\ 25,\ 25,\ 25) .
$$

**Iteration 1.** The link times are
$\bt^{(1)} = (21.88, 125.49, 62.75, 44.62, 14.50, 29.00, 13.50)$. The path
times are 21.88 and $125.49 + 44.62 + 62.75 = 232.86$ for $1 \to 2$, and
29.00 and $14.50 + 44.62 + 13.50 = 72.62$ for $5 \to 6$. With differences
this large, the logit loading is practically all-or-nothing:
$\by^{(1)} = (100, 0, 0, 0, 0, 50, 0)$. With $\alpha_1 = 1$,
$\bx^{(2)} = \by^{(1)}$, and the convergence measure is

$$
\begin{aligned}
\frac{\sqrt{\sum_a\big(x_a^{(2)} - x_a^{(1)}\big)^2}}{\sum_a x_a^{(1)}} &= \frac{145.3}{324.5} = 0.448 .
\end{aligned}
$$

**Iteration 2.** $\bt^{(2)} = (53, 1, 0.5, 1, 2, 54, 1)$: now the indirect
paths are far shorter (2.5 and 4), so
$\by^{(2)} = (0, 100, 100, 150, 50, 0, 50)$ and
$\bx^{(3)} = \tfrac{1}{2}(\bx^{(2)} + \by^{(2)}) = (50, 50, 50, 75, 25, 25, 25)$.

**Iteration 3.** $\bt^{(3)} = (28, 101, 50.5, 38.5, 14.5, 29, 13.5)$, again
favoring the direct links, and
$\bx^{(4)} = (66.67, 33.33, 33.33, 50, 16.67, 33.33, 16.67)$.

The early iterations oscillate like MSA for the DUE, but as the flows
approach equilibrium the path times get close and the logit loading splits
the demand. After a few thousand iterations,

$$
\bx^{\mathrm{SUE}} = (89.106,\ 10.894,\ 10.894,\ 28.944,\ 18.050,\ 31.950,\ 18.050),
$$

with link times $(47.55, 22.79, 11.39, 15.47, 11.02, 35.95, 10.02)$ and
path times 47.55 and 49.65 for $1 \to 2$ (difference 2.102), and 35.95 and
36.52 for $5 \to 6$ (difference 0.571). Check:
$100/(1 + e^{-2.102}) = 89.11$ and $50/(1 + e^{-0.571}) = 31.95$. The direct minimization of Fisk's function
{eq}`eq-15-fisk` gives the same flows. Compared with the DUE
$(89.615, 10.385, 10.385, 28.308, 17.923, 32.077, 17.923)$, the SUE puts
slightly more flow on the slower paths, and the used paths no longer have
equal times.
:::

## Fisk's program and continuous perception errors

:::{prf:example} Fisk's program and MSA on a five-link network
:label: ex-30-hw4-q2-sue

For the network of {prf:ref}`ex-28-hw4-q2-due`: (1) formulate Fisk's program
for the logit-based SUE and show with the KKT conditions that its solution
satisfies the logit SUE conditions; (2) solve the logit SUE with MSA for
$\theta = 0.1$.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**(1)** With the path flows $f_1, f_2, f_3$ ($1 \to 2$) and $g_1, g_2$
($3 \to 2$) and the link flows of {prf:ref}`ex-28-hw4-q2-due`, Fisk's program
{eq}`eq-15-fisk` is

$$
\begin{aligned}
\min\ z &= \frac{1}{\theta}\left[\sum_{k=1}^{3} f_k(\ln f_k - 1) + \sum_{k=1}^{2} g_k(\ln g_k - 1)\right] \\
&\quad + \int_0^{f_1} t_1\,\diff\omega + \int_0^{f_2 + g_1} t_2\,\diff\omega
+ \int_0^{f_2 + f_3} t_3\,\diff\omega
+ \int_0^{f_3 + g_2} (t_4 + t_5)\,\diff\omega \\
\text{s.t.}\quad & f_1 + f_2 + f_3 = 20, \\
& g_1 + g_2 = 60, \\
& \bff, \bg \ge \bzero .
\end{aligned}
$$

The derivative with respect to a path flow is
$\tfrac{1}{\theta}\ln(\text{flow}) + \text{path time}$, for example
$\partial z/\partial f_3 = \tfrac{1}{\theta}\ln f_3 + t_3 + t_4 + t_5$. The
KKT conditions $\tfrac{1}{\theta}\ln f_k + c_k - u_{12} - v_k = 0$,
$v_kf_k = 0$, $v_k \ge 0$ force $f_k > 0$ and $v_k = 0$, so
$f_k = e^{\theta u_{12}}e^{-\theta c_k}$; conservation then gives

$$
\begin{aligned}
f_k &= 20\,\frac{e^{-\theta c_k}}{\sum_{l=1}^{3} e^{-\theta c_l}}, \\
g_k &= 60\,\frac{e^{-\theta c_k'}}{\sum_{l=1}^{2} e^{-\theta c_l'}},
\end{aligned}
$$

where the sums run over the paths of the **same** O-D pair only. These are
the logit SUE conditions ({prf:ref}`thm-15-fisk`).

**(2) Initialization.** All free-flow link times are 1, so the path times
are $(1, 2, 3)$ for $1 \to 2$ and $(1, 2)$ for $3 \to 2$. With
$\theta = 0.1$,

$$
\begin{aligned}
(f_1, f_2, f_3) &= 20\,\frac{(e^{-0.1}, e^{-0.2}, e^{-0.3})}{e^{-0.1} + e^{-0.2} + e^{-0.3}} \\
&= (7.34,\ 6.64,\ 6.01), \\
(g_1, g_2) &= 60\,\frac{(e^{-0.1}, e^{-0.2})}{e^{-0.1} + e^{-0.2}} \\
&= (31.50,\ 28.50),
\end{aligned}
$$

so $\bx^{(1)} = (7.34, 38.14, 12.66, 34.51, 34.51)$.

**Iteration 1.** $\bt^{(1)} = (2.10, 3.86, 1.63, 2.29, 2.04)$. Path times:
$1 \to 2$: $(2.10, 5.49, 5.96)$; $3 \to 2$: $(3.86, 4.33)$. The logit
loading (not an AON assignment) gives the path flows
$(8.36, 5.96, 5.68)$ and $(30.70, 29.30)$, so

$$
\by^{(1)} = (8.36,\ 36.66,\ 11.64,\ 34.98,\ 34.98),
$$

and with $\alpha_1 = 1$, $\bx^{(2)} = \by^{(1)}$. The convergence measure is
$\sqrt{\sum_a (x_a^{(2)} - x_a^{(1)})^2}/\sum_a x_a^{(1)} = 0.017$.

**Iterations 2 and 3.** $\by^{(2)} = (8.24, 36.98, 11.76, 34.78, 34.78)$ and
$\bx^{(3)} = (8.30, 36.82, 11.70, 34.88, 34.88)$ (measure 0.0018);
$\bx^{(4)} = (8.28, 36.86, 11.72, 34.86, 34.86)$ (measure 0.0005).

**Solution.** MSA converges to

$$
\bx^{\mathrm{SUE}} = (8.255,\ 36.917,\ 11.745,\ 34.829,\ 34.829),
$$

with path flows $(8.255, 6.044, 5.702)$ and $(30.873, 29.127)$. With
$\theta = 0.1$ the perception errors (standard deviation 12.8) are much
larger than the path time differences (about 1–4), so the flows are spread
almost evenly over the paths — very different from the DUE
$(20, 35.44, 0, 24.56, 24.56)$ of {prf:ref}`ex-28-hw4-q2-due`, where only one
path of $1 \to 2$ is used.
:::

:::{prf:example} Uniformly distributed perceived times
:label: ex-30-hw4-q3

Two links connect one O-D pair with demand 2. The perceived time of link 1
is uniform on $[3, 6]$, that of link 2 uniform on $[4, 7]$, independently.
(a) Compute the SUE link flows analytically. (b) Perform a Monte Carlo
loading with 10 draws, using the numbers 3.004, 4.004, 4.691, 6.675, 3.580,
6.215, 5.426, 5.629, 4.755, 6.699, 4.440, 5.799, 4.051, 5.336, 5.688, 6.420,
5.469, 4.980, 5.240, 5.677 alternately as the times of links 1 and 2, and
compare.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**(a)** Let $X \sim U[3, 6]$ and $Y \sim U[4, 7]$ be the perceived times.
Their joint density is $1/9$ on the square $[3, 6] \times [4, 7]$. Link 2
is chosen when $Y < X$, which requires $X > 4$; this region is the triangle
$4 < y < x < 6$ with area $\tfrac{1}{2} \times 2 \times 2 = 2$:

$$
\begin{aligned}
\Prob(Y < X) &= \frac{2}{9}, \\
\Prob(X < Y) &= \frac{7}{9} .
\end{aligned}
$$

Equivalently,
$\Prob(X < Y) = \int_3^6 \int_{\max(x, 4)}^{7} \tfrac{1}{9}\,\diff y\,\diff x = 7/9$.
The flows are

$$
\begin{aligned}
x_1 &= 2 \times \frac{7}{9} = 1.556, \\
x_2 &= 2 \times \frac{2}{9} = 0.444 .
\end{aligned}
$$

(The times do not depend on flow, so the loading is the equilibrium.)

**(b)**

| $n$ | $T_1$ | $T_2$ | $\bX^{(n)}$ | $\bx^{(n)}$ |
|---|---|---|---|---|
| 1 | 3.004 | 4.004 | (2, 0) | (2.000, 0.000) |
| 2 | 4.691 | 6.675 | (2, 0) | (2.000, 0.000) |
| 3 | 3.580 | 6.215 | (2, 0) | (2.000, 0.000) |
| 4 | 5.426 | 5.629 | (2, 0) | (2.000, 0.000) |
| 5 | 4.755 | 6.699 | (2, 0) | (2.000, 0.000) |
| 6 | 4.440 | 5.799 | (2, 0) | (2.000, 0.000) |
| 7 | 4.051 | 5.336 | (2, 0) | (2.000, 0.000) |
| 8 | 5.688 | 6.420 | (2, 0) | (2.000, 0.000) |
| 9 | 5.469 | 4.980 | (0, 2) | (1.778, 0.222) |
| 10 | 5.240 | 5.677 | (2, 0) | (1.800, 0.200) |

After 10 draws the estimate is $(1.8, 0.2)$: link 1 is chosen in 90 % of
the draws against the exact 77.8 %. With 10 draws the standard error of the
estimated probability is $\sqrt{0.778 \times 0.222/10} = 0.13$, so the
difference is just sampling noise; 100 000 draws give 0.778.
:::
