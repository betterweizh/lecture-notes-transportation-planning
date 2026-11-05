# Probability Distributions for Demand Modeling

## Overview

Travel times, costs, and the unobserved parts of travelers' preferences
are random. Discrete choice models ({doc}`11-discrete-choice-models`) and
stochastic traffic assignment ({doc}`15-stochastic-user-equilibrium`) are
built by assuming particular distributions for these random terms, and the
convenient closed forms of the logit model come from the special properties
of the **Gumbel** and **logistic** distributions. This chapter reviews the
distributions used in the rest of the book and proves the properties that
the later chapters rely on.

:::{admonition} Learning objectives
:class: objectives
After completing this chapter, readers should be able to:

- compute probabilities, means, and variances for the uniform and normal
  distributions;
- state the Gumbel and logistic distributions, their moments, and how they
  arise from extreme values;
- prove that the maximum of independent Gumbel variables with a common scale
  is Gumbel, and that the difference of two such variables is logistic;
- compute probabilities for linear combinations of jointly normal variables;
  and
- explain why the probability that one of several correlated normal
  variables is the largest has no closed form.
:::

## Notation

| Symbol | Meaning |
|---|---|
| $f(x)$, $F(x)$ | probability density function (PDF) and cumulative distribution function (CDF) |
| $\E[X]$, $\Var[X]$ | mean and variance |
| $\Cov[X, Y]$, $\rho_{XY}$ | covariance and correlation coefficient |
| $\Phi(z)$ | CDF of the standard normal distribution |
| $\eta$, $\mu$ | location and scale parameters of the Gumbel and logistic distributions |
| $\gamma \approx 0.5772$ | Euler–Mascheroni constant |

Throughout the book, $\mathcal{N}(\mu, \sigma^2)$ denotes a normal
distribution with mean $\mu$ and **variance** $\sigma^2$.

## Basic definitions

For a continuous random variable $X$ with density $f$,

$$
\begin{aligned}
F(x) &= \Prob(X \le x) \\
&= \int_{-\infty}^{x} f(t)\,\diff t, \\
\E[X] &= \int_{-\infty}^{\infty} x\,f(x)\,\diff x, \\
\Var[X] &= \E\!\left[(X - \E[X])^2\right] \\
&= \E[X^2] - (\E[X])^2 .
\end{aligned}
$$

For two random variables,
$\Cov[X, Y] = \E[(X - \E[X])(Y - \E[Y])]$ and
$\rho_{XY} = \Cov[X, Y]/(\sigma_X\sigma_Y) \in [-1, 1]$. For constants $a$,
$b$,

$$
\Var[aX + bY] = a^2\Var[X] + b^2\Var[Y] + 2ab\,\Cov[X, Y].
$$ (eq-01-var-linear)

## Continuous uniform distribution

$X \sim \mathcal{U}(a, b)$ has a constant density on $[a, b]$:

$$
\begin{aligned}
f(x) &= \begin{cases} \dfrac{1}{b - a}, & a \le x \le b, \\[4pt] 0, & \text{otherwise}, \end{cases} \\[6pt]
F(x) &= \begin{cases} 0, & x < a, \\[2pt] \dfrac{x - a}{b - a}, & a \le x \le b, \\[4pt] 1, & x > b, \end{cases}
\end{aligned}
$$

with

$$
\begin{aligned}
\E[X] &= \frac{a + b}{2}, \\
\Var[X] &= \frac{(b - a)^2}{12}.
\end{aligned}
$$

It models a quantity known only to lie in an interval, for example the
waiting time for a bus that arrives at a fixed headway when the passenger
arrives at random.

## Normal distribution

$X \sim \mathcal{N}(\mu, \sigma^2)$ has density

$$
f(x) = \frac{1}{\sqrt{2\pi}\,\sigma}
\exp\!\left[-\frac{(x - \mu)^2}{2\sigma^2}\right],
\qquad -\infty < x < \infty,
$$

