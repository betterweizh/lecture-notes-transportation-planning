# Matrix Balancing: Bi-proportional Fitting

## Overview

A recurring task in modeling is to adjust a non-negative matrix so that its
row and column totals match known targets while keeping as much of its
internal structure as possible. An old trip matrix must be updated to new
trip-end totals; a cross-tabulation from a sample must be expanded to known
population margins; a matrix of deterrence values must be scaled so that
it produces the right numbers of trips from every origin and to every
destination. The standard solution multiplies every row by one factor and
every column by another, and finds the factors by alternately scaling rows
and columns. The method was discovered independently in several fields:
statisticians call it **iterative proportional fitting** (Deming &
Stephan, 1940), economists the **RAS method** for updating input–output
tables (Stone & Brown, 1962; Bacharach, 1970), mathematicians **matrix scaling**
(Sinkhorn, 1964), and transport planners the **Furness method** (Furness,
1965). This chapter states the problem and the two standard algorithms and
gives the conditions for convergence. It then explains *why* the method is
the right one: by the entropy-maximizing argument, the balanced matrix is
the most probable matrix consistent with the margins, which is the same as
the matrix closest to the seed in the sense of information distance. The
chapter ends with the tri-proportional extension, which adds totals for
groups of cells.

:::{admonition} Learning objectives
:class: objectives
After completing this chapter, readers should be able to:

- state the bi-proportional (matrix balancing) problem and the
  consistency condition on its targets;
- apply bi-proportional algorithms I (matrix scaling) and II (factor
  updating) with an appropriate stopping criterion;
- explain when the iterations converge, and what happens when the targets
  are inconsistent or incompatible with the zero cells of the seed;
- define micro-, meso-, and macro-states and the entropy of a matrix, and
  derive the most probable matrix subject to linear constraints;
- show that the balanced matrix minimizes the Kullback–Leibler divergence
  from the seed subject to the margins;
- extend the method to tri-proportional fitting with group totals; and
- recognize the bi-proportional problem in the models of the later parts of
  the book.
:::

## Notation

| Symbol | Meaning |
|---|---|
| $t_{ij} \ge 0$ | seed (prior) matrix, $i = 1, \ldots, m$, $j = 1, \ldots, n$ |
| $T_{ij}$ | balanced matrix |
| $O_i$, $D_j$ | row and column targets |
| $a_i$, $b_j$ | row and column balancing factors |
| $r$, $\epsilon$ | iteration counter and stopping tolerance |
| $I(\bT, \bt)$ | information (Kullback–Leibler) distance of $\bT$ from $\bt$ |
| $N$ | total of the matrix (number of units allocated to the cells) |
| $W\{T_{ij}\}$ | number of micro-states that produce the matrix $\{T_{ij}\}$ |
| $k = 1, \ldots, K$ | groups of cells; $\delta_{ijk} = 1$ if cell $ij$ belongs to group $k$ |
| $S_k$, $F_k$ | target total and balancing factor of group $k$ |

## The bi-proportional problem

Given a non-negative **seed** matrix $\bt = [t_{ij}]$ and positive
row and column targets $O_i$ and $D_j$, find factors $a_i$ and $b_j$ such
that

$$
\begin{aligned}
T_{ij} &= a_i\,b_j\,t_{ij}, \\
\sum_{j} T_{ij} &= O_i, \qquad i = 1, \ldots, m, \\
\sum_{i} T_{ij} &= D_j, \qquad j = 1, \ldots, n .
\end{aligned}
$$ (eq-04-matrix-balancing)

The balanced matrix keeps the **cross-product ratios** of the seed: for any
two rows $i, k$ and columns $j, l$,

$$
\frac{T_{ij}T_{kl}}{T_{il}T_{kj}} = \frac{t_{ij}t_{kl}}{t_{il}t_{kj}},
$$

because the factors cancel. The pattern of association in the seed is
preserved, and only the margins change. A cell that is zero in the seed
stays zero.

Summing the row targets and the column targets both give the total of the
matrix, so a solution can exist only if the targets are **consistent**:

$$
\sum_i O_i = \sum_j D_j .
$$ (eq-04-bp-consistency)

