# Traffic Assignment I: Deterministic User Equilibrium

## Overview

Traffic assignment is the last step of the four-step model. Its input is the
O-D trip matrix of a mode, for example the car trips of the morning peak
hour, and its output is the flow and travel time on every link of the
network. The route each traveler takes depends on the travel times, and the
travel times depend on how many travelers use each link, so the assignment
is an equilibrium problem. This chapter states Wardrop's first principle,
writes the resulting **deterministic user equilibrium (DUE)** as a system of
conditions on path flows, shows that it is the solution of Beckmann's convex
program, and presents the algorithms used in practice: all-or-nothing
assignment, the Frank–Wolfe method, and the method of successive averages.

:::{admonition} Learning objectives
:class: objectives
After completing this chapter, readers should be able to:

- describe the properties of link performance functions;
- state Wardrop's first principle and its behavioral assumptions;
- represent a network with link–path incidences and write the feasibility
  conditions for path and link flows;
- write the user equilibrium conditions and solve them for small networks;
- formulate Beckmann's program, prove its equivalence with the equilibrium
  conditions, and explain why link flows are unique but path flows are not;
  and
- solve the user equilibrium by all-or-nothing assignment, Frank–Wolfe, and
  MSA, and judge convergence.
:::

## Notation

| Symbol | Meaning |
|---|---|
| $G = (N, A)$ | network with node set $N$ and link set $A$ |
| $R$, $S$ | sets of origins and destinations (centroids) |
| $K_{rs}$ | set of paths from origin $r$ to destination $s$ |
| $q_{rs}$ | O-D demand from $r$ to $s$ (trips per unit time) |
| $x_a$, $t_a(x_a)$ | flow and travel time on link $a$ |
| $f_k^{rs}$, $c_k^{rs}$ | flow and travel time on path $k \in K_{rs}$ |
| $\delta_{a,k}^{rs}$ | 1 if link $a$ lies on path $k$ of pair $rs$, 0 otherwise |
| $\bDelta$ | link–path incidence matrix with entries $\delta_{a,k}^{rs}$ |
| $u_{rs}$ | minimum path travel time from $r$ to $s$ |
| $\by$ | auxiliary (all-or-nothing) link flows |

## Traffic assignment in the four-step model

After trip generation, distribution, and modal split, the car trips between
every pair of zones are known for the period being modeled. Traffic
assignment loads these trips onto the road network. It answers two
questions: which routes do travelers use, and what flows and travel times
result? The answers serve to evaluate projects (where will congestion
appear, how much time does a new link save?), feed back travel times to the
earlier steps (equilibrium between demand and supply, see
{doc}`05-transportation-planning-process`), and provide the inputs of
environmental and economic appraisal.

An assignment model has three ingredients: the **network** with its link
performance functions, the **O-D matrix**, and a **route choice principle**
that says how travelers choose among the paths of each O-D pair. This
chapter uses Wardrop's first principle; {doc}`15-stochastic-user-equilibrium`
relaxes its assumption of perfect information.

## Link performance functions

The average travel time on link $a$, $t_a(x_a)$, depends on the link flow
$x_a$ (vehicles per unit time) and the capacity $c_a$ (the maximum number
of vehicles that can traverse the link per unit time). It is
non-decreasing in flow and non-increasing in capacity:

$$
\begin{aligned}
\frac{\partial t_a}{\partial x_a} &\ge 0, \\
\frac{\partial t_a}{\partial c_a} &\le 0 .
\end{aligned}
$$

