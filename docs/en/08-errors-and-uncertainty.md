# Errors and Uncertainty in Modeling

## Overview

Every forecast is uncertain. The input data are measured with error, the
models are estimated from finite samples, iterative algorithms stop before
exact convergence, models simplify behavior, and the explanatory variables
of the planning year must themselves be forecast. This chapter classifies
the sources of error, shows how errors in the inputs propagate to the
output of a model, and uses the result to reason about two practical
questions: which data are worth improving, and how complex a model should be
given the quality of the data.

:::{admonition} Learning objectives
:class: objectives
After completing this chapter, readers should be able to:

- name and describe the main types of error in travel demand modeling;
- derive and apply the first-order error propagation formula, with and
  without correlation between inputs;
- compare the error behavior of sums, differences, products, ratios, and
  powers, and state the resulting rules of thumb for model building;
- compute marginal improvement rates and decide which input is the most
  cost-effective to measure more accurately; and
- explain the trade-off between model complexity and data accuracy.
:::

## Notation

| Symbol | Meaning |
|---|---|
| $z = f(x_1, \ldots, x_k)$ | model output as a function of its inputs |
| $e_{x_i}$ | error (standard deviation) of input $x_i$ |
| $e_z$ | error (standard deviation) of the output |
| $r_{ij}$ | correlation coefficient between $x_i$ and $x_j$ |
| $e_s$, $e_m$, $e$ | specification error, propagated measurement error, and total error of a forecast |

## Types of error

It is useful to separate errors that make even a correct model give wrong
forecasts from errors that cause a wrong model to be estimated.

Measurement error
: Inaccuracies in measuring the base-year data: questions misunderstood by
  respondents or answers misrecorded by interviewers, network measurement
  errors, coding and digitizing errors. Its size depends on the care taken
  in data collection.

Sampling error
: Arises because models are estimated from finite samples; it is roughly
  inversely proportional to the square root of the number of observations
  ({doc}`07-travel-surveys-and-sampling`).

Computational error
: Arises because models are solved by iterative numerical methods that are
  stopped before reaching the exact solution. It is usually small compared
  with the others, except in assignment to congested networks and in the
  equilibration of supply and demand in large model systems.

Specification error
: Arises when the phenomenon is not well understood or must be simplified:
  including an irrelevant variable, omitting a relevant one (probably the
  most common case), ignoring taste variation among individuals, or using an
  inappropriate functional form. Omitted variables are absorbed by the
  random error term of the model, which is harmless only if they are
  uncorrelated with the included variables and have the same distribution in
  the forecast population as in the estimation sample. Specification error
  can be reduced by making the model more complex, at a cost in data and
  estimation effort.

Transfer error
: Occurs when a model estimated in one context (place or time) is applied in
  another. Spatial transfer error can be reduced by re-estimating part of the
  model with local data; temporal transfer — which is what every forecast
  does — cannot be checked until the future arrives, so it grows with the
  forecasting horizon.

Aggregation error
: Arises because forecasts are needed for groups (zones, market segments)
  while behavior is best modeled at the individual level. It includes
  *data aggregation* (using zonal averages as model inputs), *aggregation of
  alternatives* (grouping destinations into zones or routes into paths), and
  *model aggregation* (obtaining aggregate forecasts from a non-linear
  individual model). Model aggregation is trivial only for linear models.

A further source of error in every forecast is the uncertainty of the
planning-year values of the explanatory variables (population, income, car
ownership), which are themselves forecasts.

## Propagation of errors

### The general formula

Let the output of a model be $z = f(x_1, \ldots, x_k)$, where each input
$x_i$ is observed with error $e_{x_i}$ (its standard deviation). Expanding
$f$ in a first-order Taylor series around the observed values
$\bar{\bx} = (\bar{x}_1, \ldots, \bar{x}_k)$,

$$
z \approx f(\bar{\bx})
  + \sum_{i=1}^{k} \frac{\partial f}{\partial x_i}\,(x_i - \bar{x}_i),
