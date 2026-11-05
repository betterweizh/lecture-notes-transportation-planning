# Trip Generation

This chapter works through the examples and problems of
{doc}`09-trip-generation`. A household-based regression model with dummy
variables is solved in {prf:ref}`ex-18-hw1-q5`. All regression results
below are computed from the data shown; the code in
{doc}`33-python-trip-generation` reproduces them.

## Growth factors and trip rates

:::{prf:example} Growth factor for car ownership
:label: ex-24-tg-growth-factor

A zone has 250 households with a car and 250 without. Car-owning households
produce 6.0 HB trips per day and the others 2.5. In the future all
households will own a car, while income and population stay constant.
Forecast the HB trips (a) with a growth factor based on car ownership, and
(b) with the household trip rates. Comment.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

The current number of trips is

$$
t_i = 250 \times 2.5 + 250 \times 6.0 = 2\,125~\text{trips/day}.
$$

**(a)** The share of car-owning households grows from $C_i^c = 0.5$ to
$C_i^d = 1$, so with a multiplicative growth factor

$$
\begin{aligned}
F_i &= \frac{C_i^{d}}{C_i^{c}} = \frac{1}{0.5} = 2, \\
T_i &= F_i\,t_i = 2 \times 2\,125 = 4\,250~\text{trips/day}.
\end{aligned}
$$

**(b)** Applying the trip rate of car-owning households to all 500
households gives $500 \times 6.0 = 3\,000$ trips/day.

The growth factor overestimates by about 42 % because it scales *all*
current trips, including the 625 trips of car-less households, by the
growth of car ownership, as if car-less households made no trips. This is
why growth factors are used only for crude estimates.
:::

:::{prf:example} Trip-rate model
:label: ex-24-tg-trip-rate

The present trip productions and attractions (thousand trips per day) and
the present and future residents (thousands) of four zones are:

| Zone | Productions | Attractions | Present residents | Future residents |
|---|---|---|---|---|
| 1 | 32 | 32 | 12 | 15 |
| 2 | 40 | 41 | 18 | 24 |
| 3 | 51 | 50 | 20 | 35 |
| 4 | 45 | 45 | 19 | 26 |

Assuming that the average number of trips per resident is stable, forecast
the total trip production per day.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

The present production rate is

$$
r = \frac{32 + 40 + 51 + 45}{12 + 18 + 20 + 19} = \frac{168}{69} = 2.435
~\text{trips per resident per day},
$$

so the future production is
$(15 + 24 + 35 + 26) \times 2.435 = 100 \times 2.435 = 243.5$ thousand
trips per day. Zonal productions follow in the same way, e.g.
$15 \times 2.435 = 36.5$ thousand for zone 1. Attractions would need their
own model (employment-based), since they need not grow with residents.
:::

## Regression models

:::{prf:example} Zonal trip production model
:label: ex-24-tg-zonal

Five residential zones have the following numbers of households and of
trips produced on a weekday:

| Zone | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Households $x$ | 1 000 | 1 500 | 2 500 | 3 000 | 4 000 |
| Trips $y$ | 7 900 | 11 900 | 20 000 | 23 800 | 31 800 |

Fit $y = \beta_0 + \beta_1 x$ and $y = \beta_1 x$, and choose a model.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**Model 1 (with intercept).** Least squares gives

$$
\hat{y} = -31.6 + 7.963\,x,
$$

with $\se(\hat\beta_0) = 90.4$, $T_0 = -0.35$ ($p = 0.75$),
$\se(\hat\beta_1) = 0.0344$, $T_1 = 231.3$, $\hat\sigma = 82.2$, and
$R^2 = 0.9999$. The intercept is not significant ($t_{0.025,3} = 3.182$) and
is negative, which would mean negative trips for a zone with very few
households.

**Model 2 (through the origin).**

$$
\hat{y} = 7.952\,x,
$$

with $\se(\hat\beta_1) = 0.0124$, $T_1 = 643.3$, and
$\hat\sigma = 72.6 < 82.2$.

