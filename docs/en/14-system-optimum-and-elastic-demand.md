# Traffic Assignment II: System Optimum, Elastic Demand, and Combined Models

## Overview

The user equilibrium describes how travelers behave; it does not minimize
the total time spent in the network. This chapter introduces Wardrop's
second principle, the **system optimum (SO)**, compares it with the user
equilibrium, and shows how marginal-cost pricing turns one into the other.
Braess's paradox illustrates that the difference matters for planning. The
chapter then relaxes the assumption of a fixed O-D matrix in two ways: an
**elastic demand** that falls as travel times rise, and a **combined
distribution–assignment model** in which the trip matrix and the network
flows are determined jointly.

:::{admonition} Learning objectives
:class: objectives
After completing this chapter, readers should be able to:

- state Wardrop's second principle and formulate the system optimum as a
  convex program;
- interpret the marginal cost of a link and solve the system optimum as a
  user equilibrium with marginal-cost functions;
- compute marginal-cost tolls that make the user equilibrium system-optimal;
- explain Braess's paradox;
- formulate and solve the user equilibrium with elastic demand, using the
  excess-demand network; and
- formulate the combined distribution–assignment model and explain how it is
  solved.
:::

## Notation

| Symbol | Meaning |
|---|---|
| $\mathrm{TSTT}$ | total system travel time $\sum_a x_at_a(x_a)$ |
| $\tilde t_a(x_a)$ | marginal (social) cost of link $a$, $t_a + x_at_a'$ |
| $\tau_a$ | toll on link $a$ (in time units) |
| $D_{rs}(u_{rs})$, $D_{rs}^{-1}(q_{rs})$ | demand function of pair $rs$ and its inverse |
| $\bar q_{rs}$ | upper bound on the demand, $D_{rs}(0)$ |
| $e_{rs}$, $W_{rs}(e_{rs})$ | excess demand and its cost function |
| $O_r$, $D_s$ | trips produced at origin $r$ and attracted to destination $s$ |
| $\beta$ | dispersion parameter of the gravity (entropy) model |

## The system optimum

### Wardrop's second principle

Wardrop (1952) stated a second principle:

> The average journey time is a minimum.

The average journey time is the total travel time divided by the total
demand, which is fixed, so minimizing it is the same as minimizing the
**total system travel time**. Summing path times over paths and regrouping
by links (each link appears in every path that uses it) gives

$$
\begin{aligned}
\sum_{r, s}\sum_{k \in K_{rs}} f_k^{rs}c_k^{rs} &= \sum_{r, s}\sum_{k \in K_{rs}} f_k^{rs}\sum_a t_a(x_a)\,\delta_{a,k}^{rs} \\
&= \sum_{a \in A} x_a\,t_a(x_a) .
\end{aligned}
$$ (eq-14-tstt)

### The system optimum program

The **system optimum** minimizes {eq}`eq-14-tstt` over the feasible flows:

$$
\begin{aligned}
\min_{\bff}\ \tilde z(\bx) &= \sum_{a \in A} x_a\,t_a(x_a) \\
\text{s.t.}\quad
\sum_{k \in K_{rs}} f_k^{rs} &= q_{rs}, \\
f_k^{rs} &\ge 0, \\
x_a &= \sum_{r, s}\sum_{k \in K_{rs}} f_k^{rs}\,\delta_{a,k}^{rs} .
\end{aligned}
$$ (eq-14-so)

The constraints are those of Beckmann's program {eq}`eq-13-beckmann`; only the
objective differs. The SO flow pattern is generally **not an equilibrium**:
it can be reached only if all travelers act jointly to minimize the total
travel time rather than their own. At the system optimum some travelers
can decrease their own travel time by changing route unilaterally, so the
pattern would not sustain itself, and it cannot be used to predict actual
route choice. It is, however, a yardstick: the total system travel time is
the key performance measure of a network, and the SO gives the best value
that any route guidance or pricing policy could achieve.

### Marginal cost and the system optimum conditions

Define the **marginal cost** of link $a$,

$$
\begin{aligned}
\tilde t_a(x_a) &= \frac{\diff\left[x_a t_a(x_a)\right]}{\diff x_a} \\
&= t_a(x_a) + x_a\,t_a'(x_a) .
\end{aligned}
$$ (eq-14-marginal-cost)

It is the increase in the total travel time on link $a$ caused by one more
traveler, and has two parts: $t_a(x_a)$, the travel time that the extra
traveler experiences, and $x_at_a'(x_a)$, the extra delay that he or she
imposes on the $x_a$ travelers already on the link. The second part is an
**externality**: travelers who choose routes for themselves ignore it.

