# Modal Split: Discrete Choice Models

## Overview

Modal split — the third step of the classical model — divides the trips
between each pair of zones among the available modes. This chapter and the
next present the two approaches. Here we start with the individual:
disaggregate (discrete) choice models describe the choice of an individual
traveler among a finite set of mutually exclusive alternatives — modes,
and equally routes, destinations, or departure times. They are built on **random utility
maximization**: each alternative has a utility with a systematic part that
depends on observed attributes and a random part that the analyst cannot
observe, and the traveler chooses the alternative with the highest utility.
Assumptions about the random part give the linear probability, probit, and
logit models. This chapter derives these models, studies the properties of
the multinomial logit model and of its nested extension, and shows how the
parameters are estimated by maximum likelihood and tested. The Gumbel and
logistic distributions on which the logit models rest are reviewed in
{doc}`01-probability-distributions`, and choice-based sampling in
{doc}`07-travel-surveys-and-sampling`. {doc}`12-aggregate-modal-split` then applies the same logit form to zonal
averages and combines it with trip distribution.

:::{admonition} Learning objectives
:class: objectives
After completing this chapter, readers should be able to:

- state the random utility maximization framework and explain why only
  utility differences and the scale of utility matter;
- specify systematic utilities with generic and alternative-specific
  variables, constants, and dummy variables;
- derive the binary linear probability, probit, and logit models and the
  multinomial logit model;
- explain the IIA property, compute elasticities, and use the log-sum;
- compute nested logit probabilities;
- write the log-likelihood of a sample, estimate parameters by maximum
  likelihood, and test them; and
- correct a model estimated on a choice-based sample.
:::

## Notation

| Symbol | Meaning |
|---|---|
| $n = 1, \ldots, N$ | decision makers (travelers) in the sample |
| $C_n$, $J_n$ | choice set of traveler $n$ and its size |
| $U_{in} = V_{in} + \varepsilon_{in}$ | utility of alternative $i$ for $n$: systematic plus random part |
| $\bx_{in}$ | vector of explanatory variables of alternative $i$ for traveler $n$ |
| $\bbeta$ | vector of coefficients, $V_{in} = \bbeta\T\bx_{in}$ |
| $P_n(i)$ | probability that $n$ chooses $i$ |
| $\mu$ | scale parameter of the Gumbel (logistic) random terms |
| $\phi_m$ | structural parameter of nest $m$ (nested logit) |
| $y_{in}$ | 1 if $n$ chose $i$, 0 otherwise |
| $\mathcal{L}(\bbeta)$, $LL(\bbeta)$ | likelihood and log-likelihood |
| $H_i$, $Q_i$ | sample and population shares of alternative $i$ (choice-based sample) |

## Random utility maximization

### Utility

In economics, a **utility function** $u: X \to \R$ ranks the alternatives of
a choice set $X$: the consumer weakly prefers $x$ to $y$ when
$u(x) \ge u(y)$ and chooses the alternative with the highest utility. Only
the ranking matters, so any increasing transformation of $u$ represents the
same preferences.

Applied to travel, the utility of a mode summarizes its attractiveness to a
traveler as a function of the attributes of the mode and of the traveler.
The analyst cannot observe everything that matters — tastes vary, some
attributes are not measured, perceptions differ — so from the analyst's
point of view utility is a **random variable**:

$$
U_{in} = V_{in} + \varepsilon_{in},
$$ (eq-11-random-utility)

where $V_{in}$ is the **systematic (deterministic) component** and
$\varepsilon_{in}$ the **random component (disturbance)**. The traveler
chooses the alternative with the highest utility, so for the analyst

$$
\begin{aligned}
P_n(i) &= \Prob\left(U_{in} \ge U_{jn},\ \forall j \in C_n\right), \\
\sum_{i \in C_n} P_n(i) &= 1 .
\end{aligned}
$$ (eq-11-rum)

Building a model has three steps: separate utility into systematic and
random parts, specify the systematic part, and specify the distribution of
the random part.

### Only differences and scale matter

For a binary choice $C_n = \{i, j\}$,

$$
\begin{aligned}
P_n(i) &= \Prob\left(V_{in} + \varepsilon_{in} \ge V_{jn} + \varepsilon_{jn}\right) \\
&= \Prob\left(\varepsilon_{jn} - \varepsilon_{in} \le V_{in} - V_{jn}\right).
\end{aligned}
$$ (eq-11-binary-rum)

