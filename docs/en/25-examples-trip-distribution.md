# Trip Distribution

This chapter works through the examples and problems of
{doc}`10-trip-distribution`; general bi-proportional and entropy examples
are in {doc}`20-examples-biproportional-fitting`. Balancing factors in
iteration tables are reported to five significant digits; the code in
{doc}`34-python-trip-distribution` reproduces them.

## Growth-factor methods

:::{prf:example} Origin-constrained growth factors
:label: ex-25-td-singly-growth

A base-year matrix and the target productions of four zones are:

| | 1 | 2 | 3 | 4 | $o_i$ | Target $O_i$ |
|---|---|---|---|---|---|---|
| 1 | 5 | 50 | 100 | 200 | 355 | 400 |
| 2 | 50 | 5 | 100 | 300 | 455 | 460 |
| 3 | 50 | 100 | 5 | 100 | 255 | 400 |
| 4 | 100 | 200 | 250 | 20 | 570 | 702 |
| $d_j$ | 205 | 355 | 455 | 620 | 1 635 | 1 962 |

Forecast the matrix with origin-specific growth factors.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

By {eq}`eq-10-origin-growth`, $\tau_i = O_i/o_i$:

$$
\begin{aligned}
\tau_1 &= \tfrac{400}{355} = 1.127, \\
\tau_2 &= \tfrac{460}{455} = 1.011, \\
\tau_3 &= \tfrac{400}{255} = 1.569, \\
\tau_4 &= \tfrac{702}{570} = 1.232 .
\end{aligned}
$$

Multiplying each row by its factor:

| | 1 | 2 | 3 | 4 | $\sum_j$ |
|---|---|---|---|---|---|
| 1 | 5.6 | 56.3 | 112.7 | 225.4 | 400 |
| 2 | 50.5 | 5.1 | 101.1 | 303.3 | 460 |
| 3 | 78.4 | 156.9 | 7.8 | 156.9 | 400 |
| 4 | 123.2 | 246.3 | 307.9 | 24.6 | 702 |
| $\sum_i$ | 257.8 | 464.6 | 529.5 | 710.1 | 1 962 |

Row totals match the targets by construction; the column totals are
whatever the row scaling produces: zone 4 attracts 710.1 trips, against
620 in the base year.
:::

:::{prf:example} Comparing the growth-factor methods
:label: ex-25-td-growth-methods

A base-year matrix of three zones and the forecast trip ends are:

| | 1 | 2 | 3 | $o_i$ | Target $O_i$ |
|---|---|---|---|---|---|
| 1 | 17 | 7 | 4 | 28 | 38.6 |
| 2 | 7 | 38 | 6 | 51 | 91.9 |
| 3 | 4 | 5 | 17 | 26 | 36.0 |
| $d_j$ | 28 | 50 | 27 | 105 | |
| Target $D_j$ | 39.3 | 90.3 | 36.9 | | 166.5 |

(1) Forecast the matrix with the uniform growth factor method. (2) Perform
the first iteration of the average growth factor, Detroit, Fratar, and
Furness methods. (3) Iterate each method until all growth factors are
within $\epsilon = 10^{-3}$ of one, and compare.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**(1) Uniform growth.** By {eq}`eq-10-uniform-growth`,
$\tau = 166.5/105 = 1.5857$, so every cell is multiplied by 1.5857:

| | 1 | 2 | 3 | $\sum_j$ | Target |
|---|---|---|---|---|---|
| 1 | 26.96 | 11.10 | 6.34 | 44.40 | 38.6 |
| 2 | 11.10 | 60.26 | 9.51 | 80.87 | 91.9 |
| 3 | 6.34 | 7.93 | 26.96 | 41.23 | 36.0 |

The total is right, but zone 2, which grows fastest, is underestimated by
12 % and zones 1 and 3 are overestimated.

**(2) First iteration.** The growth factors of the base-year matrix are

$$
\begin{aligned}
\tau^{(0)} &= \left(\tfrac{38.6}{28},\ \tfrac{91.9}{51},\ \tfrac{36.0}{26}\right) \\
&= (1.3786,\ 1.8020,\ 1.3846), \\
\Gamma^{(0)} &= \left(\tfrac{39.3}{28},\ \tfrac{90.3}{50},\ \tfrac{36.9}{27}\right) \\
&= (1.4036,\ 1.8060,\ 1.3667),
\end{aligned}
$$