Since $x_at_a(x_a) = \int_0^{x_a}\tilde t_a(\omega)\,\diff\omega$, the
SO program {eq}`eq-14-so` is Beckmann's program with $t_a$ replaced by
$\tilde t_a$. Applying {prf:ref}`thm-13-beckmann-ue` gives:

:::{prf:theorem} System optimum as a user equilibrium
:label: thm-14-so-ue

The system-optimal flows are the user equilibrium flows of the same network
with the link performance functions replaced by the marginal cost functions
$\tilde t_a(x_a)$. At the system optimum, all used paths of an O-D pair have
equal and minimum **marginal** path cost
$\tilde c_k^{rs} = \sum_a \tilde t_a(x_a)\,\delta_{a,k}^{rs}$.
:::

Consequently, any algorithm for the user equilibrium solves the SO when it
is given the marginal cost functions. The Hessian of $\tilde z$ is diagonal
with entries $\tilde t_a'(x_a) = 2t_a'(x_a) + x_a t_a''(x_a)$, so the
**system-optimal link flows are unique** if
$2t_a'(x_a) + x_at_a''(x_a) > 0$ for all links, which holds for all
strictly increasing convex link functions, including BPR functions.

### When do the UE and SO coincide?

If travel times do not depend on flows, $t_a(x_a) = t_a^0$, then
$\tilde t_a = t_a$ and both programs reduce to
$\min \sum_a t_a^0x_a$: the UE and the SO coincide and both are the AON
assignment with free-flow times. This is the case of an uncongested network.
With congestion they differ, and the UE total travel time is never smaller
than the SO total travel time. The ratio of the two, the **price of
anarchy**, is at most $4/3$ for networks with linear link functions
(Roughgarden and Tardos, 2002); in the two-route network of
{prf:ref}`ex-29-so-two-route` it is $350/279.63 = 1.25$, and in real networks
the ratio is usually much closer to 1.

## Marginal-cost pricing

Let $\{x_a^{\mathrm{SO}}\}$ be the system-optimal flows. If every link is
charged the toll (in time units)

$$
\tau_a = x_a^{\mathrm{SO}}\,t_a'\big(x_a^{\mathrm{SO}}\big), \qquad a \in A,
$$ (eq-14-mc-toll)

equal to the externality at the system optimum, travelers who minimize
their generalized time $\hat t_a(x_a) = t_a(x_a) + \tau_a$ reach a user
equilibrium that is the system optimum. Indeed, the UE with tolls minimizes

$$
\sum_a \int_0^{x_a}\left[t_a(\omega) + \tau_a\right]\diff\omega,
$$

whose KKT conditions require equal costs
$\sum_a \big[t_a(x_a) + \tau_a\big]\delta_{a,k}^{rs}$ on the used paths. At
$\bx = \bx^{\mathrm{SO}}$, $t_a + \tau_a = \tilde t_a$, so the SO flows
satisfy these conditions, and by uniqueness they are the tolled equilibrium.

The toll is expressed in time; multiplying by the value of time converts it
to money. Real pricing schemes approximate {eq}`eq-14-mc-toll` because tolls
cannot be charged on every link, and charges that vary by time of day, such
as Singapore's Electronic Road Pricing, address the dynamic version of the
problem ({doc}`16-dynamic-assignment-and-simulation`).

## Braess's paradox

Adding a link to a network cannot increase the system-optimal total travel
time — the new link can always be left empty. The user equilibrium has no
such guarantee. In the network of {numref}`fig-14-braess-network`, 6 trips per
unit time travel from node 1 to node 4. Without link 5 the equilibrium
splits them equally between the two routes, each with time 83. When link 5
is added, two of the six trips move to the new route 1–3–2–4, the three
routes carry two trips each, and every traveler's time rises to 92,
although nothing else has changed
({prf:ref}`ex-29-braess`). This is **Braess's paradox** (Braess, 1968; English translation in Braess et al., 2005): in a
user equilibrium, extra capacity can make everybody worse off, because each
traveler ignores the delay he or she imposes on others. The lesson for
planning is that network improvements must be evaluated with an assignment
model, not by intuition, and that pricing (or removing links) can improve a
network.

```{figure} figures/14-braess-network.svg
:name: fig-14-braess-network
:width: 420px
:class: dark-light

Braess's network: 6 trips from node 1 to node 4 with the link performance
functions shown. The dashed link 5 is the new road.
```

## User equilibrium with elastic demand

### Demand functions

