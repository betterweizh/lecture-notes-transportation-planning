# Linear Regression and Hypothesis Tests

## Overview

Trip generation models relate the number of trips produced or attracted by
a zone or a household to land-use and socioeconomic variables, and the most
common tool for this is linear regression. This chapter reviews the
least-squares estimation of simple and multiple linear regression models,
with and without an intercept, the measures of goodness of fit, and the
$t$-tests used to decide whether a variable belongs in the model. It ends
with the large-sample test for the equality of two population means, used
for example to compare traffic flows or trip rates between two periods or
two groups.

:::{admonition} Learning objectives
:class: objectives
After completing this chapter, readers should be able to:

- derive the least-squares estimators of a simple linear regression with and
  without an intercept;
- estimate a multiple linear regression in matrix form;
- compute and interpret $R^2$, adjusted $R^2$, and the residual variance;
- test hypotheses on individual coefficients with $t$-tests and on the whole
  model with the $F$-test;
- use dummy variables for categorical predictors; and
- test the equality of two population means from large samples.
:::

## Notation

| Symbol | Meaning |
|---|---|
| $n$ | number of observations |
| $k$ | number of predictors (excluding the intercept) |
| $y_i$, $\by$ | response of observation $i$; response vector in $\R^n$ |
| $x_{ij}$, $\bX$ | value of predictor $j$ for observation $i$; design matrix |
| $\beta_j$, $\hat\beta_j$ | regression coefficient and its least-squares estimate |
| $\hat{y}_i$, $e_i = y_i - \hat{y}_i$ | fitted value and residual |
| $\bar{x}$, $\bar{y}$ | sample means |
| $S_{xx} = \sum_i (x_i - \bar{x})^2$ | corrected sum of squares of $x$ |
| $S_{xy} = \sum_i (x_i - \bar{x})(y_i - \bar{y})$ | corrected sum of cross-products |
| $\mathit{SS}_T, \mathit{SS}_R, \mathit{SS}_E$ | total, regression, and error (residual) sums of squares |
| $\hat\sigma^2 = \mathit{MS}_E$ | estimate of the error variance |

## The linear regression model

The response $Y$ (for example the trips produced by a zone) is related to
predictors $X_1, \ldots, X_k$ (households, cars, workers, floor space) by

$$
\begin{aligned}
Y &= \beta_0 + \beta_1 X_1 + \beta_2 X_2 + \cdots + \beta_k X_k + \varepsilon, \\
\varepsilon &\sim \mathcal{N}(0, \sigma^2),
\end{aligned}
$$ (eq-02-mlr)

where $\beta_0$ is the intercept, $\beta_1, \ldots, \beta_k$ are the
**partial regression coefficients**, and the errors of different
observations are independent with a common unknown variance $\sigma^2$.
The data are $n$ observations $(y_i, x_{i1}, \ldots, x_{ik})$,
$i = 1, \ldots, n$.

## Simple linear regression

### Least-squares estimation

With one predictor, $Y = \beta_0 + \beta_1 X + \varepsilon$. The
**least-squares** estimates minimize the sum of squared errors

$$
L(\beta_0, \beta_1) = \sum_{i=1}^{n}\left(y_i - \beta_0 - \beta_1 x_i\right)^2 .
$$

The partial derivatives are

$$
\begin{aligned}
\frac{\partial L}{\partial \beta_0}
&= -2\sum_{i=1}^{n}\left(y_i - \beta_0 - \beta_1 x_i\right), \\
\frac{\partial L}{\partial \beta_1}
&= -2\sum_{i=1}^{n}\left(y_i - \beta_0 - \beta_1 x_i\right)x_i .
\end{aligned}
$$

Setting them to zero gives the two **normal equations**, whose solution is

$$
\begin{aligned}
\hat\beta_1 &= \frac{S_{xy}}{S_{xx}} \\
&= \frac{\sum_i x_i y_i - \left(\sum_i x_i\right)\left(\sum_i y_i\right)/n}{\sum_i x_i^2 - \left(\sum_i x_i\right)^2/n}, \\
\hat\beta_0 &= \bar{y} - \hat\beta_1\bar{x}.
\end{aligned}
$$ (eq-02-slr-estimates)