Model 2 is preferred: it is simpler, it has a smaller residual standard
error, and it implies a constant rate of about 7.95 trips per household per
day. The near-perfect $R^2$ of both models is typical of models fitted to
zonal *totals* and says little about their forecasting ability.
:::

:::{prf:example} Household-based regression and its application
:label: ex-24-tg-household-regression

A household survey gives the average number of trips per day by household
size:

| Household size $x$ | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|
| Average trips per day $y$ | 5 | 7 | 8 | 10 | 10 |

(a) Fit models with and without an intercept and check their validity at
$\alpha = 0.05$. (b) A new town will have 1 000 households of size 2, 2 000
of size 4, 1 000 of size 6, 500 of size 8, and 400 of size 10. Forecast its
daily trip production with the model through the origin.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**(a) Model 1 (with intercept).** With $\bar{x} = 4$, $\bar{y} = 8$,
$S_{xx} = 10$, and $S_{xy} = 13$,

$$
\begin{aligned}
\hat\beta_1 &= \frac{13}{10} = 1.30, \\
\hat\beta_0 &= 8 - 1.30 \times 4 = 2.80 .
\end{aligned}
$$

$\mathit{SS}_E = 1.10$, so $\hat\sigma^2 = 1.10/3 = 0.367$
($\hat\sigma = 0.606$) and $R^2 = 0.939$. The standard errors are
$\se(\hat\beta_0) = 0.812$ and $\se(\hat\beta_1) = 0.191$, giving
$T_0 = 3.45$ and $T_1 = 6.79$, both above $t_{0.025,3} = 3.182$: both
coefficients are significant.

**Model 2 (through the origin).** $\sum x_i y_i = 173$ and
$\sum x_i^2 = 90$, so $\hat\beta = 1.922$ with
$\se(\hat\beta) = 0.123$ and $T = 15.6 > t_{0.025,4} = 2.776$; the uncentered
$R_0^2 = 0.984$ and $\hat\sigma = 1.168$.

Model 1 fits much better ($\hat\sigma = 0.61$ against 1.17) and its
intercept is significant, so statistically it should be preferred: a
household has about 2.8 trips plus 1.3 per member. Model 2's higher $R^2$
is the uncentered value and is not comparable.

**(b)** The new town has

$$
1000 \times 2 + 2000 \times 4 + 1000 \times 6 + 500 \times 8 + 400 \times 10 = 24\,000
$$

residents, so Model 2 gives
$\hat\beta \times 24\,000 = (173/90) \times 24\,000 = 46\,133$ trips/day.
Model 1 gives
$2.80 \times 4\,900 + 1.30 \times 24\,000 = 44\,920$ trips/day for the
4 900 households. Both models extrapolate far beyond the surveyed household
sizes (2–6), so the forecasts for households of 8 and 10 persons are
uncertain.
:::

:::{prf:example} Stepwise household model with dummy variables
:label: ex-24-tg-stepwise-household

A large household survey relates trips per household $Y$ to the number of
workers $X_1$ and cars $X_2$. Successive steps of a stepwise estimation gave
($t$ values in parentheses):

| Step | Equation | $R^2$ |
|---|---|---|
| 1 | $Y = 2.36\,X_1$ | 0.203 |
| 2 | $Y = 1.80\,X_1 + 1.31\,X_2$ | 0.325 |
| 3 | $Y = 0.91\ (3.7) + 1.44\,X_1\ (8.2) + 1.07\,X_2\ (4.2)$ | 0.384 |

