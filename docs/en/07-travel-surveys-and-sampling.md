# Travel Surveys and Sampling

## Overview

Travel demand models are estimated from samples: a few thousand households
out of a million, a few hundred drivers stopped at a roadside station out of
tens of thousands that pass. This chapter covers the statistical side of
data collection — how to draw a sample, how large it must be, and how the
sampling method affects the estimation of models — and then reviews the
main types of transport surveys, from household interviews to stated
preference experiments.

:::{admonition} Learning objectives
:class: objectives
After completing this chapter, readers should be able to:

- define population, sampling unit, sampling frame, sampling error, and
  sampling bias;
- describe simple random, stratified, and choice-based sampling and write
  the joint distribution of choices and attributes in each type of sample;
- compute weighting factors that remove the bias of a choice-based sample;
- compute the sample size needed to estimate a mean or a proportion with a
  given precision and confidence, with and without a finite-population
  correction; and
- describe household interview, roadside, cordon, screen-line, travel-time,
  and revealed- and stated-preference surveys.
:::

## Notation

| Symbol | Meaning |
|---|---|
| $N$, $n$ | population size and sample size |
| $\mu$, $\sigma^2$ | population mean and variance of the attribute of interest |
| $\bar{x}$, $s^2$ | sample mean and sample variance |
| $\mathrm{CV} = \sigma/\mu$ | coefficient of variation |
| $z_{\alpha/2}$ | standard normal quantile with upper-tail probability $\alpha/2$ |
| $Y$ | observed choice of a sampled individual (e.g., travel mode) |
| $\bX$ | characteristics of the individual and of the alternatives |
| $\Pr(\cdot)$ | probabilities in the population |
| $f(\cdot)$ | probabilities in the sample |
| $\btheta$ | parameters of the choice model |
| $w_Y$ | weighting factor of alternative $Y$ in a choice-based sample |
| $E$, $e$ | relative error of a mean; absolute error of a proportion |
| $p$, $\hat p$ | population proportion and its sample estimate |

## Basic sampling concepts

The **population of interest** is the complete group about which information
is sought; its definition follows from the study objectives (for example,
all households resident in the study area). A **sample** is a subset of the
population selected to represent it with respect to the attributes of
interest (trip rates, income, mode used). Samples are drawn in **sampling
units**, which need not be the elements of interest: households are
sampled, but the trips of each person in them are recorded. The list from
which units are drawn is the **sampling frame** (a dwelling register, a
census list, a list of road crossings at the cordon).

Sample design asks three questions: which population the sample represents,
how large it must be, and how the units are selected. Two kinds of error
must be distinguished.

Sampling error
: arises because only a sample is observed. It is always present, does not
  affect the expected value of an estimator, and decreases roughly in
  proportion to $1/\sqrt{n}$. It determines the width of confidence
  intervals.

Sampling bias
: arises from mistakes in defining the population, the sampling frame, the
  selection method, or the data collection technique (for example a
  telephone survey that misses households without a fixed line). Bias
  shifts the estimates themselves, does not decrease as the sample grows,
  and is much more damaging than sampling error.

## Three sampling methods

### Simple random sampling

Each unit of the population is given an identifier, and identifiers are
drawn at random so that every unit has the same probability of selection,
independently of the others. Simple random sampling has high internal and
external validity, but it requires a complete list of the population, and
**very large samples may be needed to obtain enough observations of
minority groups or rarely chosen options**.

### Stratified random sampling

Prior information is used to divide the population into homogeneous
**strata** with respect to an exogenous variable (income, car ownership,
household size, location), and simple random sampling is carried out within
each stratum. The sampling rates may differ between strata, so small but
important groups can be over-sampled. Stratification on variables that are
*explanatory* variables of the model is called **exogenous** stratification.

### Choice-based sampling

The population is stratified by the **outcome of the choice being
modeled** — for example, interviewing bus passengers at bus stops and
drivers in car parks. This is common and cheap in transport studies,
because users of a mode are easy to find where they use it, and it is the
only practical way to obtain enough users of a mode with a small market
share. The price is that the sample is not random with respect to the
choice, so estimates must be corrected (see below).

### The joint distribution in each type of sample

Describe every sampled individual by the chosen alternative $Y$ and by the
vector $\bX$ of characteristics of the individual and of the alternatives.
In the population, the choice process is represented by a model with
parameters $\btheta$ (for example a logit mode-choice model,
{doc}`11-discrete-choice-models`), so that the joint distribution is

$$
\Pr(Y, \bX \mid \btheta) = \Pr(Y \mid \bX, \btheta)\,\Pr(\bX).
$$ (eq-07-population-joint)