Because $\sum_i (x_i - \bar{x}) = 0$, the numerator can also be written
$S_{xy} = \sum_i y_i (x_i - \bar{x})$, which is convenient for hand
calculation.

### Analysis of variance and goodness of fit

The total variation of the response splits into a part explained by the
regression and a residual part:

$$
\begin{aligned}
\underbrace{\sum_{i}(y_i - \bar{y})^2}_{\mathit{SS}_T,\ n-1\ \text{d.f.}} &= \underbrace{\sum_{i}(\hat{y}_i - \bar{y})^2}_{\mathit{SS}_R,\ 1\ \text{d.f.}}
+ \underbrace{\sum_{i}(y_i - \hat{y}_i)^2}_{\mathit{SS}_E,\ n-2\ \text{d.f.}} .
\end{aligned}
$$ (eq-02-anova-slr)

The **coefficient of determination**

$$
\begin{aligned}
R^2 &= \frac{\mathit{SS}_R}{\mathit{SS}_T} \\
&= 1 - \frac{\mathit{SS}_E}{\mathit{SS}_T}
\end{aligned}
$$ (eq-02-r2)

is the share of the variation of $y$ explained by the model; it lies in
$[0, 1]$. The error variance is estimated by the **residual mean square**

$$
\begin{aligned}
\hat\sigma^2 &= \mathit{MS}_E \\
&= \frac{\mathit{SS}_E}{n - 2}.
\end{aligned}
$$

### Tests on the coefficients

Under the model assumptions, the estimators are normally distributed:

$$
\begin{aligned}
\hat\beta_1 &\sim \mathcal{N}\!\left(\beta_1,\ \frac{\sigma^2}{S_{xx}}\right), \\
\hat\beta_0 &\sim \mathcal{N}\!\left(\beta_0,\ \sigma^2\left[\frac{1}{n} + \frac{\bar{x}^2}{S_{xx}}\right]\right).
\end{aligned}
$$ (eq-02-slr-distributions)

Replacing $\sigma^2$ by $\hat\sigma^2$ gives the standard errors
$\se(\hat\beta_1) = \sqrt{\hat\sigma^2/S_{xx}}$ and
$\se(\hat\beta_0) = \sqrt{\hat\sigma^2(1/n + \bar{x}^2/S_{xx})}$. To test
$H_0: \beta_j = \beta_{j,0}$ the statistic

$$
T_j = \frac{\hat\beta_j - \beta_{j,0}}{\se(\hat\beta_j)}
\ \sim\ t(n - 2) \quad \text{under } H_0
$$ (eq-02-t-test)

is compared with the critical values of the $t$ distribution:

| Alternative hypothesis | Reject $H_0$ at level $\alpha$ if |
|---|---|
| $H_1: \beta_j \ne \beta_{j,0}$ | $\lvert T_j\rvert > t_{\alpha/2,\,\nu}$ |
| $H_1: \beta_j > \beta_{j,0}$ | $T_j > t_{\alpha,\,\nu}$ |
| $H_1: \beta_j < \beta_{j,0}$ | $T_j < -t_{\alpha,\,\nu}$ |

Here $\nu$ is the residual degrees of freedom ($\nu = n - 2$ in simple
regression). The most common test is $H_0: \beta_j = 0$ against a two-sided
alternative: rejecting it means that the predictor has a statistically
significant linear effect.

### Regression through the origin

If theory requires zero trips when the predictor is zero, and the data do
not contradict this (the intercept is not significantly different from
zero), the model $Y = \beta_1 X + \varepsilon$ can be fitted. Minimizing
$\sum_i (y_i - \beta_1 x_i)^2$ gives

$$
\begin{aligned}
\hat\beta_1 &= \frac{\sum_i x_i y_i}{\sum_i x_i^2}, \\
\hat\beta_1 &\sim \mathcal{N}\!\left(\beta_1,\ \frac{\sigma^2}{\sum_i x_i^2}\right), \\
\hat\sigma^2 &= \frac{\mathit{SS}_E}{n - 1}.
\end{aligned}
$$ (eq-02-slr-origin)