(a) Which model should be chosen? (b) Replacing $X_2$ by dummy variables
$Z_1$ (one car) and $Z_2$ (two or more cars) gives
$Y = 0.84\ (3.6) + 1.41\,X_1\ (8.1) + 0.75\,Z_1\ (3.2) + 3.14\,Z_2\ (3.5)$
with $R^2 = 0.387$. Interpret this model.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**(a)** The sample is large, so the $t$ statistics can be compared with the
normal critical value. The alternatives are one-sided (trips should increase
with workers and cars), so the critical value at 5 % is $z_{0.05} = 1.645$.
In step 3 all three $t$ values (3.7, 8.2, 4.2) exceed 1.645, the signs are
as expected, and the intercept (0.91 trips) is small compared with the
effect of a worker (1.44 trips). The third model has the highest $R^2$,
which is modest — as is usual for household-level data, where much of the
variation is individual — and is the one to choose. Steps 1 and 2 are
forced through the origin, which the significant intercept in step 3 shows
to be inappropriate.

**(b)** For a given number of workers, the dummy model predicts

$$
\begin{aligned}
\text{no car:}\quad & Y = 0.84 + 1.41\,X_1, \\
\text{one car:}\quad & Y = 0.84 + 0.75 + 1.41\,X_1 = 1.59 + 1.41\,X_1, \\
\text{two or more cars:}\quad & Y = 0.84 + 3.14 + 1.41\,X_1 = 3.98 + 1.41\,X_1,
\end{aligned}
$$

three parallel lines. The first car adds 0.75 trips but the second adds
$3.14 - 0.75 = 2.39$ more — a strongly non-linear effect that the linear
term $1.07\,X_2$ (1.07 trips per car) cannot capture. All coefficients are
significant and $R^2$ rises slightly; the dummy model is better.
:::

:::{prf:example} Trip attraction model
:label: ex-24-tg-attraction

Five zones have the following employment and daily work trips attracted:

| Zone | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Manufacturing jobs $X_1$ | 60 | 40 | 30 | 20 | 100 |
| Service jobs $X_2$ | 30 | 100 | 20 | 30 | 20 |
| Work trips attracted $Y$ | 190 | 290 | 150 | 120 | 250 |

Compare the models (1) $Y = \beta_1 X_1$, (2) $Y = \beta_2 X_2$,
(3) $Y = \beta_1 X_1 + \beta_2 X_2$, and
(4) $Y = \beta_0 + \beta_1 X_1 + \beta_2 X_2$ at $\alpha = 0.05$.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

Estimating each model by least squares:

| Model | Estimates ($t$ values) | d.f. | $t_{0.025}$ | $\hat\sigma$ | $R^2$ |
|---|---|---|---|---|---|
| 1 | $3.327\,X_1$ (4.45) | 4 | 2.776 | 96.1 | 0.832 (uncentered) |
| 2 | $3.675\,X_2$ (3.71) | 4 | 2.776 | 111.2 | 0.775 (uncentered) |
| 3 | $2.167\,X_1$ (8.12) $+\ 2.126\,X_2$ (6.96) | 3 | 3.182 | 26.8 | 0.990 (uncentered) |
| 4 | $47.9$ (2.33) $+\ 1.657\,X_1$ (5.99) $+\ 1.730\,X_2$ (6.70) | 2 | 4.303 | 17.0 | 0.970 |

- Models 1 and 2 omit an important variable: their residual standard errors
  are four to six times those of Models 3 and 4.
- In Model 4 the intercept is not significant ($2.33 < 4.303$), and a
  positive intercept would mean work trips to a zone without jobs.
- Model 3 has both coefficients significant with the expected signs: each
  job attracts about 2.1–2.2 work trips per day.

**Model 3** is chosen. (Model 4 fits slightly better, but with only two
residual degrees of freedom the evidence for its intercept is weak.)
:::

:::{prf:example} Stepwise selection of a trip attraction model
:label: ex-24-tg-stepwise-attraction

For 16 zones the peak-hour trips attracted $Y$ and the employment in
manufacturing $X_2$, retail and services $X_3$, and other sectors $X_4$
(total $X_1 = X_2 + X_3 + X_4$) are:

| Zone | $X_1$ | $X_2$ | $X_3$ | $X_4$ | $Y$ |
|---|---|---|---|---|---|
| 1 | 9 482 | 6 820 | 2 547 | 115 | 9 428 |
| 2 | 2 010 | 111 | 1 899 | 0 | 2 192 |
| 3 | 574 | 228 | 87 | 259 | 330 |
| 4 | 127 | 0 | 127 | 0 | 153 |
| 5 | 3 836 | 2 729 | 813 | 294 | 3 948 |
| 6 | 953 | 101 | 773 | 79 | 1 188 |
| 7 | 223 | 165 | 58 | 0 | 240 |
| 8 | 36 | 6 | 30 | 0 | 556 |
| 9 | 2 223 | 1 550 | 499 | 174 | 2 064 |
| 10 | 272 | 0 | 166 | 106 | 280 |
| 11 | 50 | 0 | 48 | 2 | 280 |
| 12 | 209 | 36 | 173 | 0 | 230 |
| 13 | 410 | 140 | 7 | 263 | 420 |
| 14 | 11 023 | 10 932 | 63 | 28 | 9 654 |
| 15 | 527 | 188 | 325 | 14 | 450 |
| 16 | 183 | 123 | 59 | 1 | 130 |

Develop the model with the stepwise procedure.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**Steps 1–3: correlations.** The sample correlation matrix is

| | $X_1$ | $X_2$ | $X_3$ | $X_4$ | $Y$ |
|---|---|---|---|---|---|
| $X_1$ | 1 | | | | |
| $X_2$ | 0.978 | 1 | | | |
| $X_3$ | 0.496 | 0.304 | 1 | | |
| $X_4$ | 0.110 | 0.068 | 0.074 | 1 | |
| $Y$ | 0.996 | 0.959 | 0.554 | 0.113 | 1 |

Total employment $X_1$ is almost perfectly associated with $Y$ (0.996), and
so is manufacturing $X_2$ (0.959); $X_3$ and $X_4$ are less associated. But
$X_1$ and $X_2$ are highly correlated (0.978), because manufacturing is the
largest component of total employment — and $X_1$ is an exact linear
combination of $X_2$, $X_3$, $X_4$.

**Step 4: collinearity.** $X_1$ must not appear together with its
components. The candidate models are therefore

- A: $Y = \beta_0 + \beta_1 X_1$;
- B: $Y = \beta_0 + \beta_2 X_2$;
- C: $Y = \beta_0 + \beta_2 X_2 + \beta_3 X_3$; D: the same without $\beta_0$;
- E: $Y = \beta_0 + \beta_2 X_2 + \beta_3 X_3 + \beta_4 X_4$; F: the same
  without $\beta_0$.

**Steps 5–6: estimation and assessment** ($t$ values in parentheses):

| Model | Estimates | $\hat\sigma$ | $R^2$ |
|---|---|---|---|
| A | $124.5$ (1.42) $+\ 0.919\,X_1$ (40.3) | 299.6 | 0.992 |
| B | $563.9$ (2.21) $+\ 0.974\,X_2$ (12.6) | 920.3 | 0.919 |
| C | $102.8$ (1.43) $+\ 0.884\,X_2$ (43.4) $+\ 1.230\,X_3$ (14.4) | 231.9 | 0.995 |
| D | $0.891\,X_2$ (43.4) $+\ 1.285\,X_3$ (16.2) | 240.4 | 0.996 (uncentered) |
| E | $31.0$ (0.40) $+\ 0.883\,X_2$ (46.9) $+\ 1.222\,X_3$ (15.5) $+\ 0.935\,X_4$ (1.81) | 213.8 | 0.996 |
| F | $0.884\,X_2$ (49.4) $+\ 1.234\,X_3$ (17.3) $+\ 1.041\,X_4$ (2.43) | 206.8 | 0.997 (uncentered) |

Models with two parameters (A, B, D) have 14 residual degrees of freedom
($t_{0.025,14} = 2.145$), models with three (C, F) have 13
($t_{0.025,13} = 2.160$), and E has 12 ($t_{0.025,12} = 2.179$).

