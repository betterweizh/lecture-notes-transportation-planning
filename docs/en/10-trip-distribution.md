# Trip Distribution: Growth-Factor and Gravity Models

## Overview

Trip generation tells how many trips leave and arrive at each zone; trip
distribution decides **where** they go, filling the cells $T_{ij}$ of the
trip matrix. This chapter presents the two classical families of
distribution models. **Growth-factor** models update an observed base-year
matrix to match future trip ends: the uniform, average, Detroit, Fratar,
and Furness methods. **Gravity** models synthesize the matrix from trip
ends and the cost of travel between zones; the entropy-maximizing principle
of {doc}`04-biproportional-fitting` derives both families from one
argument and explains the role of every parameter. Gravity models must be
calibrated against observed trip lengths. The chapter ends with practical
issues: partial matrices, external and intra-zonal trips, trip purposes,
and $K$-factors.

:::{admonition} Learning objectives
:class: objectives
After completing this chapter, readers should be able to:

- write the balance constraints of a trip matrix and distinguish singly and
  doubly constrained models;
- define generalized cost;
- apply the uniform, singly constrained, average, Detroit, Fratar, and
  Furness growth-factor methods and compare them;
- specify gravity models with exponential, power, combined, and stepwise
  deterrence functions;
- derive the balancing factors of singly and doubly constrained gravity
  models;
- derive the growth-factor and gravity models by entropy maximization and
  interpret the multipliers as balancing factors and deterrence parameters;
- calibrate a gravity model to an observed trip length distribution with
  the tri-proportional method, including partial matrices; and
- treat external zones, intra-zonal trips, purposes, and $K$-factors.
:::

## Notation

| Symbol | Meaning |
|---|---|
| $i, j = 1, \ldots, z$ | origin and destination zones |
| $T_{ij}$, $O_i$, $D_j$, $T$ | modeled (future) trips, trip ends, and total |
| $t_{ij}$, $o_i$, $d_j$, $t$ | observed (base-year or sample) trips, trip ends, and total |
| $c_{ij}$ | generalized cost of travel from $i$ to $j$ |
| $f(c_{ij})$ | deterrence function |
| $A_i$, $B_j$; $a_i$, $b_j$ | balancing factors; $a_i = A_iO_i$, $b_j = B_jD_j$ |
| $\tau$, $\tau_i$, $\Gamma_j$ | overall, origin-specific, and destination-specific growth factors |
| $T_{ij}^{(m)}$ | matrix after iteration $m$ of a growth-factor method |
| $\psi_{ij}^{(m)}$, $\epsilon$ | growth function of a cell and stopping tolerance of the iterative methods |
| $G^{(m)}$; $L_i^{O(m)}$, $L_j^{D(m)}$ | overall growth (Detroit); origin and destination location factors (Fratar) |
| $k = 1, \ldots, K$ | cost bins; $\delta_{ijk} = 1$ if $c_{ij}$ falls in bin $k$ |
| $F_k$, $S_k$ | separation factor and observed number of trips of bin $k$ |

Lower-case letters denote observations, upper-case letters the quantities
being modeled.

## The trip matrix and its constraints

The **trip matrix** $[T_{ij}]_{z\times z}$ holds the trips from each origin
to each destination in a period (an O-D matrix) or, over a day, from
production to attraction zones (a P–A matrix). It can be disaggregated by
person type $n$ and mode $k$, $T_{ij} = \sum_{n}\sum_{k} T_{ij}^{nk}$. Its
row and column sums must equal the trip ends,

$$
\begin{aligned}
\sum_{j} T_{ij} &= O_i \quad (i = 1, \ldots, z), \\
\sum_{i} T_{ij} &= D_j \quad (j = 1, \ldots, z),
\end{aligned}
$$ (eq-10-td-balance)

which requires $\sum_i O_i = \sum_j D_j = T$
({doc}`09-trip-generation` balances them). A model that satisfies both sets of
constraints is **doubly constrained**; one that satisfies only the origin
(production) constraints or only the destination (attraction) constraints is
**singly constrained**. Work trips, whose attractions (jobs) are well known,
are usually modeled with doubly constrained models; shopping, social, and
recreational trips, whose attractions are uncertain, with origin-constrained
models.

### Generalized cost

The cost of travel combines the attributes that deter a trip, weighted by
their perceived importance:

$$
\begin{aligned}
c_{ij} ={}& a_1 t_{ij}^{v} + a_2 t_{ij}^{w} + a_3 t_{ij}^{t} + a_4 t_{ij}^{n} \\
          & + a_5 F_{ij} + a_6 \phi_j + \delta ,