The usual form is the BPR function {eq}`eq-06-bpr`,
$t_a(x_a) = t_a^0\left[1 + \alpha(x_a/c_a)^\beta\right]$. The parameter
$\alpha$ fixes the travel time at capacity, $t_a^0(1 + \alpha)$, and $\beta$
fixes how abruptly the time rises once the flow approaches capacity: with
$\beta = 1$ the time grows linearly from the start, whereas with $\beta = 4$
it barely changes at low flows and rises steeply above about 80 % of
capacity. For a link with $t_a^0 = 30$ min and $c_a = 3\,600$ veh/h,
the time at $x_a = 3\,600$ veh/h is 34.5 min for any $\beta$, but at
$x_a = 1\,800$ veh/h it is 32.25 min with $\beta = 1$ and only 30.28 min
with $\beta = 4$. Doubling $\alpha$ to 0.30 doubles the delay
$t_a - t_a^0$ at every flow. Typical values of $\alpha$ and $\beta$ by
facility type are tabulated by Cambridge Systematics et al. (2012,
Section 4.11).

The theory below requires only that every $t_a$ be continuous and
**strictly increasing**, and that the travel time of a link depend on its
own flow only (**separable** functions). Linear functions $t_a = A_a + B_ax_a$
are used in most hand examples because they keep the algebra simple.

## Wardrop's first principle

Travelers who know the network well choose the route they believe to be the
quickest. They do not all use the same route, because the travel time of a
route grows with the number of travelers on it: as the shortest route
fills up, an alternative becomes equally attractive. After a period of
adjustment the flows settle in a state described by **Wardrop's first
principle** (Wardrop, 1952):

> The journey times on all the routes actually used are equal, and less than
> those which would be experienced by a single vehicle on any unused route.

Equivalent statements are:

- no traveler can reduce his or her travel time by unilaterally changing
  route; and
- for every O-D pair, all used paths have equal travel time, and no unused
  path has a smaller travel time.

The resulting flow pattern is the **deterministic user equilibrium (DUE)**,
or simply the user equilibrium (UE). The principle rests on three
assumptions:

1. travelers are rational and choose the path of minimum travel time;
2. travelers have perfect information about the travel times of all paths;
   and
3. travelers are identical in their route choice behavior.

For a single O-D pair connected by two parallel links, the equilibrium
follows directly from the principle. If both links are used,
$t_1(x_1) = t_2(x_2)$ and $x_1 + x_2 = q$. If the solution of these two
equations makes one flow negative, that link is unused, all the demand takes
the other link, and its travel time is no larger than the free-flow time of
the unused one. {prf:ref}`ex-28-ue-two-route` works through both cases and
shows how the set of used routes changes with demand.

## Network representation and feasible flows

A network is a directed graph $G = (N, A)$. Origins $r \in R$ and
destinations $s \in S$ are centroid nodes, and $K_{rs}$ is the set of paths
(sequences of links) from $r$ to $s$. In the network of
{numref}`fig-13-six-node-network`, for example, $R = \{1, 5\}$,
$S = \{2, 6\}$, and the O-D pair $1 \to 2$ has two paths: link 1, and links
2–4–3.

```{figure} figures/13-six-node-network.svg
:name: fig-13-six-node-network
:width: 460px
:class: dark-light

The six-node network used in the examples. Origins (green) are nodes 1 and
5, destinations (orange) nodes 2 and 6; link numbers are in brackets. The
O-D pair $1 \to 2$ has paths [1] and [2]–[4]–[3]; the pair $5 \to 6$ has
paths [6] and [5]–[4]–[7].
```

The structure of the paths is recorded in the **link–path incidence**

$$
\delta_{a,k}^{rs} =
\begin{cases}
1 & \text{if link } a \text{ is on path } k \text{ from } r \text{ to } s, \\
0 & \text{otherwise,}
\end{cases}
$$

collected in the matrix $\bDelta$ with one row per link and one
column per path.

A set of path flows $\{f_k^{rs}\}$ is **feasible** if it satisfies **flow
conservation** and **non-negativity**:

$$
\begin{aligned}
\sum_{k \in K_{rs}} f_k^{rs} &= q_{rs}, && r \in R,\ s \in S, \\
f_k^{rs} &\ge 0, && k \in K_{rs},\ r \in R,\ s \in S.
\end{aligned}
$$ (eq-13-flow-conservation)