So far the O-D matrix has been fixed. In reality, congestion discourages
some trips: they are made at another time, to another destination, by
another mode, or not at all. Suppose that the demand of pair $rs$ is a
decreasing function of the equilibrium travel time,

$$
\begin{aligned}
q_{rs} &= D_{rs}(u_{rs}), \\
u_{rs} &= D_{rs}^{-1}(q_{rs}),
\end{aligned}
$$

for example $q_{rs} = 10 - 0.2\,u_{rs}$ (inverse $u_{rs} = 50 - 5q_{rs}$) or
$q_{rs} = \bar q_{rs}\exp(-\beta u_{rs})$ (inverse
$u_{rs} = -\ln(q_{rs}/\bar q_{rs})/\beta$). The inverse demand
$D_{rs}^{-1}(q_{rs})$ is the travel time at which exactly $q_{rs}$ trips
would be made: the willingness to travel of the marginal traveler.

### Formulation and equilibrium conditions

The **user equilibrium with elastic demand** solves

$$
\begin{aligned}
\min_{\bff, \bq}\ z(\bx, \bq) &= \sum_{a}\int_0^{x_a} t_a(\omega)\,\diff\omega
- \sum_{r, s}\int_0^{q_{rs}} D_{rs}^{-1}(\omega)\,\diff\omega \\
\text{s.t.}\quad
\sum_{k \in K_{rs}} f_k^{rs} &= q_{rs}, \\
f_k^{rs} &\ge 0, \\
q_{rs} &\ge 0,
\end{aligned}
$$ (eq-14-elastic)

with the link flows defined by {eq}`eq-13-link-path-flow`. Repeating the proof
of {prf:ref}`thm-13-beckmann-ue` with the additional variables $q_{rs}$ gives
the KKT conditions

$$
\begin{aligned}
f_k^{rs}\left(c_k^{rs} - u_{rs}\right) &= 0, \\
c_k^{rs} - u_{rs} &\ge 0, \\
q_{rs}\left(u_{rs} - D_{rs}^{-1}(q_{rs})\right) &= 0, \\
u_{rs} - D_{rs}^{-1}(q_{rs}) &\ge 0 .
\end{aligned}
$$ (eq-14-elastic-conditions)

The first pair is Wardrop's principle. The second says that, if trips are
made between $r$ and $s$, their number is exactly the demand at the
equilibrium travel time, $q_{rs} = D_{rs}(u_{rs})$; if none are made, the
travel time exceeds what even the first traveler is willing to bear. Since
$-D_{rs}^{-1}$ is increasing, the objective is strictly convex in
$(\bx, \bq)$, and the equilibrium link flows and O-D demands are unique.

### The excess-demand network

Let $\bar q_{rs} = D_{rs}(0)$ be an upper bound on the demand (or any number
large enough that the demand never reaches it), and define the **excess
demand** $e_{rs} = \bar q_{rs} - q_{rs}$: the trips that are not made.
Substituting $\omega = \bar q_{rs} - v$ in the demand integral,

$$
\begin{aligned}
-\int_0^{q_{rs}} D_{rs}^{-1}(\omega)\,\diff\omega
&= -\int_0^{\bar q_{rs}} D_{rs}^{-1}(\omega)\,\diff\omega
+ \int_{q_{rs}}^{\bar q_{rs}} D_{rs}^{-1}(\omega)\,\diff\omega \\
&= \text{constant} + \int_0^{e_{rs}} D_{rs}^{-1}(\bar q_{rs} - v)\,\diff v .
\end{aligned}
$$

With the **excess-demand function**
$W_{rs}(e_{rs}) = D_{rs}^{-1}(\bar q_{rs} - e_{rs})$, program
{eq}`eq-14-elastic` becomes

$$
\begin{aligned}
\min\ & \sum_a \int_0^{x_a} t_a(\omega)\,\diff\omega
+ \sum_{r, s}\int_0^{e_{rs}} W_{rs}(v)\,\diff v \\
\text{s.t.}\ & \sum_{k \in K_{rs}} f_k^{rs} + e_{rs} = \bar q_{rs}, \\
& f_k^{rs} \ge 0, \\
& e_{rs} \ge 0 .
\end{aligned}
$$ (eq-14-excess-demand)

This is a **fixed-demand** user equilibrium on an augmented network: add,
for each O-D pair, a dummy link from $r$ directly to $s$ with performance
function $W_{rs}(e_{rs})$, and assign the fixed demand $\bar q_{rs}$. The
flow on the dummy link is the excess demand, and at equilibrium the dummy
link's cost equals the time of the used paths: the trips "not made" are
those whose willingness to travel is below the equilibrium travel time.
$W_{rs}$ is increasing because $D_{rs}^{-1}$ is decreasing, so any
fixed-demand algorithm — Frank–Wolfe, MSA — solves the elastic problem
without modification ({prf:ref}`ex-29-elastic-demand`). The value of
$\bar q_{rs}$ does not affect the solution as long as it exceeds the
equilibrium demand.