Two consequences follow, and they hold for any number of alternatives.

1. **Adding a constant to all utilities does not change the probabilities.**
   Only the differences $V_{in} - V_{jn}$ and $\varepsilon_{jn} - \varepsilon_{in}$
   matter. Hence at most $J - 1$ alternative-specific constants can be
   estimated, and a variable that does not vary across alternatives (income,
   age) can enter the utilities of at most $J - 1$ alternatives.
2. **Multiplying all utilities by a positive constant does not change the
   probabilities.** The scale of utility is arbitrary and must be fixed by a
   normalization, usually by fixing the variance of the disturbances (for
   example $\mu = 1$ in logit, $\sigma = 1$ in probit). Nonzero means of the
   disturbances are absorbed into the constants.

## Specifying the systematic utility

The systematic utility depends on the attributes $\bz_{in}$ of alternative
$i$ as faced by traveler $n$ (time, cost, comfort, reliability) and on the
socioeconomic characteristics $\mathbf{s}_n$ of the traveler (income, car
ownership, household size, age). In practice it is specified as a function
**linear in the parameters**:

$$
\begin{aligned}
V_{in} &= \beta_1 x_{in1} + \beta_2 x_{in2} + \cdots + \beta_K x_{inK} \\
&= \bbeta\T\bx_{in},
\end{aligned}
$$ (eq-11-linear-utility)

where each $x_{ink}$ is a function of $\bz_{in}$ and $\mathbf{s}_n$. The
variables can be

- **generic**, with the same coefficient in all utilities (e.g., in-vehicle
  time valued equally in every mode);
- **alternative-specific**, entering one utility only (e.g., a coefficient
  for walking time to transit), including **alternative-specific constants**
  (ASC), which are coded as a variable equal to 1 for that alternative and 0
  for the others;
- **socioeconomic**, entered in at most $J - 1$ utilities or interacted with
  attributes (cost divided by income, time multiplied by age); and
- **dummy variables** for categories (age groups, sex, CBD destination),
  with at most $L - 1$ dummies for a variable with $L$ categories.

Linearity in the *parameters* does not prevent non-linear effects of the
*variables* (logarithms, piecewise terms, interactions). Categorizing a
continuous variable, however, discards information and is usually
inadvisable.

The ratio of two coefficients is a **marginal rate of substitution**. If
$\beta_t$ multiplies time and $\beta_c$ multiplies cost, the subjective
**value of time** is $\beta_t/\beta_c$ (money per unit of time).

## Binary choice models

Let $\varepsilon_n = \varepsilon_{jn} - \varepsilon_{in}$ with density
$f$, so that by {eq}`eq-11-binary-rum`
$P_n(i) = \int_{-\infty}^{V_{in} - V_{jn}} f(y)\,\diff y$. Each assumption
on $f$ gives a model.

### Linear probability model

If $\varepsilon_n$ is uniform on $[-L, L]$,

$$
P_n(i) =
\begin{cases}
0, & V_{in} - V_{jn} < -L, \\[2pt]
\dfrac{V_{in} - V_{jn} + L}{2L}, & -L \le V_{in} - V_{jn} \le L, \\[6pt]
1, & V_{in} - V_{jn} > L .
\end{cases}
$$ (eq-11-linear-probability)

The model is simple, but it is not differentiable at $\pm L$, and it
predicts probabilities of exactly zero or one, although in reality some
travelers choose an alternative that the model says nobody would choose.

### Binary probit

If $\varepsilon_{in}$ and $\varepsilon_{jn}$ are normal with zero means,
variances $\sigma_i^2$ and $\sigma_j^2$, and covariance $\sigma_{ij}$, then
$\varepsilon_n$ is normal with variance
$\sigma^2 = \sigma_i^2 + \sigma_j^2 - 2\sigma_{ij}$ and

$$
\begin{aligned}
P_n(i) &= \Phi\!\left(\frac{V_{in} - V_{jn}}{\sigma}\right) \\
&= \Phi\!\left(\frac{\bbeta\T(\bx_{in} - \bx_{jn})}{\sigma}\right).
\end{aligned}
$$ (eq-11-binary-probit)

