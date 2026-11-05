# Regression and Hypothesis Tests

This chapter works through the examples and problems of
{doc}`02-regression-and-hypothesis-tests`, including a model with dummy
variables. All tests use the significance level $\alpha = 0.05$ unless stated otherwise.
Numbers are computed at full precision and rounded for display; the Python
code in {doc}`32-python-foundations` reproduces them.

## Simple linear regression

The first two examples use the same data: the number of cars $x$ and the
number of trips $y$ of eight zones.

| Zone | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| Cars $x$ | 200 | 50 | 500 | 100 | 100 | 400 | 300 | 400 |
| Trips $y$ | 500 | 300 | 1300 | 200 | 400 | 1200 | 900 | 1000 |

:::{prf:example} Zonal trips and car ownership
:label: ex-18-slr-trips

Fit the model $Y = \beta_0 + \beta_1 X + \varepsilon$ to the data above and
check its validity at $\alpha = 0.05$.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**Summary statistics.** With $n = 8$, $\sum x_i = 2\,050$ and
$\sum y_i = 5\,800$, so $\bar{x} = 256.25$ and $\bar{y} = 725$. Further,

$$
\begin{aligned}
S_{xx} &= \sum_i (x_i - \bar{x})^2 = 197\,187.5, \\
S_{xy} &= \sum_i y_i (x_i - \bar{x}) = 488\,750, \\
\mathit{SS}_T &= \sum_i (y_i - \bar{y})^2 = 1\,275\,000 .
\end{aligned}
$$

**Estimates.** By {eq}`eq-02-slr-estimates`,

$$
\begin{aligned}
\hat\beta_1 &= \frac{488\,750}{197\,187.5} = 2.4786, \\
\hat\beta_0 &= 725 - 2.4786 \times 256.25 = 89.86,
\end{aligned}
$$

so $\hat{y} = 89.86 + 2.479\,x$: each additional car is associated with
about 2.5 additional trips.

**Goodness of fit.** The residual sum of squares is
$\mathit{SS}_E = \sum_i (y_i - \hat{y}_i)^2 = 63\,582$, so
$\mathit{SS}_R = 1\,275\,000 - 63\,582 = 1\,211\,418$ and

$$
R^2 = \frac{1\,211\,418}{1\,275\,000} = 0.950 .
$$

**Error variance.** $\hat\sigma^2 = 63\,582/(8 - 2) = 10\,597$, so
$\hat\sigma = 102.9$ trips.

**Test on the intercept.** $H_0: \beta_0 = 0$ against $H_1: \beta_0 \ne 0$.

$$
\begin{aligned}
\se(\hat\beta_0) &= \sqrt{10\,597\left(\frac{1}{8} + \frac{256.25^2}{197\,187.5}\right)} \\
&= 69.67, \\
T_0 &= \frac{89.86}{69.67} = 1.29 .
\end{aligned}
$$

Since $\lvert T_0\rvert = 1.29 < t_{0.025,\,6} = 2.447$, $H_0$ is **not
rejected** ($p = 0.24$): the data do not show a non-zero intercept.

**Test on the slope.** $H_0: \beta_1 = 0$ against $H_1: \beta_1 \ne 0$.

$$
\begin{aligned}
\se(\hat\beta_1) &= \sqrt{\frac{10\,597}{197\,187.5}} = 0.2318, \\
T_1 &= \frac{2.4786}{0.2318} = 10.69 .
\end{aligned}
$$

Since $10.69 > 2.447$, $H_0$ is **rejected** ($p = 4\times 10^{-5}$): car
ownership has a significant effect on trips.

Because the intercept is not significant, it is natural to try the model
without an intercept ({prf:ref}`ex-18-slr-origin`).
:::

:::{prf:example} Regression through the origin
:label: ex-18-slr-origin

Fit the model $Y = \beta_1 X + \varepsilon$ to the same data, test the
slope, and compare the model with that of {prf:ref}`ex-18-slr-trips`.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**Estimate.** With $\sum x_i y_i = 1\,975\,000$ and
$\sum x_i^2 = 722\,500$, by {eq}`eq-02-slr-origin`

$$
\begin{aligned}
\hat\beta_1 &= \frac{1\,975\,000}{722\,500} = 2.7336, \\
\hat{y} &= 2.734\,x .
\end{aligned}
$$