## Combined distribution and assignment

### Motivation

The gravity model of {doc}`10-trip-distribution` treats the travel costs
$c_{rs}$ as given, but those costs are the result of assigning the trip
matrix to the network. Running the four steps in sequence once leaves the
two inconsistent: the costs used to distribute the trips are not the costs
produced by assigning them. A **combined model** determines the trip matrix
and the link flows simultaneously, so that the trips are distributed
according to the equilibrium costs.

### Formulation

Evans (1976) combined Beckmann's objective with the entropy term of the
doubly constrained gravity model ({doc}`10-trip-distribution`):

$$
\begin{aligned}
\min_{\bff, \bq}\ z(\bx, \bq) &= \sum_a\int_0^{x_a} t_a(\omega)\,\diff\omega
+ \frac{1}{\beta}\sum_{r, s} q_{rs}\left(\ln q_{rs} - 1\right) \\
\text{s.t.}\quad
\sum_{s} q_{rs} &= O_r, \\
\sum_{r} q_{rs} &= D_s, \\
\sum_{k \in K_{rs}} f_k^{rs} &= q_{rs}, \\
f_k^{rs} &\ge 0,
\end{aligned}
$$ (eq-14-combined-da)

with link flows given by {eq}`eq-13-link-path-flow`. The objective is strictly
convex in $(\bx, \bq)$, so the solution is unique in link flows and trip
matrix.

### Optimality conditions

With multipliers $u_{rs}$ for path conservation and $\mu_r$, $\lambda_s$
for the trip-end constraints, the conditions for the path flows are
Wardrop's conditions {eq}`eq-13-ue-conditions`: $u_{rs}$ is the equilibrium
travel time. For the (positive) O-D flows,

$$
\frac{\partial L}{\partial q_{rs}} = \frac{1}{\beta}\ln q_{rs} + u_{rs} - \mu_r - \lambda_s,
$$

which is zero at the optimum, so $q_{rs} = \exp(\beta\mu_r)\exp(\beta\lambda_s)\exp(-\beta u_{rs})$.
Imposing $\sum_s q_{rs} = O_r$ and $\sum_r q_{rs} = D_s$ determines the two
exponential factors, and

$$
\begin{aligned}
q_{rs} &= A_r O_r B_s D_s \exp(-\beta u_{rs}), \\
A_r &= \frac{1}{\sum_s B_s D_s \exp(-\beta u_{rs})}, \\
B_s &= \frac{1}{\sum_r A_r O_r \exp(-\beta u_{rs})} .
\end{aligned}
$$ (eq-14-combined-da-solution)

The trip matrix is a doubly constrained gravity model **evaluated at the
equilibrium travel times**, and the link flows are a user equilibrium for
that trip matrix: distribution and assignment are mutually consistent.

### Solution algorithms

Applying Frank–Wolfe to {eq}`eq-14-combined-da` linearizes the objective in
both $\bx$ and $\bq$. The linearized cost of an O-D flow is
$u_{rs}^{(n)} + \tfrac{1}{\beta}\ln q_{rs}^{(n)}$, so the direction-finding
step is a **Hitchcock transportation problem** — a linear program that
distributes the trip ends at minimum linearized cost — followed by an AON
assignment of the resulting matrix (Sheffi, 1985, Sections 7.3–7.4). Evans's
(1976) **partial linearization** keeps the entropy term exactly and
linearizes only the network part, which is more efficient:

:::{prf:algorithm} Evans's algorithm for combined distribution and assignment
:label: alg-14-evans

1. **Initialization.** Compute shortest-path times with free-flow link
   times, solve the gravity model {eq}`eq-14-combined-da-solution` with these
   times, and assign the matrix AON. This gives $\bq^{(1)}$ and
   $\bx^{(1)}$. Set $n = 1$.
2. **Update.** Set $t_a^{(n)} = t_a\big(x_a^{(n)}\big)$ and compute the
   shortest-path times $u_{rs}^{(n)}$.
3. **Direction finding.** Solve the doubly constrained gravity model with
   costs $u_{rs}^{(n)}$ (biproportional fitting). This gives the auxiliary
   matrix $\bv^{(n)}$. Assign $\bv^{(n)}$ AON on the shortest
   paths, giving the auxiliary link flows $\by^{(n)}$.