**Simple random sample.** The sample reproduces the population:

$$
f(Y, \bX \mid \btheta) = \Pr(Y, \bX \mid \btheta).
$$ (eq-07-srs-joint)

**Stratified (exogenous) sample.** The sampling process selects an
observation with characteristics $\bX$ with probability $f(\bX)$, which
differs from the population share $\Pr(\bX)$. Within each stratum the
choices are still random, so

$$
f(Y, \bX \mid \btheta) = f(\bX)\,\Pr(Y \mid \bX, \btheta).
$$ (eq-07-stratified-joint)

Simple random sampling is the special case $f(\bX) = \Pr(\bX)$. Dividing
{eq}`eq-07-stratified-joint` by $f(\bX)$ gives the key property

$$
f(Y \mid \bX, \btheta) = \Pr(Y \mid \bX, \btheta).
$$ (eq-07-stratified-property)

That is, **conditional choice probabilities are the same in an exogenously stratified
sample as in the population**, so a choice model can be estimated from it
without correction.

**Choice-based sample.** The sampling process selects an observation that
chose $Y$ with probability $f(Y)$, which differs from the population share
$\Pr(Y)$; within each choice group the characteristics are random, so

$$
f(Y, \bX \mid \btheta) = f(Y)\,\Pr(\bX \mid Y, \btheta).
$$

By Bayes' theorem,

$$
\begin{aligned}
\Pr(\bX \mid Y, \btheta) &= \frac{\Pr(Y \mid \bX, \btheta)\,\Pr(\bX)}{\Pr(Y \mid \btheta)}, \\
\Pr(Y \mid \btheta) &= \sum_{\bX}\Pr(Y \mid \bX, \btheta)\,\Pr(\bX),
\end{aligned}
$$

where the sum runs over the (discrete) values of $\bX$. Therefore