- The intercepts of A, C, and E are not significant; B's intercept of 564
  trips is significant but implausibly large, and B omits retail and
  services, which attract more trips per job than manufacturing
  ($\approx 1.2$ against $0.9$).
- A is simple and fits well, but it hides the different attraction rates of
  the sectors, so it cannot represent a change in the employment mix.
- D and F have plausible coefficients, all significant; F adds $X_4$
  ($t = 2.43 > 2.160$) and has the smallest residual standard error.

**Model F**, $Y = 0.884\,X_2 + 1.234\,X_3 + 1.041\,X_4$, is chosen; Model D
is an acceptable simpler alternative if other employment is hard to
forecast. Zone 8 (36 jobs but 556 trips) is an outlier that should be
checked in the data.
:::

## Cross-classification and person categories

:::{prf:example} Household cross-classification
:label: ex-24-tg-cross-class

Average daily HB work trip rates by household type are:

| Car ownership | Low income, 1–3 persons | Low, ≥ 4 | Medium, 1–3 | Medium, ≥ 4 | High, 1–3 | High, ≥ 4 |
|---|---|---|---|---|---|---|
| No car | 3.4 | 4.9 | 3.7 | 5.0 | 3.8 | 5.1 |
| 1 car | 5.2 | 6.9 | 7.3 | 8.3 | 8.0 | 10.2 |
| 2 or more cars | 5.8 | 7.2 | 8.1 | 11.8 | 10.0 | 12.9 |

A zone has 100 low-income households of 1–3 persons without a car, 200
low-income households of 4 or more persons without a car, 300
medium-income households of 4 or more persons with one car, and 50
high-income households of 4 or more persons with two or more cars. Estimate
its HB work trip production.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

By {eq}`eq-09-cross-class-production`, multiply the number of households of
each type by its rate and add:

$$
\begin{aligned}
O_i &= 100 \times 3.4 + 200 \times 4.9 + 300 \times 8.3 + 50 \times 12.9 \\
    &= 340 + 980 + 2\,490 + 645 = 4\,455
\end{aligned}
$$

HB work trips per day. The rates increase with car ownership and household
size in almost every column, but not linearly — exactly the kind of
relationship a cross-classification model represents without assuming a
functional form.
:::

:::{prf:example} Trip attraction rates
:label: ex-24-tg-attraction-rates

A published model gives daily HB non-work trip attractions of 0.7 per
household, 0.7 per basic employee, 8.4 per retail employee, and 3.5 per
service employee (school enrollment does not apply here). Compute the
attractions of a zone with 20 households, 200 basic, 10 retail, and 100
service employees.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

$$
\begin{aligned}
D_j &= 20 \times 0.7 + 200 \times 0.7 + 10 \times 8.4 + 100 \times 3.5 \\
&= 14 + 140 + 84 + 350 = 588
\end{aligned}
$$

person trips per day. Retail and service jobs dominate, although the zone
has twice as many basic employees.
:::

:::{prf:example} Person-category model
:label: ex-24-tg-person-category

Daily **vehicle** trip rates for eight person categories (Supernak et al.,
1983) are:

| Category | Description | HB work and education | HB other | NHB | Total |
|---|---|---|---|---|---|
| 1 | age < 18 | 0.63 | 0.48 | 0.15 | 1.26 |
| 2 | 18–65, employed, no car | 0.98 | 0.28 | 0.27 | 1.53 |
| 3 | 18–65, employed, 1 car | 1.57 | 0.83 | 0.52 | 2.91 |
| 4 | 18–65, employed, 2+ cars | 1.61 | 0.82 | 0.63 | 3.09 |
| 5 | 18–65, not employed, no car | 0.06 | 0.31 | 0.11 | 0.48 |
| 6 | 18–65, not employed, 1 car | 0.16 | 1.04 | 0.32 | 1.52 |
| 7 | 18–65, not employed, 2+ cars | 0.21 | 1.50 | 0.39 | 2.10 |
| 8 | age > 65 | 0.12 | 0.60 | 0.28 | 1.00 |