and the overall growth is $G^{(0)} = 1.5857$. For cell (1, 1):

- *Average* {eq}`eq-10-average-growth`:
  $17 \times (1.3786 + 1.4036)/2 = 17 \times 1.3911 = 23.65$.
- *Detroit* {eq}`eq-10-detroit`:
  $17 \times 1.3786 \times 1.4036/1.5857 = 17 \times 1.2203 = 20.74$.
- *Fratar* {eq}`eq-10-fratar`: the location factors are

  $$
  \begin{aligned}
  L_1^{O} &= \frac{28}{17 \times 1.4036 + 7 \times 1.8060 + 4 \times 1.3667} \\
  &= \frac{28}{41.970} = 0.6671, \\
  L_1^{D} &= \frac{28}{17 \times 1.3786 + 7 \times 1.8020 + 4 \times 1.3846} \\
  &= \frac{28}{41.588} = 0.6733,
  \end{aligned}
  $$

  for origin 1 and destination 1, so the cell becomes
  $17 \times 1.3786 \times 1.4036 \times (0.6671 + 0.6733)/2 = 22.05$.
- *Furness*: the row step gives $17 \times 1.3786 = 23.44$; column 1 then
  sums to $23.44 + 7 \times 1.8020 + 4 \times 1.3846 = 41.59$, and the
  column step gives $23.44 \times 39.3/41.59 = 22.15$.

The complete first-iteration matrices and their totals are:

| Method | Row 1 | Row 2 | Row 3 | Row totals | Column totals |
|---|---|---|---|---|---|
| Average | 23.65, 11.15, 5.49 | 11.22, 68.55, 9.51 | 5.58, 7.98, 23.39 | 40.28, 89.28, 36.94 | 40.44, 87.67, 38.38 |
| Detroit | 20.74, 10.99, 4.75 | 11.16, 77.99, 9.32 | 4.90, 7.88, 20.29 | 36.49, 98.47, 33.07 | 36.81, 96.86, 34.36 |
| Fratar | 22.05, 10.94, 5.07 | 11.17, 72.74, 9.35 | 5.28, 7.97, 21.93 | 38.05, 93.27, 35.19 | 38.50, 91.65, 36.35 |
| Furness | 22.15, 10.25, 5.10 | 11.92, 72.70, 10.01 | 5.23, 7.35, 21.79 | 37.50, 94.63, 34.37 | 39.30, 90.30, 36.90 |

After one iteration the Fratar matrix is the closest to both sets of
targets; the Detroit method overshoots zone 2, whose two growth factors are
both well above the average growth.

**(3) Converged results.**

| Cell | Average | Detroit | Fratar | Furness |
|---|---|---|---|---|
| (1, 1) | 22.53 | 22.58 | 22.56 | 22.58 |
| (1, 2) | 10.98 | 10.89 | 10.91 | 10.89 |
| (1, 3) | 5.12 | 5.12 | 5.13 | 5.13 |
| (2, 1) | 11.29 | 11.23 | 11.24 | 11.23 |
| (2, 2) | 71.24 | 71.42 | 71.37 | 71.39 |
| (2, 3) | 9.38 | 9.28 | 9.31 | 9.29 |
| (3, 1) | 5.46 | 5.48 | 5.47 | 5.48 |
| (3, 2) | 8.07 | 8.03 | 8.04 | 8.02 |
| (3, 3) | 22.44 | 22.47 | 22.46 | 22.48 |
| Iterations | 8 | 9 | 3 | 5 |

All four methods reach essentially the same matrix; they differ in speed
and in what they guarantee. Fratar converges fastest here, the average and
Detroit methods slowest. Only the Furness limit is the bi-proportional
matrix of {doc}`04-biproportional-fitting`, the most probable matrix given
the base-year pattern and the new trip ends (its exact value of cell (2, 2)
is 71.38); the limits of the other methods differ from it slightly (by up to
1 % here) and have no such property.
:::