4. **Line search.** Find $\alpha_n \in [0, 1]$ minimizing
   $z\big(\bx^{(n)} + \alpha(\by^{(n)} - \bx^{(n)}),\ \bq^{(n)} + \alpha(\bv^{(n)} - \bq^{(n)})\big)$.
5. **Move.** Update $\bx$ and $\bq$ with step $\alpha_n$.
6. **Convergence test.** Stop if the flows and the matrix no longer change;
   otherwise set $n \leftarrow n + 1$ and return to step 2.
:::

The derivative of the line-search function is the Frank–Wolfe derivative
{eq}`eq-13-fw-line-search` plus
$\tfrac{1}{\beta}\sum_{r,s}\ln\big(q_{rs} + \alpha(v_{rs} - q_{rs})\big)(v_{rs} - q_{rs})$.
{prf:ref}`ex-29-combined-da` applies the algorithm to the six-node network.
The same idea extends to combined models with mode choice, in which the
log-sum of {doc}`12-aggregate-modal-split` replaces the travel time.

## Summary and Common Mistakes

### Summary

- The SO {eq}`eq-14-so` minimizes the total system travel time
  {eq}`eq-14-tstt`; it is the UE with the marginal costs
  $\tilde t_a = t_a + x_at_a'$ {eq}`eq-14-marginal-cost`
  ({prf:ref}`thm-14-so-ue`).
- The marginal-cost toll {eq}`eq-14-mc-toll` makes the UE system-optimal;
  Braess's paradox ({numref}`fig-14-braess-network`) shows that the UE can
  deteriorate when capacity is added.
- Elastic demand adds $-\sum\int D^{-1}$ to Beckmann's objective
  {eq}`eq-14-elastic`, with conditions {eq}`eq-14-elastic-conditions`; the
  excess-demand network {eq}`eq-14-excess-demand` turns it into a
  fixed-demand problem.
- The combined model {eq}`eq-14-combined-da` adds an entropy term; its
  solution is a gravity model evaluated at the equilibrium travel times
  {eq}`eq-14-combined-da-solution`, computed by Evans's algorithm
  ({prf:ref}`alg-14-evans`).

### Common mistakes

- **Treating the system optimum as a prediction of route choice.** At the
  SO some travelers can gain by changing route; the SO is a benchmark, not a
  behavioral model.
- **Solving the SO with the link times instead of the marginal costs.** The
  SO is the UE with $\tilde t_a$; for linear functions remember the factor 2
  in $\tilde t_a = A_a + 2B_ax_a$.
- **Computing tolls from the UE flows.** The toll {eq}`eq-14-mc-toll` is
  evaluated at the SO flows.
- **Assuming that extra capacity always reduces travel time.** In a user
  equilibrium it can increase everybody's travel time (Braess's paradox).
- **Choosing an upper bound $\bar q_{rs}$ below the equilibrium demand.** The
  excess demand $e_{rs}$ would then have to be negative; $\bar q_{rs}$ must
  exceed the demand, for example $\bar q_{rs} = D_{rs}(0)$.
- **Running the four steps once in sequence and calling the result an
  equilibrium.** The costs used for distribution then differ from the
  assigned costs; feedback or a combined model is needed for consistency.

## References

- Braess, D. (1968). Über ein Paradoxon aus der Verkehrsplanung.
  *Unternehmensforschung*, *12*, 258–268.
- Braess, D., Nagurney, A., & Wakolbinger, T. (2005). On a paradox of
  traffic planning [English translation of Braess, 1968]. *Transportation
  Science*, 39(4), 446–450. <https://doi.org/10.1287/trsc.1050.0127>
- Evans, S. P. (1976). Derivation and analysis of some models for combining
  trip distribution and assignment. *Transportation Research*, *10*(1), 37–57.
- Ortúzar, J. de D., & Willumsen, L. G. (2011). *Modelling Transport* (4th
  ed.), Chapters 10 and 11. Wiley.
- Roughgarden, T., & Tardos, É. (2002). How bad is selfish routing?
  *Journal of the ACM*, *49*(2), 236–259.
- Sheffi, Y. (1985). *Urban Transportation Networks: Equilibrium Analysis
  with Mathematical Programming Methods*, Sections 3.4–3.5, 6.1–6.3, and
  7.3–7.4. Prentice-Hall.
- Wardrop, J. G. (1952). Some theoretical aspects of road traffic research.
  *Proceedings of the Institution of Civil Engineers, Part II*, *1*(3),
  325–378. <https://doi.org/10.1680/ipeds.1952.11259>
