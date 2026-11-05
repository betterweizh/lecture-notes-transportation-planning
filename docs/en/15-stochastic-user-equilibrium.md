# Traffic Assignment III: Stochastic User Equilibrium

## Overview

Wardrop's first principle assumes that every traveler knows the travel
time of every path exactly. Real travelers do not: they perceive travel
times with error, and different travelers perceive them differently. The
**stochastic user equilibrium (SUE)** treats the perceived path travel time
as a random variable and applies the random utility theory of
{doc}`11-discrete-choice-models` to route choice. This chapter defines the SUE,
derives the logit- and probit-based versions, presents Fisk's convex
program for the logit SUE, and describes the stochastic loading methods and
the method of successive averages used to compute it.

:::{admonition} Learning objectives
:class: objectives
After completing this chapter, readers should be able to:

- explain the difference between deterministic and stochastic user
  equilibrium;
- write the SUE conditions and their logit and probit versions;
- formulate Fisk's program and show that its optimality conditions are the
  logit SUE conditions;
- perform logit, probit, and Monte Carlo stochastic network loadings; and
- solve the SUE with the method of successive averages.
:::

## Notation

| Symbol | Meaning |
|---|---|
| $C_k^{rs}$ | perceived travel time of path $k$, a random variable |
| $c_k^{rs}(\bff)$ | mean (deterministic) path travel time |
| $\varepsilon_k^{rs}$ | perception error of path $k$ |
| $P_k^{rs}$ | probability that path $k$ is perceived as the shortest |
| $\theta$ | dispersion parameter of the logit route choice model |
| $T_a$, $\zeta_a$ | perceived link travel time and its random error |
| $\bSigma$ | covariance matrix of the path perception errors |

## Perceived travel times

The perceived travel time of path $k$ between $r$ and $s$ has a
deterministic part and a random part:

$$
\begin{aligned}
C_k^{rs}(\bff) &= c_k^{rs}(\bff) + \varepsilon_k^{rs}, \\
\E\big[\varepsilon_k^{rs}\big] &= 0,
\end{aligned}
$$ (eq-15-perceived-cost)