Link flows and path costs follow from the path flows through the incidence
matrix:

$$
x_a = \sum_{r \in R}\sum_{s \in S}\sum_{k \in K_{rs}} f_k^{rs}\,\delta_{a,k}^{rs},
\qquad a \in A,
$$ (eq-13-link-path-flow)

$$
c_k^{rs} = \sum_{a \in A} t_a(x_a)\,\delta_{a,k}^{rs},
\qquad k \in K_{rs}.
$$ (eq-13-path-cost)

In matrix form, $\bx = \bDelta\bff$ and
$\bc = \bDelta\T\bt(\bx)$. Equation {eq}`eq-13-path-cost` assumes
that path costs are **additive**: the time of a path is the sum of the times
of its links. A given O-D matrix admits infinitely many feasible path flow
patterns, and therefore infinitely many feasible link flow patterns; the
route choice principle selects one of them.

## The equilibrium conditions

Let $u_{rs}$ be the minimum path travel time between $r$ and $s$. Wardrop's
first principle states that a path carries flow only if its travel time
equals $u_{rs}$. Together with feasibility this gives the **user equilibrium
conditions**:

$$
\begin{aligned}
f_k^{rs}\left(c_k^{rs} - u_{rs}\right) &= 0, && k \in K_{rs},\ r \in R,\ s \in S, \\
c_k^{rs} - u_{rs} &\ge 0, && k \in K_{rs},\ r \in R,\ s \in S, \\
\sum_{k \in K_{rs}} f_k^{rs} &= q_{rs}, && r \in R,\ s \in S, \\
f_k^{rs} &\ge 0, && k \in K_{rs},\ r \in R,\ s \in S.
\end{aligned}
$$ (eq-13-ue-conditions)

The first line says that a used path ($f_k^{rs} > 0$) has the minimum time;
the second that no path is quicker than $u_{rs}$. Because the path costs
depend on the flows through {eq}`eq-13-link-path-flow` and
{eq}`eq-13-path-cost`, {eq}`eq-13-ue-conditions` is a system of non-linear
equations and inequalities, a **complementarity problem**.

For small networks the conditions can be solved by hand: guess which paths
are used, set their costs equal, solve the resulting equations together with
flow conservation, and check that every flow is non-negative and that every
unused path is no quicker. If a check fails, change the guess.
{prf:ref}`ex-28-ue-three-link` and {prf:ref}`ex-28-ue-six-node` apply this
procedure. For realistic networks, with thousands of paths, the number of
possible guesses is astronomical, and an optimization formulation is needed.

## Beckmann's formulation

### The convex program

Beckmann, McGuire, and Winsten (1956) showed that the equilibrium flows
solve the program

$$
\begin{aligned}
\min_{\bff}\ z(\bx) &= \sum_{a \in A}\int_0^{x_a} t_a(\omega)\,\diff\omega \\
\text{s.t.}\quad
\sum_{k \in K_{rs}} f_k^{rs} &= q_{rs}, && r \in R,\ s \in S, \\
f_k^{rs} &\ge 0, && k \in K_{rs},\ r \in R,\ s \in S, \\
x_a &= \sum_{r, s}\sum_{k \in K_{rs}} f_k^{rs}\,\delta_{a,k}^{rs}, && a \in A.
\end{aligned}
$$ (eq-13-beckmann)

The objective is the sum of the areas under the link performance functions.
It has no behavioral or economic interpretation of its own; it is a
mathematical construction whose optimality conditions happen to be
Wardrop's conditions. (It should not be confused with the total travel time
$\sum_a x_at_a(x_a)$, which is the objective of the system optimum in
{doc}`14-system-optimum-and-elastic-demand`.)

### Equivalence with the equilibrium conditions

:::{prf:theorem} Equivalence of Beckmann's program and the user equilibrium
:label: thm-13-beckmann-ue