:::{prf:example} Doubly constrained growth: the Furness method
:label: ex-25-td-furness

Update the base-year matrix below to the target trip ends with the Furness
method ({prf:ref}`alg-04-biprop-2`, $\epsilon = 10^{-4}$).

| | 1 | 2 | 3 | Target $O_i$ |
|---|---|---|---|---|
| 1 | 3.0 | 1.1 | 1.1 | 100 |
| 2 | 1.1 | 3.0 | 3.0 | 200 |
| 3 | 1.8 | 1.8 | 3.0 | 250 |
| Target $D_j$ | 220 | 165 | 165 | 550 |
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

The totals agree ($\sum O_i = \sum D_j = 550$). Start with $b_j^{(0)} = 1$.

**Iteration 1.** Row factors $a_i = O_i/\sum_j b_j t_{ij}$:

$$
\begin{aligned}
a_1 &= \frac{100}{5.2} = 19.23, \\
a_2 &= \frac{200}{7.1} = 28.17, \\
a_3 &= \frac{250}{6.6} = 37.88 .
\end{aligned}
$$

After the row step the matrix $a_it_{ij}$ is

| | 1 | 2 | 3 |
|---|---|---|---|
| 1 | 57.7 | 21.2 | 21.2 |
| 2 | 31.0 | 84.5 | 84.5 |
| 3 | 68.2 | 68.2 | 113.6 |
| $\sum_i$ | 156.9 | 173.8 | 219.3 |

and the column factors are $b_j = D_j/\sum_i a_it_{ij}$:
$b = (220/156.9,\ 165/173.8,\ 165/219.3) = (1.4025,\ 0.94913,\ 0.75240)$.

**Subsequent iterations.**

| $n$ | $a_1$ | $a_2$ | $a_3$ | $b_1$ | $b_2$ | $b_3$ |
|---|---|---|---|---|---|---|
| 1 | 19.231 | 28.169 | 37.879 | 1.4025 | 0.94913 | 0.75240 |
| 2 | 16.449 | 30.087 | 38.520 | 1.4495 | 0.92858 | 0.73689 |
| 3 | 16.180 | 30.345 | 38.514 | 1.4546 | 0.92614 | 0.73538 |
| 4 | 16.151 | 30.374 | 38.512 | 1.4551 | 0.92587 | 0.73521 |
| 5 | 16.148 | 30.377 | 38.512 | 1.4552 | 0.92584 | 0.73520 |

The relative change of every $b_j$ in iteration 5 is below $10^{-4}$, so
the algorithm stops. The forecast matrix $T_{ij} = a_ib_jt_{ij}$ is

| | 1 | 2 | 3 | $\sum_j$ |
|---|---|---|---|---|
| 1 | 70.5 | 16.4 | 13.1 | 100 |
| 2 | 48.6 | 84.4 | 67.0 | 200 |
| 3 | 100.9 | 64.2 | 84.9 | 250 |
| $\sum_i$ | 220 | 165 | 165 | 550 |
:::

## Gravity model

:::{prf:example} Doubly constrained gravity model
:label: ex-25-td-gravity

The generalized costs (minutes) and target trip ends of four zones are
given below. Estimate a doubly constrained gravity model
$T_{ij} = a_ib_j\exp(-\beta c_{ij})$ with $\beta = 0.1$.

| | 1 | 2 | 3 | 4 | $O_i$ |
|---|---|---|---|---|---|
| 1 | 3 | 11 | 18 | 22 | 400 |
| 2 | 12 | 3 | 12 | 19 | 460 |
| 3 | 15.5 | 13 | 5 | 7 | 400 |
| 4 | 24 | 18 | 8 | 5 | 702 |
| $D_j$ | 260 | 400 | 500 | 802 | 1 962 |
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**Seed matrix.** Compute $f(c_{ij}) = \exp(-0.1\,c_{ij})$:

| | 1 | 2 | 3 | 4 | $\sum_j$ |
|---|---|---|---|---|---|
| 1 | 0.74 | 0.33 | 0.17 | 0.11 | 1.35 |
| 2 | 0.30 | 0.74 | 0.30 | 0.15 | 1.49 |
| 3 | 0.21 | 0.27 | 0.61 | 0.50 | 1.59 |
| 4 | 0.09 | 0.17 | 0.45 | 0.61 | 1.31 |
| $\sum_i$ | 1.34 | 1.51 | 1.52 | 1.36 | 5.74 |