When the targets come from different sources and do not add up, they are
usually rescaled to a common total before balancing, for example the
average of the two sums or the total of the more reliable source.

Imposing the row and column constraints on $T_{ij} = a_ib_jt_{ij}$ gives two
coupled sets of equations for the factors:

$$
\begin{aligned}
a_i &= \frac{O_i}{\sum_j b_j\, t_{ij}}, \\
b_j &= \frac{D_j}{\sum_i a_i\, t_{ij}} .
\end{aligned}
$$ (eq-04-bp-factors)

The factors are determined only up to a common scale: replacing $a_i$ by
$ca_i$ and $b_j$ by $b_j/c$ leaves every $T_{ij}$ unchanged. Only the
products $a_ib_j$ are meaningful.

## The algorithms

Equations {eq}`eq-04-bp-factors` are solved by fixed-point iteration: satisfy
the row targets, then the column targets, and repeat. The iteration can be
written on the matrix itself or on the factors.

:::{prf:algorithm} Bi-proportional algorithm I (matrix scaling)
:label: alg-04-biprop-1

1. Set $T_{ij}^{(0)} = t_{ij}$ and $r = 1$.
2. **Row step:**
   $T_{ij}' = T_{ij}^{(r-1)}\, O_i \big/ \sum_{l} T_{il}^{(r-1)}$ for all
   $i, j$.
3. **Column step:**
   $T_{ij}^{(r)} = T_{ij}'\, D_j \big/ \sum_{k} T_{kj}'$ for all $i, j$.
4. Stop if
   $\lvert\sum_j T_{ij}^{(r)} - O_i\rvert / O_i \le \epsilon$ for all $i$
   (the column totals are exact after step 3); otherwise set
   $r \leftarrow r + 1$ and return to step 2.
:::

:::{prf:algorithm} Bi-proportional algorithm II (factor updating)
:label: alg-04-biprop-2

1. Set $b_j^{(0)} = 1$ for all $j$ and $r = 1$.
2. $a_i^{(r)} = O_i \big/ \sum_j b_j^{(r-1)} t_{ij}$ for all $i$.
3. $b_j^{(r)} = D_j \big/ \sum_i a_i^{(r)} t_{ij}$ for all $j$.
4. Stop if
   $\lvert b_j^{(r)} - b_j^{(r-1)}\rvert / b_j^{(r)} \le \epsilon$ for all
   $j$ (equivalently, the row totals are within tolerance); otherwise set
   $r \leftarrow r + 1$ and return to step 2.
5. Output $T_{ij} = a_i^{(r)} b_j^{(r)} t_{ij}$.
:::

The two algorithms produce the same sequence of matrices. Algorithm II
stores only $m + n$ factors instead of $mn$ cells, which matters for large
matrices, and it delivers the factors themselves, which some models need
(for example the balancing factors of the gravity model in
{doc}`10-trip-distribution`). A combined relative-change criterion,

$$
\frac{\lVert \ba^{(r)} - \ba^{(r-1)}\rVert}{\sum_i a_i^{(r)}}
+ \frac{\lVert \bb^{(r)} - \bb^{(r-1)}\rVert}{\sum_j b_j^{(r)}}
\le \epsilon,
$$

can also be used. The tolerance should be small, say $10^{-4}$ or less in
relative terms: a loose tolerance such as 5 % may stop the algorithm far
from the solution. Convergence is usually fast — a few iterations for a
well-behaved seed ({prf:ref}`ex-20-bp-ras`) — but becomes slow when the
targets differ strongly from the seed margins or the seed has many zeros.

## Existence, uniqueness, and convergence

A balanced matrix exists if the targets are consistent and some matrix with
the same pattern of zero cells as the seed has the required margins. When
the seed is strictly positive and the targets are consistent, this is always
the case. Under this condition the iterations converge, and the limit
$\bT$ is unique.

If no matrix with the zero pattern of the seed can meet the targets, the
iterations do not converge: the row step and the column step keep
undoing each other, and the cells that would have to be zero shrink towards
zero while the other cells oscillate ({prf:ref}`ex-20-bp-infeasible`). A
balancing run that fails to converge is therefore a diagnostic: the targets
are inconsistent with each other or with the structure of the seed.

## Entropy maximization