mean $\mu$ and variance $\sigma^2$. Its CDF has no closed form; it is
computed through the **standardized** variable $Z = (X - \mu)/\sigma$, which
follows the standard normal distribution $\mathcal{N}(0, 1)$:

$$
\Prob(X \le x) = \Phi\!\left(\frac{x - \mu}{\sigma}\right).
$$ (eq-01-standardize)

The normal distribution is justified by the **central limit theorem**: the
sum of many independent small effects is approximately normal. It is used
for travel times that result from many small delays and for estimators such
as sample means and regression coefficients.

### Related distributions used in tests

If $Z \sim \mathcal{N}(0, 1)$ and $W \sim \chi^2(\nu)$ are independent, then
$Z/\sqrt{W/\nu} \sim t(\nu)$; if $W_1 \sim \chi^2(\nu_1)$ and
$W_2 \sim \chi^2(\nu_2)$ are independent, then
$(W_1/\nu_1)/(W_2/\nu_2) \sim F(\nu_1, \nu_2)$. These give the $t$- and
$F$-tests of {doc}`02-regression-and-hypothesis-tests`. As $\nu \to \infty$,
$t(\nu)$ tends to $\mathcal{N}(0, 1)$, which is why $z$ is used instead of
$t$ for large samples.

## Gumbel distribution

### Origin: the largest of many random variables

Let $T_1, \ldots, T_n$ be independent and identically distributed with CDF
$F_T$. The CDF of their maximum $M_n = \max\{T_1, \ldots, T_n\}$ is

$$
\begin{aligned}
\Prob(M_n \le x) &= \Prob(T_1 \le x, \ldots, T_n \le x) \\
&= [F_T(x)]^{n}.
\end{aligned}
$$

If $F_T$ has an exponential-type upper tail (as the normal, exponential,
and gamma distributions do), then after suitable centering and scaling the
distribution of $M_n$ converges, as $n \to \infty$, to the **Gumbel**
(type I extreme value) distribution. This is why the Gumbel distribution is
a natural model for the maximum of many random influences — such as the
unobserved part of the utility of an alternative.

### Definition and properties

$X \sim \mathrm{Gumbel}(\eta, \mu)$, with location $\eta$ and scale
parameter $\mu > 0$, has

$$
\begin{aligned}
F(x) &= \exp\!\left\{-e^{-\mu(x - \eta)}\right\}, \\
f(x) &= \mu\,e^{-\mu(x - \eta)}\exp\!\left\{-e^{-\mu(x - \eta)}\right\}, \quad -\infty < x < \infty.
\end{aligned}
$$ (eq-01-gumbel)

Note that $\mu$ is an *inverse* scale: a larger $\mu$ means a more
concentrated distribution ({numref}`fig-01-gumbel-logistic`).

:::{prf:property} Properties of the Gumbel distribution
:label: prop-01-gumbel

Let $X \sim \mathrm{Gumbel}(\eta, \mu)$.

1. The mode is $\eta$.
2. The mean is $\eta + \gamma/\mu$, where $\gamma \approx 0.5772$.
3. The variance is $\pi^2/(6\mu^2)$.
4. For constants $V$ and $\alpha > 0$,
   $\alpha X + V \sim \mathrm{Gumbel}(\alpha\eta + V,\ \mu/\alpha)$.
5. If $X_1 \sim \mathrm{Gumbel}(\eta_1, \mu)$ and
   $X_2 \sim \mathrm{Gumbel}(\eta_2, \mu)$ are independent, then
   $\max\{X_1, X_2\} \sim \mathrm{Gumbel}\!\left(\frac{1}{\mu}\ln\left(e^{\mu\eta_1} + e^{\mu\eta_2}\right),\ \mu\right)$.
6. More generally, if $X_1, \ldots, X_J$ are independent with
   $X_j \sim \mathrm{Gumbel}(\eta_j, \mu)$, then

   $$
   \max_{j = 1,\ldots,J} X_j \sim
   \mathrm{Gumbel}\!\left(\frac{1}{\mu}\ln\sum_{j=1}^{J} e^{\mu\eta_j},\ \mu\right).
   $$ (eq-01-gumbel-max)