$$

where the derivatives are evaluated at $\bar{\bx}$. The variance of a linear
combination of random variables gives

$$
\begin{aligned}
e_z^2 &= \sum_{i=1}^{k}\left(\frac{\partial f}{\partial x_i}\right)^{2} e_{x_i}^2
  + \sum_{i=1}^{k}\sum_{j \ne i}
    \frac{\partial f}{\partial x_i}\,\frac{\partial f}{\partial x_j}\,
    r_{ij}\, e_{x_i}\, e_{x_j},
\end{aligned}
$$ (eq-08-error-propagation)

where $r_{ij}$ is the correlation coefficient between $x_i$ and $x_j$ (the
double sum counts each pair twice). Formula {eq}`eq-08-error-propagation` is
exact for linear functions and a good approximation for smooth non-linear
functions when the errors are small relative to the values. When the inputs
are uncorrelated it reduces to

$$
e_z^2 = \sum_{i=1}^{k}\left(\frac{\partial f}{\partial x_i}\right)^{2} e_{x_i}^2 .
$$ (eq-08-error-propagation-indep)

### Basic operations

For two independent inputs $x \pm e_x$ and $y \pm e_y$,
{eq}`eq-08-error-propagation-indep` gives:

| Operation | Absolute error $e_z$ | Relative error $e_z/z$ |
|---|---|---|
| $z = x + y$ | $\sqrt{e_x^2 + e_y^2}$ | $\sqrt{e_x^2 + e_y^2}\,/\,(x + y)$ |
| $z = x - y$ | $\sqrt{e_x^2 + e_y^2}$ | $\sqrt{e_x^2 + e_y^2}\,/\,(x - y)$ |
| $z = xy$ | $\sqrt{y^2e_x^2 + x^2e_y^2}$ | $\sqrt{(e_x/x)^2 + (e_y/y)^2}$ |
| $z = x/y$ | $\sqrt{e_x^2/y^2 + x^2e_y^2/y^4}$ | $\sqrt{(e_x/x)^2 + (e_y/y)^2}$ |
| $z = x^{m}$ | $\lvert m\,x^{m-1}\rvert\, e_x$ | $\lvert m\rvert\,e_x/\lvert x\rvert$ |

Absolute errors add in quadrature for sums and differences; relative errors
add in quadrature for products and ratios; a power multiplies the relative
error by the exponent. The difference of two similar quantities is the
worst case: its absolute error is that of a sum, but it is divided by a
small number ({prf:ref}`ex-23-error-operations`).

These results lead to the following **rules of thumb** for choosing between
model forms that are otherwise equally acceptable:

1. avoid inter-correlated variables (positive correlation inflates the error
   of sums and products);
2. prefer additive forms where possible;
3. if addition is not possible, products and ratios are the next best
   choice; and
4. avoid, as far as possible, differences of similar quantities and raising
   variables to powers.

### Errors of forecasts and specification error

A forecast $\hat{z}$ obtained from a model is subject to two independent
sources of error: the propagated input error $e_{\hat{z}}$, obtained from
{eq}`eq-08-error-propagation`, and the specification error of the model
itself. Writing the true value as $z = \hat{z} + D$, where the discrepancy
$D$ has mean zero and standard deviation $e_s$ (the specification error)
and is independent of the input errors,

$$
e_z = \sqrt{e_{\hat{z}}^2 + e_s^2}.
$$ (eq-08-forecast-error)

{prf:ref}`ex-23-hw1-q3` shows how including the
specification error can reverse the choice between two forecasting models.

## The value of better data

### Marginal improvement rates

Given a fixed budget, which input should be measured more accurately?
Differentiating the square root of {eq}`eq-08-error-propagation-indep` with
respect to $e_{x_i}$,

$$
\begin{aligned}
\frac{\partial e_z}{\partial e_{x_i}} &= \left(\frac{\partial f}{\partial x_i}\right)^{2}\frac{e_{x_i}}{e_z}.
\end{aligned}
$$ (eq-08-marginal-improvement)