Why scale rows and columns, rather than adjust the cells in some other way?
The entropy-maximizing argument of Wilson (1967, 1970) gives the answer: the
balanced matrix is the **most probable** matrix that is consistent with the
known totals. The argument applies to any matrix of counts — trips between
zones, persons cross-classified by two attributes, money flowing between
sectors — so it is stated here in general terms.

### Micro-, meso-, and macro-states

Consider $N$ distinguishable units (trips, persons, transactions), each of
which falls in one cell $ij$ of a matrix.

- A **micro-state** specifies the cell of each individual unit.
- A **meso-state** specifies only how many units fall in each cell — the
  matrix $\{T_{ij}\}$.
- A **macro-state** specifies aggregate quantities such as the row and
  column totals $O_i$ and $D_j$, or other linear functions of the cells.

What is known, or can be forecast, is usually a macro-state. Many
meso-states are consistent with it, and each meso-state can be realized by
many micro-states. The number of micro-states that produce the meso-state
$\{T_{ij}\}$ is the multinomial coefficient

$$
W\{T_{ij}\} = \frac{N!}{\prod_{i}\prod_{j} T_{ij}!} .
$$ (eq-04-microstates)

For example, four units that can fall in two cells H and W can be split as
(4H, 0W), (3H, 1W), (2H, 2W), (1H, 3W), or (0H, 4W), realized by $1$, $4$,
$6$, $4$, and $1$ of the $2^4 = 16$ micro-states. If all micro-states are
equally likely, the even split is the most probable meso-state, and as $N$
grows the distribution of $W$ concentrates ever more sharply around its
maximum ({prf:ref}`ex-20-bp-entropy`). The **entropy-maximizing** principle
therefore takes as estimate the meso-state that can be realized in the
largest number of ways, subject to the known macro-state.

### The entropy function

Maximizing $W$ is equivalent to maximizing $\ln W$. With Stirling's
approximation $\ln x! \approx x\ln x - x$, and dropping the constant
$\ln N!$,

$$
\ln W' = -\sum_{i}\sum_{j}\left(T_{ij}\ln T_{ij} - T_{ij}\right),
$$ (eq-04-entropy)

