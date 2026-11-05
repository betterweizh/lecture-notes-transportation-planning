# Probability Distributions

This chapter works through the examples and problems of
{doc}`01-probability-distributions`.

## Uniform and normal distributions

:::{prf:example} Uniformly distributed travel time
:label: ex-17-uniform

The travel time $X$ from a campus to a metro station by public transport is
uniformly distributed between 15 and 25 minutes. Give its PDF, CDF, mean,
and variance, and the probability that the trip takes more than 22 minutes.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

With $a = 15$ and $b = 25$,

$$
\begin{aligned}
f(x) &= \frac{1}{10}\ \ (15 \le x \le 25), \\
F(x) &= \frac{x - 15}{10}\ \ (15 \le x \le 25),
\end{aligned}
$$

with $f = 0$ outside the interval and $F = 0$ below 15 and $F = 1$ above
25. The moments are

$$
\begin{aligned}
\E[X] &= \frac{15 + 25}{2} = 20~\text{min}, \\
\Var[X] &= \frac{(25 - 15)^2}{12} = 8.33~\text{min}^2,
\end{aligned}
$$

so the standard deviation is 2.89 min. Finally,
$\Prob(X > 22) = 1 - F(22) = 1 - 0.7 = 0.3$.
:::

:::{prf:example} Normally distributed walking time
:label: ex-17-normal

The walking time $X$ from a campus to a metro station is normally
distributed with mean 20 minutes and standard deviation 10 minutes. What is
the probability that the walk takes at most 30 minutes?
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

Standardize with {eq}`eq-01-standardize`:

$$
\Prob(X \le 30) = \Phi\!\left(\frac{30 - 20}{10}\right) = \Phi(1.00) = 0.8413 .
$$

A normal model also assigns probability to negative walking times:
$\Prob(X \le 0) = \Phi(-2) = 0.0228$. If only positive times are admitted,

$$
\Prob(0 < X \le 30) = \Phi(1) - \Phi(-2) = 0.8413 - 0.0228 = 0.8186 .
$$

A large coefficient of variation (here 0.5) is a warning that a normal
model for a positive quantity is crude; a log-normal or gamma distribution
may be preferable.
:::

## Gumbel and logistic distributions

:::{prf:example} A Gumbel probability
:label: ex-17-gumbel

The maximum $X$ of many travel times is Gumbel distributed with $\eta = 0.5$
and $\mu = 0.5$. Compute $\Prob(X \le 5)$, the mean, and the standard
deviation of $X$.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

By {eq}`eq-01-gumbel`,

$$
\begin{aligned}
\Prob(X \le 5) &= \exp\!\left\{-e^{-0.5\,(5 - 0.5)}\right\} \\
&= \exp\!\left\{-e^{-2.25}\right\} = \exp(-0.1054) = 0.900 .
\end{aligned}
$$

By {prf:ref}`prop-01-gumbel`, the mean is
$\eta + \gamma/\mu = 0.5 + 0.5772/0.5 = 1.654$, and the standard deviation
is $\pi/(\sqrt{6}\,\mu) = 2.565$.
:::

:::{prf:example} Choosing between two Gumbel alternatives
:label: ex-17-gumbel-difference

The utilities of two routes are $U_1 = V_1 + \varepsilon_1$ and
$U_2 = V_2 + \varepsilon_2$ with $V_1 = -10$, $V_2 = -12$ (minus the travel
times in minutes), and $\varepsilon_1, \varepsilon_2$ independent
$\mathrm{Gumbel}(0, \mu)$ with $\mu = 0.5$. (a) Find the probability that
route 1 is chosen. (b) Find the distribution of the maximum utility.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**(a)** Route 1 is chosen if $U_1 > U_2$, i.e. if
$\varepsilon_2 - \varepsilon_1 < V_1 - V_2$. By {prf:ref}`prop-01-logistic`,
$\varepsilon_2 - \varepsilon_1 \sim \mathrm{Logistic}(0, \mu)$, so

$$
\begin{aligned}
\Prob(U_1 > U_2) &= \frac{1}{1 + e^{-\mu(V_1 - V_2)}} \\
&= \frac{e^{\mu V_1}}{e^{\mu V_1} + e^{\mu V_2}} \\
&= \frac{1}{1 + e^{-0.5 \times 2}} = 0.731 .
\end{aligned}
$$

