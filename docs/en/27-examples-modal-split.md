# Aggregate and Combined Modal Split

This chapter works through the examples and problems of
{doc}`12-aggregate-modal-split`, including calibration and market
segmentation. The code in
{doc}`35-python-mode-choice` reproduces the numbers.

## Diversion curves

:::{prf:example} A logit diversion curve
:label: ex-27-ms-diversion

Between zones $i$ and $j$, 2 000 commuters per hour can travel by car
(S\$6.00, 20 min) or by bus (S\$1.85, 30 min). Assuming a value of time of
S\$0.25 per minute, compute the bus share with the diversion curve
{eq}`eq-12-diversion-curve` for $\beta = 0.2$, 0.5, and 1.0 per S\$.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

The generalized costs (in S\$) are

$$
\begin{aligned}
C^{c} &= 6.00 + 0.25 \times 20 = 11.00, \\
C^{t} &= 1.85 + 0.25 \times 30 = 9.35,
\end{aligned}
$$

so the bus is cheaper by $C^{c} - C^{t} = 1.65$. The bus share is
$P^{t} = 1/[1 + \exp(-1.65\,\beta)]$:

| $\beta$ (1/S\$) | 0.2 | 0.5 | 1.0 |
|---|---|---|---|
| bus share $P^t$ | 0.582 | 0.695 | 0.839 |
| bus users (per hour) | 1 164 | 1 391 | 1 678 |

The same cost advantage produces a mild or a strong shift depending on
$\beta$, which must therefore be calibrated from observed shares
({prf:ref}`ex-27-ms-calibration`). The value of time used here is an
assumption made for the example.
:::

## Combined distribution and modal split

:::{prf:example} Trips by destination and mode
:label: ex-27-ms-combined

Three residential zones produce $O = (200, 150, 250)$ trips per hour to two
work zones that attract $D = (280, 320)$. Trips can be made by car ($k = 1$)
or bus ($k = 2$) with the generalized times (minutes)

| $C_{ij}^k$ | $j = 1$, car | $j = 1$, bus | $j = 2$, car | $j = 2$, bus |
|---|---|---|---|---|
| $i = 1$ | 30 | 45 | 46 | 57 |
| $i = 2$ | 40 | 60 | 43 | 57 |
| $i = 3$ | 20 | 26 | 25 | 32 |

Estimate the most probable trip matrix by mode with the entropy-maximizing
model {eq}`eq-12-combined-dms`, taking $\beta = 0.05$ per minute.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**Model.** By {eq}`eq-12-combined-solution`,
$T_{ij}^k = A_iO_iB_jD_j\exp(-\beta C_{ij}^k)$. Summing over modes, the
O-D matrix is a doubly constrained gravity model with deterrence

$$
\begin{aligned}
f_{ij} &= \sum_k e^{-0.05\,C_{ij}^k}, \\
\begin{bmatrix} f_{11} & f_{12} \\ f_{21} & f_{22} \\ f_{31} & f_{32} \end{bmatrix}
&= \begin{bmatrix}
0.2231 + 0.1054 & 0.1003 + 0.0578 \\
0.1353 + 0.0498 & 0.1165 + 0.0578 \\
0.3679 + 0.2725 & 0.2865 + 0.2019
\end{bmatrix}.
\end{aligned}
$$

**Balancing.** Starting from $B_j = 1$, alternate
$A_i = 1/\sum_j B_jD_jf_{ij}$ and $B_j = 1/\sum_i A_iO_if_{ij}$ (Furness)
until the trip ends are reproduced. The result is

$$
[T_{ij}] = \begin{bmatrix} 111.17 & 88.83 \\ 58.51 & 91.49 \\ 110.32 & 139.68 \end{bmatrix},
$$

whose row sums are 200, 150, 250 and column sums 280, 320.

**Modal split.** The balancing factors cancel in the shares, so each cell
is split by the binary logit {eq}`eq-12-logit-split`; for example

$$
\begin{aligned}
P_{11}^{1} &= \frac{e^{-0.05 \times 30}}{e^{-0.05 \times 30} + e^{-0.05 \times 45}} \\
&= \frac{1}{1 + e^{-0.75}} = 0.679 .
\end{aligned}
$$