\end{aligned}
$$ (eq-10-generalized-cost)

where $t^{v}$ is the in-vehicle time, $t^{w}$ the walking time to and from
stops or parking, $t^{t}$ the waiting (or parking search) time, $t^{n}$ the
interchange time, $F_{ij}$ the fare or vehicle operating cost including
tolls, $\phi_j$ the terminal (parking) cost, and $\delta$ a modal penalty
for unmeasured attributes such as comfort and safety. If cost is measured in
money ($a_5 = 1$), $a_1$ is the **value of in-vehicle time**; walking and
waiting time are typically valued at two to three times $a_1$.

## Growth-factor methods

Let $[t_{ij}]$ be a base-year matrix (from a recent survey or a previous
study), with $o_i = \sum_j t_{ij}$, $d_j = \sum_i t_{ij}$, and
$t = \sum_{ij} t_{ij}$. Growth-factor methods multiply each cell by a
factor that reflects the growth of trips at its two ends. They differ in
how much is known about the future and in how the factors are combined.

### Uniform growth factor method

If only the total future trips $T$ are known, every cell grows at the same
rate:

$$
\begin{aligned}
T_{ij} &= \tau\, t_{ij}, \\
\tau &= \frac{T}{t} .
\end{aligned}
$$ (eq-10-uniform-growth)

The method is also called the **constant growth factor** method. It ignores
the different growth of different zones, so the future row and column
totals are almost never right.

### Singly constrained growth factor method

If the future trips originating in each zone are known, each row is scaled
by its own factor:

$$
\begin{aligned}
T_{ij} &= \tau_i\, t_{ij}, \\
\tau_i &= \frac{O_i}{o_i} \\
&= \frac{O_i}{\sum_j t_{ij}} .
\end{aligned}
$$ (eq-10-origin-growth)

Destination-specific factors $\Gamma_j = D_j/d_j$ scale columns in the same
way. The other set of totals is then not respected
({prf:ref}`ex-25-td-singly-growth`).

### Doubly constrained growth: iterative methods

When both $O_i$ and $D_j$ are known, no single scaling of the cells can
satisfy both sets of totals. The classical methods therefore iterate. Start
from $T_{ij}^{(0)} = t_{ij}$ and, at iteration $m = 0, 1, 2, \ldots$,
compute the current totals and growth factors

$$
\begin{aligned}
O_i^{(m)} &= \sum_j T_{ij}^{(m)}, \\
D_j^{(m)} &= \sum_i T_{ij}^{(m)}, \\
\tau_i^{(m)} &= \frac{O_i}{O_i^{(m)}}, \\
\Gamma_j^{(m)} &= \frac{D_j}{D_j^{(m)}},
\end{aligned}
$$

and update every cell with a growth function $\psi$ of the two factors:

$$
\begin{aligned}
T_{ij}^{(m+1)} &= T_{ij}^{(m)}\, \psi_{ij}^{(m)}, \\
\psi_{ij}^{(m)} &= \psi\!\left(\tau_i^{(m)}, \Gamma_j^{(m)}\right) .
\end{aligned}
$$ (eq-10-growth-iteration)

The iterations stop when every factor is close to one,
$\lvert\tau_i^{(m)} - 1\rvert \le \epsilon$ and
$\lvert\Gamma_j^{(m)} - 1\rvert \le \epsilon$. Textbook examples often use
$\epsilon = 0.03$; a tolerance of $10^{-3}$ or smaller is advisable when
the result is used further. The methods differ only in the growth
function.

**Average growth factor method.** Each cell grows by the average of the
factors of its two ends:

$$
\psi_{ij}^{(m)} = \frac{\tau_i^{(m)} + \Gamma_j^{(m)}}{2} .
$$ (eq-10-average-growth)

The method is simple, but averaging satisfies neither constraint, so it
converges slowly, and the matrix it converges to has no particular
optimality property.

**Detroit method.** Developed for the Detroit Metropolitan Area Traffic
Study (Carroll, 1957), it makes each cell grow with the product of the two
end factors, divided by the overall growth so that the total is not
counted twice:

$$
\begin{aligned}
\psi_{ij}^{(m)} &= \frac{\tau_i^{(m)}\, \Gamma_j^{(m)}}{G^{(m)}}, \\
G^{(m)} &= \frac{T}{\sum_{ij} T_{ij}^{(m)}} .
\end{aligned}
$$ (eq-10-detroit)