Optionally, scale the seed by the common ratio
$\tau = 1962/5.74 = 341.7$ so that it already has the right total; this
only speeds up the first iteration.

**Balancing.** Applying the Furness method to the seed matrix with the
targets $O_i$ and $D_j$ converges in 12 iterations
($\epsilon = 10^{-6}$) to

| | 1 | 2 | 3 | 4 | $O_i$ |
|---|---|---|---|---|---|
| 1 | 157.0 | 100.4 | 66.1 | 76.5 | 400 |
| 2 | 57.5 | 201.1 | 108.5 | 92.9 | 460 |
| 3 | 25.3 | 46.1 | 136.2 | 192.4 | 400 |
| 4 | 20.2 | 52.4 | 189.1 | 440.2 | 702 |
| $D_j$ | 260 | 400 | 500 | 802 | 1 962 |

The modeled mean trip cost is
$\sum_{ij}T_{ij}c_{ij}/T = 8.65$ minutes. In a calibration, $\beta$ would be
adjusted until this value matches the observed mean trip cost.
:::

:::{prf:example} Tri-proportional calibration of a stepwise deterrence function
:label: ex-25-td-tri-proportional

For the four zones of {prf:ref}`ex-25-td-gravity`, with the slightly different
cost matrix

$$
[c_{ij}] = \begin{bmatrix}
3 & 11 & 18 & 22 \\ 10 & 3 & 13 & 19 \\ 15 & 13 & 5 & 7 \\ 24 & 18 & 6 & 5
\end{bmatrix},
$$

a survey gives the trip length distribution in six bins of 4 minutes:

| Bin $k$ | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Cost range (min) | 0–4 | 4–8 | 8–12 | 12–16 | 16–20 | 20–24 |
| Trips $S_k$ | 365 | 962 | 160 | 150 | 230 | 95 |

Calibrate $T_{ij} = a_ib_j\sum_k F_k\delta_{ijk}$ with the trip ends
$O = (400, 460, 400, 702)$ and $D = (260, 400, 500, 802)$.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**Bins.** Assign each cell to its cost bin:

| | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| 1 | 1 | 3 | 5 | 6 |
| 2 | 3 | 1 | 4 | 5 |
| 3 | 4 | 4 | 2 | 2 |
| 4 | 6 | 5 | 2 | 2 |

**First iteration** (starting from $a_i = b_j = F_k = 1$). The row step
gives $a_i = O_i/4$, i.e. $a = (100, 115, 100, 175.5)$; the column step
$b_j = D_j/\sum_i a_i = D_j/1\,962$, i.e. $b = (0.530, 0.816, 1.019, 1.635)$;
and the bin step $F_k = S_k/\sum_{ij} a_ib_j\delta_{ijk}$, i.e.
$F = (2.487, 1.316, 1.123, 0.596, 0.531, 0.370)$.

**Consistency check.** Before iterating further, check that the targets
can be met simultaneously. Bins 4, 5, and 6 contain only cells in rows 3–4
and columns 1–2, or in rows 1–2 and columns 3–4. The block of rows 3–4 and
columns 3–4 is entirely bin 2 (962 trips), so the remaining trips of rows
3–4 must lie in bins 4–6:

$$
O_3 + O_4 - S_2 = 1\,102 - 962 = 140 .
$$

Likewise columns 3–4 must contribute $D_3 + D_4 - S_2 = 1\,302 - 962 = 340$
trips to bins 4–6. Hence bins 4–6 must contain $140 + 340 = 480$ trips, but
$S_4 + S_5 + S_6 = 475$. The targets are **inconsistent**: no matrix
satisfies all constraints, and the tri-proportional iterations never
converge (the factors drift without bound). Similarly, rows 1–2 require
$S_1 + S_3 = 860 - 340 = 520$, not 525.