If the link performance functions are continuous and non-decreasing, a
feasible path flow pattern solves {eq}`eq-13-beckmann` if and only if it
satisfies the user equilibrium conditions {eq}`eq-13-ue-conditions`.
:::

:::{dropdown} Proof
:class-container: proof
:animate: fade-in

Substituting {eq}`eq-13-link-path-flow` into the objective makes $z$ a function
of the path flows only, with linear constraints. Introduce a multiplier
$u_{rs}$ for each conservation constraint and $v_k^{rs} \ge 0$ for each
non-negativity constraint. The Lagrangian is

$$
\begin{aligned}
L(\bff, \bu, \bv) = z\big(\bx(\bff)\big)
&+ \sum_{r, s} u_{rs}\Big(q_{rs} - \sum_{k \in K_{rs}} f_k^{rs}\Big) \\
&- \sum_{r, s}\sum_{k \in K_{rs}} v_k^{rs} f_k^{rs}.
\end{aligned}
$$

By the chain rule and the fundamental theorem of calculus,

$$
\begin{aligned}
\frac{\partial z}{\partial f_k^{rs}} &= \sum_{a \in A} \frac{\partial z}{\partial x_a}\,\frac{\partial x_a}{\partial f_k^{rs}} \\
&= \sum_{a \in A} t_a(x_a)\,\delta_{a,k}^{rs} \\
&= c_k^{rs} .
\end{aligned}
$$

The KKT conditions ({prf:ref}`thm-03-kkt`) are therefore

$$
\begin{aligned}
c_k^{rs} - u_{rs} - v_k^{rs} &= 0, \\
v_k^{rs} &\ge 0, \\
v_k^{rs} f_k^{rs} &= 0,
\end{aligned}
$$

plus feasibility. Eliminating $v_k^{rs} = c_k^{rs} - u_{rs}$ gives
$c_k^{rs} - u_{rs} \ge 0$ and $f_k^{rs}(c_k^{rs} - u_{rs}) = 0$, which are
exactly {eq}`eq-13-ue-conditions`. The constraints are linear, so the KKT
conditions are necessary at a minimum; the objective is convex (shown
below), so they are also sufficient. The multiplier $u_{rs}$ is the
equilibrium O-D travel time.
:::

### Uniqueness of link flows

The Hessian of $z$ with respect to the link flows is diagonal, because each
term of the objective depends on one link flow only:

$$
\nabla^2_{\bx} z(\bx) = \diag\left(t_1'(x_1),\ t_2'(x_2),\ \ldots,\ t_{|A|}'(x_{|A|})\right).
$$

If every $t_a$ is strictly increasing, the Hessian is positive definite, $z$
is strictly convex in $\bx$, and the feasible set (a linear image of a
polyhedron) is convex. Hence the **equilibrium link flows are unique**
({prf:ref}`thm-03-convex-program`).

### Non-uniqueness of path flows

In terms of path flows the Hessian is
$\nabla^2_{\bff} z = \bDelta\T\diag(t_a')\bDelta$,
which is only positive **semi**-definite (singular) whenever the columns of
$\bDelta$ are linearly dependent, as they must be when there are more paths
than links and as they often are when paths overlap. Then different path
flow patterns can produce the same unique link flows, and the **equilibrium path flows are not unique in
general** ({prf:ref}`ex-28-ue-nonunique`). This matters in practice: analyses
that need path flows, such as select-link analysis or O-D matrix estimation
from counts, must choose among the equilibrium path flows, for example by
maximizing entropy.

## Solution algorithms

### All-or-nothing assignment

:::{prf:algorithm} All-or-nothing (AON) assignment
:label: alg-13-aon

**Inputs:** fixed link travel times $\{t_a\}$ and the O-D matrix.

1. For each origin $r$, find the shortest paths to all destinations
   ({prf:ref}`alg-03-label-correcting`).
2. Load the whole demand $q_{rs}$ on the shortest path from $r$ to $s$.
3. The flow on each link is the sum of the flows of the paths that use it.
:::

AON ignores congestion: it is the assignment that results if travel times
do not depend on flows (or the first step of a model that later corrects
the times). It is useful for uncongested networks, and it is the building
block of the equilibrium algorithms below. With congestion, the AON flows
are not an equilibrium: the shortest paths become overloaded and their times
exceed those of the paths left empty ({prf:ref}`ex-28-ue-aon`).

### The Frank–Wolfe method

Beckmann's program has a convex objective and linear constraints, so the
Frank–Wolfe method ({prf:ref}`alg-03-frank-wolfe`) applies. Its direction
finding step minimizes the linearized objective,

$$
\min_{\by}\ \nabla z(\bx^{(n)})\T\by = \sum_{a} t_a\big(x_a^{(n)}\big)\,y_a,
$$

over the feasible link flows. With the link times fixed at
$t_a^{(n)} = t_a(x_a^{(n)})$, the cheapest way to send every O-D flow is to
put it on its shortest path: the linear subproblem is an **all-or-nothing
assignment**. LeBlanc, Morlok, and Pierskalla (1975) introduced this
algorithm to traffic assignment; it is available in all planning software
packages, such as Visum, EMME, and TransCAD, which now also offer the faster
methods described at the end of this section.

:::{prf:algorithm} Frank–Wolfe method for the user equilibrium
:label: alg-13-fw-ue

1. **Initialization.** Perform an AON assignment with free-flow times
   $t_a(0)$. This gives $\bx^{(1)}$. Set $n = 1$.
2. **Update.** Set $t_a^{(n)} = t_a\big(x_a^{(n)}\big)$ for all $a$.
3. **Direction finding.** Perform an AON assignment with the times
   $t_a^{(n)}$. This gives the auxiliary flows $\by^{(n)}$.
4. **Line search.** Find $\alpha_n \in [0, 1]$ that minimizes
   $z\big(\bx^{(n)} + \alpha(\by^{(n)} - \bx^{(n)})\big)$.
5. **Move.** Set $\bx^{(n+1)} = \bx^{(n)} + \alpha_n\big(\by^{(n)} - \bx^{(n)}\big)$.
6. **Convergence test.** If a stopping criterion is met, stop; otherwise
   set $n \leftarrow n + 1$ and return to step 2.
:::

The line search in step 4 is one-dimensional. Its objective is convex in
$\alpha$, and its derivative is

$$
\frac{\diff}{\diff\alpha}\,
z\big(\bx^{(n)} + \alpha(\by^{(n)} - \bx^{(n)})\big)
= \sum_{a \in A} t_a\big(x_a^{(n)} + \alpha(y_a^{(n)} - x_a^{(n)})\big)\big(y_a^{(n)} - x_a^{(n)}\big),
$$ (eq-13-fw-line-search)

so $\alpha_n$ is the root of {eq}`eq-13-fw-line-search` in $[0, 1]$, found by
bisection ({prf:ref}`alg-03-bisection`), or in closed form when the functions
are linear; if the derivative is negative at $\alpha = 1$, then
$\alpha_n = 1$.

### Stopping criteria

Common stopping criteria compare successive iterations:

$$
\begin{aligned}
&\text{(1)}\quad z\big(\bx^{(n)}\big) - z\big(\bx^{(n+1)}\big) \le \varepsilon, \\
&\text{(2)}\quad \sum_{r, s}\frac{\big|u_{rs}^{(n+1)} - u_{rs}^{(n)}\big|}{u_{rs}^{(n)}} \le \varepsilon, \\
&\text{(3)}\quad \frac{\sqrt{\sum_a\big(x_a^{(n+1)} - x_a^{(n)}\big)^2}}{\sum_a x_a^{(n)}} \le \varepsilon .
\end{aligned}
$$

They measure progress rather than distance from equilibrium, and an
algorithm that moves slowly can satisfy them far from the solution. A better
measure follows from the Frank–Wolfe gap {eq}`eq-03-fw-gap`: since
$\nabla z = \bt(\bx)$,

$$
\begin{aligned}
\mathrm{RG}^{(n)} &= \frac{\sum_a t_a^{(n)}\big(x_a^{(n)} - y_a^{(n)}\big)}{\sum_a t_a^{(n)}x_a^{(n)}} \\
&= \frac{\sum_a t_a^{(n)}x_a^{(n)} - \sum_{r,s} q_{rs}u_{rs}^{(n)}}{\sum_a t_a^{(n)}x_a^{(n)}} .
\end{aligned}
$$ (eq-13-relative-gap)

The numerator is the total travel time of the current flows minus the total
travel time if everybody could travel at the current shortest-path times; it
is zero only at equilibrium, and it bounds $z(\bx^{(n)}) - z(\bx^*)$ from
above. The **relative gap** {eq}`eq-13-relative-gap` is the standard
convergence measure of planning software, with typical targets of $10^{-4}$
or less.

### The method of successive averages

The **method of successive averages (MSA)** replaces the line search by a
predetermined step size:

:::{prf:algorithm} Method of successive averages (MSA)
:label: alg-13-msa-ue

Steps 1–3 and 6 as in {prf:ref}`alg-13-fw-ue`; replace steps 4 and 5 by

$$
\bx^{(n+1)} = \bx^{(n)} + \frac{1}{n}\big(\by^{(n)} - \bx^{(n)}\big).
$$
:::

The first step ($\alpha_1 = 1$) discards the initial flows, and by induction

$$
\bx^{(n+1)} = \frac{1}{n}\sum_{m=1}^{n}\by^{(m)} :
$$

the current flows are the plain average of all the auxiliary AON flows,
which gives the method its name. Any step sizes $\alpha_n$ with
$\sum_n \alpha_n = \infty$ and $\sum_n \alpha_n^2 < \infty$ guarantee
convergence (Robbins and Monro, 1951; Blum, 1954; Powell and Sheffi, 1982),
and $1/n$ is the simplest choice. MSA does not need the objective function, which makes it the method
of choice for stochastic assignment ({doc}`15-stochastic-user-equilibrium`).
For the deterministic UE it is slower than Frank–Wolfe: early steps
overshoot, late steps are too short, and the objective can increase from one
iteration to the next ({prf:ref}`ex-28-ue-fw-three-link`).

### Beyond Frank–Wolfe

Frank–Wolfe slows down near the solution because successive AON directions
zigzag between a few extreme points ({prf:ref}`ex-28-hw4-q2-due`). Faster
methods keep more information between iterations: **path-based** algorithms
(gradient projection, Jayakrishnan et al., 1994) shift flow between the
used paths of each O-D pair, and **origin- or bush-based** algorithms
(Bar-Gera, 2002; Dial, 2006) work with acyclic subnetworks rooted at each
origin. They reach relative gaps of $10^{-8}$ or smaller and also produce
consistent path flows. The TNTP benchmark networks
(<https://github.com/bstabler/TransportationNetworks>) are widely used to
compare them.

## Summary and Common Mistakes

### Summary

- Wardrop's first principle: at the user equilibrium, all used paths of an
  O-D pair have equal and minimum travel time, and no unused path is
  quicker.
- Feasible path flows satisfy conservation and non-negativity
  {eq}`eq-13-flow-conservation`; link flows and path costs follow through the
  link–path incidences {eq}`eq-13-link-path-flow` and {eq}`eq-13-path-cost`.
- The equilibrium conditions {eq}`eq-13-ue-conditions` are complementarity
  conditions between path flows and excess path costs
  $c_k^{rs} - u_{rs}$.
- Beckmann's program {eq}`eq-13-beckmann` has the equilibrium conditions as
  its KKT conditions ({prf:ref}`thm-13-beckmann-ue`); with strictly
  increasing link functions the link flows are unique, the path flows
  generally are not.
- Frank–Wolfe ({prf:ref}`alg-13-fw-ue`) solves the program by AON
  assignments ({prf:ref}`alg-13-aon`) and line searches
  {eq}`eq-13-fw-line-search`; MSA ({prf:ref}`alg-13-msa-ue`) uses the step
  $1/n$. The relative gap {eq}`eq-13-relative-gap` measures convergence.

### Common mistakes

- **Setting path times equal without checking the result.** The guess of
  used paths can be wrong: check that every flow is non-negative and that no
  unused path is quicker, and change the guess otherwise.
- **Treating Beckmann's objective as the total travel time.** The integral
  {eq}`eq-13-beckmann` has no behavioral meaning; the total travel time
  $\sum_a x_at_a(x_a)$ is the objective of the system optimum.
- **Expecting unique path flows.** Only the link flows are unique; many path
  flow patterns can produce them ({prf:ref}`ex-28-ue-nonunique`).
- **Starting Frank–Wolfe from zero flows.** Zero flows do not satisfy flow
  conservation; the starting point must be feasible, hence the initial AON
  assignment.
- **Stopping on a fixed number of iterations or on the change in flows.**
  These measure progress, not distance from equilibrium; report the relative
  gap {eq}`eq-13-relative-gap`.
- **Forgetting the end points in the line search.** If the derivative
  {eq}`eq-13-fw-line-search` is still negative at $\alpha = 1$, the step is
  $\alpha_n = 1$, not the (non-existent) root in $[0, 1]$.

## References

- Bar-Gera, H. (2002). Origin-based algorithm for the traffic assignment
  problem. *Transportation Science*, *36*(4), 398–417.
- Beckmann, M., McGuire, C. B., & Winsten, C. B. (1956). *Studies in the
  Economics of Transportation*. Yale University Press.
- Blum, J. R. (1954). Multidimensional stochastic approximation methods.
  *Annals of Mathematical Statistics*, *25*(4), 737–744.
  <https://doi.org/10.1214/aoms/1177728659>
- Cambridge Systematics et al. (2012). *Travel Demand Forecasting:
  Parameters and Techniques* (NCHRP Report 716), Section 4.11.
  Transportation Research Board. <https://doi.org/10.17226/14665>
- Dial, R. B. (2006). A path-based user-equilibrium traffic assignment
  algorithm that obviates path storage and enumeration. *Transportation
  Research Part B*, 40(10), 917–936.
- Jayakrishnan, R., Tsai, W. K., Prashker, J. N., & Rajadhyaksha, S.
  (1994). A faster path-based algorithm for traffic assignment.
  *Transportation Research Record*, *1443*, 75–83.
- LeBlanc, L. J., Morlok, E. K., & Pierskalla, W. P. (1975). An efficient
  approach to solving the road network equilibrium traffic assignment
  problem. *Transportation Research*, *9*(5), 309–318.
- Ortúzar, J. de D., & Willumsen, L. G. (2011). *Modelling Transport* (4th
  ed.), Chapters 10 and 11. Wiley.
- Powell, W. B., & Sheffi, Y. (1982). The convergence of equilibrium
  algorithms with predetermined step sizes. *Transportation Science*, *16*(1),
  45–55.
- Robbins, H., & Monro, S. (1951). A stochastic approximation method.
  *Annals of Mathematical Statistics*, *22*(3), 400–407.
  <https://doi.org/10.1214/aoms/1177729586>
- Sheffi, Y. (1985). *Urban Transportation Networks: Equilibrium Analysis
  with Mathematical Programming Methods*, Sections 1.3, 3.1–3.3, 4.3, and
  5.1–5.3. Prentice-Hall.
- Wardrop, J. G. (1952). Some theoretical aspects of road traffic research.
  *Proceedings of the Institution of Civil Engineers, Part II*, *1*(3),
  325–378. <https://doi.org/10.1680/ipeds.1952.11259>