This is the **marginal improvement rate** of the output error with respect to
the error of input $i$: the reduction in $e_z$ obtained per unit reduction
in $e_{x_i}$. Dividing the marginal cost of improving each input by its
marginal improvement rate gives the cost of reducing $e_z$ by one unit
through that input; the cheapest option should be taken first
({prf:ref}`ex-23-value-better-data`).

In practice, the law of diminishing returns applies — each further
reduction in the error of a variable costs proportionally more — so the
calculation must be repeated as the errors change. Two rules follow
directly from {eq}`eq-08-marginal-improvement`:

- concentrate on variables with **large errors** $e_{x_i}$; and
- concentrate on the **most relevant** variables, those with large
  $\lvert\partial f/\partial x_i\rvert$.

### Model complexity versus data accuracy

A more complex model usually has a smaller specification error $e_s$, but
it uses more variables, each measured with error, so its propagated
measurement error $e_m$ is larger. If the two are independent, the total
error is, as in {eq}`eq-08-forecast-error`,

$$
e = \sqrt{e_s^2 + e_m^2}.
$$ (eq-08-total-error)

As complexity increases, $e_s$ falls and $e_m$ rises, so the total error has
a minimum at an intermediate level of complexity
({numref}`fig-08-error-vs-complexity`). The optimal model therefore depends on
the quality of the data: with poor data, a simpler model can forecast
better than a "perfect" but data-hungry one
({prf:ref}`ex-23-simple-vs-complex`).

```{figure} figures/08-error-vs-complexity.svg
:name: fig-08-error-vs-complexity
:width: 460px
:class: dark-light

Specification error falls and propagated measurement error rises with model
complexity; their combination, the total forecast error, is smallest at an
intermediate complexity.
```

## Summary and Common Mistakes

### Summary

- Errors arise from measurement, sampling, computation, specification,
  transfer, and aggregation, plus uncertainty in planning-year inputs.
- First-order error propagation {eq}`eq-08-error-propagation` adds
  covariance terms for correlated inputs; for independent inputs it reduces
  to $e_z^2 = \sum_i (\partial f/\partial x_i)^2 e_{x_i}^2$
  {eq}`eq-08-error-propagation-indep`.
- Absolute errors add in quadrature for sums and differences, relative
  errors for products and ratios; differences of similar quantities and
  powers amplify errors.
- The error of a forecast combines the propagated input error and the
  specification error {eq}`eq-08-forecast-error`.
- Marginal improvement rates {eq}`eq-08-marginal-improvement` identify which
  data are worth improving: inputs with large errors and large sensitivities.
- The total error {eq}`eq-08-total-error` is minimized at an intermediate
  model complexity that depends on data quality
  ({numref}`fig-08-error-vs-complexity`).

### Common mistakes

- **Adding independent errors linearly.** Independent errors add in
  quadrature; adding them linearly overstates the error, while adding
  strongly positively correlated errors in quadrature understates it
  (include the covariance terms of {eq}`eq-08-error-propagation`).
- **Applying the first-order formula to large errors.** The Taylor
  linearization assumes small relative errors; for large errors or highly
  non-linear models, simulate the output distribution instead.
- **Choosing the most detailed model available without asking whether the
  data can support it.** Each extra variable adds measurement error; with
  poor data a simpler model can give a smaller total error.

## References

- Ortúzar, J. de D., & Willumsen, L. G. (2011). *Modelling Transport* (4th
  ed.), Section 3.2 (Errors in modelling and forecasting). Wiley.
  <https://doi.org/10.1002/9781119993308>
- Alonso, W. (1968). Predicting best with imperfect data. *Journal of the
  American Institute of Planners*, *34*(4), 248–255.
  <https://doi.org/10.1080/01944366808977813>
- Taylor, J. R. (1997). *An Introduction to Error Analysis* (2nd ed.),
  Chapter 3. University Science Books.
