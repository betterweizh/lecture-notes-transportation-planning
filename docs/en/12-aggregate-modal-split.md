# Aggregate and Combined Modal-Split Models

## Overview

{doc}`11-discrete-choice-models` modeled the mode choice of individual
travelers. This chapter covers the **aggregate** approach to modal split,
in which the share of each mode on an O-D pair is a function of zonal
averages of the travel costs. It starts from the
empirical diversion curves of early studies, derives the logit modal-split
formula from the entropy-maximizing combined distribution–modal-split
model, introduces the composite cost and hierarchical (nested) structures
that are needed for more than two modes, shows how a binary logit split is
calibrated by linear regression, and applies the model to two policy
questions: congestion pricing and bus lanes. The aggregate models use the
logit form derived for individuals in {doc}`11-discrete-choice-models`, but
apply it to the share of each mode in each cell $T_{ij}$ of the trip
matrix.

:::{admonition} Learning objectives
:class: objectives
After completing this chapter, readers should be able to:

- list the factors that influence mode choice and distinguish aggregate
  from disaggregate models;
- derive the combined trip distribution and modal-split model from entropy
  maximization and explain the double role of its parameter;
- define the composite cost of a set of modes and show why the log-sum, not
  the weighted average, is the correct definition;
- explain the red-bus/blue-bus problem and the hierarchical (nested)
  structure that solves it;
- calibrate a binary logit split with a modal penalty by linear regression;
  and
- use an aggregate logit split together with congestion functions to
  evaluate congestion pricing and bus-lane schemes.
:::

## Notation

| Symbol | Meaning |
|---|---|
| $k$, $m$ | modes |
| $n$ | person type (e.g., with or without access to a car) |
| $T_{ij}^k$ | trips from $i$ to $j$ by mode $k$; $T_{ij} = \sum_k T_{ij}^k$ |
| $P_{ij}^k = T_{ij}^k/T_{ij}$ | share of mode $k$ on pair $ij$ |
| $C_{ij}^k$ | generalized cost from $i$ to $j$ by mode $k$ |
| $K_{ij}$ | composite cost of all modes from $i$ to $j$ |
| $\beta$ | dispersion parameter of destination choice; also of a single binary split (diversion curve, policy applications) |
| $\lambda$ | dispersion parameter of mode choice |
| $\delta$ | modal penalty (constant) of a mode |
| $A_i$, $B_j$ | balancing factors of the gravity model |

## Factors influencing mode choice

Three groups of factors determine which mode a traveler uses.

Characteristics of the traveler
: car availability and ownership, possession of a driving license,
  household structure (young couple, family with children, retired,
  single), obligations decided elsewhere (a car needed at work, children
  to escort), income, and residential density.

Characteristics of the trip
: purpose (work trips, being regular, are easier to make by public transport
  than shopping or social trips), time of day (late trips are harder to
  serve by public transport), and whether the trip is part of a chain of
  trips.

Characteristics of the modes
: quantitative factors — in-vehicle time, waiting and walking time, fares,
  fuel and parking costs, parking availability — and qualitative ones —
  comfort, convenience, reliability, regularity, and security.

The time and money components are combined into a **generalized cost**

$$
C_{ij}^k = a_1 t_{ij}^{k,\mathrm{iv}} + a_2 t_{ij}^{k,\mathrm{wait}}
         + a_3 t_{ij}^{k,\mathrm{walk}} + a_4 F_{ij}^k + \cdots + \delta^k ,
$$ (eq-12-generalized-cost-mode)

where the weights $a_\ell$ convert each component into common units (money
via the value of time, or time via its inverse) and the **modal penalty**
$\delta^k$ captures the effect of attributes not included explicitly, such
as comfort. Waiting and walking time are usually weighted about twice as
heavily as in-vehicle time.

**Aggregate** models predict the *share* of each mode on an O-D pair from
zonal averages of these variables; **disaggregate** models predict the
*probability* that an individual chooses each mode from that individual's
own data ({doc}`11-discrete-choice-models`).

## Diversion curves

Early studies plotted the observed share of public transport on each O-D
pair against the difference (or ratio) of the costs of car and transit and
found S-shaped **diversion curves**. The logistic function reproduces this
shape:

$$
\begin{aligned}
P_{ij}^{t} &= \frac{T_{ij}^{t}}{T_{ij}} \\
&= \frac{1}{1 + \exp\left[-\beta\left(C_{ij}^{c} - C_{ij}^{t}\right)\right]},
\end{aligned}
$$ (eq-12-diversion-curve)

where $c$ denotes car and $t$ transit. When the two costs are equal each
mode has half the market; the parameter $\beta \ge 0$ controls the
steepness of the curve. As $\beta \to 0$ the split stays at 50 % whatever
the costs, and as $\beta \to \infty$ the choice becomes all-or-nothing: the
cheaper mode takes every trip ({prf:ref}`ex-27-ms-diversion`).

## Combined distribution and modal split

### The entropy-maximizing model

Extend the entropy-maximizing derivation of the gravity model
({doc}`10-trip-distribution`) to trips by mode (Wilson, 1969). Given the trip
ends $O_i$, $D_j$ and the total expenditure $C$ on travel, the most probable
distribution of trips by origin, destination, and mode solves

$$
\begin{aligned}
\max_{T_{ij}^k \ge 0}\quad & H = -\sum_{i}\sum_{j}\sum_{k}\left(T_{ij}^k\ln T_{ij}^k - T_{ij}^k\right) \\
\text{s.t.}\quad & \sum_{j}\sum_{k} T_{ij}^k = O_i, \qquad \forall i, \\
& \sum_{i}\sum_{k} T_{ij}^k = D_j, \qquad \forall j, \\
& \sum_{i}\sum_{j}\sum_{k} T_{ij}^k C_{ij}^k = C .
\end{aligned}
$$ (eq-12-combined-dms)

The objective is strictly concave and the constraints are linear, so the
solution is unique. With multipliers $\alpha_i$, $\gamma_j$, and $\beta$
for the three groups of constraints, setting the derivative of the
Lagrangian with respect to $T_{ij}^k$ to zero gives
$-\ln T_{ij}^k - \alpha_i - \gamma_j - \beta C_{ij}^k = 0$, that is

$$
T_{ij}^k = A_i O_i B_j D_j \exp\left(-\beta C_{ij}^k\right),
$$ (eq-12-combined-solution)

where $A_i O_i = e^{-\alpha_i}$ and $B_j D_j = e^{-\gamma_j}$ are chosen so
that the trip-end constraints hold:

$$
\begin{aligned}
A_i &= \frac{1}{\sum_j B_j D_j \sum_k e^{-\beta C_{ij}^k}}, \\
B_j &= \frac{1}{\sum_i A_i O_i \sum_k e^{-\beta C_{ij}^k}} .
\end{aligned}
$$

They are found by the Furness iteration of {doc}`10-trip-distribution`, using
$\sum_k e^{-\beta C_{ij}^k}$ as the deterrence function.

**The modal split is logit.** Dividing {eq}`eq-12-combined-solution` by its sum
over modes, the balancing factors cancel:

$$
\begin{aligned}
P_{ij}^1 &= \frac{T_{ij}^1}{\sum_k T_{ij}^k} \\
&= \frac{\exp\left(-\beta C_{ij}^1\right)}{\sum_k \exp\left(-\beta C_{ij}^k\right)} .
\end{aligned}
$$ (eq-12-logit-split)

For two modes this is the diversion curve {eq}`eq-12-diversion-curve`. The
logit split has the properties observed in practice: an S-shaped curve,
equal shares for equal costs, a share tending to one when the cost of the
competing mode grows, and an immediate extension to any number of modes
({prf:ref}`ex-27-ms-combined`).

### Separate dispersion parameters

In {eq}`eq-12-combined-solution` the single parameter $\beta$ plays two roles:
it controls the dispersion of the choice between *destinations* at
different costs and the dispersion of the choice between *modes*. There is
no reason why travelers should be equally sensitive to cost in the two
choices, so a more flexible model uses a separate mode-choice parameter
$\lambda$ and lets destination choice respond to a **composite cost**
$K_{ij}$ that summarizes all modes. Allowing also for different person
types $n$ (for example with and without a car available),