**Corrected data.** Moving five trips from bin 3 to bin 6, i.e.
$S = (365, 962, 155, 150, 230, 100)$, makes the targets consistent. The
algorithm, with the factors renormalized in each iteration, then converges
in about 20 iterations to

| | 1 | 2 | 3 | 4 | $O_i$ |
|---|---|---|---|---|---|
| 1 | 155.2 | 98.1 | 68.8 | 77.9 | 400 |
| 2 | 56.9 | 209.8 | 84.9 | 108.4 | 460 |
| 3 | 25.8 | 39.3 | 120.6 | 214.4 | 400 |
| 4 | 22.1 | 52.8 | 225.7 | 401.4 | 702 |
| $D_j$ | 260 | 400 | 500 | 802 | 1 962 |

with separation factors, normalized to $F_1 = 1$,

$$
F = (1.000,\ 0.459,\ 0.414,\ 0.246,\ 0.177,\ 0.113),
$$

a decreasing deterrence function estimated without assuming its form. An
exponential or power function can be fitted to these values.
:::

## Inconsistent trip ends and partial matrices

:::{prf:example} Furness method with inconsistent trip ends
:label: ex-25-hw2-q1

A survey in 2020 gave the following O-D matrix (intra-zonal trips not
observed):

| | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| 1 | – | 60 | 275 | 571 |
| 2 | 50 | – | 410 | 443 |
| 3 | 123 | 61 | – | 47 |
| 4 | 205 | 265 | 75 | – |

A trip generation model predicts for 2025:

| Zone | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| Trips originated $O_i$ | 1 200 | 1 050 | 380 | 770 |
| Trips attracted $D_j$ | 670 | 730 | 950 | 995 |

(a) Explain why the doubly constrained growth-factor model cannot be used
directly. (b) Adjust the trip ends. (c) Forecast the 2025 matrix with
{prf:ref}`alg-04-biprop-2`.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**(a)** $\sum_i O_i = 3\,400$ but $\sum_j D_j = 3\,345$. Summing the row
constraints gives $\sum_{ij}T_{ij} = 3\,400$ and summing the column
constraints gives $3\,345$: no matrix satisfies both, and the Furness
iterations would oscillate.

**(b)** Scale one set of trip ends to the other's total. Taking the
attractions as control total (scaling the attractions up to 3 400 is
equally valid), multiply each $O_i$ by
$3\,345/3\,400 = 0.98382$:

$$
\begin{aligned}
O' &= (1\,180.6,\ 1\,033.0,\ 373.9,\ 757.5), \\
\sum_i O_i' &= 3\,345 .
\end{aligned}
$$

**(c)** The diagonal cells are structural zeros and stay zero. With
$b_j^{(0)} = 1$, the first iterations are

| $n$ | $a_1$ | $a_2$ | $a_3$ | $a_4$ | $b_1$ | $b_2$ | $b_3$ | $b_4$ |
|---|---|---|---|---|---|---|---|---|
| 1 | 1.3031 | 1.1440 | 1.6184 | 1.3900 | 1.2380 | 1.3388 | 1.0197 | 0.74986 |
| 2 | 1.4965 | 1.2719 | 1.3889 | 1.1058 | 1.4530 | 1.5613 | 0.93509 | 0.67084 |
| 3 | 1.6087 | 1.3715 | 1.2238 | 0.96904 | 1.6038 | 1.7057 | 0.88178 | 0.62830 |
| ⋮ | | | | | | | | |
| 16 | 1.7748 | 1.5239 | 1.0104 | 0.80076 | 1.8375 | 1.9194 | 0.80994 | 0.57316 |

For example, $a_1^{(1)} = 1\,180.6/(60 + 275 + 571) = 1.3031$ and
$b_1^{(1)} = 670/(1.1440 \times 50 + 1.6184 \times 123 + 1.3900 \times 205) = 1.2380$.
With $\epsilon = 10^{-4}$ (relative change of every factor) the algorithm
stops after 16 iterations, giving

| | 1 | 2 | 3 | 4 | $O_i'$ |
|---|---|---|---|---|---|
| 1 | – | 204.4 | 395.3 | 580.9 | 1 180.6 |
| 2 | 140.0 | – | 506.0 | 386.9 | 1 033.0 |
| 3 | 228.4 | 118.3 | – | 27.2 | 373.9 |
| 4 | 301.6 | 407.3 | 48.6 | – | 757.5 |
| $D_j$ | 670 | 730 | 950 | 995 | 3 345 |