**Fratar method.** Fratar (1954) argued that the trips of zone $i$ should
be shared among destinations in proportion to the growth of each
destination. Distributing the growth of row $i$ with weights $\Gamma_j$
alone would change the row total, so each end is corrected by a
**location factor**, and the two corrections are averaged:

$$
\begin{aligned}
\psi_{ij}^{(m)} &= \tau_i^{(m)}\, \Gamma_j^{(m)}\, \frac{L_i^{O(m)} + L_j^{D(m)}}{2}, \\
L_i^{O(m)} &= \frac{O_i^{(m)}}{\sum_{j'} T_{ij'}^{(m)}\,\Gamma_{j'}^{(m)}}, \\
L_j^{D(m)} &= \frac{D_j^{(m)}}{\sum_{i'} T_{i'j}^{(m)}\,\tau_{i'}^{(m)}} .
\end{aligned}
$$ (eq-10-fratar)

With $L_i^{O}$ alone, the row totals would be met exactly after one step;
with $L_j^{D}$ alone, the column totals. The average is a compromise that usually
converges in a few iterations.

**Furness method.** Furness (1965) avoided the compromise altogether by
alternating: in one half-step every row is scaled by $\tau_i$, which meets
the row totals exactly; in the next every column is scaled by $\Gamma_j$,
which meets the column totals. The limit has the form

$$
\begin{aligned}
T_{ij} &= a_i\, b_j\, t_{ij}, \\
\sum_j T_{ij} &= O_i, \\
\sum_i T_{ij} &= D_j .
\end{aligned}
$$ (eq-10-biproportional)

This is the **bi-proportional problem** of {doc}`04-biproportional-fitting`
(the method is also known as iterative proportional fitting or the RAS
method). It is the only one of these methods with a convergence proof
and a clear optimality property: by entropy maximization, its result is
the most probable matrix given the base-year pattern and the new trip
ends ({prf:ref}`ex-25-td-furness`, {prf:ref}`ex-25-hw2-q1`).

**Comparison.** On the three-zone example of
{prf:ref}`ex-25-td-growth-methods`, with $\epsilon = 10^{-3}$, the average
method needs 8 iterations, the Detroit method 9, the Fratar method 3, and
the Furness method 5; the four final matrices agree to within about 1 %.
The average, Detroit, and Fratar methods are mainly of historical
interest, but they still appear in many textbooks and examinations; in
practice the Furness method is the standard.

**Limitations.** Growth-factor methods are simple, use the observed pattern
directly, and preserve it as far as the new trip ends allow. That is also
their limitation: they are reasonable only for short horizons with stable
costs; they need an expensive base-year matrix and inherit its errors
(cells that were not observed stay empty); and they cannot respond to
changes in travel costs, new links, new modes, pricing, or new zones.

## Gravity models

### From Newton's law to deterrence functions

Gravity models synthesize the matrix without a base-year pattern. The
original analogy with Newton's law,

$$
T_{ij} = \alpha\,\frac{P_i P_j}{d_{ij}^2},
$$

with $P_i$, $P_j$ the zone populations and $d_{ij}$ the distance, was
generalized to

$$
T_{ij} = \alpha\, O_i\, D_j\, f(c_{ij}),
$$ (eq-10-gravity-basic)

where the **deterrence function** $f$ decreases with the generalized cost.
Common forms are

$$
\begin{aligned}
f(c) &= e^{-\beta c} \ \ \text{(exponential)}, \\
f(c) &= c^{-n} \ \ \text{(power)}, \\
f(c) &= c^{\,n} e^{-\beta c} \ \ \text{(combined)},
\end{aligned}
$$

with $\beta, n > 0$, and the **stepwise** function

$$
f(c_{ij}) = \sum_{k=1}^{K} F_k\,\delta_{ijk},
$$ (eq-10-stepwise-deterrence)

where the costs are divided into $K$ bins, $\delta_{ijk} = 1$ if $c_{ij}$
lies in bin $k$ and 0 otherwise, and $F_k$ is the **separation factor** of
bin $k$. The exponential function suits short urban trips; the combined
function, which first rises and then falls, reproduces the scarcity of very
short trips in longer-distance travel.

### Singly and doubly constrained gravity models

Replacing the single constant $\alpha$ by sets of balancing factors makes
the model satisfy the balance constraints:

$$
\begin{aligned}
T_{ij} &= A_i\, O_i\, B_j\, D_j\, f(c_{ij}) \\
&= a_i\, b_j\, f(c_{ij}) .
\end{aligned}
$$ (eq-10-gravity)

**Origin-constrained** ($B_j = 1$). Summing over $j$ and imposing
$\sum_j T_{ij} = O_i$ gives

$$
\begin{aligned}
A_i &= \frac{1}{\sum_j D_j\, f(c_{ij})}, \\
T_{ij} &= O_i\,\frac{D_j f(c_{ij})}{\sum_{j'} D_{j'} f(c_{ij'})} .
\end{aligned}
$$ (eq-10-origin-constrained)

Each origin's trips are shared among destinations in proportion to their
attractiveness discounted by cost — a "destination choice" model.

**Destination-constrained** ($A_i = 1$): $B_j = 1/\sum_i O_i f(c_{ij})$.

**Doubly constrained.** Imposing both constraints gives

$$
\begin{aligned}
A_i &= \frac{1}{\sum_j B_j D_j f(c_{ij})}, \\
B_j &= \frac{1}{\sum_i A_i O_i f(c_{ij})} .
\end{aligned}
$$ (eq-10-doubly-constrained)

The factors depend on each other and are found iteratively. With
$a_i = A_iO_i$ and $b_j = B_jD_j$, the model is exactly the bi-proportional
problem {eq}`eq-10-biproportional` with the "seed" matrix $[f(c_{ij})]$ in place
of $[t_{ij}]$, so the Furness method applies unchanged
({prf:ref}`ex-25-td-gravity`). Scaling the seed matrix by
$\tau = \sum_i O_i / \sum_{ij} f(c_{ij})$ before the first iteration only
changes the starting point.

## Entropy maximization and the distribution models

The growth-factor and gravity models look like two separate recipes.
Entropy maximization (Wilson, 1967; {doc}`04-biproportional-fitting`)
shows that they follow from one principle: choose the **most probable** trip matrix — the
one that can be realized by the largest number of assignments of
individual trips to zone pairs — subject to what is known about the trips.
Each piece of knowledge, written as a linear constraint, adds one factor to
the model.

### Trip ends only

Maximizing the entropy {eq}`eq-04-entropy` subject to the balance constraints
{eq}`eq-10-td-balance` gives $T_{ij} = a_ib_j$ and hence $T_{ij} = O_iD_j/T$:
without cost information, every origin sends its trips to destinations in
proportion to their attractions ({prf:ref}`ex-20-bp-entropy`). This is a
gravity model with constant deterrence.

### With a base-year matrix: the growth-factor model

If a base-year matrix $\{t_{ij}\}$ provides prior probabilities, the most
probable matrix minimizes the information distance {eq}`eq-04-bp-information`
subject to the new trip ends, and by {prf:ref}`thm-04-bp-information`

$$
\begin{aligned}
T_{ij} &= A_i O_i B_j D_j\, t_{ij} \\
&= a_i b_j t_{ij},
\end{aligned}
$$ (eq-10-entropy-growth)

the **doubly constrained growth-factor model**: the Furness method finds the
matrix closest to the base-year matrix, in the information sense, that
satisfies the new trip ends.

### With a cost constraint: the exponential gravity model

Suppose the total expenditure on travel, $C = \sum_{ij} T_{ij}c_{ij}$, is
also known (or, equivalently, the mean trip cost $C/T$). Adding this
constraint to the entropy problem, with multiplier $\beta$, stationarity
gives

$$
\frac{\partial\mathcal{L}}{\partial T_{ij}} = -\ln T_{ij} - \lambda_i - \mu_j - \beta\, c_{ij},
$$

which is zero at the optimum, so

$$
T_{ij} = A_i O_i B_j D_j \exp(-\beta\, c_{ij}),
$$ (eq-10-entropy-gravity)

the doubly constrained gravity model with an **exponential** deterrence
function. The multipliers of the balance constraints are the logarithms of
the balancing factors, and the deterrence parameter $\beta$ is the
multiplier of the cost constraint: it is chosen so that the model
reproduces the observed mean trip cost, which is the calibration rule
below. A larger $\beta$ means shorter trips.

### Other deterrence functions

The form of the deterrence function follows from the form of the cost
constraint:

- a constraint on $\sum_{ij} T_{ij}\ln c_{ij}$, with multiplier $n$,
  gives the **power** function $T_{ij} = A_iO_iB_jD_j\, c_{ij}^{-n}$;
- constraints on both $\sum T_{ij}c_{ij}$ and $\sum T_{ij}\ln c_{ij}$ give
  the **combined** function $c_{ij}^{\,n}e^{-\beta c_{ij}}$, where $-n$ is
  the multiplier of the second constraint; and
- one constraint per cost bin on the number of trips,
  $\sum_{ij} T_{ij}\delta_{ijk} = S_k$ with multiplier $\beta_k$, gives

  $$
  \begin{aligned}
  T_{ij} &= A_iO_iB_jD_j \sum_k e^{-\beta_k}\delta_{ijk} \\
  &= a_i b_j \sum_k F_k \delta_{ijk},
  \end{aligned}
  $$

  the **stepwise** model {eq}`eq-10-stepwise-deterrence` with
  $F_k = e^{-\beta_k}$, whose calibration is a tri-proportional problem.

The **competing destinations** model of Fotheringham (1983) adds a
constraint on $\sum T_{ij}\ln S_{ij}$, where $S_{ij}$ measures the
accessibility of destination $j$ to other destinations, giving
$T_{ij} = A_iO_iB_jD_j\,S_{ij}^{\rho}\exp(-\beta c_{ij})$.

The objective is strictly convex and the constraints are linear, so each of
these problems has at most one solution ({prf:ref}`thm-03-convex-program`):
the balancing algorithms that compute the models have unique limits.

### Interpretation and limits

Entropy maximization does not claim that travelers choose destinations at
random. It provides the *least biased* estimate of the matrix given the
information used as constraints: any structure in the result comes from the
constraints, not from hidden assumptions. Its behavioral counterpart is the
destination-choice logit model of {doc}`11-discrete-choice-models`: an
origin-constrained gravity model with exponential deterrence has the same
form as a multinomial logit model of destination choice with utility
$\ln D_j - \beta c_{ij}$.

## Calibration and validation

Before a gravity model can be used, its parameters ($\beta$, $n$, or the
$F_k$) must be **calibrated** so that the model reproduces the base-year
pattern as well as its functional form allows. **Validation** is a
different task: checking that the calibrated model can reproduce a known
state of the system not used in calibration, with an accuracy suited to the
decisions it will support.

### Trip length distribution

The natural calibration target is the observed **trip length (cost)
distribution** (TLD): the number of trips $S_k$ whose cost falls in each bin
$k$, obtained from a survey. For an exponential deterrence function, a
convenient target is the mean trip cost: $\beta$ is adjusted until the
modeled mean $\sum_{ij}T_{ij}c_{ij}/T$ equals the observed one, the
condition that defines $\beta$ in the entropy derivation
{eq}`eq-10-entropy-gravity`.

### Calibrating a stepwise deterrence function

With the stepwise function {eq}`eq-10-stepwise-deterrence`, calibration means
finding $a_i$, $b_j$, and $F_k$ such that the model meets the trip ends
and reproduces the observed number of trips $S_k$ in every cost bin. This
is the tri-proportional problem {eq}`eq-04-tri-proportional` of
{doc}`04-biproportional-fitting`, with a seed of ones and the cost bins as
the groups of cells; it is solved by {prf:ref}`alg-04-triprop`. The estimated
$F_k$ trace the shape of the deterrence function without assuming a
functional form, and a smooth function can then be fitted to them. As in
every tri-proportional problem, one factor (say $F_1 = 1$) is fixed, and
the trip ends and the trip length distribution must be mutually consistent,
or the algorithm cannot converge ({prf:ref}`ex-25-td-tri-proportional`).

### Partial matrices

Survey data rarely cover every cell: roadside interviews observe only the
movements that pass the survey sites. The calibration is then carried out
on the **observed cells only**, with the trip ends and TLD computed from
those cells, and the fitted model fills the missing cells:
$\hat{T}_{ij} = a_i b_j \sum_k F_k \delta_{ijk}$ for unobserved $ij$
({prf:ref}`ex-25-hw2-q2`). Equivalently, for a growth-factor model, the
balancing is done with unobserved cells set to zero, and missing cells are
estimated from the resulting factors.

## Practical considerations

External zones
: Trips with one or both ends outside the study area do not have meaningful
  costs within the model. They are usually taken from cordon roadside
  interviews and forecast with growth-factor (Furness) methods rather than
  gravity models.

Intra-zonal trips
: The cost of a trip within a zone is poorly represented by centroid
  connectors. Intra-zonal trips are better removed from the synthetic model
  and forecast as a fixed share of the zone's trip ends.

Trip purposes
: Separate models are estimated for different purposes and person types,
  with different deterrence parameters: purposes differ in their sensitivity
  to cost.

$K$-factors
: Special associations between zones (for example a company town) can be
  represented by zone-pair adjustment factors,
  $T_{ij} = K_{ij} A_i O_i B_j D_j f(c_{ij})$. They improve the fit in the
  base year but have no behavioral basis and their future values are
  unknown; they should be avoided, or limited to a very small share of
  zone pairs with a clearly identified reason.

## Summary and Common Mistakes

### Summary

- Trip matrices must match the trip ends {eq}`eq-10-td-balance`; doubly
  constrained models satisfy both rows and columns, which requires
  $\sum_i O_i = \sum_j D_j$.
- Generalized cost {eq}`eq-10-generalized-cost` combines times and money
  costs weighted by their perceived importance.
- Growth-factor methods scale an observed matrix: uniformly
  {eq}`eq-10-uniform-growth`, by row {eq}`eq-10-origin-growth`, or, with both
  trip ends known, iteratively {eq}`eq-10-growth-iteration` with the average
  {eq}`eq-10-average-growth`, Detroit {eq}`eq-10-detroit`, Fratar
  {eq}`eq-10-fratar`, or Furness {eq}`eq-10-biproportional` growth function;
  only the Furness method has a convergence proof and an optimality
  property.
- Gravity models {eq}`eq-10-gravity` synthesize the matrix from trip ends
  and costs; the origin-constrained version {eq}`eq-10-origin-constrained` is
  a destination-choice model, and the doubly constrained version
  {eq}`eq-10-doubly-constrained` is the bi-proportional problem with seed
  $f(c_{ij})$.
- Entropy maximization derives the growth-factor model
  {eq}`eq-10-entropy-growth` (with a base-year matrix) and the gravity model
  {eq}`eq-10-entropy-gravity` (with a cost constraint); the multiplier of the
  cost constraint is the deterrence parameter.
- Calibration fits the deterrence function to the observed trip length
  distribution; the tri-proportional method estimates a stepwise function
  {eq}`eq-10-stepwise-deterrence` and handles partial matrices.

### Common mistakes

- **Running a doubly constrained method with $\sum_i O_i \ne \sum_j D_j$.**
  No matrix satisfies both sets of constraints, and the iterations
  oscillate; balance the trip ends first ({doc}`09-trip-generation`).
- **Averaging growth factors and stopping after one iteration.** Neither
  set of totals is then met; iterate until all factors are close to one.
- **Comparing gravity models by the fit of the trip-end totals.** Every
  balanced model reproduces them exactly; compare the trip length
  distribution and individual cells.
- **Stopping a balancing algorithm with a loose tolerance.** A tolerance
  such as 5 % can leave totals several percent off target; use $10^{-3}$ or
  smaller and check the totals of the reported matrix.
- **Treating the separation factors $F_k$ as costs.** They are relative
  propensities to travel in each cost bin and are defined only up to scale.
- **Constraining the *cost* within each bin when deriving the stepwise
  model.** The stepwise model follows from constraints on the *number of
  trips* in each bin.

## References

- Ortúzar, J. de D., & Willumsen, L. G. (2011). *Modelling Transport* (4th
  ed.), Chapter 5 (Trip distribution modelling). Wiley.
  <https://doi.org/10.1002/9781119993308>
- Fratar, T. J. (1954). Vehicular trip distribution by successive
  approximations. *Traffic Quarterly*, *8*(1), 53–65.
- Carroll, J. D., Jr. (1957). Future traffic predictions for the Detroit
  area. *Highway Research Board Proceedings*, 36.
- Furness, K. P. (1965). Time function iteration. *Traffic Engineering and
  Control*, 7(7), 458–460.
- Wilson, A. G. (1967). A statistical theory of spatial distribution
  models. *Transportation Research*, *1*(3), 253–269.
  <https://doi.org/10.1016/0041-1647(67)90035-4>
- Wilson, A. G. (1970). *Entropy in Urban and Regional Modelling*. Pion.
- Evans, A. W. (1970). Some properties of trip distribution methods.
  *Transportation Research*, *4*(1), 19–36.
  <https://doi.org/10.1016/0041-1647(70)90072-9>
- Fotheringham, A. S. (1983). A new set of spatial-interaction models: the
  theory of competing destinations. *Environment and Planning A*, *15*(1),
  15–36. <https://doi.org/10.1068/a150015>