The normal assumption is natural (the disturbance is the sum of many
omitted effects), but $\Phi$ has no closed form; $1/\sigma$ acts as the
scale and is normalized to 1.

### Binary logit

If $\varepsilon_{in}$ and $\varepsilon_{jn}$ are independent and identically
Gumbel distributed with scale $\mu$, then $\varepsilon_n$ is logistic
(property 4 of {prf:ref}`prop-01-logistic`), with mean 0 and variance
$\pi^2/(3\mu^2)$, and

$$
\begin{aligned}
P_n(i) &= \frac{1}{1 + e^{-\mu(V_{in} - V_{jn})}} \\
&= \frac{e^{\mu V_{in}}}{e^{\mu V_{in}} + e^{\mu V_{jn}}} .
\end{aligned}
$$ (eq-11-binary-logit)

With linear utilities,
$P_n(i) = 1/\{1 + \exp[-\mu\bbeta\T(\bx_{in} - \bx_{jn})]\}$; $\mu$ is
normalized to 1. The logistic and normal CDFs are very close once their
variances are equated, so binary logit and probit give almost identical
fits; logit coefficients are about $\pi/\sqrt{3} \approx 1.8$ times larger
than probit coefficients because of the different normalization of the
variance.

### Extreme cases

All three models have the same two limits. As the variance of the
disturbances tends to zero ($\mu \to \infty$, $\sigma \to 0$, $L \to 0$) the
choice becomes **deterministic**: $P_n(i) = 1$ if $V_{in} > V_{jn}$ and 0 if
$V_{in} < V_{jn}$. As the variance tends to infinity ($\mu \to 0$,
$\sigma \to \infty$, $L \to \infty$) the model carries no information and
$P_n(i) = P_n(j) = 1/2$.

## Multinomial logit

### The model

When $C_n$ contains $J_n > 2$ alternatives,

$$
P_n(i) = \Prob\left(\varepsilon_{jn} \le V_{in} - V_{jn} + \varepsilon_{in},\ \forall j \in C_n,\ j \ne i\right),
$$

and a model follows from the joint distribution of the disturbances.

:::{prf:theorem} Multinomial logit
:label: thm-11-mnl

If the disturbances $\varepsilon_{in}$, $i \in C_n$, are independent and
identically distributed (i.i.d.) $\mathrm{Gumbel}(0, \mu)$, then

$$
P_n(i) = \frac{\exp\left(\mu V_{in}\right)}{\sum_{j \in C_n}\exp\left(\mu V_{jn}\right)},
\qquad i \in C_n .
$$ (eq-11-mnl)

The common standard deviation of the disturbances is
$\sigma = \pi/(\sqrt{6}\,\mu)$.
:::

:::{dropdown} Proof
:class-container: proof
:animate: fade-in

By property 4 of {prf:ref}`prop-01-gumbel`,
$U_{jn} = V_{jn} + \varepsilon_{jn} \sim \mathrm{Gumbel}(V_{jn}, \mu)$. By
property 6, the best of the other alternatives,
$U_n^{*} = \max_{j \ne i} U_{jn}$, is Gumbel with scale $\mu$ and location

$$
V_n^{*} = \frac{1}{\mu}\ln\sum_{j \ne i} e^{\mu V_{jn}} .
$$

Then $P_n(i) = \Prob(U_{in} \ge U_n^{*})$ is a binary choice between two
independent Gumbel variables with a common scale, and by
{eq}`eq-11-binary-logit`

$$
\begin{aligned}
P_n(i) &= \frac{e^{\mu V_{in}}}{e^{\mu V_{in}} + e^{\mu V_n^{*}}} \\
&= \frac{e^{\mu V_{in}}}{e^{\mu V_{in}} + \sum_{j \ne i} e^{\mu V_{jn}}},
\end{aligned}
$$

which is {eq}`eq-11-mnl`.
:::

The Gumbel distribution approximates the normal one well; it is chosen for
analytical convenience. The i.i.d. assumption is the real restriction: it
implies equal variances of all disturbances and no correlation between
alternatives.

With $\mu = 1$ the coefficients absorb the scale: estimating
$V_{jn}$ with $\mu = 1$ gives $\mu\bbeta$, not $\bbeta$. Comparisons of
coefficients between models estimated on different data sets (for example
RP and SP data) are therefore meaningful only for ratios such as the value
of time.