The $t$-test {eq}`eq-02-t-test` now has $n - 1$ degrees of freedom. Without an
intercept the decomposition {eq}`eq-02-anova-slr` holds only for *uncentered*
sums of squares, $\sum_i y_i^2 = \sum_i \hat{y}_i^2 + \sum_i e_i^2$, so the
goodness of fit is measured by the **uncentered** coefficient

$$
\begin{aligned}
R_0^2 &= \frac{\sum_i \hat{y}_i^2}{\sum_i y_i^2} \\
&= 1 - \frac{\mathit{SS}_E}{\sum_i y_i^2}.
\end{aligned}
$$ (eq-02-r2-uncentered)

:::{admonition} Uncentered $R^2$ is not comparable with $R^2$
:class: warning
Because $\sum_i y_i^2 \ge \sum_i (y_i - \bar{y})^2$, the uncentered $R_0^2$
is almost always larger than the ordinary $R^2$ of a model with an
intercept, even when the model without intercept fits worse. Compare the two
models by their residual sums of squares or residual standard errors, not by
$R^2$ ({prf:ref}`ex-18-slr-origin`).
:::

## Multiple linear regression

### Matrix form and estimation

Stacking the $n$ observations of {eq}`eq-02-mlr` gives
$\by = \bX\bbeta + \bvarepsilon$ with

$$
\by = \begin{bmatrix} y_1 \\ y_2 \\ \vdots \\ y_n \end{bmatrix},
\quad
\bX = \begin{bmatrix}
1 & x_{11} & \cdots & x_{1k} \\
1 & x_{21} & \cdots & x_{2k} \\
\vdots & \vdots & \ddots & \vdots \\
1 & x_{n1} & \cdots & x_{nk}
\end{bmatrix},
\quad
\bbeta = \begin{bmatrix} \beta_0 \\ \beta_1 \\ \vdots \\ \beta_k \end{bmatrix}.
$$

The least-squares criterion and its gradient are

$$
\begin{aligned}
L(\bbeta) &= (\by - \bX\bbeta)\T(\by - \bX\bbeta), \\
\nabla L(\bbeta) &= -2\bX\T(\by - \bX\bbeta).
\end{aligned}
$$

Setting the gradient to zero gives the normal equations
$\bX\T\bX\,\bbeta = \bX\T\by$ and, when $\bX$ has full column rank,

$$
\begin{aligned}
\hat\bbeta &= (\bX\T\bX)^{-1}\bX\T\by, \\
\hat{\by} &= \bX\hat\bbeta.
\end{aligned}
$$ (eq-02-ols)

### Goodness of fit

The decomposition $\mathit{SS}_T = \mathit{SS}_R + \mathit{SS}_E$ holds with
$n - 1$, $k$, and $n - k - 1$ degrees of freedom. Adding a predictor never
decreases $R^2$, even if the predictor is irrelevant, so models with
different numbers of predictors are compared with the **adjusted** $R^2$,
which divides each sum of squares by its degrees of freedom:

$$
\begin{aligned}
\bar{R}^2
&= 1 - \frac{\mathit{SS}_E/(n - k - 1)}{\mathit{SS}_T/(n - 1)} \\
&= 1 - (1 - R^2)\,\frac{n - 1}{n - k - 1}.
\end{aligned}
$$ (eq-02-adjusted-r2)

$\bar{R}^2$ decreases when an unnecessary predictor is added and can be
negative.

### Tests on individual coefficients

Each $\hat\beta_j$ is a linear combination of $y_1, \ldots, y_n$, hence
normally distributed:

$$
\hat\beta_j \sim \mathcal{N}\!\left(\beta_j,\ \sigma^2 c_{jj}\right),
\qquad j = 0, 1, \ldots, k,
$$

where $c_{jj}$ is the $(j+1)$-th diagonal element of $(\bX\T\bX)^{-1}$
(rows and columns are numbered from 1, so $c_{00}$ is the first). With

$$
\begin{aligned}
\hat\sigma^2 &= \mathit{MS}_E \\
&= \frac{\mathit{SS}_E}{n - k - 1}
\end{aligned}
$$ (eq-02-mse)