**Goodness of fit.** The residual sum of squares is
$\mathit{SS}_E = 81\,211$ and $\sum y_i^2 = 5\,480\,000$, so the
uncentered coefficient {eq}`eq-02-r2-uncentered` is

$$
R_0^2 = 1 - \frac{81\,211}{5\,480\,000} = 0.985 .
$$

**Test on the slope.** With $n - 1 = 7$ degrees of freedom,
$\hat\sigma^2 = 81\,211/7 = 11\,602$ and

$$
\begin{aligned}
\se(\hat\beta_1) &= \sqrt{\frac{11\,602}{722\,500}} = 0.1267, \\
T_1 &= \frac{2.7336}{0.1267} = 21.57 > t_{0.025,\,7} = 2.365,
\end{aligned}
$$

so $H_0: \beta_1 = 0$ is rejected.

**Comparison.** The $R_0^2 = 0.985$ of this model is *not* comparable with
the $R^2 = 0.950$ of the model with an intercept, because it is measured
around zero rather than around $\bar{y}$. Comparing residual standard errors
instead, the model through the origin has $\hat\sigma = 107.7$ against
$102.9$ with an intercept: it fits slightly worse, as it must since it has
one parameter less, but the difference is small and the intercept is not
significant. The model through the origin is simpler and has the sensible
property that a zone without cars generates no car-related trips; either
model is acceptable.
:::

## Multiple linear regression

:::{prf:example} Freight volume model
:label: ex-18-mlr-freight

Fit $Y = \beta_0 + \beta_1 X_1 + \beta_2 X_2 + \beta_3 X_3 + \varepsilon$
to five observations of freight volume $Y$, population $X_1$, vehicles
$X_2$, and production $X_3$, and test the coefficients.

| No. | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Freight volume $Y$ | 100 | 95 | 106 | 111 | 90 |
| Population $X_1$ | 14 | 11 | 16 | 18 | 10 |
| Vehicles $X_2$ | 1.6 | 1.4 | 1.8 | 1.9 | 1.2 |
| Production $X_3$ | 4.2 | 4.0 | 5.0 | 5.9 | 3.2 |
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**Normal equations.** With a column of ones for the intercept,

$$
\bX\T\bX = \begin{bmatrix}
5 & 69 & 7.9 & 22.3 \\
69 & 997 & 112.8 & 321 \\
7.9 & 112.8 & 12.81 & 36.37 \\
22.3 & 321 & 36.37 & 103.69
\end{bmatrix},
\qquad
\bX\T\by = \begin{bmatrix} 502 \\ 7039 \\ 802.7 \\ 2272.9 \end{bmatrix},
$$

$$
(\bX\T\bX)^{-1} = \begin{bmatrix}
24.133 & 3.357 & -48.712 & 1.503 \\
3.357 & 0.875 & -8.372 & -0.495 \\
-48.712 & -8.372 & 123.440 & -6.905 \\
1.503 & -0.495 & -6.905 & 3.641
\end{bmatrix}.
$$

**Estimates.** By {eq}`eq-02-ols`,

$$
\hat{y} = 60.75 + 0.811\,x_1 + 10.40\,x_2 + 2.697\,x_3 .
$$

**Goodness of fit.** $\mathit{SS}_E = 0.01148$ and
$\mathit{SS}_T = 281.2$, so

$$
\begin{aligned}
R^2 &= 1 - \frac{0.01148}{281.2} = 0.99996, \\
\bar{R}^2 &= 1 - \frac{0.01148/1}{281.2/4} = 0.99984 .
\end{aligned}
$$

**Tests.** There are $n - k - 1 = 5 - 3 - 1 = 1$ residual degree of
freedom, $\hat\sigma^2 = 0.01148$, and $t_{0.025,\,1} = 12.706$. With
$\se(\hat\beta_j) = \sqrt{\hat\sigma^2 c_{jj}}$:

| Coefficient | Estimate | $c_{jj}$ | Std. error | $T_j$ | Decision |
|---|---|---|---|---|---|
| $\beta_0$ | 60.749 | 24.133 | 0.526 | 115.43 | reject $H_0$ |
| $\beta_1$ | 0.811 | 0.875 | 0.100 | 8.09 | do not reject |
| $\beta_2$ | 10.402 | 123.440 | 1.190 | 8.74 | do not reject |
| $\beta_3$ | 2.697 | 3.641 | 0.204 | 13.20 | reject $H_0$ |