$$
T_{ij}^{kn} = \underbrace{A_i^n O_i^n B_j^n D_j^n \exp\left(-\beta^n K_{ij}^n\right)}_{T_{ij}^{n}:\ \text{distribution}}
\ \times\
\underbrace{\frac{\exp\left(-\lambda^n C_{ij}^{k}\right)}{\sum_{m}\exp\left(-\lambda^n C_{ij}^{m}\right)}}_{P_{ij}^{kn}:\ \text{modal split}},
$$ (eq-12-distribution-modal-split)

where the sum in the modal split runs over the modes available to person
type $n$. For consistency the parameters must satisfy $\lambda^n \ge \beta^n$:
travelers are at least as sensitive to cost when choosing between modes
to a given destination as when choosing between destinations.

### The composite cost

How should $K_{ij}$ be defined? An apparently natural choice is the average
cost weighted by the modal shares, $K = \sum_k P^k C^k$. It is wrong.
Suppose a single mode with cost $C^1$ is available, so that $K = C^1$, and a
second, more expensive mode ($C^2 > C^1$) is introduced. With shares $P^1$
and $P^2 = 1 - P^1$,

$$
\begin{aligned}
K^{*} &= (1 - P^2)\,C^1 + P^2 C^2 \\
&= C^1 + P^2\left(C^2 - C^1\right) \\
&> C^1 = K .
\end{aligned}
$$

Adding an option makes travel to that destination appear *more* costly,
which is absurd: a new mode can only help, or at worst leave travelers
indifferent. The weighted average fails because it ignores that each
traveler who switches does so because the new mode is better *for him or
her*.

The consistent definition (Williams, 1977) is the **log-sum**

$$
K_{ij}^n = -\frac{1}{\lambda^n}\ln\left[\sum_k \exp\left(-\lambda^n C_{ij}^k\right)\right],
\qquad \lambda^n > 0 .
$$ (eq-12-composite-cost)

Up to the additive constant $-\gamma/\lambda^n$, it is the expected minimum
perceived cost when the perceived costs are the true costs minus
independent $\mathrm{Gumbel}(0, \lambda^n)$ errors (property 6 of
{prf:ref}`prop-01-gumbel` and {eq}`eq-11-logsum`), and it has the required
properties:

1. $K_{ij}^n \le \min_k C_{ij}^k$: the composite cost is never higher than
   the cheapest mode, and adding a mode lowers it;
2. $\lim_{\lambda^n \to \infty} K_{ij}^n = \min_k C_{ij}^k$, the
   all-or-nothing limit; and
3. $\partial K_{ij}^n / \partial C_{ij}^k = P_{ij}^{kn}$: a unit increase in
   the cost of a mode raises the composite cost by the share of that mode
   ({prf:ref}`ex-27-ms-composite`).

## Multimodal split

### The N-way structure and the red-bus/blue-bus problem

With more than two modes, the simplest structure applies {eq}`eq-12-logit-split`
to all modes at once (an *N-way* or multinomial split). It works when the
modes are clearly distinct, but fails when two of them are close
substitutes.

Suppose half of the travelers in a city use car and half use bus, so that
$C_C = C_B$. The bus company now paints half of its buses red and half blue,
without changing the service. The N-way logit model sees three alternatives
with equal costs and predicts

$$
P_C = P_{RB} = P_{BB} = \frac{1}{3},
$$

so painting buses would attract car users to public transport. In reality,
travelers regard the two colors as one mode, and the shares stay at
$P_C = 1/2$ and $P_{RB} = P_{BB} = 1/4$. The flaw comes from the
**independence of irrelevant alternatives** (IIA) property of the logit
model: the ratio $P_C/P_{RB}$ does not depend on whether the blue bus
exists ({doc}`11-discrete-choice-models`). Similar or identical modes must
therefore not be entered as separate alternatives of an N-way split.

### Hierarchical (nested) structure

A **hierarchical** structure groups modes that share common elements into a
composite mode. A **primary split** allocates trips between the composite
mode and the remaining modes, using the composite cost of the group; a
**secondary split** then divides the composite mode's trips among its
members. For the red/blue-bus case,

$$
\begin{aligned}
P_C &= \frac{1}{1 + \exp\left[-\lambda_1\left(C_B - C_C\right)\right]}, \\
P_B &= 1 - P_C, \\
P_{RB \mid B} &= \frac{1}{1 + \exp\left[-\lambda_2\left(C_{BB} - C_{RB}\right)\right]}, \\
P_{BB \mid B} &= 1 - P_{RB \mid B},
\end{aligned}
$$ (eq-12-hierarchical-split)