which is strictly concave in $\{T_{ij}\}$. (The term $\sum T_{ij} = N$ is
constant but is kept because it simplifies the derivatives:
$\partial \ln W'/\partial T_{ij} = -\ln T_{ij}$.) The approximation is
asymptotic: it requires large cell counts.

### The most probable matrix with given margins

Maximize {eq}`eq-04-entropy` subject to the row and column totals, with
multipliers $\lambda_i$ and $\mu_j$:

$$
\begin{aligned}
\max_{T_{ij} \ge 0}\quad & -\sum_{i}\sum_{j}\left(T_{ij}\ln T_{ij} - T_{ij}\right) \\
\text{s.t.}\quad & \sum_j T_{ij} = O_i, \\
& \sum_i T_{ij} = D_j .
\end{aligned}
$$

Stationarity of the Lagrangian gives

$$
\begin{aligned}
-\ln T_{ij} - \lambda_i - \mu_j &= 0 \\
\Longrightarrow\quad T_{ij} &= e^{-\lambda_i}\, e^{-\mu_j} \\
&= a_i\, b_j .
\end{aligned}
$$

The logarithm forces $T_{ij} > 0$, so the non-negativity constraints are
not binding, and the multipliers are the logarithms of the balancing
factors. Imposing the margins gives $T_{ij} = O_iD_j/N$: without further
information, the most probable matrix is the **independence** matrix, in
which every row is distributed in proportion to the column totals.

### Prior information and information distance

Usually a seed matrix $\{t_{ij}\}$ is available — an earlier observation of
the same matrix, or a matrix built from a model. If each unit falls in cell
$ij$ with prior probability $t_{ij}/t$, where $t = \sum_{ij} t_{ij}$, the
probability of a meso-state is the multinomial probability
$W\{T_{ij}\}\prod_{ij}(t_{ij}/t)^{T_{ij}}$. Taking logarithms and applying
Stirling's approximation, maximizing it is equivalent to **minimizing**

$$
I(\bT, \bt) = \sum_{i}\sum_{j}\left[T_{ij}\ln\frac{T_{ij}}{t_{ij}} - T_{ij} + t_{ij}\right],
$$ (eq-04-bp-information)

summed over the cells with $t_{ij} > 0$. Each term is zero when
$T_{ij} = t_{ij}$ and positive otherwise; $I$ is the (generalized)
**Kullback–Leibler divergence** (Kullback & Leibler, 1951) of $\bT$ from
$\bt$, a
measure of the information added by moving from the seed to the estimate.
Near the seed, a second-order expansion gives

$$
T_{ij}\ln\frac{T_{ij}}{t_{ij}} - T_{ij} + t_{ij}
\approx \frac{(T_{ij} - t_{ij})^2}{2\,t_{ij}},
$$

so $I$ behaves like a chi-square distance. Maximizing entropy without a
seed is the special case of a uniform seed.

Minimizing $I$ subject to the margins gives exactly the bi-proportional
matrix:

:::{prf:theorem} Bi-proportional fitting minimizes information distance
:label: thm-04-bp-information

The balanced matrix {eq}`eq-04-matrix-balancing` is the unique solution of

$$
\begin{aligned}
\min_{\bT \ge \bzero}\ & I(\bT, \bt) \\
\text{s.t.}\ & \sum_j T_{ij} = O_i, \qquad i = 1, \ldots, m, \\
& \sum_i T_{ij} = D_j, \qquad j = 1, \ldots, n .
\end{aligned}
$$ (eq-04-bp-program)
:::

:::{dropdown} Proof
:class-container: proof
:animate: fade-in

With multipliers $\lambda_i$ and $\mu_j$ for the row and column
constraints, the Lagrangian is

$$
\mathcal{L} = I(\bT, \bt)
+ \sum_i \lambda_i\Big(O_i - \sum_j T_{ij}\Big)
+ \sum_j \mu_j\Big(D_j - \sum_i T_{ij}\Big) .
$$

Setting its derivative with respect to $T_{ij}$ to zero,

$$
\ln\frac{T_{ij}}{t_{ij}} - \lambda_i - \mu_j = 0,
$$

so $T_{ij} = e^{\lambda_i}e^{\mu_j}\,t_{ij}$, which is the form
$a_ib_jt_{ij}$ with $a_i = e^{\lambda_i}$ and $b_j = e^{\mu_j}$. The
solution is positive wherever $t_{ij} > 0$, so the non-negativity
constraints are not binding. The objective is strictly convex (its Hessian
is $\diag(1/T_{ij})$) and the constraints are linear, so the
KKT conditions are sufficient and the solution is unique
({prf:ref}`thm-03-convex-program`).
:::

The algorithms of this chapter are a **coordinate ascent** on the
dual of {eq}`eq-04-bp-program`: the row step chooses the $\lambda_i$ that
satisfy the row constraints exactly with the $\mu_j$ fixed, and the column
step does the same for the $\mu_j$. Each half-step solves a strictly convex
problem exactly, which is the basis of the convergence proof (Bregman,
1967).

Thus the balanced matrix is at the same time the most probable matrix
given the seed and the margins, and the matrix closest to the seed in the
information sense. It adds no structure that the margins do not demand:
any pattern in the result comes from the seed or from the constraints.

### Additional linear constraints

The argument extends to any additional information that can be written as
a linear constraint on the cells, $\sum_{ij} g_{ij}T_{ij} = G$. Each such
constraint, with multiplier $\nu$, contributes a factor $e^{-\nu g_{ij}}$
to the solution:

$$
T_{ij} = a_i\, b_j\, t_{ij}\, e^{-\nu g_{ij}} .
$$

The objective stays strictly convex and the constraints linear, so the
solution is unique whenever the constraints are feasible
({prf:ref}`thm-03-convex-program`). Two cases are used later in the book. If
$g_{ij}$ is the cost of travel and $G$ the total expenditure, the extra
factor is an exponential deterrence function, and the result is the
gravity model of {doc}`10-trip-distribution`. If $g_{ij} = \delta_{ijk}$
indicates membership of a group of cells, one constraint per group gives
one factor per group: the tri-proportional problem of the next section.

## Tri-proportional fitting

Sometimes totals are known not only for the rows and columns but also for
**groups of cells** — for example the number of trips in each trip-length
band, which cuts across rows and columns. Let $\delta_{ijk} = 1$ if cell
$ij$ belongs to group $k$ ($k = 1, \ldots, K$), with every cell in exactly
one group, and let $S_k$ be the target total of group $k$. The
**tri-proportional problem** seeks factors $a_i$, $b_j$, and $F_k$ such that

$$
\begin{aligned}
T_{ij} &= a_i\, b_j\, t_{ij} \sum_{k} F_k\,\delta_{ijk}, \\
\sum_j T_{ij} &= O_i, \\
\sum_i T_{ij} &= D_j, \\
\sum_{i}\sum_{j} T_{ij}\,\delta_{ijk} &= S_k \quad (k = 1, \ldots, K).
\end{aligned}
$$ (eq-04-tri-proportional)

Since each cell lies in exactly one group, $\sum_k F_k\delta_{ijk}$ picks
out one factor. It is the solution of the entropy problem with the three
sets of constraints, by the previous section, and the conditions give

$$
\begin{aligned}
a_i &= \frac{O_i}{\sum_j b_j\, t_{ij} \sum_k F_k\delta_{ijk}}, \\
b_j &= \frac{D_j}{\sum_i a_i\, t_{ij} \sum_k F_k\delta_{ijk}}, \\
F_k &= \frac{S_k}{\sum_i\sum_j a_i b_j\, t_{ij}\,\delta_{ijk}} .
\end{aligned}
$$ (eq-04-tri-factors)

:::{prf:algorithm} Tri-proportional algorithm
:label: alg-04-triprop

1. Set $b_j = 1$ and $F_k = 1$ for all $j$ and $k$.
2. Update the $a_i$, then the $b_j$, then the $F_k$ with
   {eq}`eq-04-tri-factors`, each with the latest values of the others.
3. Stop when all three sets of totals are met to within the tolerance;
   otherwise return to step 2.
:::

Two practical points:

- the factors are determined only up to scale ($c\,a_i$, $d\,b_j$, and
  $F_k/(cd)$ give the same $T_{ij}$ for any $c, d > 0$), so one value, for example
  $F_1 = 1$, is fixed, or the factors are renormalized in each iteration;
  and
- the targets must be **mutually consistent**: besides
  $\sum_i O_i = \sum_j D_j = \sum_k S_k$, no group of cells may be forced
  by the row, column, and group constraints to sum to two different
  values. Otherwise no solution exists and the algorithm does not converge
  ({prf:ref}`ex-25-td-tri-proportional`).

More sets of totals are handled in the same way by adding a scaling step
for each (**multi-proportional fitting**). Two further variants are common:

- **Fixed or missing cells.** Cells whose values are known are removed from
  the problem (and their values subtracted from the targets); cells that
  are not observed are given a zero seed and estimated afterwards from the
  fitted factors ({prf:ref}`ex-25-hw2-q2`).
- **Weights for samples.** In survey weighting the same algorithm is called
  **raking**: sample weights are scaled so that weighted counts match
  known population totals for several variables at once.

## Applications in this book

The bi-proportional problem appears in many of the models that follow:

- **Growth-factor distribution.** Updating a base-year trip matrix to
  forecast trip ends is the Furness method of
  {doc}`10-trip-distribution`, with the base-year matrix as seed.
- **Gravity models.** The doubly constrained gravity model
  $T_{ij} = A_iO_iB_jD_jf(c_{ij})$ is {eq}`eq-04-matrix-balancing` with the
  deterrence matrix $[f(c_{ij})]$ as seed; algorithm II computes its
  balancing factors. Entropy maximization with a cost constraint derives
  the model, and calibration of a stepwise deterrence function is the
  tri-proportional problem with the cost bins as groups
  ({doc}`10-trip-distribution`).
- **Combined models.** The combined distribution–modal-split model is
  balanced over origins and destinations with a deterrence summed over
  modes ({doc}`12-aggregate-modal-split`), and the combined
  distribution–assignment model solves a gravity model by bi-proportional
  fitting in every iteration of Evans's algorithm
  ({doc}`14-system-optimum-and-elastic-demand`).
- **Survey weighting.** Choice-based and stratified samples are weighted to
  match known population shares ({doc}`07-travel-surveys-and-sampling`);
  when several sets of population totals must be matched at once, the
  weights are found by raking, the same algorithm.

## Summary and Common Mistakes

### Summary

- The bi-proportional problem {eq}`eq-04-matrix-balancing` seeks
  $T_{ij} = a_ib_jt_{ij}$ with given row and column totals; it requires
  consistent targets {eq}`eq-04-bp-consistency` and preserves the
  cross-product ratios of the seed.
- Algorithm I ({prf:ref}`alg-04-biprop-1`) alternately scales rows and
  columns of the matrix; algorithm II ({prf:ref}`alg-04-biprop-2`) updates
  the factors {eq}`eq-04-bp-factors`. Both converge to a unique limit when
  the targets are consistent and compatible with the zero cells.
- By entropy maximization {eq}`eq-04-entropy`, the balanced matrix is the
  most probable matrix given the seed and the margins; equivalently, it
  minimizes the Kullback–Leibler distance {eq}`eq-04-bp-information` from
  the seed ({prf:ref}`thm-04-bp-information`), and the algorithms are
  coordinate ascent on the dual.
- Every further linear constraint adds a multiplicative factor; group
  totals give the tri-proportional method {eq}`eq-04-tri-proportional`
  ({prf:ref}`alg-04-triprop`).
- The same algorithm appears in this book as the Furness method, as the
  balancing of gravity and combined models, and in survey expansion.

### Common mistakes

- **Balancing to targets whose sums differ.** The row and column totals
  cannot both be met; rescale the targets to a common total first.
- **Stopping on a loose tolerance, or checking only the margin fitted
  last.** After a column step the column totals are always exact; test the
  row totals, with a tolerance of $10^{-4}$ or less.
- **Interpreting the individual factors $a_i$ or $b_j$.** They are
  determined only up to a common scale; only their products $a_ib_j$ are
  identified.
- **Expecting a zero cell of the seed to become positive.** Bi-proportional
  fitting cannot create structure that the seed does not have.
- **Ignoring non-convergence.** It signals targets that are inconsistent
  with each other or with the zero pattern of the seed.
- **Forgetting that the entropy derivation relies on Stirling's
  approximation.** The approximation needs large cell counts; for small
  counts the most probable matrix can differ from the balanced one.

## References

- Deming, W. E., & Stephan, F. F. (1940). On a least squares adjustment of
  a sampled frequency table when the expected marginal totals are known.
  *Annals of Mathematical Statistics*, *11*(4), 427–444.
  <https://doi.org/10.1214/aoms/1177731829>
- Sinkhorn, R. (1964). A relationship between arbitrary positive matrices
  and doubly stochastic matrices. *Annals of Mathematical Statistics,
  35*(2), 876–879. <https://doi.org/10.1214/aoms/1177703591>
- Bregman, L. M. (1967). Proof of the convergence of Sheleikhovskii's
  method for a problem with transportation constraints. *USSR Computational
  Mathematics and Mathematical Physics, 7*(1), 191–204.
  <https://doi.org/10.1016/0041-5553(67)90069-9>
- Stone, R., & Brown, A. (1962). *A Computable Model of Economic Growth*.
  Chapman and Hall.
- Bacharach, M. (1970). *Biproportional Matrices and Input–Output Change*.
  Cambridge University Press.
- Kullback, S., & Leibler, R. A. (1951). On information and sufficiency.
  *Annals of Mathematical Statistics*, *22*(1), 79–86.
  <https://doi.org/10.1214/aoms/1177729694>
- Wilson, A. G. (1967). A statistical theory of spatial distribution
  models. *Transportation Research*, *1*(3), 253–269.
  <https://doi.org/10.1016/0041-1647(67)90035-4>
- Wilson, A. G. (1970). *Entropy in Urban and Regional Modelling*. Pion.
- Furness, K. P. (1965). Time function iteration. *Traffic Engineering and
  Control, 7*(7), 458–460.
- Ortúzar, J. de D., & Willumsen, L. G. (2011). *Modelling Transport* (4th
  ed.), Sections 5.2, 5.4, and 5.6. Wiley.