For example, $T_0 = 60.749/\sqrt{0.01148 \times 24.133} = 115.43$.

**Interpretation.** The fit looks almost perfect, yet $\beta_1$ and
$\beta_2$ are not significant at 5 % (they would be at 10 %, where
$t_{0.05,1} = 6.31$). With four parameters and five observations there is a
single residual degree of freedom, the critical $t$ value is huge, and $R^2$
is close to one almost automatically. Population, vehicles, and production
are also strongly correlated with each other. A model for planning should
be estimated from many more observations, probably with fewer predictors.
:::

:::{prf:example} Model without an intercept
:label: ex-18-mlr-noint

Fit $Y = \beta_1 X_1 + \beta_2 X_2 + \varepsilon$ to six observations of
the number of trips per year $Y$, cars per household member $X_1$, and
income $X_2$, and test the coefficients.

| No. | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| Trips per year $Y$ | 21 | 17 | 28 | 18 | 34 | 38 |
| Cars per member $X_1$ | 0.4 | 0.4 | 3.1 | 0.6 | 1.7 | 9.4 |
| Income $X_2$ | 15.8 | 16.3 | 3.7 | 15.7 | 12.3 | 4.6 |
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**Estimates.** Without a column of ones,

$$
\bX\T\bX = \begin{bmatrix} 101.54 & 97.88 \\ 97.88 & 947.96 \end{bmatrix},
\qquad
\bX\T\by = \begin{bmatrix} 527.8 \\ 1588.1 \end{bmatrix},
$$

$$
(\bX\T\bX)^{-1} = \begin{bmatrix}
0.0109369 & -0.0011293 \\ -0.0011293 & 0.0011715
\end{bmatrix},
\qquad
\hat\bbeta = \begin{bmatrix} 3.979 \\ 1.264 \end{bmatrix}.
$$

So $\hat{y} = 3.979\,x_1 + 1.264\,x_2$.

**Goodness of fit.** $\mathit{SS}_E = 329.79$ and $\sum y_i^2 = 4\,438$; by
{eq}`eq-02-r2-uncentered-mlr`,

$$
\begin{aligned}
R_0^2 &= 1 - \frac{329.79}{4\,438} = 0.926, \\
\bar{R}_0^2 &= 1 - \frac{329.79/(6 - 2)}{4\,438/6} = 0.889 .
\end{aligned}
$$

**Tests.** $\hat\sigma^2 = 329.79/(6 - 2) = 82.45$ and
$t_{0.025,\,4} = 2.776$:

$$
\begin{aligned}
T_1 &= \frac{3.979}{\sqrt{82.45 \times 0.0109369}} = \frac{3.979}{0.950} = 4.19, \\
T_2 &= \frac{1.264}{\sqrt{82.45 \times 0.0011715}} = \frac{1.264}{0.311} = 4.07 .
\end{aligned}
$$

Both exceed 2.776, so both predictors are significant.
:::

## Comparing two means

:::{prf:example} Morning and afternoon traffic flows
:label: ex-18-two-means

Traffic flows on a campus avenue (thousands of vehicles) were recorded on 48
mornings and 43 afternoons. Is the mean flow different in the two periods?

Morning ($n_1 = 48$):

| | | | | | | | |
|---|---|---|---|---|---|---|---|
| 6.491 | 7.253 | 6.604 | 7.131 | 6.779 | 6.863 | 6.622 | 7.843 |
| 7.903 | 7.166 | 8.420 | 7.941 | 6.789 | 6.601 | 8.287 | 5.741 |
| 7.433 | 6.995 | 7.822 | 6.712 | 7.359 | 7.075 | 7.456 | 6.386 |
| 6.683 | 8.229 | 6.918 | 7.895 | 7.050 | 6.145 | 7.248 | 8.104 |
| 7.157 | 7.163 | 6.403 | 7.211 | 8.080 | 5.536 | 6.361 | 7.091 |
| 8.614 | 6.004 | 6.930 | 6.624 | 7.028 | 7.012 | 5.579 | 6.644 |

Afternoon ($n_2 = 43$):