| | $T_{i1}^1$ (car) | $T_{i1}^2$ (bus) | $T_{i2}^1$ (car) | $T_{i2}^2$ (bus) |
|---|---|---|---|---|
| $i = 1$ | 75.51 | 35.67 | 56.33 | 32.50 |
| $i = 2$ | 42.78 | 15.74 | 61.13 | 30.36 |
| $i = 3$ | 63.37 | 46.95 | 81.94 | 57.74 |

Car takes 57–73 % of each pair, depending on the time difference. The total
travel time is $\sum T_{ij}^kC_{ij}^k = 21\,712$ person-minutes per hour;
the model that reproduces an observed total expenditure $C$ is obtained by
adjusting $\beta$ until this value matches.
:::

## Composite costs and nesting

:::{prf:example} Composite cost of three modes
:label: ex-27-ms-composite

Three modes have generalized costs $C^1 = 30$, $C^2 = 20$, and $C^3 = 25$.
With $\lambda = 0.1$, compute the modal shares, the log-sum composite cost,
and the share-weighted average cost.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

$\sum_k e^{-0.1C^k} = e^{-3} + e^{-2} + e^{-2.5} = 0.0498 + 0.1353 + 0.0821 = 0.2672$, so

$$
\begin{aligned}
P^1 &= \frac{0.0498}{0.2672} = 0.186, \\
P^2 &= \frac{0.1353}{0.2672} = 0.506, \\
P^3 &= \frac{0.0821}{0.2672} = 0.307 .
\end{aligned}
$$

The composite cost {eq}`eq-12-composite-cost` is

$$
K = -\frac{1}{0.1}\ln 0.2672 = 13.20,
$$

lower than the cost of every mode, while the weighted average
$\sum_k P^kC^k = 0.186 \times 30 + 0.506 \times 20 + 0.307 \times 25 \approx 23.40$
lies between the costs. The log-sum reflects that each traveler uses the
mode that is best for him or her, including the unobserved part of the
cost; with three options available, the expected minimum perceived cost is
well below the cheapest *measured* cost.
:::

:::{prf:example} The red-bus/blue-bus problem
:label: ex-27-ms-red-blue

Car and bus have equal generalized costs and each carries half of the
travelers. The bus fleet is painted half red and half blue with no change
in service. Compare the predictions of an N-way logit split and of a
hierarchical split with $\lambda_1 = \lambda$ and $\lambda_2 \ge \lambda_1$.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

Let $C_C = C_{RB} = C_{BB} = C$.

**N-way logit.**
$P_C = P_{RB} = P_{BB} = e^{-\lambda C}/(3e^{-\lambda C}) = 1/3$: the car
share falls from 1/2 to 1/3 because of the paint.

**Hierarchical split.** The composite bus cost is

$$
C_B = -\frac{1}{\lambda_2}\ln\left(2e^{-\lambda_2 C}\right) = C - \frac{\ln 2}{\lambda_2},
$$

so

$$
\begin{aligned}
P_C &= \frac{1}{1 + \exp\left[-\lambda_1\left(C_B - C\right)\right]} \\
&= \frac{1}{1 + 2^{\lambda_1/\lambda_2}}, \\
P_{RB} &= P_{BB} = \frac{1 - P_C}{2}.
\end{aligned}
$$

For buses that are perfect substitutes, $\lambda_2 \to \infty$ and
$P_C \to 1/2$, $P_{RB} = P_{BB} \to 1/4$, the realistic answer. For
$\lambda_2 = \lambda_1$ the nest disappears and the N-way result 1/3 is
recovered. Intermediate values describe partially similar modes, such as
bus and light rail.
:::

## Calibration

:::{prf:example} Calibrating a binary logit split
:label: ex-27-ms-calibration

Observed shares of mode 1 and generalized costs on five O-D pairs are:

| Pair | $P_1$ (%) | $C_1$ | $C_2$ |
|---|---|---|---|
| 1 | 51 | 21.0 | 18.0 |
| 2 | 57 | 15.8 | 13.1 |
| 3 | 80 | 15.9 | 14.7 |
| 4 | 71 | 18.2 | 16.4 |
| 5 | 63 | 11.0 | 8.5 |

Calibrate $\lambda$ and the modal penalty $\delta$ of
{eq}`eq-12-binary-split-penalty`.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

By {eq}`eq-12-logit-linearization`, regress $y = \ln[P_1/(1 - P_1)]$ on
$x = C_2 - C_1$:

| Pair | $x = C_2 - C_1$ | $y$ | $x - \bar{x}$ | $(x - \bar{x})^2$ | $y(x - \bar{x})$ |
|---|---|---|---|---|---|
| 1 | −3.0 | 0.040 | −0.76 | 0.5776 | −0.0304 |
| 2 | −2.7 | 0.282 | −0.46 | 0.2116 | −0.1297 |
| 3 | −1.2 | 1.386 | 1.04 | 1.0816 | 1.4417 |
| 4 | −1.8 | 0.895 | 0.44 | 0.1936 | 0.3940 |
| 5 | −2.5 | 0.532 | −0.26 | 0.0676 | −0.1384 |
| Sum | −11.2 | 3.136 | 0 | 2.1320 | 1.5373 |

With $\bar{x} = -2.24$ and $\bar{y} = 0.627$,

$$
\begin{aligned}
\hat\lambda &= \frac{1.5373}{2.1320} = 0.721, \\
\widehat{\lambda\delta} &= 0.627 - 0.721 \times (-2.24) = 2.242, \\
\hat\delta &= \frac{2.242}{0.721} = 3.11 ,
\end{aligned}
$$

and $R^2 = 0.989$. The penalty is positive: mode 2 is cheaper in measured
cost on every pair, yet mode 1 has more than half of the trips, so mode 2
carries an unmeasured disadvantage equivalent to about 3.1 cost units.
:::

## Policy evaluation

:::{prf:example} Congestion pricing on a corridor
:label: ex-27-ms-pricing

A corridor carries $Q = 20\,000$ commuters per hour by rapid transit or by
car on a tolled highway. The value of time is $\alpha = 2.0$ HK\$/min, the
transit time is $T_T = 45$ min, the auto time is
$T_A = 30 + 2.0\times 10^{-6} Q_A^2$ min, and the logit parameter is
$\beta = 0.1$ per HK\$.

(1) With a transit fare $P_T = 3.0$ HK\$ and a toll $P_A = 10.0$ HK\$, find
the auto and transit volumes. (2) What toll reduces the auto volume to
2 500 veh/h?
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**(1) Equilibrium split.** The generalized costs are

$$
\begin{aligned}
C_T &= 2.0 \times 45 + 3.0 = 93.0~\text{HK\$}, \\
C_A &= 2.0\left(30 + 2.0\times 10^{-6}Q_A^2\right) + 10.0 = 70.0 + 4.0\times 10^{-6}Q_A^2 .
\end{aligned}
$$

By {eq}`eq-12-pricing-equilibrium`,

$$
\begin{aligned}
Q_A &= \frac{20\,000}{1 + \exp\left[-0.1\left(93.0 - 70.0 - 4.0\times 10^{-6}Q_A^2\right)\right]} \\
    &= \frac{20\,000}{1 + \exp\left(4.0\times 10^{-7}Q_A^2 - 2.3\right)} .
\end{aligned}
$$

With $x = Q_A/1000$, solve $f(x) = x - 20/[1 + \exp(0.4x^2 - 2.3)] = 0$ by
Newton's method, with

$$
f'(x) = 1 + \frac{16x\exp(0.4x^2 - 2.3)}{\left[1 + \exp(0.4x^2 - 2.3)\right]^2} .
$$

| $k$ | $x_k$ | $f(x_k)$ | $f'(x_k)$ |
|---|---|---|---|
| 0 | 2.0000 | −11.3638 | 8.0948 |
| 1 | 3.4038 | 1.6376 | 5.3848 |
| 2 | 3.0997 | −0.4214 | 8.1943 |
| 3 | 3.1511 | −0.0123 | 7.7134 |
| 4 | 3.1527 | 0.0000 | 7.6983 |

So $Q_A = 3\,153$ veh/h and $Q_T = 16\,847$ persons/h; the auto time is
$30 + 2\times 10^{-6}\times 3\,153^2 = 49.9$ min. The iteration stops when
$|f(x_k)|$ is below $10^{-4}$ (0.1 veh/h).

**(2) Toll for $Q_A = 2\,500$.** Now
$C_A = 2.0(30 + 2.0\times 10^{-6}\times 2500^2) + P_A = 85.0 + P_A$, and