A loose tolerance of $\epsilon = 0.05$ stops after 5 iterations with row
totals still 1.4–2.8 % off target (e.g. 1 164.3 instead of 1 180.6 for
zone 1); a tolerance of $10^{-3}$ or smaller is advisable.
:::

:::{prf:example} Calibrating a gravity model on a partial matrix
:label: ex-25-hw2-q2

Four zones A–D (intra-zonal trips excluded) have the generalized travel
times

| | A | B | C | D |
|---|---|---|---|---|
| A | – | 1.23 | 1.85 | 2.67 |
| B | 1.23 | – | 2.48 | 1.21 |
| C | 1.85 | 2.48 | – | 1.44 |
| D | 2.67 | 1.21 | 1.44 | – |

A gravity model $T_{ij} = a_ib_j\sum_k F_k\delta_{ijk}$ with two cost bins
(bin 1: cost below 1.9; bin 2: cost above 1.9) is to be calibrated on
roadside interview counts, in which A→C, B→A, and C→B were not observed:

| | A | B | C | D |
|---|---|---|---|---|
| A | – | 6 | N.A. | 2 |
| B | N.A. | – | 1 | 4 |
| C | 8 | N.A. | – | 8 |
| D | 6 | 18 | 6 | – |

Estimate $a_i$, $b_j$, $F_k$, and the three missing entries with the
tri-proportional algorithm.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**Bins.** Cells with cost below 1.9 (bin 1) are AB, AC, BA, BD, CA, CD, DB,
DC; cells above 1.9 (bin 2) are AD, BC, CB, DA.

**Targets from the observed cells only.** Missing cells are excluded from
every sum:

$$
\begin{aligned}
O &= (6 + 2,\ 1 + 4,\ 8 + 8,\ 6 + 18 + 6) = (8,\ 5,\ 16,\ 30), \\
D &= (8 + 6,\ 6 + 18,\ 1 + 6,\ 2 + 4 + 8) = (14,\ 24,\ 7,\ 14), \\
S_1 &= 6 + 4 + 8 + 8 + 18 + 6 = 50, \\
S_2 &= 2 + 1 + 6 = 9 .
\end{aligned}
$$

**Iterations.** Run the tri-proportional algorithm over the nine observed
cells, starting from $a_i = b_j = F_k = 1$. With the convergence tolerance
$\epsilon = 10^{-6}$ on the cell values (after renormalizing the factors),
the algorithm converges to factors that, normalized to $F_1 = 1$, are

$$
\begin{aligned}
a &= (6,\ 6,\ 12,\ 18), \\
b &= \left(\tfrac{2}{3},\ 1,\ \tfrac{1}{3},\ \tfrac{2}{3}\right), \\
F &= \left(1,\ \tfrac{1}{2}\right).
\end{aligned}
$$

These reproduce **every** observed count exactly; for example
$T_{AB} = 6 \times 1 \times F_1 = 6$, $T_{AD} = 6 \times \tfrac{2}{3}\times F_2 = 2$,
and $T_{DB} = 18 \times 1 \times F_1 = 18$. Trips in the longer cost bin are
half as likely, other things being equal.

**Missing entries.**

$$
\begin{aligned}
\hat{T}_{AC} &= a_A\, b_C\, F_1 = 6 \times \tfrac{1}{3} \times 1 = 2, \\
\hat{T}_{BA} &= a_B\, b_A\, F_1 = 6 \times \tfrac{2}{3} \times 1 = 4, \\
\hat{T}_{CB} &= a_C\, b_B\, F_2 = 12 \times 1 \times \tfrac{1}{2} = 6 .
\end{aligned}
$$

*Convergence note.* The algorithm converges slowly on this sparse matrix
(about 100 iterations for a relative tolerance of $10^{-8}$). Stopping with
$\epsilon = 0.05$ after three iterations gives 1.87, 3.62, and 8.72 for the
three entries, still far from the converged values 2, 4, and 6.
:::