| | | | | | | | |
|---|---|---|---|---|---|---|---|
| 6.485 | 7.252 | 7.966 | 7.490 | 8.703 | 6.725 | 7.648 | 7.386 |
| 9.985 | 7.926 | 9.185 | 7.440 | 8.797 | 7.235 | 9.731 | 7.816 |
| 7.801 | 7.496 | 8.214 | 8.543 | 7.598 | 8.059 | 7.809 | 6.955 |
| 7.721 | 6.340 | 8.415 | 8.356 | 8.098 | 7.773 | 8.437 | 7.930 |
| 7.086 | 8.138 | 6.936 | 8.782 | 8.410 | 6.575 | 7.699 | 6.988 |
| 8.090 | 8.461 | 7.238 | | | | | |
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**Hypotheses.** $H_0: \mu_1 = \mu_2$ against $H_1: \mu_1 \ne \mu_2$.

**Sample statistics.**

$$
\begin{aligned}
\bar{x}_1 &= \frac{339.38}{48} = 7.070, \\
s_1^2 &= 0.522; \\
\bar{x}_2 &= \frac{337.72}{43} = 7.854, \\
s_2^2 &= 0.637 .
\end{aligned}
$$

**Test statistic.** Both samples are larger than 40, so by
{eq}`eq-02-two-sample-z`

$$
\begin{aligned}
z_0 &= \frac{7.070 - 7.854}{\sqrt{0.522/48 + 0.637/43}} \\
&= \frac{-0.7835}{0.1603} = -4.89 .
\end{aligned}
$$

**Decision.** $\lvert z_0\rvert = 4.89 > z_{0.025} = 1.96$, so $H_0$ is
rejected; the $p$-value is $2[1 - \Phi(4.89)] \approx 1\times 10^{-6}$. The
afternoon flow is significantly higher, by about 780 vehicles on average.
:::

## Models with dummy variables

:::{prf:example} Household work-trip models
:label: ex-18-hw1-q5

A household survey gives the number of morning-peak work trips $y$, the
number of workers $x_1$, and the number of cars $x_2$ of ten households.

| Household | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|---|---|---|---|
| Trips $y$ | 2 | 4 | 6 | 3 | 4 | 5 | 4 | 5 | 7 | 7 |
| Workers $x_1$ | 2 | 4 | 5 | 1 | 1 | 3 | 2 | 2 | 4 | 3 |
| Cars $x_2$ | 0 | 0 | 1 | 1 | 1 | 1 | 2 | 2 | 3 | 2 |

Two models are proposed:

$$
\begin{aligned}
\text{Model 1:}\quad y &= \beta_0^{(1)} + \beta_1^{(1)} x_1 + \beta_2^{(1)} x_2, \\
\text{Model 2:}\quad y &= \beta_0^{(2)} + \beta_1^{(2)} x_1 + \beta_2^{(2)} z_1 + \beta_3^{(2)} z_2,
\end{aligned}
$$

where $z_1 = 1$ if the household has exactly one car and $z_2 = 1$ if it has
two or more cars (0 otherwise).

(a) Estimate both models, with $t$-tests and $R^2$. (b) Choose one model.
(c) A zone has 1 000 households with an average of two workers each; 50 %
have no car, 35 % one car, and 15 % two cars. Estimate the trips $O_i$
generated by the zone with both models and discuss the results.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**(a) Model 1.** With $\bX = [\mathbf{1}, \bx_1, \bx_2]$,

$$
\bX\T\bX = \begin{bmatrix} 10 & 27 & 13 \\ 27 & 89 & 36 \\ 13 & 36 & 25 \end{bmatrix},
\qquad
\bX\T\by = \begin{bmatrix} 47 \\ 139 \\ 71 \end{bmatrix},
$$

$$
(\bX\T\bX)^{-1} = \begin{bmatrix}
0.7168 & -0.1597 & -0.1427 \\
-0.1597 & 0.0625 & -0.0069 \\
-0.1427 & -0.0069 & 0.1242
\end{bmatrix},
\qquad
\hat\bbeta^{(1)} = \begin{bmatrix} 1.354 \\ 0.688 \\ 1.146 \end{bmatrix}.
$$

$\mathit{SS}_E = 4.4375$, $\mathit{SS}_T = 24.1$, so $R^2 = 0.816$ and
$\bar{R}^2 = 0.763$; $\hat\sigma^2 = 4.4375/7 = 0.634$ and
$t_{0.025,7} = 2.365$.