As $\mu \to 0$, $P_n(i) \to 1/J_n$ (all alternatives equally likely); as
$\mu \to \infty$, $P_n(i) \to 1$ for the alternative with the largest
$V_{in}$ and 0 for the others.

### Independence of irrelevant alternatives

For any two alternatives $i$ and $l$,

$$
\begin{aligned}
\frac{P_n(i)}{P_n(l)} &= \frac{e^{\mu V_{in}}}{e^{\mu V_{ln}}} \\
&= e^{\mu(V_{in} - V_{ln})},
\end{aligned}
$$ (eq-11-iia)

independent of the other alternatives in the choice set. This
**independence of irrelevant alternatives (IIA)** property (Luce, 1959) is a direct
consequence of the i.i.d. assumption. It simplifies estimation (the model
can be estimated on a subset of alternatives) and forecasting (a new
alternative draws from all others in proportion to their shares), but it is
unrealistic when alternatives are correlated. In the classic
**red-bus/blue-bus** problem, travelers split equally between car and a red
bus; painting half of the buses blue adds an alternative identical to the
red bus, and the logit model predicts shares of 1/3 each, whereas common
sense says the car keeps 1/2 and the two buses share the other half
({prf:ref}`ex-27-ms-red-blue` treats the aggregate version). Any model with i.i.d. disturbances, not
only logit, fails in that case.

### Elasticities

With linear utilities, the **direct elasticity** of $P_n(i)$ with respect to
attribute $x_{ink}$ of alternative $i$, and the **cross elasticity** with
respect to the attribute $x_{jnk}$ of another alternative $j$, are

$$
\begin{aligned}
E^{P_n(i)}_{x_{ink}} &= \frac{\partial P_n(i)}{\partial x_{ink}}\frac{x_{ink}}{P_n(i)} \\
&= \mu\beta_k\, x_{ink}\left[1 - P_n(i)\right],
\end{aligned}
$$ (eq-11-direct-elasticity)

$$
E^{P_n(i)}_{x_{jnk}} = -\mu\beta_k\, x_{jnk}\, P_n(j), \qquad j \ne i .
$$ (eq-11-cross-elasticity)

The cross elasticity is the same for every alternative $i \ne j$ — another
expression of IIA. Aggregate elasticities are obtained by weighting the
individual elasticities by the choice probabilities.

### Expected maximum utility

By property 6 of {prf:ref}`prop-01-gumbel`, the maximum utility of the choice
set is Gumbel with location $\mu^{-1}\ln\sum_j e^{\mu V_{jn}}$, so

$$
\E\left[\max_{j \in C_n} U_{jn}\right] = \frac{1}{\mu}\ln\sum_{j \in C_n} e^{\mu V_{jn}} + \frac{\gamma}{\mu},
$$ (eq-11-logsum)

where $\gamma \approx 0.5772$ is Euler's constant. The **log-sum**
$\mu^{-1}\ln\sum_j e^{\mu V_{jn}}$ (expected maximum utility, EMU, up to the
constant $\gamma/\mu$) measures the overall attractiveness of the choice
set. With utilities equal to minus the generalized costs and $\mu$ equal to
the dispersion parameter $\lambda$, it is the composite cost
{eq}`eq-12-composite-cost` with the sign reversed. Divided by the marginal
utility of money, its change gives the change in consumer surplus caused by
a policy (Williams, 1977).

## Multinomial probit

If the disturbances are multivariate normal,
$(\varepsilon_{1n}, \ldots, \varepsilon_{J_nn}) \sim \mathcal{N}(\bzero, \bSigma)$,
any pattern of variances and correlations can be represented, and IIA does
not hold. The probability $P_n(i)$ is the $J_n$-dimensional normal integral
{eq}`eq-01-probit-probability`, which has no closed form for $J_n > 2$; it is
evaluated by numerical integration or by Monte Carlo simulation
({prf:ref}`ex-17-mvn-maximum`). Probit is the natural model for route choice
with overlapping routes ({doc}`15-stochastic-user-equilibrium`).

## Nested logit