:::

:::{dropdown} Proof
:class-container: proof
:animate: fade-in

Property 4: for $\alpha > 0$,
$\Prob(\alpha X + V \le x) = F\big((x - V)/\alpha\big)
= \exp\{-e^{-(\mu/\alpha)(x - V - \alpha\eta)}\}$, which is the Gumbel CDF
with location $\alpha\eta + V$ and scale $\mu/\alpha$.

Property 6 (property 5 is the case $J = 2$): by independence,

$$
\begin{aligned}
\Prob\!\left(\max_j X_j \le x\right)
&= \prod_{j=1}^{J}\exp\!\left\{-e^{-\mu(x - \eta_j)}\right\} \\
&= \exp\!\left\{-e^{-\mu x}\sum_{j=1}^{J} e^{\mu\eta_j}\right\} \\
&= \exp\!\left\{-e^{-\mu(x - \eta^{*})}\right\},
\end{aligned}
$$

where

$$
\eta^{*} = \frac{1}{\mu}\ln\sum_{j=1}^{J} e^{\mu\eta_j},
$$

since $e^{\mu\eta^{*}} = \sum_j e^{\mu\eta_j}$. Properties 1–3 follow from
{eq}`eq-01-gumbel` by differentiation and integration.
:::

Property 6 is the reason the logit model has a closed form: if the
utilities of $J$ alternatives are independent Gumbel variables with a
common scale, the utility of the best alternative is again Gumbel. Its
location, the **log-sum** $\eta^{*}$, determines the expected maximum utility
of the choice set, which by property 2 equals $\eta^{*} + \gamma/\mu$.

## Logistic distribution

$X \sim \mathrm{Logistic}(\eta, \mu)$, with location $\eta$ and scale
parameter $\mu > 0$, has

$$
\begin{aligned}
F(x) &= \frac{1}{1 + e^{-\mu(x - \eta)}}, \\
f(x) &= \frac{\mu\,e^{-\mu(x - \eta)}}{\left[1 + e^{-\mu(x - \eta)}\right]^{2}}, \quad -\infty < x < \infty.
\end{aligned}
$$ (eq-01-logistic)

```{figure} figures/01-gumbel-logistic.svg
:name: fig-01-gumbel-logistic
:width: 640px
:class: dark-light

Gumbel and logistic densities. The Gumbel density is skewed to the right
with its mode at $\eta$; the logistic density is symmetric about $\eta$.
Halving $\mu$ doubles the spread.
```

:::{prf:property} Properties of the logistic distribution
:label: prop-01-logistic

Let $X \sim \mathrm{Logistic}(\eta, \mu)$.

1. The mode, median, and mean are all $\eta$.
2. The variance is $\pi^2/(3\mu^2)$.
3. For constants $V$ and $\alpha > 0$,
   $\alpha X + V \sim \mathrm{Logistic}(\alpha\eta + V,\ \mu/\alpha)$.
4. If $X_1 \sim \mathrm{Gumbel}(\eta_1, \mu)$ and
   $X_2 \sim \mathrm{Gumbel}(\eta_2, \mu)$ are independent, then
   $X_1 - X_2 \sim \mathrm{Logistic}(\eta_1 - \eta_2,\ \mu)$.
:::

:::{dropdown} Proof
:class-container: proof
:animate: fade-in

Property 3 is proved as for the Gumbel distribution. For property 4, let
$Y = X_1 - X_2$ and condition on $X_2$:

$$
\begin{aligned}
\Prob(Y \le y)
&= \int_{-\infty}^{\infty} F_1(x + y)\, f_2(x)\,\diff x \\
&= \int_{-\infty}^{\infty}
   \exp\!\left\{-e^{-\mu(x + y - \eta_1)}\right\}
   \mu e^{-\mu(x - \eta_2)}\exp\!\left\{-e^{-\mu(x - \eta_2)}\right\}\diff x .