the statistic $T_j = (\hat\beta_j - \beta_{j,0})/\sqrt{\hat\sigma^2 c_{jj}}$
follows $t(n - k - 1)$ under $H_0: \beta_j = \beta_{j,0}$, and the rejection
rules of the table above apply with $\nu = n - k - 1$.

### Overall significance

The hypothesis that none of the predictors matters,
$H_0: \beta_1 = \cdots = \beta_k = 0$, is tested with

$$
F_0 = \frac{\mathit{SS}_R/k}{\mathit{SS}_E/(n - k - 1)}
\ \sim\ F(k,\ n - k - 1) \quad \text{under } H_0,
$$ (eq-02-f-test)

rejecting $H_0$ when $F_0 > F_{\alpha;\,k,\,n-k-1}$.

### Models without an intercept

If the intercept is omitted, $\bX$ has no column of ones and contains only
the $k$ predictors. The estimator {eq}`eq-02-ols` is unchanged in form, the
residual degrees of freedom become $n - k$, so
$\hat\sigma^2 = \mathit{SS}_E/(n - k)$ and the $t$-tests have $n - k$
degrees of freedom. Goodness of fit is again measured with uncentered sums
of squares:

$$
\begin{aligned}
R_0^2 &= 1 - \frac{\mathit{SS}_E}{\sum_i y_i^2}, \\
\bar{R}_0^2 &= 1 - \frac{\mathit{SS}_E/(n - k)}{\sum_i y_i^2/n}.
\end{aligned}
$$ (eq-02-r2-uncentered-mlr)

### Categorical predictors: dummy variables

A categorical predictor with $m$ categories (for example 0, 1, and 2 or
more cars) is represented by $m - 1$ **dummy variables**, each equal to 1
for one category and 0 otherwise; the omitted category is the reference
and is absorbed by the intercept. Using all $m$ dummies together with an
intercept makes $\bX$ rank-deficient (the *dummy-variable trap*). Dummy
variables let the effect of a variable be non-linear: in
{prf:ref}`ex-18-hw1-q5`, the effect of the first car on trips
differs from that of the second.

### Choosing between models

Statistical tests are one input to model choice, together with

- **plausibility** — every coefficient should have the expected sign and a
  sensible magnitude (more cars should not reduce car trips);
- **significance** — each predictor should be significant, unless theory
  requires it;
- **fit** — compare $\bar{R}^2$ or $\hat\sigma$, not $R^2$, across models
  with different numbers of predictors; and
- **parsimony and forecastability** — every predictor must itself be
  forecast for the planning year, so fewer, well-forecastable predictors are
  preferable.

With few observations the $t$ critical values are large: with one residual
degree of freedom $t_{0.025,1} = 12.71$. Highly significant-looking
coefficients may then fail the test ({prf:ref}`ex-18-mlr-freight`).

## Testing the equality of two population means

Let two populations have means $\mu_1$, $\mu_2$ and variances
$\sigma_1^2$, $\sigma_2^2$, and let independent random samples of sizes
$n_1$ and $n_2$ give sample means $\bar{x}_1$, $\bar{x}_2$ and sample
variances

$$
s_\ell^2 = \frac{1}{n_\ell - 1}\sum_{j=1}^{n_\ell}\left(x_{\ell j} - \bar{x}_\ell\right)^2,
\qquad \ell = 1, 2.
$$

The difference of the sample means is approximately normal,

$$
\bar{x}_1 - \bar{x}_2 \ \dot\sim\
\mathcal{N}\!\left(\mu_1 - \mu_2,\ \frac{\sigma_1^2}{n_1} + \frac{\sigma_2^2}{n_2}\right).
$$

For **large samples** (say $n_1, n_2 > 40$) the variances can be replaced by
their estimates, and under $H_0: \mu_1 = \mu_2$ the statistic

$$
z_0 = \frac{\bar{x}_1 - \bar{x}_2}{\sqrt{s_1^2/n_1 + s_2^2/n_2}}
$$ (eq-02-two-sample-z)