The **nested logit** model (Ben-Akiva, 1973; Williams, 1977; McFadden,
1978) relaxes IIA for groups of similar
alternatives, such as the red and blue buses: alternatives that share
unobserved attributes are grouped in a **nest**. For a two-level structure with nests $m$ and
alternatives $i \in C_m$, the probability of $i$ is the product of a
conditional and a marginal probability:

$$
\begin{aligned}
P_n(i) &= P_n(i \mid m)\,P_n(m), \\
P_n(i \mid m) &= \frac{e^{V_{in}}}{\sum_{l \in C_m} e^{V_{ln}}}, \\
P_n(m) &= \frac{e^{V_{mn}}}{\sum_{m'} e^{V_{m'n}}},
\end{aligned}
$$ (eq-11-nested-logit)

where the utility of a nest is its own systematic utility (if any) plus
$\phi_m$ times the **expected maximum utility** of the alternatives in it:

$$
\begin{aligned}
V_{mn} &= V_{mn}^0 + \phi_m\,\mathrm{EMU}_{mn}, \\
\mathrm{EMU}_{mn} &= \ln\sum_{l \in C_m} e^{V_{ln}} .
\end{aligned}
$$ (eq-11-emu)

The **structural parameter** $\phi_m$ equals the ratio of the upper-level to
the lower-level scale parameters. For consistency with random utility
maximization it must satisfy $0 < \phi_m \le 1$: the smaller $\phi_m$, the
more correlated the alternatives in the nest; $\phi_m = 1$ reduces the model
to multinomial logit. Within a nest IIA holds; between nests it does not
({prf:ref}`ex-26-hw3-q4`).

## Maximum likelihood estimation

### The likelihood

Let $y_{in} = 1$ if traveler $n$ chose $i$ and 0 otherwise. For a random
sample of $N$ independent travelers, the **likelihood** is the probability
that the model reproduces all the observed choices,

$$
\mathcal{L}(\bbeta) = \prod_{n=1}^{N}\prod_{i \in C_n} P_n(i)^{y_{in}},
$$ (eq-11-likelihood)

and the **log-likelihood** is

$$
LL(\bbeta) = \sum_{n=1}^{N}\sum_{i \in C_n} y_{in}\ln P_n(i) .
$$ (eq-11-log-likelihood)

For a binary model with $y_n = y_{in}$ this is
$LL = \sum_n \{y_n\ln P_n(i) + (1 - y_n)\ln[1 - P_n(i)]\}$, the negative
of the binary cross-entropy loss of machine learning. Since every
$P_n(i) \le 1$, $LL \le 0$. The **maximum likelihood (ML)** estimate
$\hat\bbeta$ maximizes $LL$: it gives the parameters under which the
observed choices are most probable ({prf:ref}`ex-26-dc-likelihood`).

### Gradient, Hessian, and concavity

For the binary logit model with $\mu = 1$, write
$\bx_n = \bx_{in} - \bx_{jn}$ and $P_n = P_n(i) = 1/(1 + e^{-\bbeta\T\bx_n})$.
Since $\partial P_n/\partial\bbeta = P_n(1 - P_n)\bx_n$,

$$
\begin{aligned}
\nabla LL(\bbeta) &= \sum_{n=1}^{N}\left(y_n - P_n\right)\bx_n, \\
\nabla^2 LL(\bbeta) &= -\sum_{n=1}^{N} P_n\left(1 - P_n\right)\bx_n\bx_n\T .
\end{aligned}
$$ (eq-11-logit-gradient-hessian)

The Hessian is negative semidefinite, so the log-likelihood is
**concave**, and negative definite if the matrix of the $\bx_n$ has full
column rank. The first-order conditions $\nabla LL = \bzero$ — "observed
minus predicted, weighted by the variables, sums to zero" — therefore
identify the global maximum, if a maximum exists. For the multinomial logit
model the gradient is
$\sum_n\sum_i (y_{in} - P_n(i))\bx_{in}$ and the log-likelihood is again
concave.

The maximum is found by the **Newton–Raphson** method,

$$
\hat\bbeta^{(t+1)} = \hat\bbeta^{(t)} - \left[\nabla^2 LL\big(\hat\bbeta^{(t)}\big)\right]^{-1}\nabla LL\big(\hat\bbeta^{(t)}\big),
$$ (eq-11-newton-raphson)