\end{aligned}
$$

Substitute $u = e^{-\mu(x - \eta_2)}$, so that
$\diff u = -\mu u\,\diff x$ and
$e^{-\mu(x + y - \eta_1)} = u\,e^{-\mu(y - \eta_1 + \eta_2)} = u\,a$ with
$a = e^{-\mu(y - (\eta_1 - \eta_2))}$:

$$
\begin{aligned}
\Prob(Y \le y) &= \int_{0}^{\infty} e^{-u(1 + a)}\,\diff u \\
&= \frac{1}{1 + a} \\
&= \frac{1}{1 + e^{-\mu[y - (\eta_1 - \eta_2)]}},
\end{aligned}
$$

which is the CDF {eq}`eq-01-logistic` with location $\eta_1 - \eta_2$ and
scale $\mu$.
:::

Property 4 gives the **binary logit model**: if the utilities of two
alternatives have independent Gumbel errors with a common scale, the
difference of the errors is logistic and the probability of choosing the
first alternative has the closed form of {eq}`eq-01-logistic`. The sum of two
Gumbel variables, in contrast, is *not* logistic.

The logistic distribution also arises from extreme values: for a symmetric
parent distribution with exponential tails, the maximum and the minimum of a
large sample are asymptotically independent, and their average (the
*mid-range*), suitably centered and scaled, converges to a logistic
distribution. For practical purposes the logistic distribution is a close
approximation to the normal one: with the same variance, the two CDFs never
differ by more than about 0.02.

## Bivariate and multivariate normal distributions

### Bivariate normal

Travel time $X$ and travel cost $Y$ of the same trip are usually correlated.
If $(X, Y)$ is bivariate normal with means $\mu_X, \mu_Y$, standard
deviations $\sigma_X, \sigma_Y$, and correlation $\rho$, the joint density is

$$
f(x, y) = \frac{1}{2\pi\sigma_X\sigma_Y\sqrt{1 - \rho^2}}
\exp\!\left\{-\frac{Q(x, y)}{2(1 - \rho^2)}\right\},
$$

where

$$
Q(x, y) = \frac{(x - \mu_X)^2}{\sigma_X^2}
- \frac{2\rho(x - \mu_X)(y - \mu_Y)}{\sigma_X\sigma_Y}
+ \frac{(y - \mu_Y)^2}{\sigma_Y^2}.
$$

The marginal distributions are $\mathcal{N}(\mu_X, \sigma_X^2)$ and
$\mathcal{N}(\mu_Y, \sigma_Y^2)$, and $\Cov[X, Y] = \rho\sigma_X\sigma_Y$.

**Linear combinations are normal.** For constants $a$ and $b$,
$aX + bY$ is normal with mean $a\mu_X + b\mu_Y$ and, by
{eq}`eq-01-var-linear`, variance
$a^2\sigma_X^2 + b^2\sigma_Y^2 + 2ab\rho\sigma_X\sigma_Y$. In particular

$$
X - Y \sim \mathcal{N}\!\left(\mu_X - \mu_Y,\
\sigma_X^2 + \sigma_Y^2 - 2\rho\sigma_X\sigma_Y\right),
$$ (eq-01-normal-difference)

so probabilities such as $\Prob(X - Y \le c)$ need only the standard normal
table ({prf:ref}`ex-17-bivariate-normal`). Equation {eq}`eq-01-normal-difference`
is the basis of the **binary probit** model.

### Multivariate normal

A random vector $\bX \in \R^m$ is multivariate normal,
$\bX \sim \mathcal{N}(\bmu, \bSigma)$, with mean vector $\bmu$ and
covariance matrix $\bSigma$ (symmetric, positive definite), if its density
is

$$
\phi(\bx) = \frac{1}{(2\pi)^{m/2}\lvert\bSigma\rvert^{1/2}}
\exp\!\left[-\frac{1}{2}(\bx - \bmu)\T\bSigma^{-1}(\bx - \bmu)\right],
\qquad \bx \in \R^m.
$$