| Coefficient | Estimate | Std. error | $T_j$ | Significant at 5 %? |
|---|---|---|---|---|
| $\beta_0^{(1)}$ | 1.354 | 0.674 | 2.01 | no ($p = 0.085$) |
| $\beta_1^{(1)}$ | 0.688 | 0.199 | 3.45 | yes |
| $\beta_2^{(1)}$ | 1.146 | 0.281 | 4.08 | yes |

**Model 2.** With $\bX = [\mathbf{1}, \bx_1, \bz_1, \bz_2]$, where
$\bz_1 = (0,0,1,1,1,1,0,0,0,0)\T$ and $\bz_2 = (0,0,0,0,0,0,1,1,1,1)\T$,

$$
\bX\T\bX = \begin{bmatrix}
10 & 27 & 4 & 4 \\ 27 & 89 & 10 & 11 \\ 4 & 10 & 4 & 0 \\ 4 & 11 & 0 & 4
\end{bmatrix},
\qquad
\bX\T\by = \begin{bmatrix} 47 \\ 139 \\ 18 \\ 23 \end{bmatrix},
\qquad
\hat\bbeta^{(2)} = \begin{bmatrix} 0.571 \\ 0.810 \\ 1.905 \\ 2.952 \end{bmatrix}.
$$

$\mathit{SS}_E = 3.4286$, so $R^2 = 0.858$ and $\bar{R}^2 = 0.787$;
$\hat\sigma^2 = 3.4286/6 = 0.571$ and $t_{0.025,6} = 2.447$.

| Coefficient | Estimate | Std. error | $T_j$ | Significant at 5 %? |
|---|---|---|---|---|
| $\beta_0^{(2)}$ | 0.571 | 0.782 | 0.73 | no ($p = 0.49$) |
| $\beta_1^{(2)}$ | 0.810 | 0.190 | 4.25 | yes |
| $\beta_2^{(2)}$ | 1.905 | 0.662 | 2.88 | yes |
| $\beta_3^{(2)}$ | 2.952 | 0.656 | 4.50 | yes |

**(b) Choice of model.** Model 2 has the higher adjusted $R^2$ (0.787 vs.
0.763) and the smaller residual standard error (0.756 vs. 0.796), and all
its slope coefficients are significant. It is also more plausible: the
first car adds about 1.9 work trips and the second only about 1.05 more
($2.95 - 1.90$), a diminishing effect that Model 1 cannot represent because
it forces every car to add the same 1.15 trips. In both models the
intercept is not significant, and a positive intercept implies that a
household without workers makes work trips, which is implausible.
Re-estimating Model 2 **without an intercept** gives

$$
\hat{y} = 0.911\,x_1 + 2.222\,z_1 + 3.244\,z_2,
$$

with $t$ values 7.25, 4.61, and 6.45 (all significant at
$t_{0.025,7} = 2.365$) and a residual standard error of 0.730, the smallest
of all the models. This is the recommended model.

**(c) Zonal trips.** Average over the households of the zone:
$\bar{x}_1 = 2$, $\bar{x}_2 = 0.5 \times 0 + 0.35 \times 1 + 0.15 \times 2 = 0.65$,
$\bar{z}_1 = 0.35$, $\bar{z}_2 = 0.15$. Because the models are linear, the
zonal total is 1 000 times the prediction at the average values:

$$
\begin{aligned}
O_i^{(1)} &= 1000\,(1.354 + 0.688 \times 2 + 1.146 \times 0.65) = 3\,474, \\
O_i^{(2)} &= 1000\,(0.571 + 0.810 \times 2 + 1.905 \times 0.35 + 2.952 \times 0.15) \\
&= 3\,300, \\
O_i^{(2,\ \text{no } \beta_0)} &= 1000\,(0.911 \times 2 + 2.222 \times 0.35 + 3.244 \times 0.15) = 3\,087 .
\end{aligned}
$$

The forecasts differ by about 12 %. Model 1 gives the largest value because
its linear car effect over-predicts for car-less households — half the
zone. The intercepts add 1 354 or 571 trips that are not explained by
workers or cars. The model without intercept, which attributes all trips to
workers and cars, gives the lowest and most defensible forecast. Note also
that trips per household (about 3.1–3.5) exceed the two workers per
household; this is possible because the survey counts all household trips
to work in the peak, but it should be checked against the data definition.
:::