starting for example from $\hat\bbeta^{(0)} = \bzero$, until the change in
$\hat\bbeta$ or in $LL$ is negligible; spreadsheet solvers, `scipy`, and
specialized packages (Biogeme, Apollo, `statsmodels`) all implement it.

:::{admonition} When the maximum does not exist
:class: warning
Two situations prevent estimation.

- **Unidentified parameters.** A coefficient whose variable takes the same
  value in all utilities, or that multiplies a variable equal to zero for
  every observation used, cannot be estimated (the likelihood is flat in
  that direction).
- **Perfect separation.** If some combination of the variables predicts every
  observed choice exactly, the log-likelihood increases towards 0 as the
  coefficients grow without bound and no finite maximum exists. This is
  common in very small samples ({prf:ref}`ex-26-hw3-q6`).
:::

### Standard errors and tests

Under standard regularity conditions the ML estimator is consistent and
asymptotically normal, with covariance matrix equal to the inverse of the
**Fisher information**,

$$
\Var\big[\hat\bbeta\big] \approx \left(-\E\left[\nabla^2 LL(\bbeta)\right]\right)^{-1},
$$ (eq-11-ml-covariance)

estimated by $[-\nabla^2 LL(\hat\bbeta)]^{-1}$. Three tests are standard.

Asymptotic $t$-test
: $t_k = \hat\beta_k/\se(\hat\beta_k)$ is approximately standard normal
  under $H_0: \beta_k = 0$; $|t_k| > 1.96$ rejects $H_0$ at 5 %.

Likelihood ratio test
: for a restricted model $R$ nested in an unrestricted model $U$ with $r$
  fewer parameters,
  $-2[LL(\hat\bbeta_R) - LL(\hat\bbeta_U)] \;\dot\sim\; \chi^2(r)$ under the
  restrictions. It tests several restrictions at once — for example that a
  coefficient is generic rather than alternative-specific.

Goodness of fit
: the **likelihood ratio index**
  $\rho^2 = 1 - LL(\hat\bbeta)/LL(\bzero)$, where $LL(\bzero)$ is the
  log-likelihood of the equally-likely model
  ($LL(\bzero) = \sum_n \ln(1/J_n)$). It lies between 0 and 1, but values
  of 0.2–0.4 already indicate a good fit, and it is not comparable with the
  $R^2$ of regression. The adjusted version
  $\bar\rho^2 = 1 - [LL(\hat\bbeta) - K]/LL(\bzero)$ penalizes the number
  of parameters $K$. Measuring the fit relative to a model with constants
  only, $LL(\bc)$, gives $\rho^2(\bc)$, which is more
  informative when the market shares are unequal.

As in regression, coefficients should also be checked for **sign and
plausible magnitude** (cost and time coefficients negative, values of time
reasonable).

### Choice-based samples

If the model was estimated on a choice-based sample in which alternative
$i$ has share $H_i$ while its population share is $Q_i$
({doc}`07-travel-surveys-and-sampling`), the multinomial logit model with a
full set of alternative-specific constants is still consistent for all
coefficients except the constants. The constants are corrected by

$$
K_i' = K_i - \ln\frac{H_i}{Q_i},
$$ (eq-11-asc-correction)

up to an additive constant common to all alternatives
({prf:ref}`ex-26-hw3-q5`). Alternatively, the model is estimated by the
weighted likelihood (WESML) with weights $Q_i/H_i$.

### Forecasting with disaggregate models

A disaggregate model predicts probabilities for individuals. Aggregate
forecasts are obtained by **sample enumeration** — applying the model to
each individual of a representative sample, possibly reweighted to the
forecast year, and summing the probabilities with expansion factors — or by
classification into homogeneous groups. Applying the model to zonal
averages of the variables (the "naïve" method) introduces aggregation
error, because the logit function is non-linear.

## Summary and Common Mistakes

### Summary

- Random utility {eq}`eq-11-random-utility`: travelers choose the
  alternative of maximum utility {eq}`eq-11-rum`; only utility differences
  and the scale of utility are identified {eq}`eq-11-binary-rum`.
- Uniform, normal, and Gumbel disturbances give the linear probability
  {eq}`eq-11-linear-probability`, probit {eq}`eq-11-binary-probit`, and
  logit {eq}`eq-11-binary-logit` models.