Every linear transformation $\bA\bX$ is again multivariate normal
with mean $\bA\bmu$ and covariance $\bA\bSigma\bA\T$.

In route or mode choice with normally distributed utilities, the
probability that alternative $i$ has the largest value,

$$
\begin{aligned}
P_i(\bmu, \bSigma) &= \Prob\!\left(X_i > \max_{j \ne i} X_j\right) \\
&= \int_{\{\bx:\ x_i > x_j\ \forall j \ne i\}} \phi(\bx)\,\diff\bx,
\end{aligned}
$$ (eq-01-probit-probability)

is an $m$-dimensional integral over a region bounded by the hyperplanes
$x_i = x_j$. It has no closed form when $m > 2$ and is evaluated
numerically, usually by Monte Carlo simulation
({prf:ref}`ex-17-mvn-maximum`). This is the **multinomial probit** model, more
flexible than logit because $\bSigma$ can represent correlation between
alternatives (for example routes that share links), but more expensive to
compute.

## Summary and Common Mistakes

### Summary

- Uniform: mean $(a + b)/2$, variance $(b - a)^2/12$. Normal probabilities
  are obtained by standardizing, equation {eq}`eq-01-standardize`.
- Gumbel$(\eta, \mu)$, equation {eq}`eq-01-gumbel`: mean
  $\eta + \gamma/\mu$, variance $\pi^2/(6\mu^2)$; the maximum of
  independent Gumbels with a common scale is Gumbel with location
  $\mu^{-1}\ln\sum_j e^{\mu\eta_j}$ ({prf:ref}`prop-01-gumbel`, equation
  {eq}`eq-01-gumbel-max`).
- Logistic$(\eta, \mu)$, equation {eq}`eq-01-logistic`: mean $\eta$,
  variance $\pi^2/(3\mu^2)$; the difference of two independent Gumbels with a
  common scale is logistic ({prf:ref}`prop-01-logistic`), which gives the
  binary logit model.
- Linear combinations of jointly normal variables are normal, equation
  {eq}`eq-01-normal-difference` (binary probit); the probability that one of
  several correlated normals is the maximum, equation
  {eq}`eq-01-probit-probability`, requires numerical integration
  (multinomial probit).

### Common mistakes

- **Mixing up variance and standard deviation in
  $\mathcal{N}(\mu, \sigma^2)$.** The second argument is the variance;
  standardize with its square root $\sigma$.
- **Treating $\mu$ in the Gumbel and logistic distributions as a standard
  deviation.** It is an inverse scale: the variances are $\pi^2/(6\mu^2)$ and
  $\pi^2/(3\mu^2)$, so a larger $\mu$ means less spread.
- **Restricting the Gumbel distribution to $x \ge 0$.** It is defined on the
  whole real line.
- **Taking the Gumbel location $\eta$ as its mean.** The location is the
  mode; the mean is $\eta + \gamma/\mu$.
- **Applying the max-stability property {eq}`eq-01-gumbel-max` to Gumbel
  variables with *different* scales.** The maximum is Gumbel only when all
  variables share a common $\mu$.

## References

- Ben-Akiva, M., & Lerman, S. R. (1985). *Discrete Choice Analysis:
  Theory and Application to Travel Demand*, Chapter 5. MIT Press.
- Sheffi, Y. (1985). *Urban Transportation Networks*, Appendix (Normal
  distribution and probit analysis). Prentice-Hall.
- Train, K. E. (2009). *Discrete Choice Methods with Simulation* (2nd ed.),
  Chapter 3. Cambridge University Press.
  <https://eml.berkeley.edu/books/choice2.html>
- Gumbel, E. J. (1958). *Statistics of Extremes*. Columbia University
  Press.
- Montgomery, D. C., & Runger, G. C. (2018). *Applied Statistics and
  Probability for Engineers* (7th ed.), Chapters 4–5. Wiley.