where $c_k^{rs}(\bff) = \sum_a t_a(x_a)\,\delta_{a,k}^{rs}$ is the mean
travel time, which depends on the flows as before. The random term
represents variations in perception across travelers (and, from the
analyst's point of view, unobserved attributes of the routes). Each
traveler chooses the path that he or she **perceives** to be the shortest.
Travelers of the same O-D pair therefore spread over several paths, and the
shortest path in mean travel time does not attract everybody.

For given flows, and hence given mean travel times, the share of travelers
choosing path $k$ is the probability that its perceived time is the
smallest,

$$
P_k^{rs}(\bff) = \Prob\left(C_k^{rs} \le C_l^{rs},\ \forall l \in K_{rs}\right),
$$

exactly as in random utility maximization with utility
$U_k = -C_k^{rs}$.

## The stochastic user equilibrium

Daganzo and Sheffi (1977) defined the SUE as the state in which no traveler
believes that he or she can improve the perceived travel time by changing
route unilaterally. The flow on each path is then the demand times the
probability that the path is perceived as the shortest, evaluated at the
equilibrium flows:

$$
f_k^{rs} = q_{rs}\,\Prob\left(c_k^{rs}(\bff) + \varepsilon_k^{rs}
\le c_l^{rs}(\bff) + \varepsilon_l^{rs},\ \forall l \in K_{rs}\right),
\qquad k \in K_{rs},\ r \in R,\ s \in S .
$$ (eq-15-sue)

These are fixed-point conditions: the probabilities depend on the flows
through the travel times, and the flows depend on the probabilities. As the
variance of the perception errors goes to zero, the SUE tends to the
deterministic user equilibrium; as it grows, travel times matter less and
less, and the travelers tend to spread evenly over the paths.

### Logit-based SUE

If the errors $\varepsilon_k^{rs}$ are independent and identically
distributed Gumbel variables, the choice probabilities are multinomial logit
({prf:ref}`thm-11-mnl`), and the **logit-based SUE** conditions are

$$
f_k^{rs} = q_{rs}\,\frac{\exp\left[-\theta c_k^{rs}(\bff)\right]}
{\sum_{l \in K_{rs}}\exp\left[-\theta c_l^{rs}(\bff)\right]},
\qquad k \in K_{rs},\ r \in R,\ s \in S .
$$ (eq-15-logit-sue)

The dispersion parameter $\theta > 0$ is inversely related to the standard
deviation of the perception errors (the Gumbel scale, $\mu = \theta$, so the
error variance is $\pi^2/(6\theta^2)$). A large $\theta$ means small errors
and a solution close to the DUE.

Because the logit model depends only on the differences of path times, a
time difference of 10 min produces the same split on a 15-min trip as on a
2-hour trip, which is unrealistic. The logit model also inherits the IIA
property {eq}`eq-11-iia`: two paths that share most of their links are treated
as independent alternatives and together receive too much flow. Corrections
such as C-logit (Cascetta et al., 1996) and path-size logit (Ben-Akiva and
Bierlaire, 1999) add an overlap term to the path utility; the probit model below handles overlap naturally.

### Probit-based SUE

If the path errors follow a multivariate normal distribution with mean zero
and covariance matrix $\bSigma$, the conditions {eq}`eq-15-sue` are
**probit-based**. A natural way to build $\bSigma$ is to give
each link an independent perception error $\zeta_a$ with variance
$\sigma_a^2$, so that the perceived link time is $T_a = t_a(x_a) + \zeta_a$
and the path error is the sum of the errors of its links:

$$
\begin{aligned}
\varepsilon_k^{rs} &= \sum_a \zeta_a\,\delta_{a,k}^{rs}, \\
\Cov\big[\varepsilon_k^{rs}, \varepsilon_l^{rs}\big] &= \sum_a \sigma_a^2\,\delta_{a,k}^{rs}\delta_{a,l}^{rs} .
\end{aligned}
$$ (eq-15-probit-covariance)

In matrix form $\bSigma = \bDelta\T\diag(\sigma_a^2)\bDelta$.
Overlapping paths share links and are therefore positively correlated, which
removes the overlap problem of the logit model. Daganzo and Sheffi (1977)
suggest variances proportional to the free-flow link time,
$\sigma_a^2 = \xi\,t_a^0$, which also makes the path variance grow with
trip length. The price is that probit probabilities have no closed form for
more than two paths and are computed by simulation.

## Fisk's formulation of the logit SUE

Fisk (1980) showed that the logit SUE solves the program

$$
\begin{aligned}
\min_{\bff}\ z(\bff) &= \frac{1}{\theta}\sum_{r, s}\sum_{k \in K_{rs}} f_k^{rs}\left(\ln f_k^{rs} - 1\right)
+ \sum_a \int_0^{x_a} t_a(\omega)\,\diff\omega \\
\text{s.t.}\quad
\sum_{k \in K_{rs}} f_k^{rs} &= q_{rs}, \\
f_k^{rs} &\ge 0,
\end{aligned}
$$ (eq-15-fisk)

with $x_a$ given by {eq}`eq-13-link-path-flow`. The first term is (minus) the
entropy of the path flows, as in the entropy-maximizing derivation of the
gravity model; the second is Beckmann's objective.

:::{prf:theorem} Fisk's program and the logit SUE
:label: thm-15-fisk

The path flows that solve {eq}`eq-15-fisk` satisfy the logit SUE conditions
{eq}`eq-15-logit-sue`, and the solution is unique in path flows.
:::

:::{dropdown} Proof
:class-container: proof
:animate: fade-in

With multipliers $u_{rs}$ and $v_k^{rs} \ge 0$ as in
{prf:ref}`thm-13-beckmann-ue`, and since

$$
\frac{\partial z}{\partial f_k^{rs}} = \frac{1}{\theta}\ln f_k^{rs} + c_k^{rs},
$$

the KKT conditions are

$$
\begin{aligned}
\frac{1}{\theta}\ln f_k^{rs} + c_k^{rs} - u_{rs} - v_k^{rs} &= 0, \\
v_k^{rs}f_k^{rs} &= 0, \\
v_k^{rs} &\ge 0 .
\end{aligned}
$$

As $f_k^{rs} \to 0$, $\ln f_k^{rs} \to -\infty$, so a zero path flow cannot
satisfy the first condition: every path carries positive flow, and
$v_k^{rs} = 0$. Then
$f_k^{rs} = \exp(\theta u_{rs})\exp(-\theta c_k^{rs})$, and summing over
$k \in K_{rs}$ and using conservation,

$$
\begin{aligned}
\exp(\theta u_{rs}) &= \frac{q_{rs}}{\sum_{l \in K_{rs}}\exp(-\theta c_l^{rs})}, \\
f_k^{rs} &= q_{rs}\,\frac{\exp(-\theta c_k^{rs})}{\sum_{l \in K_{rs}}\exp(-\theta c_l^{rs})} .
\end{aligned}
$$

This is {eq}`eq-15-logit-sue`. For uniqueness, the Hessian of $z$ in path flows
is

$$
\nabla^2_{\bff} z = \frac{1}{\theta}\diag\left(\frac{1}{f_k^{rs}}\right)
+ \bDelta\T\diag\big(t_a'(x_a)\big)\bDelta,
$$

the sum of a positive definite diagonal matrix and a positive semi-definite
matrix. It is positive definite, so $z$ is strictly convex in the path flows
and the solution is unique — in contrast with the DUE, where only the link
flows are unique.
:::

At the SUE every path receives some flow, however long it is: the logit
model assigns a positive probability to every alternative. In practice the
path set is restricted to "reasonable" paths, for example those that move
away from the origin and towards the destination (the STOCH algorithm of
Dial, 1971), or those generated by repeated shortest-path searches.

## Stochastic network loading

A **stochastic network loading** computes the path and link flows for
**fixed** link travel times $\{t_a\}$: it evaluates the right-hand side of
{eq}`eq-15-sue` once. It plays the role that the AON assignment plays for the
DUE. Three methods are used.

**Logit loading.** With the path times
$c_k^{rs} = \sum_a t_a\,\delta_{a,k}^{rs}$, apply {eq}`eq-15-logit-sue`
directly. With path enumeration this is straightforward for small
networks; Dial's algorithm performs the same loading on large networks
without enumerating paths ({prf:ref}`ex-30-sue-logit-loading`).

**Analytical probit loading.** For two paths, the probability that path 1
is perceived as shorter is a normal CDF:

$$
\begin{aligned}
\Prob\big(C_1 \le C_2\big) &= \Prob\big(\varepsilon_1 - \varepsilon_2 \le c_2 - c_1\big) \\
&= \Phi\left(\frac{c_2 - c_1}{\sqrt{\Var[\varepsilon_1 - \varepsilon_2]}}\right),
\end{aligned}
$$ (eq-15-probit-two-paths)

where, with independent link errors, $\Var[\varepsilon_1 - \varepsilon_2]$
is the sum of the variances of the links that belong to exactly one of the
two paths; shared links cancel ({prf:ref}`ex-30-sue-probit-loading`).

**Monte Carlo loading.** For more paths, the probit probabilities are
estimated by simulation (Sheffi, 1985, Section 11.2):

:::{prf:algorithm} Monte Carlo (simulation) stochastic loading
:label: alg-15-monte-carlo-loading

**Inputs:** mean link times $\{t_a\}$, error distributions, O-D matrix, and
a tolerance $\varepsilon$.

1. Set $n = 1$ and $\bx^{(0)} = \bzero$.
2. **Sampling.** Draw a perceived time $T_a^{(n)}$ for every link from its
   distribution.
3. **All-or-nothing assignment.** Assign every O-D flow to its shortest path
   with link times $T_a^{(n)}$. This gives the link flows $\bX^{(n)}$.
4. **Averaging.** Set
   $x_a^{(n)} = \big[(n - 1)\,x_a^{(n-1)} + X_a^{(n)}\big]/n$ for all $a$.
5. **Stopping test.** If $n > 1$ and the change of the averaged flows,
   for example $\max_a \lvert x_a^{(n)} - x_a^{(n-1)}\rvert/x_a^{(n-1)}$
   over the links with positive flow, is at most $\varepsilon$, stop.
   Otherwise set $n \leftarrow n + 1$ and return to step 2.
:::

Each draw represents a traveler (or a group of travelers) with a
particular perception of the network. The averaged flows converge to the
probit loading at the slow rate $1/\sqrt{n}$ of all simulations, so a small
change between successive averages is a weak stopping criterion; in
practice a fixed, large number of draws is used
({prf:ref}`ex-30-sue-monte-carlo`).

## The method of successive averages for the SUE

The SUE combines a stochastic loading with the congestion feedback of the
DUE. Fisk's objective could be minimized with Frank–Wolfe-type methods, but
the loading of the probit model is a simulation, its objective function
(Sheffi and Powell, 1982) is expensive to evaluate, and the loaded flows are
noisy. The **method of successive averages** avoids the line search and
tolerates noise (Sheffi and Powell, 1982):

:::{prf:algorithm} MSA for the stochastic user equilibrium
:label: alg-15-msa-sue

1. **Initialization.** Perform a stochastic loading with the free-flow times
   $t_a(0)$. This gives $\bx^{(1)}$. Set $n = 1$.
2. **Update.** Set $t_a^{(n)} = t_a\big(x_a^{(n)}\big)$ for all $a$.
3. **Direction finding.** Perform a stochastic loading with the times
   $t_a^{(n)}$. This gives the auxiliary flows $\by^{(n)}$.
4. **Move.** Set $\bx^{(n+1)} = \bx^{(n)} + \frac{1}{n}\big(\by^{(n)} - \bx^{(n)}\big)$.
5. **Convergence test.** If
   $\sqrt{\sum_a\big(x_a^{(n+1)} - x_a^{(n)}\big)^2}\big/\sum_a x_a^{(n)} \le \varepsilon$,
   stop; otherwise set $n \leftarrow n + 1$ and return to step 2.
:::

The algorithm is {prf:ref}`alg-13-msa-ue` with the AON assignment replaced by a
stochastic loading. Because the step size shrinks as $1/n$, the noise of a
Monte Carlo loading is averaged out over the iterations; a single draw per
iteration is enough in principle. The stopping criterion is again weak,
because the step itself becomes small; a better check compares the current
flows with a fresh loading at the current times
({prf:ref}`ex-30-sue-msa`).

### DUE and SUE compared

| | DUE | SUE |
|---|---|---|
| Information | perfect | perceived with error |
| Path choice | only minimum-time paths are used | every path has a positive probability |
| Conditions | {eq}`eq-13-ue-conditions` | {eq}`eq-15-sue` |
| Program | Beckmann {eq}`eq-13-beckmann` | Fisk {eq}`eq-15-fisk` (logit) |
| Uniqueness | link flows | link and path flows (logit) |
| Loading | AON | logit, probit, Monte Carlo |
| Algorithm | Frank–Wolfe, MSA, path- or bush-based | MSA |

The SUE is closer to observed behavior on networks with many similar
routes, and it spreads flow over parallel routes even when congestion is
light. Its parameters ($\theta$, or the error variances) must be calibrated,
for example against observed route choices or link counts.

## Summary and Common Mistakes

### Summary

- The SUE assumes that travelers minimize perceived travel times
  {eq}`eq-15-perceived-cost`; path flows equal demand times the probability
  of being perceived as the shortest {eq}`eq-15-sue`.
- Gumbel errors give the logit SUE {eq}`eq-15-logit-sue`; normal errors built
  from link errors {eq}`eq-15-probit-covariance` give the probit SUE, with
  correlated overlapping paths.
- Fisk's program {eq}`eq-15-fisk` adds an entropy term to Beckmann's
  objective; its unique solution is the logit SUE ({prf:ref}`thm-15-fisk`).
- Stochastic loadings — logit, analytical probit
  {eq}`eq-15-probit-two-paths`, and Monte Carlo
  ({prf:ref}`alg-15-monte-carlo-loading`) — replace AON, and MSA
  ({prf:ref}`alg-15-msa-sue`) solves the equilibrium.

### Common mistakes

- **Expecting zero flow on long paths at the SUE.** The logit model gives
  every enumerated path a positive probability, so every path is used;
  restrict the path set instead.
- **Applying the logit model to heavily overlapping paths without a
  correction.** IIA treats them as independent and overloads them; use a
  correction term or the probit model.
- **Confusing a stochastic loading with the stochastic user equilibrium.** A
  loading uses fixed times; at the equilibrium the times depend on the
  flows.
- **Using too few Monte Carlo draws, or judging convergence only by the
  change between successive averages.** Simulation error falls like
  $1/\sqrt{n}$, and small steps do not mean small errors.
- **Forgetting that $\theta$ has units.** It is measured per unit of time:
  its value depends on whether times are in minutes or hours.

## References

- Ben-Akiva, M., & Bierlaire, M. (1999). Discrete choice methods and their
  applications to short term travel decisions. In R. W. Hall (Ed.),
  *Handbook of Transportation Science* (pp. 5–33). Kluwer.
- Cascetta, E., Nuzzolo, A., Russo, F., & Vitetta, A. (1996). A modified
  logit route choice model overcoming path overlapping problems:
  Specification and some calibration results for interurban networks. In
  J.-B. Lesort (Ed.), *Transportation and Traffic Theory* (pp. 697–711).
  Pergamon.
- Daganzo, C. F., & Sheffi, Y. (1977). On stochastic models of traffic
  assignment. *Transportation Science*, *11*(3), 253–274.
- Dial, R. B. (1971). A probabilistic multipath traffic assignment model
  which obviates path enumeration. *Transportation Research*, *5*(2), 83–111.
- Fisk, C. (1980). Some developments in equilibrium traffic assignment.
  *Transportation Research Part B*, *14*(3), 243–255.
- Ortúzar, J. de D., & Willumsen, L. G. (2011). *Modelling Transport* (4th
  ed.), Chapters 10 and 11. Wiley.
- Sheffi, Y. (1985). *Urban Transportation Networks: Equilibrium Analysis
  with Mathematical Programming Methods*, Sections 10.1–10.2 and Chapters
  11–12. Prentice-Hall.
- Sheffi, Y., & Powell, W. B. (1982). An algorithm for the equilibrium
  assignment problem with random link times. *Networks*, *12*(2), 191–207.