- Multinomial logit ({prf:ref}`thm-11-mnl`):
  $P_n(i) = e^{\mu V_{in}}/\sum_j e^{\mu V_{jn}}$ {eq}`eq-11-mnl`, with the
  IIA property {eq}`eq-11-iia`, direct elasticity
  $\mu\beta_k x_{ink}[1 - P_n(i)]$ {eq}`eq-11-direct-elasticity`, uniform
  cross elasticities {eq}`eq-11-cross-elasticity`, and the log-sum as
  expected maximum utility {eq}`eq-11-logsum`.
- Nested logit {eq}`eq-11-nested-logit` groups correlated alternatives; the
  nest utility carries $\phi_m$ times the log-sum of its members
  {eq}`eq-11-emu`, with $0 < \phi_m \le 1$.
- Parameters are estimated by maximizing the log-likelihood
  {eq}`eq-11-log-likelihood`, which is concave for logit
  {eq}`eq-11-logit-gradient-hessian`, with Newton–Raphson
  {eq}`eq-11-newton-raphson`; inference uses the covariance
  {eq}`eq-11-ml-covariance`, $t$-tests, likelihood ratio tests, and $\rho^2$.
- With a choice-based sample, only the alternative-specific constants are
  biased and are corrected by {eq}`eq-11-asc-correction`.

### Common mistakes

- **Including a constant or a socioeconomic variable in all $J$
  utilities.** Only utility differences matter, so such a parameter is not
  identified; normalize one alternative (at most $J - 1$ constants, and
  socioeconomic variables in at most $J - 1$ utilities).
- **Comparing coefficients across data sets directly.** Estimated
  coefficients are $\mu\bbeta$, and the scale $\mu$ differs between data
  sets (for example RP and SP data); compare ratios such as values of time.
- **Using multinomial logit for alternatives that share unobserved
  attributes.** IIA then gives absurd substitution patterns
  (red-bus/blue-bus); use a nested logit or a probit model.
- **Allowing a nested logit structural parameter outside $(0, 1]$.** Values
  above one are inconsistent with random utility maximization; values at
  or below zero have no meaning.
- **Interpreting $\rho^2$ like a regression $R^2$.** The likelihood ratio
  index is on a different scale: values of 0.2–0.4 already indicate a good
  fit.
- **Forecasting with a model estimated on a choice-based sample without
  correcting the constants.** The constants reproduce the sample shares,
  not the population shares; apply {eq}`eq-11-asc-correction` first.

## References

- Ben-Akiva, M. (1973). *Structure of passenger travel demand models*
  [Doctoral dissertation, Massachusetts Institute of Technology].
- Ben-Akiva, M., & Lerman, S. R. (1985). *Discrete Choice Analysis: Theory
  and Application to Travel Demand*, Chapters 3–8 and 10. MIT Press.
- Ortúzar, J. de D., & Willumsen, L. G. (2011). *Modelling Transport* (4th
  ed.), Chapters 7 and 8. Wiley.
- Train, K. E. (2009). *Discrete Choice Methods with Simulation* (2nd ed.),
  Chapters 2–5 and 8. Cambridge University Press.
  <https://eml.berkeley.edu/books/choice2.html>
- McFadden, D. (1974). Conditional logit analysis of qualitative choice
  behavior. In P. Zarembka (Ed.), *Frontiers in Econometrics* (pp. 105–142).
  Academic Press.
- McFadden, D. (1978). Modelling the choice of residential location. In
  A. Karlqvist, L. Lundqvist, F. Snickars, & J. W. Weibull (Eds.),
  *Spatial Interaction Theory and Planning Models* (pp. 75–96).
  North-Holland.
- Luce, R. D. (1959). *Individual Choice Behavior: A Theoretical Analysis*.
  Wiley.
- Williams, H. C. W. L. (1977). On the formation of travel demand models
  and economic evaluation measures of user benefit. *Environment and
  Planning A*, 9(3), 285–344. <https://doi.org/10.1068/a090285>
- Manski, C. F., & Lerman, S. R. (1977). The estimation of choice
  probabilities from choice based samples. *Econometrica*, *45*(8),
  1977–1988. <https://doi.org/10.2307/1914121>