A zone has 200, 300, 400, 500, 600, 700, 800, and 900 persons in
categories 1 to 8. Estimate its vehicle trip production.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

By {eq}`eq-09-person-category`, $T_i = \sum_j N_i\alpha_{ij}t_j$, where
$N_i\alpha_{ij}$ is the number of persons in category $j$. By purpose:

$$
\begin{aligned}
\text{HB work/education:}\quad
& 200(0.63) + 300(0.98) + 400(1.57) \\
& + 500(1.61) + 600(0.06) + 700(0.16) \\
& + 800(0.21) + 900(0.12) = 2\,277, \\
\text{HB other:}\quad
& 200(0.48) + 300(0.28) + 400(0.83) \\
& + 500(0.82) + 600(0.31) + 700(1.04) \\
& + 800(1.50) + 900(0.60) = 3\,576, \\
\text{NHB:}\quad
& 200(0.15) + 300(0.27) + 400(0.52) \\
& + 500(0.63) + 600(0.11) + 700(0.32) \\
& + 800(0.39) + 900(0.28) = 1\,488 .
\end{aligned}
$$

The total is $2\,277 + 3\,576 + 1\,488 = 7\,341$ vehicle trips per day.
(Using the rounded totals of the last column gives 7 352; the difference
comes from rounding in the published rates.) Employed adults with cars
(categories 3 and 4) produce 37 % of the vehicle trips although they are
20 % of the population.
:::

## Bayesian updating

:::{prf:example} Updating trip rates with a small sample
:label: ex-24-tg-bayes

A study ten years ago gave, for two household categories, the following
trip rates; a small new stratified sample gives the second set of values.

| | Category 1 (prior) | Category 2 (prior) | Category 1 (new) | Category 2 (new) |
|---|---|---|---|---|
| Mean trips per day | 8 | 5 | 12 | 6 |
| Observations | 65 | 300 | 30 | 30 |
| Trip-rate variance | 64 | 15 | 144 | 36 |
| Variance of the mean | 0.985 | 0.050 | 4.80 | 1.20 |

Compute the updated rates and their variances.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

The variances of the means are $S^2/n$: for category 1, $64/65 = 0.985$
(prior) and $144/30 = 4.80$ (new). By {eq}`eq-09-bayes-update`,

$$
\begin{aligned}
t_2^{(1)} &= \frac{8/0.985 + 12/4.80}{1/0.985 + 1/4.80} \\
           &= \frac{8.125 + 2.500}{1.016 + 0.208} = 8.68, \\
\sigma_2^{2\,(1)} &= \frac{1}{1/0.985 + 1/4.80} = 0.817, \\
t_2^{(2)} &= \frac{5/0.050 + 6/1.20}{1/0.050 + 1/1.20} \\
           &= \frac{100 + 5}{20 + 0.833} = 5.04, \\
\sigma_2^{2\,(2)} &= \frac{1}{20.833} = 0.048 .
\end{aligned}
$$

For category 1 the prior and the new sample have comparable precision, so
the updated rate (8.68) moves noticeably toward the new value 12; for
category 2 the prior, based on 300 observations with small variance, is 24
times more precise than the new sample and the rate hardly changes (5.04).
:::

## Balancing productions and attractions

:::{prf:example} Balancing trip ends
:label: ex-24-tg-balancing

Trip generation models give productions $O = (200, 300, 250)$ and
attractions $D = (280, 320, 200)$ for three zones. Balance them.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

$\sum_i O_i = 750$ and $\sum_j D_j = 800$. Taking productions as the
control total, by {eq}`eq-09-balance-attractions`

$$
\begin{aligned}
f &= \frac{750}{800} = 0.9375, \\
D' &= 0.9375 \times (280, 320, 200) = (262.5,\ 300,\ 187.5),
\end{aligned}
$$

which sums to 750. The balanced trip ends can now be used in a doubly
constrained distribution model.
:::