This is the binary logit formula.

**(b)** $U_j = V_j + \varepsilon_j \sim \mathrm{Gumbel}(V_j, \mu)$ by
property 4 of {prf:ref}`prop-01-gumbel`. By property 6,

$$
\max\{U_1, U_2\} \sim \mathrm{Gumbel}\!\left(\frac{1}{\mu}\ln\left(e^{\mu V_1} + e^{\mu V_2}\right),\ \mu\right),
$$

with location $2\ln(e^{-5} + e^{-6}) = -9.373$. The expected maximum
utility is $-9.373 + \gamma/\mu = -8.219$, higher than both $V_1$ and $V_2$
because the traveler can pick whichever route turns out better.
:::

## Bivariate and multivariate normal distributions

:::{prf:example} Time and cost of a trip
:label: ex-17-bivariate-normal

Travel time $X$ and travel cost $Y$ of a trip are jointly normal with
$X \sim \mathcal{N}(20, 10)$, $Y \sim \mathcal{N}(10, 5)$ (second argument:
variance), and correlation $\rho = 0.5$. Compute $\Prob(X - Y \le 15)$.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

By {eq}`eq-01-normal-difference`, $X - Y$ is normal with mean
$20 - 10 = 10$ and variance

$$
\begin{aligned}
\sigma_X^2 + \sigma_Y^2 - 2\rho\sigma_X\sigma_Y &= 10 + 5 - 2 \times 0.5 \times \sqrt{10}\sqrt{5} = 15 - 7.071 = 7.929,
\end{aligned}
$$

so its standard deviation is 2.816. Hence

$$
\begin{aligned}
\Prob(X - Y \le 15) &= \Phi\!\left(\frac{15 - 10}{2.816}\right) \\
&= \Phi(1.776) = 0.962 .
\end{aligned}
$$

The same value is obtained by integrating the bivariate density over the
half-plane $x - y \le 15$ numerically.
:::

:::{prf:example} Probability of being the largest
:label: ex-17-mvn-maximum

The perceived utilities of three alternatives are multivariate normal with

$$
\bmu = \begin{bmatrix} 2 \\ 2 \\ 3 \end{bmatrix},
\qquad
\bSigma = \begin{bmatrix} 2 & 0 & 1 \\ 0 & 2 & 1 \\ 1 & 1 & 3 \end{bmatrix}.
$$

Compute the probability $P_i = \Prob(X_i > \max_{j \ne i} X_j)$ that each
alternative has the largest utility.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

The integral {eq}`eq-01-probit-probability` has no closed form for three
alternatives, so it is evaluated by **Monte Carlo simulation**: draw a large
number $R$ of vectors $\bx^{(r)} \sim \mathcal{N}(\bmu, \bSigma)$ and count
how often each component is the largest,

$$
\hat{P}_i = \frac{1}{R}\sum_{r=1}^{R}\mathbb{1}\!\left[x_i^{(r)} > \max_{j \ne i} x_j^{(r)}\right].
$$

With $R = 2\,000\,000$ draws ({doc}`32-python-foundations`),

$$
\begin{aligned}
\hat{P}_1 &= 0.222, \\
\hat{P}_2 &= 0.222, \\
\hat{P}_3 &= 0.556 .
\end{aligned}
$$

Alternatives 1 and 2 are symmetric, so $P_1 = P_2$. The standard error of
each estimate, $\sqrt{\hat{P}(1 - \hat{P})/R}$, is at most 0.0004. As a
check, alternative 3 is the largest exactly when both differences
$X_3 - X_1$ and $X_3 - X_2$ are positive; these differences are bivariate
normal with means 1 and 1, variances 3 and 3, and covariance 1, and a
numerical evaluation of their bivariate normal CDF gives
$P_3 = 0.5563$ and $P_1 = P_2 = (1 - P_3)/2 = 0.2218$.

For a pair of alternatives the probability is available in closed form. For
example, $X_3 - X_1 \sim \mathcal{N}(1,\ 3 + 2 - 2 \times 1) = \mathcal{N}(1, 3)$,
so $\Prob(X_3 > X_1) = \Phi(1/\sqrt{3}) = 0.718$.
:::