with the composite bus cost

$$
C_B = -\frac{1}{\lambda_2}\ln\left[\exp\left(-\lambda_2 C_{RB}\right) + \exp\left(-\lambda_2 C_{BB}\right)\right],
$$

and the unconditional shares $P_{RB} = P_B\,P_{RB \mid B}$ and
$P_{BB} = P_B\,P_{BB \mid B}$. For consistency with utility maximization the
dispersion parameter of the lower split must be at least that of the upper
one, $\lambda_2 \ge \lambda_1$. In the limit $\lambda_2 \to \infty$ (the two
buses are perfect substitutes) $C_B = C_{RB} = C_C$, and the model gives
$P_C = 1/2$ and $P_{RB} = P_{BB} = 1/4$, as it should
({prf:ref}`ex-27-ms-red-blue`). This structure is the aggregate counterpart of
the **nested logit** model of {doc}`11-discrete-choice-models`.

## Calibrating a binary logit split

To account for factors not included in the measured costs, add a modal
penalty $\delta$ to the second mode:

$$
\begin{aligned}
P_1 &= \frac{1}{1 + \exp\left[-\lambda\left(C_2 + \delta - C_1\right)\right]}, \\
P_2 &= 1 - P_1 .
\end{aligned}
$$ (eq-12-binary-split-penalty)

Two parameters must be calibrated: the dispersion parameter $\lambda$ and
the penalty $\delta$. Taking the ratio of the shares and logarithms,

$$
\begin{aligned}
\frac{P_1}{1 - P_1} &= \exp\left[\lambda\left(C_2 + \delta - C_1\right)\right] \\
\Longrightarrow\quad \ln\frac{P_1}{1 - P_1} &= \lambda\left(C_2 - C_1\right) + \lambda\delta .
\end{aligned}
$$ (eq-12-logit-linearization)

If observed shares $P_1$ and costs are available for several O-D pairs, a
simple linear regression of $y = \ln[P_1/(1 - P_1)]$ on
$x = C_2 - C_1$ gives the slope $\hat\lambda$ and the intercept
$\widehat{\lambda\delta}$, hence $\hat\delta = \widehat{\lambda\delta}/\hat\lambda$
({prf:ref}`ex-27-ms-calibration`, {prf:ref}`ex-27-hw3-q1`). The linearization
requires $0 < P_1 < 1$ on every pair and gives every pair the same weight
regardless of the number of trips; with disaggregate data, maximum
likelihood is preferred ({doc}`11-discrete-choice-models`).

## Policy applications

Aggregate logit splits are combined with congestion functions to evaluate
transport policies. Because the travel time of road users depends on the
number of cars, the modal split and the travel times must be found
simultaneously, as the solution of a fixed-point equation.

### Congestion pricing

Consider a corridor between a residential area and a workplace served by a
rapid transit line and a highway, with $Q$ commuters per hour and one person
per car. The generalized costs of transit and auto are

$$
\begin{aligned}
C_T &= \alpha T_T + P_T, \\
C_A &= \alpha T_A(Q_A) + P_A,
\end{aligned}
$$ (eq-12-pricing-costs)

where $\alpha$ is the value of time, $T_T$ the (constant) door-to-door time
by transit, $P_T$ the flat fare, $P_A$ the road toll, and $T_A(Q_A)$ an
increasing function of the auto volume $Q_A$. With a logit split,

$$
\begin{aligned}
Q_A &= \frac{Q}{1 + \exp\left[-\beta\left(C_T - C_A(Q_A)\right)\right]}, \\
Q_T &= Q - Q_A .
\end{aligned}
$$ (eq-12-pricing-equilibrium)

Equation {eq}`eq-12-pricing-equilibrium` has $Q_A$ on both sides; its unique
solution (the right-hand side decreases in $Q_A$, the left-hand side
increases) is found by Newton's method. Conversely, the toll that achieves a
target auto volume $\bar{Q}_A$ follows in closed form by solving
{eq}`eq-12-pricing-equilibrium` for $P_A$ ({prf:ref}`ex-27-ms-pricing`).

### Bus lanes