$$
\begin{aligned}
f(Y, \bX \mid \btheta) &= \frac{f(Y)\,\Pr(Y \mid \bX, \btheta)\,\Pr(\bX)}
       {\displaystyle\sum_{\bX'}\Pr(Y \mid \bX', \btheta)\,\Pr(\bX')}.
\end{aligned}
$$ (eq-07-choice-based-joint)

In a choice-based sample the conditional choice probabilities
$f(Y \mid \bX)$ are **not** equal to $\Pr(Y \mid \bX)$: a model estimated by
treating the sample as random is biased.

### Correcting choice-based samples: weighting

Let $w_Y = \Pr(Y)/f(Y)$ be the ratio of the population share of alternative
$Y$ to its share in the sample. Since $f(\bX \mid Y) = \Pr(\bX \mid Y)$ in a
choice-based sample,

$$
\begin{aligned}
\Pr(Y \mid \bX)
&= \frac{\Pr(\bX \mid Y)\,\Pr(Y)}{\sum_{Y'}\Pr(\bX \mid Y')\,\Pr(Y')} \\
&= \frac{f(\bX \mid Y)\,\Pr(Y)}{\sum_{Y'} f(\bX \mid Y')\,\Pr(Y')} \\
&= \frac{w_Y\, f(Y, \bX)}{\sum_{Y'} w_{Y'}\, f(Y', \bX)}.
\end{aligned}
$$ (eq-07-choice-based-weights)

Weighting each observation by

$$
\begin{aligned}
w_Y &= \frac{\Pr(Y)}{f(Y)} \\
&= \frac{\text{share of alternative } Y \text{ in the population}}
       {\text{share of alternative } Y \text{ in the sample}}
\end{aligned}
$$ (eq-07-weight)

therefore recovers the population choice probabilities. In estimation, the
**weighted exogenous sample maximum likelihood (WESML)** estimator of
Manski and Lerman maximizes the weighted log-likelihood
$\sum_n w_{Y_n}\ln\Pr(Y_n \mid \bX_n, \btheta)$, which standard software for
random samples can do once the weights are supplied. Only the population
market shares $\Pr(Y)$ need to be known. For a multinomial logit model with
a full set of alternative-specific constants, the unweighted estimator is
also consistent for all coefficients except the constants, and the constant
of alternative $i$ is corrected by subtracting $\ln[f(i)/\Pr(i)]$.

### Practical considerations

Stratified and choice-based sampling require random sampling *within* each
stratum, which presupposes that the stratum can be isolated. They also
require the size of each subpopulation. This can be obtained

- **by direct measurement**, for example from a census;
- **from a random sample**, since the share of observations in each stratum
  is a consistent estimator of the population share; or
- **by solving simultaneous equations.** If the population averages of a few
  variables are known (say average income and car ownership) and small
  on-mode surveys give the average of the same variables among the users of
  each mode, the unknown mode shares $F_m$ satisfy one linear equation per
  variable plus $\sum_m F_m = 1$ ({prf:ref}`ex-22-subpopulation-shares`).

## Sample size

### Estimating a mean

Let a population of size $N$ have mean $\mu$ and variance $\sigma^2$ for
the attribute of interest. By the central limit theorem, the sample mean
$\bar{x}$ of a random sample of size $n$ is approximately normal with mean
$\mu$ and **standard error**

$$
\se(\bar{x}) = \sqrt{\frac{(N - n)\,\sigma^2}{n\,(N - 1)}}.
$$ (eq-07-se-finite)

The factor $(N - n)/(N - 1)$ is the **finite population correction**. With
the sample variance $s^2$ in place of $\sigma^2$, the estimated standard
error is

$$
\se(\bar{x}) \approx \sqrt{\left(1 - \frac{n}{N}\right)\frac{s^2}{n}},
$$ (eq-07-se-estimated)

and for a large population and a comparatively small sample,
$\se(\bar{x}) \approx s/\sqrt{n}$. Solving {eq}`eq-07-se-estimated` for $n$
with a target standard error $\se$ gives the sample size in two steps:

$$
\begin{aligned}
n' &= \frac{s^2}{\se^2}, \\
n &= \frac{n'}{1 + n'/N}.
\end{aligned}
$$ (eq-07-sample-size-fpc)

The first value ignores the finite population; the second corrects it and
matters only when $n'$ is not small relative to $N$.

### Precision, confidence, and the coefficient of variation

A target standard error is chosen from two judgments:

1. the **confidence level** $1 - \alpha$, that is how often the analyst
   accepts being wrong when using $\bar{x}$ for $\mu$ (typically 95 %); and
2. the acceptable **error of estimation** $E$, either absolute (a
   *tolerance*, e.g. $\pm 0.2$ trips) or relative (a *precision*, e.g.
   $\pm 10\,\%$ of the mean).

The confidence interval $\bar{x} \pm z_{\alpha/2}\,\sigma/\sqrt{n}$ has
half-width $z_{\alpha/2}\,\sigma/\sqrt{n}$. Requiring it to equal a
relative error $E\mu$ gives

$$
\begin{aligned}
n &= \left(\frac{z_{\alpha/2}\,\sigma}{E\,\mu}\right)^2 \\
&= \frac{z_{\alpha/2}^2\,\mathrm{CV}^2}{E^2}.
\end{aligned}
$$ (eq-07-sample-size-cv)

For 95 % confidence ($z_{0.025} = 1.96$) and a 10 % error,
$n = (1.96/0.1)^2\,\mathrm{CV}^2 \approx 384\,\mathrm{CV}^2$. The sample
size depends on the variability of the attribute relative to its mean, not
on the size of the population — as long as the population is large.

### Estimating a proportion

Many survey targets are proportions: the share of trips between a given
O-D pair, or the share of households owning a car. Suppose $N$ vehicles pass
a roadside station, $N_1$ of them travel between O-D pair 1, and
$p = N_1/N$. A sample of $n$ vehicles is drawn without replacement; the
number $X_1$ of sampled vehicles of pair 1 follows a hypergeometric
distribution with

$$
\begin{aligned}
\E[X_1] &= np, \\
\Var[X_1] &= np(1 - p)\,\frac{N - n}{N - 1} \\
&\approx np(1 - p)\left(1 - \frac{n}{N}\right).
\end{aligned}
$$

By the normal approximation, the estimator $\hat{p} = X_1/n$ satisfies

$$
\hat{p} \;\dot\sim\; \mathcal{N}\!\left(p,\ \frac{p(1 - p)(1 - n/N)}{n}\right),
$$

so an approximate $100(1-\alpha)\,\%$ confidence interval for $p$ is
$\hat{p} \pm z_{\alpha/2}\sqrt{p(1 - p)(1 - n/N)/n}$. Requiring its
half-width not to exceed an absolute error $e$ (commonly $e = 0.1$) gives

$$
n \ \ge\ \frac{p(1 - p)}{(e/z_{\alpha/2})^2 + p(1 - p)/N}.
$$ (eq-07-sample-size-proportion)

The right-hand side increases with $p(1 - p)$, which is largest at
$p = 1/2$. Without prior knowledge of $p$, the **conservative sample size**
is therefore

$$
n^{*} = \frac{0.25}{(e/z_{\alpha/2})^2 + 0.25/N}.
$$ (eq-07-sample-size-conservative)

As $N \to \infty$, $n^* \to 0.25\,(z_{\alpha/2}/e)^2$, which is
$0.25 \times 19.6^2 = 96.04$, that is 97 after rounding up, for $e = 0.1$
and 95 % confidence.

:::{admonition} Response rates
:class: note
The formulas give the number of *usable responses*. If only a fraction $r$
of the contacted units respond, about $n/r$ units must be contacted — and
non-response may also cause bias if non-respondents differ systematically
from respondents.
:::

## Household interview travel surveys

Household surveys are the richest source of information on travel behavior
and are used for strategic models. Early surveys were criticized for
recording *average* rather than actual behavior, for capturing only part of
people's movements, and for poor reporting of level-of-service variables.
Modern surveys therefore

- record travel on a **pre-assigned day** rather than "usual" behavior;
- use an **activity-recall** framework: respondents report the activities of
  the day and the trips between them, which reduces forgotten trips and
  allows complete tours to be reconstructed;
- include all modes, including walking and cycling, and all household
  members, including non-family members; and
- record trips by **stages**, a new stage starting at every change of mode.

Questions should be simple and direct, each should serve a purpose, open
questions should be few, and the trip purpose must always be recorded.
Personal and household questions cover relationship to the head of household,
age, sex, license holding, education, occupation, income, dwelling, and
vehicles.

**Sampling frames** include census or dwelling lists, utility or
property-tax registers, and random selection of blocks; non-residents are
reached through lists of hotels and other non-private dwellings, transport
interchanges, and road crossings at the cordon.

**Sample size.** If the target is the mean number of daily trips per
household with relative error $E$ and the coefficient of variation is known
from previous studies, {eq}`eq-07-sample-size-cv` applies directly
({prf:ref}`ex-22-household-sample-size`).

**Optimizing the sample design.** To estimate trip rates by socioeconomic
class at minimum cost, let $\eta_{ij}$ be the number of households of class
$i$ in zone $j$, $\mu_i$ the minimum acceptable number of observations of
class $i$ (say 30 or 50), and $\alpha_j$ the sampling rate in zone $j$,
bounded by $\delta$ (say 5 %). The design that minimizes the total number of
interviews solves the linear program

$$
\begin{aligned}
\min_{\alpha_j}\quad & \sum_j \alpha_j \sum_i \eta_{ij} \\
\text{s.t.}\quad & \sum_j \alpha_j\,\eta_{ij} \ \ge\ \mu_i, \qquad \forall i, \\
& 0 \le \alpha_j \le \delta, \qquad \forall j.
\end{aligned}
$$ (eq-07-sample-design-lp)

A simpler heuristic samples zones class by class, starting from the least
represented class, until every class reaches its minimum; it is easy to
apply but has no guarantee of optimality.

## Other surveys

Roadside interview surveys
: A sample of vehicles is stopped at a roadside station (with police
  assistance) and drivers are asked a few questions: at least origin,
  destination, and purpose. They capture trips not recorded by the household
  survey, such as through trips, and allow larger samples of specific O-D
  movements. The sample size per station follows from
  {eq}`eq-07-sample-size-conservative`.

Cordon and screen-line surveys
: Counts and short interviews at the external cordon measure trips entering,
  leaving, or crossing the study area; screen-line counts are used to check
  and correct household survey data, taking care not to introduce bias.

Commercial vehicle, para-transit, and public transport surveys
: Trip logs of goods vehicles (each loading or unloading point is a trip
  end), of intermediate public transport such as taxis and minibuses, and
  on-board or boarding–alighting surveys of buses and trains.

Travel time surveys
: Travel time consists of running time and delay. The **test car (floating
  car)** method drives a vehicle through the section many times; the
  **license plate** method records plates and passing times at successive
  points and matches them; the **moving observer** method counts vehicles
  met and overtaken while driving with and against the stream (Wardrop &
  Charlesworth, 1954). With $x$ the
  number of vehicles met while traveling against the stream (time $t_a$)
  and $y$ the number overtaking minus overtaken while traveling with it
  (time $t_w$), the flow and mean travel time of the stream are
  $q = (x + y)/(t_a + t_w)$ and $\bar{t} = t_w - y/q$. Today GPS traces,
  automatic number-plate recognition, and smart-card data provide the same
  information continuously.

## Revealed and stated preference

**Revealed preference (RP)** data record actual choices. They are reliable
but limited: attributes of real alternatives are often correlated and vary
little, secondary qualitative attributes (information, security, comfort)
are hard to measure, and entirely new options cannot be observed.

**Stated preference (SP)** methods ask respondents how they would act in
hypothetical situations designed by the analyst. Three families exist:

- **contingent valuation**, which elicits willingness to pay (WTP) for a
  whole policy or product but cannot separate the value of its attributes;
- **conjoint analysis**, in which respondents rank or rate profiles whose
  attribute levels are varied systematically; regressing ratings on
  attributes gives part-worths, and the ratio of an attribute's coefficient
  to the cost coefficient is its marginal WTP; and
- **stated choice**, in which respondents choose one alternative from a
  small set, repeated over several choice tasks, and the data are analyzed
  with discrete choice models.

Designing a stated choice experiment involves

1. clarifying the objectives, the alternatives (labeled or unlabeled), and
   the attributes;
2. choosing the attribute levels and their ranges and deciding whether
   interactions must be estimable;
3. generating an experimental design. A full factorial with $J$
   alternatives, $K$ attributes each, and $L$ levels per attribute has
   $L^{KJ}$ profiles — for 3 alternatives with 7 three-level attributes,
   $3^{21} \approx 10^{10}$ — so an orthogonal fractional factorial or an
   efficient (D-optimal or D-efficient) design with a few dozen choice
   situations is used, split into blocks across respondents;
4. testing the design by Monte Carlo simulation (bias and efficiency of the
   parameter estimates for plausible parameter values and sample sizes); and
5. building the questionnaire, with clear graphics, realistic contexts
   (for example levels pivoted around the respondent's current trip), and a
   "none of these" option where rejecting all alternatives is realistic.

## Summary and Common Mistakes

### Summary

- Sampling error shrinks in proportion to $1/\sqrt{n}$; sampling bias does
  not shrink at all.
- Exogenous stratification leaves conditional choice probabilities
  unchanged {eq}`eq-07-stratified-property`; choice-based sampling does not
  {eq}`eq-07-choice-based-joint`, but weighting each observation by
  $w_Y = \Pr(Y)/f(Y)$ {eq}`eq-07-weight` restores them
  {eq}`eq-07-choice-based-weights` (the WESML estimator).
- The standard error of a sample mean carries the finite population
  correction {eq}`eq-07-se-estimated`, and the required sample size is
  corrected in the same way {eq}`eq-07-sample-size-fpc`.
- Sample sizes follow from the target precision, the confidence level, and
  the variability of the attribute: {eq}`eq-07-sample-size-cv` for means
  and {eq}`eq-07-sample-size-proportion`, or the conservative
  {eq}`eq-07-sample-size-conservative` with $p = 1/2$, for proportions.
- The cost-minimizing allocation of household interviews to zones is the
  linear program {eq}`eq-07-sample-design-lp`.
- Household, roadside, cordon, travel-time, RP, and SP surveys play
  complementary roles in model building and validation.

### Common mistakes

- **Estimating a choice model from a choice-based sample as if it were
  random.** The conditional choice probabilities of such a sample differ
  from those of the population; weight the observations by
  $\Pr(Y)/f(Y)$ or correct the alternative-specific constants.
- **Confusing stratification on explanatory variables with stratification
  on the choice.** The first leaves the conditional choice probabilities
  unchanged and needs no correction; the second biases the estimates unless
  it is corrected.
- **Ignoring non-response when converting a required sample size into a
  number of contacts.** The formulas give usable responses; with response
  rate $r$ about $n/r$ units must be contacted, and non-response may also
  bias the sample.
- **Misusing the finite population correction.** It applies only to
  sampling without replacement from a finite population; it must not be
  dropped when $n/N$ is large, and it is negligible when $n/N$ is small.

## References

- Ortúzar, J. de D., & Willumsen, L. G. (2011). *Modelling Transport* (4th
  ed.), Chapter 3 (Data and space). Wiley.
  <https://doi.org/10.1002/9781119993308>
- Manski, C. F., & Lerman, S. R. (1977). The estimation of choice
  probabilities from choice based samples. *Econometrica*, *45*(8),
  1977–1988. <https://doi.org/10.2307/1914121>
- Lerman, S. R., & Manski, C. F. (1976). Alternative sampling procedures
  for calibrating disaggregate choice models. *Transportation Research
  Record*, *592*, 24–28.
- Ben-Akiva, M., & Lerman, S. R. (1985). *Discrete Choice Analysis*,
  Chapter 8. MIT Press.
- Wardrop, J. G., & Charlesworth, G. (1954). A method of estimating speed
  and flow of traffic from a moving vehicle. *Proceedings of the Institution
  of Civil Engineers*, *3*(1), 158–171. <https://doi.org/10.1680/ipeds.1954.11628>
- Hensher, D. A., Rose, J. M., & Greene, W. H. (2015). *Applied Choice
  Analysis* (2nd ed.). Cambridge University Press.