is approximately standard normal. With $\Phi$ the standard normal CDF:

| Alternative hypothesis | Reject $H_0$ if | $p$-value |
|---|---|---|
| $H_1: \mu_1 \ne \mu_2$ | $\lvert z_0\rvert > z_{\alpha/2}$ | $2[1 - \Phi(\lvert z_0\rvert)]$ |
| $H_1: \mu_1 > \mu_2$ | $z_0 > z_\alpha$ | $1 - \Phi(z_0)$ |
| $H_1: \mu_1 < \mu_2$ | $z_0 < -z_\alpha$ | $\Phi(z_0)$ |

For small samples from normal populations, the same statistic follows
approximately a $t$ distribution with Welch–Satterthwaite degrees of
freedom (Satterthwaite, 1946; Welch, 1947).

## Summary and Common Mistakes

### Summary

- Least squares gives $\hat\bbeta = (\bX\T\bX)^{-1}\bX\T\by$, equation
  {eq}`eq-02-ols`; in simple regression $\hat\beta_1 = S_{xy}/S_{xx}$ and
  $\hat\beta_0 = \bar{y} - \hat\beta_1\bar{x}$, equation
  {eq}`eq-02-slr-estimates`, and through the origin
  $\hat\beta_1 = \sum_i x_iy_i/\sum_i x_i^2$, equation {eq}`eq-02-slr-origin`.
- $R^2 = 1 - \mathit{SS}_E/\mathit{SS}_T$, equation {eq}`eq-02-r2`;
  $\bar{R}^2$ corrects for the number of predictors, equation
  {eq}`eq-02-adjusted-r2`; without an intercept, uncentered sums of squares
  are used, equations {eq}`eq-02-r2-uncentered` and
  {eq}`eq-02-r2-uncentered-mlr`.
- $t$-tests on single coefficients, equation {eq}`eq-02-t-test`, use
  $\hat\sigma^2 c_{jj}$ and $n - p$ degrees of freedom, where $p$ is the
  number of estimated coefficients ($p = k + 1$ with an intercept, $p = k$
  without); the $F$-test {eq}`eq-02-f-test` checks all slopes jointly.
- Two large-sample means are compared with
  $z_0 = (\bar{x}_1 - \bar{x}_2)/\sqrt{s_1^2/n_1 + s_2^2/n_2}$, equation
  {eq}`eq-02-two-sample-z`.

### Common mistakes

- **Comparing the $R^2$ of a model without intercept with the $R^2$ of a
  model with intercept.** The first is uncentered and almost always larger;
  compare the residual standard errors $\hat\sigma$ instead.
- **Using $n - 2$ degrees of freedom for every test.** The residual degrees
  of freedom are $n - p$, where $p$ is the number of estimated coefficients.
- **Dropping the intercept only because its $t$-test is not significant.**
  This forces the fitted line through the origin and can bias the slope if
  the true relationship has a non-zero intercept; drop it only when theory
  also requires a zero intercept.
- **Including a dummy for every category together with an intercept.** The
  columns of $\bX$ are then linearly dependent and $\bX\T\bX$ cannot be
  inverted; use $m - 1$ dummies for $m$ categories.

## References

- Montgomery, D. C., & Runger, G. C. (2018). *Applied Statistics and
  Probability for Engineers* (7th ed.), Chapters 10–12. Wiley.
- Montgomery, D. C., Peck, E. A., & Vining, G. G. (2021). *Introduction to
  Linear Regression Analysis* (6th ed.), Chapters 2–3 and 8. Wiley.
- Satterthwaite, F. E. (1946). An approximate distribution of estimates of
  variance components. *Biometrics Bulletin*, *2*(6), 110–114.
  <https://doi.org/10.2307/3002019>
- Welch, B. L. (1947). The generalization of "Student's" problem when
  several different population variances are involved. *Biometrika,
  34*(1–2), 28–35. <https://doi.org/10.1093/biomet/34.1-2.28>
- Ortúzar, J. de D., & Willumsen, L. G. (2011). *Modelling Transport* (4th
  ed.), Section 4.2 (Regression analysis). Wiley.