On an $n$-lane highway carrying $N$ commuters who drive alone or take the
bus, reserving $n_{\mathrm{bus}}$ lanes for buses speeds up buses, attracts
some drivers to the bus, and leaves fewer lanes for the remaining cars. With
generalized times $C_{\mathrm{car}} = t_{\mathrm{car}}$ and
$C_{\mathrm{bus}} = t_{\mathrm{bus}} + \Delta$, where $\Delta$ lumps the
access, waiting, and discomfort penalty of the bus, the logit split is

$$
\begin{aligned}
N_{\mathrm{car}} &= \frac{N}{1 + \exp\left[-\beta\left(C_{\mathrm{bus}} - C_{\mathrm{car}}\right)\right]}, \\
N_{\mathrm{bus}} &= N - N_{\mathrm{car}},
\end{aligned}
$$

and the total travel cost is

$$
TC = N_{\mathrm{bus}}\left(t_{\mathrm{bus}} + \Delta\right) + N_{\mathrm{car}}\,t_{\mathrm{car}} .
$$ (eq-12-bus-lane-tc)

The scheme is worthwhile if the **cost-effectiveness** ratio
$CE = TC_n^{n_{\mathrm{bus}}}/TC_n^{0}$ is below one
({prf:ref}`ex-27-ms-bus-lane`).

## Summary and Common Mistakes

### Summary

- The generalized cost of a mode {eq}`eq-12-generalized-cost-mode` combines
  times, money costs, and a modal penalty; the empirical diversion curve is
  logistic {eq}`eq-12-diversion-curve`.
- Entropy maximization with trips by mode {eq}`eq-12-combined-dms` gives
  $T_{ij}^k = A_iO_iB_jD_j e^{-\beta C_{ij}^k}$
  {eq}`eq-12-combined-solution`, whose modal split is logit
  {eq}`eq-12-logit-split`.
- A separate mode-choice parameter $\lambda^n \ge \beta^n$
  {eq}`eq-12-distribution-modal-split` requires a composite cost; the
  consistent composite cost is the log-sum {eq}`eq-12-composite-cost`, never
  higher than the cheapest mode.
- Similar modes are grouped in a hierarchical structure with a primary and a
  secondary split {eq}`eq-12-hierarchical-split`, with
  $\lambda_2 \ge \lambda_1$.
- A binary logit split with a modal penalty
  {eq}`eq-12-binary-split-penalty` is calibrated by regressing
  $\ln[P_1/(1-P_1)]$ on $C_2 - C_1$ {eq}`eq-12-logit-linearization`.
- Policy evaluation couples the logit split with congestion functions and
  solves for the equilibrium split ({eq}`eq-12-pricing-equilibrium`,
  {eq}`eq-12-bus-lane-tc`).

### Common mistakes

- **Using the share-weighted average cost as the composite cost.** It
  increases when a more expensive mode is added, as if a new option made
  travel worse; use the log-sum {eq}`eq-12-composite-cost`.
- **Applying an N-way logit split to modes that are close substitutes.** IIA
  then lets a mere relabeling (red-bus/blue-bus) attract travelers; group
  such modes in a hierarchical split.
- **Choosing $\lambda < \beta$ in the combined model, or
  $\lambda_2 < \lambda_1$ in a hierarchical split.** Travelers would then be
  more sensitive to cost between destinations (or main modes) than between
  close alternatives, which is inconsistent with utility maximization.
- **Evaluating a policy with the modal split at *current* travel times.**
  The congested times change with the split, so the split and the times must
  be solved together as a fixed point.

## References

- Ortúzar, J. de D., & Willumsen, L. G. (2011). *Modelling Transport* (4th
  ed.), Chapter 6 (Modal split and direct demand models). Wiley.
- Williams, H. C. W. L. (1977). On the formation of travel demand models
  and economic evaluation measures of user benefit. *Environment and
  Planning A*, 9(3), 285–344. <https://doi.org/10.1068/a090285>
- Wilson, A. G. (1969). The use of entropy maximising models in the theory
  of trip distribution, mode split and route split. *Journal of Transport
  Economics and Policy*, 3(1), 108–126.
- Wilson, A. G. (1970). *Entropy in Urban and Regional Modelling*. Pion.
- Cambridge Systematics et al. (2012). *Travel Demand Forecasting:
  Parameters and Techniques* (NCHRP Report 716), Section 4.7.
  Transportation Research Board.