$$
\begin{aligned}
2\,500 &= \frac{20\,000}{1 + \exp\left[-0.1\left(93.0 - 85.0 - P_A\right)\right]} \\
\Longrightarrow\quad e^{0.1P_A - 0.8} &= 7 \\
\Longrightarrow\quad P_A &= 10\ln 7 + 8 = 27.46~\text{HK\$}.
\end{aligned}
$$

Raising the toll from 10 to about 27.5 HK\$ removes some 650 cars per hour
and cuts the auto travel time from 49.9 to 42.5 minutes.
:::

:::{prf:example} Evaluating a bus lane
:label: ex-27-ms-bus-lane

$N = 5\,000$ commuters per hour use a three-lane highway by car (one person
per car) or by bus. The travel time per lane is $t = 9.0 + 0.012\,q$ min,
with $q$ the flow in veh/h/lane; 110 buses per hour run, each counting as
one car; $\beta = 0.5$ per minute; and the bus penalty is $\Delta = 5$ min.
Should one lane be reserved for buses?
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**Without a bus lane.** Buses and cars share the three lanes and have the
same travel time, so $C_{\mathrm{bus}} - C_{\mathrm{car}} = \Delta$ and

$$
\begin{aligned}
N_{\mathrm{bus}} &= \frac{5000}{1 + e^{0.5 \times 5}} = 379, \\
N_{\mathrm{car}} &= 4\,621 .
\end{aligned}
$$

The flow is $(4\,621 + 110)/3 = 1\,577$ veh/h/lane, so
$t = 9.0 + 0.012 \times 1\,576.9 = 27.923$ min and

$$
TC_3^0 = 379.3\times(27.923 + 5) + 4\,620.7\times 27.923 = 141\,511~\text{person-min/h}.
$$

**With one bus lane.** The buses alone use one lane:
$C_{\mathrm{bus}} = 9.0 + 0.012\times 110 + 5.0 = 15.32$ min. Cars share two
lanes, $C_{\mathrm{car}} = 9.0 + 0.012\,N_{\mathrm{car}}/2 = 9.0 + 0.006\,N_{\mathrm{car}}$,
and

$$
\begin{aligned}
N_{\mathrm{car}} &= \frac{5000}{1 + \exp\left[-0.5\left(15.32 - 9.0 - 0.006\,N_{\mathrm{car}}\right)\right]} \\
&= \frac{5000}{1 + \exp\left(0.003\,N_{\mathrm{car}} - 3.16\right)} .
\end{aligned}
$$

Newton's method on
$f(x) = x - 5000/[1 + \exp(0.003x - 3.16)]$ from $x_0 = 2000$ gives

| $k$ | $x_k$ | $f(x_k)$ | $f'(x_k)$ |
|---|---|---|---|
| 0 | 2000.0 | 1724.00 | 1.7823 |
| 1 | 1032.7 | −1544.59 | 4.7464 |
| 2 | 1358.1 | −72.36 | 4.0637 |
| 3 | 1375.9 | −0.63 | 3.9927 |
| 4 | 1376.1 | 0.00 | 3.9921 |

so $N_{\mathrm{car}} = 1\,376$, $N_{\mathrm{bus}} = 3\,624$,
$C_{\mathrm{car}} = 9.0 + 0.006 \times 1\,376 = 17.26$ min, and

$$
TC_3^1 = 3\,624 \times 15.32 + 1\,376 \times 17.26 = 79\,265~\text{person-min/h}.
$$

**Decision.** $CE = 79\,265/141\,511 = 0.560 < 1$: the bus lane cuts the
total travel cost by 44 %. Most commuters switch to the now much faster bus,
and the remaining cars are also faster (17.3 instead of 27.9 minutes). The
analysis assumes that the bus fleet can carry 3 624 passengers per hour
with 110 buses (about 33 per bus), which should be checked.
:::

## Calibration and market segments

:::{prf:example} Calibrating a car–rail split
:label: ex-27-hw3-q1

A corridor connects four residential areas A–D with three employment areas
U–W by car and rail. For each O-D pair the survey gives in-vehicle time
$X_1$ (min), excess (walking and waiting) time $X_2$ (min), out-of-pocket
cost $X_3$ (cents), parking cost $X_4$ (cents, car only), and the observed
car share:

| Pair | Car $X_1$ | Car $X_2$ | Car $X_3$ | Car $X_4$ | Rail $X_1$ | Rail $X_2$ | Rail $X_3$ | Car share |
|---|---|---|---|---|---|---|---|---|
| A-U | 23 | 3 | 120 | 40 | 19 | 10 | 72 | 0.80 |
| B-U | 20 | 3 | 96 | 40 | 17 | 8 | 64 | 0.82 |
| C-U | 18 | 3 | 80 | 40 | 14 | 10 | 28 | 0.85 |
| D-U | 15 | 3 | 68 | 40 | 14 | 12 | 20 | 0.90 |
| A-V | 26 | 4 | 152 | 60 | 23 | 10 | 104 | 0.70 |
| B-V | 19 | 4 | 96 | 60 | 18 | 9 | 72 | 0.90 |
| C-V | 14 | 4 | 60 | 60 | 11 | 9 | 36 | 0.75 |
| D-V | 12 | 4 | 56 | 60 | 12 | 11 | 28 | 0.90 |
| A-W | 30 | 5 | 160 | 80 | 25 | 10 | 120 | 0.50 |
| B-W | 20 | 5 | 100 | 80 | 16 | 8 | 92 | 0.55 |
| C-W | 15 | 5 | 64 | 80 | 12 | 9 | 36 | 0.58 |
| D-W | 10 | 5 | 52 | 80 | 8 | 9 | 24 | 0.60 |

(a) Calibrate a logit modal-split model, valuing in-vehicle time at
S\$10/h and excess time at twice that. (b) Estimate the effect of doubling
the perceived cost of running a car ($X_3$). (c) Estimate the effect of
free rail travel.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**(a) Generalized costs** (S\$; times converted at S\$10/h and S\$20/h,
cents divided by 100):

$$
\begin{aligned}
C_c &= \frac{10X_1}{60} + \frac{20X_2}{60} + \frac{X_3 + X_4}{100}, \\
C_r &= \frac{10X_1}{60} + \frac{20X_2}{60} + \frac{X_3}{100}.
\end{aligned}
$$

| Pair | $C_c$ | $C_r$ | $C_r - C_c$ | $\ln\frac{P_c}{1 - P_c}$ |
|---|---|---|---|---|
| A-U | 6.43 | 7.22 | 0.79 | 1.39 |
| B-U | 5.69 | 6.14 | 0.45 | 1.52 |
| C-U | 5.20 | 5.95 | 0.75 | 1.73 |
| D-U | 4.58 | 6.53 | 1.95 | 2.20 |
| A-V | 7.79 | 8.21 | 0.42 | 0.85 |
| B-V | 6.06 | 6.72 | 0.66 | 2.20 |
| C-V | 4.87 | 5.19 | 0.33 | 1.10 |
| D-V | 4.49 | 5.95 | 1.45 | 2.20 |
| A-W | 9.07 | 8.70 | −0.37 | 0.00 |
| B-W | 6.80 | 6.25 | −0.55 | 0.20 |
| C-W | 5.61 | 5.36 | −0.25 | 0.32 |
| D-W | 4.65 | 4.57 | −0.08 | 0.41 |

With rail as the mode carrying the penalty,
$P_c = 1/\{1 + \exp[-\lambda(C_r + \delta - C_c)]\}$, so
$\ln[P_c/(1 - P_c)] = \lambda(C_r - C_c) + \lambda\delta$
({eq}`eq-12-logit-linearization`). Regressing the last column on the one
before it gives

$$
\begin{aligned}
\hat\lambda &= 1.002, \\
\widehat{\lambda\delta} &= 0.712, \\
\hat\delta &= 0.710~\text{S\$}, \\
R^2 &= 0.81,
\end{aligned}
$$

so

$$
P_c = \frac{1}{1 + \exp\left[-1.002\left(C_r + 0.710 - C_c\right)\right]} .
$$

Rail carries a penalty equivalent to about S\$0.71 per trip beyond its
measured costs. The fit is weaker than in {prf:ref}`ex-27-ms-calibration`:
the costs explain about 81 % of the variation of the log-odds.

**(b) Doubling the car running cost** raises $C_c$ by $X_3/100$:

| Pair | new $C_c$ | model $P_c$ before | model $P_c$ after | change |
|---|---|---|---|---|
| A-U | 7.63 | 0.82 | 0.57 | −0.24 |
| B-U | 6.65 | 0.76 | 0.55 | −0.21 |
| C-U | 6.00 | 0.81 | 0.66 | −0.15 |
| D-U | 5.26 | 0.94 | 0.88 | −0.06 |
| A-V | 9.31 | 0.76 | 0.40 | −0.35 |
| B-V | 7.02 | 0.80 | 0.60 | −0.20 |
| C-V | 5.47 | 0.74 | 0.61 | −0.13 |
| D-V | 5.05 | 0.90 | 0.83 | −0.06 |
| A-W | 10.67 | 0.59 | 0.22 | −0.36 |
| B-W | 7.80 | 0.54 | 0.30 | −0.24 |
| C-W | 6.25 | 0.61 | 0.46 | −0.16 |
| D-W | 5.17 | 0.65 | 0.53 | −0.13 |

The car share falls by 6 to 36 percentage points; the largest falls are on
the long trips from A to W and V, where running costs are highest and the
car share is lowest, so that the logit curve is steepest.

**(c) Free rail** removes $X_3/100$ from $C_r$:

| Pair | new $C_r$ | model $P_c$ after | change |
|---|---|---|---|
| A-U | 6.50 | 0.69 | −0.13 |
| B-U | 5.50 | 0.63 | −0.13 |
| C-U | 5.67 | 0.76 | −0.05 |
| D-U | 6.33 | 0.92 | −0.01 |
| A-V | 7.17 | 0.52 | −0.23 |
| B-V | 6.00 | 0.66 | −0.14 |
| C-V | 4.83 | 0.66 | −0.08 |
| D-V | 5.67 | 0.87 | −0.03 |
| A-W | 7.50 | 0.30 | −0.29 |
| B-W | 5.33 | 0.32 | −0.22 |
| C-W | 5.00 | 0.53 | −0.09 |
| D-W | 4.33 | 0.60 | −0.06 |

Free fares shift fewer travelers than doubling car running costs, because
rail fares are smaller than car running costs on every pair. Changes should
be measured against the *model* shares in the base situation, not the
observed ones, so that the calibration error is not counted as an effect of
the policy.
:::

:::{prf:example} A distribution–modal-split model by person type
:label: ex-27-hw3-q2

Consider the model {eq}`eq-12-distribution-modal-split`,
$T_{ij}^n = A_iO_iB_jD_j\exp(-\beta K_{ij}^n)$, with composite cost
{eq}`eq-12-composite-cost`
$K_{ij}^n = -\frac{1}{\lambda^n}\ln\sum_k\exp(-\lambda^nC_{ij}^k)$, where person
type $n = 1$ has a car available and $n = 2$ does not; mode $k = 1$ is car
and $k = 2$ public transport. With $\lambda^1 = 0.20$, $\lambda^2 = 0.15$,
$\beta = 0.05$, $C_{ij}^1 = 20$, $C_{ij}^2 = 40$, and
$T_{ij} = T_{ij}^1 + T_{ij}^2 = 2\,000$ trips, how many trips use car and how
many use public transport?
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**Composite costs.** Person type 1 can use both modes:

$$
\begin{aligned}
K_{ij}^1 &= -\frac{1}{0.20}\ln\left(e^{-0.2 \times 20} + e^{-0.2 \times 40}\right) \\
&= -5\ln\left(0.018316 + 0.000335\right) = 19.91 .
\end{aligned}
$$

Person type 2 has only public transport, so $K_{ij}^2 = C_{ij}^2 = 40$.

**Trips by person type.** The factor $A_iO_iB_jD_j$ is common to both types:

$$
\begin{aligned}
A_iO_iB_jD_j &= \frac{2000}{e^{-0.05 \times 19.91} + e^{-0.05 \times 40}} \\
&= \frac{2000}{0.3695 + 0.1353} = 3\,961.3,
\end{aligned}
$$

so $T_{ij}^1 = 3\,961.3 \times 0.3695 = 1\,463.9$ and
$T_{ij}^2 = 536.1$.

**Modal split.** For type 1,

$$
P(\text{car} \mid n = 1) = \frac{e^{-4}}{e^{-4} + e^{-8}} = 0.9820 ;
$$

type 2 travelers all use public transport. Hence

$$
\begin{aligned}
\text{car} &= 1\,463.9 \times 0.9820 = 1\,437.6 \approx 1\,438, \\
\text{public transport} &= 1\,463.9 \times 0.0180 + 536.1 = 562.4 \approx 562 .
\end{aligned}
$$
:::
