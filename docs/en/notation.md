# Notation

The symbols below are used consistently throughout the book. Chapter-specific
symbols are defined in the notation table at the start of each chapter.

## Key symbols

The ten symbols that appear in almost every chapter:

| Symbol | Meaning | First used in |
|---|---|---|
| $i, j$ | origin and destination zones, $i, j = 1, \ldots, z$ | {doc}`04-biproportional-fitting` |
| $O_i$, $D_j$ | trips produced by (originating in) zone $i$ and attracted to (destined for) zone $j$ | {doc}`04-biproportional-fitting` |
| $T_{ij}$ | trips from zone $i$ to zone $j$ (trip matrix entry) | {doc}`04-biproportional-fitting` |
| $c_{ij}$ | generalized cost of travel from $i$ to $j$ | {doc}`04-biproportional-fitting` |
| $G = (N, A)$ | directed network with node set $N$ and link set $A$ | {doc}`06-zoning-and-networks` |
| $x_a$, $t_a(x_a)$ | flow on link $a$ and its travel time (link performance function) | {doc}`06-zoning-and-networks` |
| $q_{rs}$ | travel demand from origin $r$ to destination $s$ | {doc}`13-user-equilibrium-assignment` |
| $f_k^{rs}$, $c_k^{rs}$ | flow and travel time on path $k$ between $r$ and $s$ | {doc}`13-user-equilibrium-assignment` |
| $\delta_{a,k}^{rs}$ | link–path incidence: 1 if link $a$ lies on path $k$ of pair $rs$ | {doc}`13-user-equilibrium-assignment` |
| $U_{in} = V_{in} + \varepsilon_{in}$ | random utility of alternative $i$ for traveler $n$ | {doc}`11-discrete-choice-models` |

The sections below list the symbols by topic.

## General conventions

| Convention | Meaning | First used in |
|---|---|---|
| $x$, $\bx$, $\bX$ | scalars in italics; vectors in bold lower case; matrices in bold upper case | {doc}`02-regression-and-hypothesis-tests` |
| $\bx\T$ | transpose | {doc}`02-regression-and-hypothesis-tests` |
| $\R^n$ | $n$-dimensional real space | {doc}`02-regression-and-hypothesis-tests` |
| $\E[\cdot]$, $\Var[\cdot]$, $\Cov[\cdot,\cdot]$ | expectation, variance, covariance | {doc}`01-probability-distributions` |
| $\Prob(\cdot)$, $\Pr(\cdot)$ | probability (in the population) | {doc}`01-probability-distributions` |
| $f(\cdot)$ | a density, or a probability in a sample ({doc}`07-travel-surveys-and-sampling`) | {doc}`01-probability-distributions` |
| $\mathcal{N}(\mu, \sigma^2)$ | normal distribution with mean $\mu$ and **variance** $\sigma^2$ | {doc}`01-probability-distributions` |
| $\Phi(\cdot)$ | standard normal CDF | {doc}`01-probability-distributions` |
| $\hat\theta$ | estimate of a parameter $\theta$ | {doc}`02-regression-and-hypothesis-tests` |
| $\mathbb{1}[\cdot]$ | indicator function | {doc}`17-examples-probability` |

## Space and demand

| Symbol | Meaning | First used in |
|---|---|---|
| $i, j$; $z$ | origin and destination zones; number of zones | {doc}`04-biproportional-fitting` |
| $O_i$, $D_j$ | trips produced by / originating in zone $i$; attracted to / destined for zone $j$ | {doc}`04-biproportional-fitting` |
| $T_{ij}$, $T$ | trips from $i$ to $j$; total trips | {doc}`04-biproportional-fitting` |
| $T_{ij}^k$ | trips from $i$ to $j$ by mode $k$ | {doc}`12-aggregate-modal-split` |
| $c_{ij}$ | generalized cost from $i$ to $j$ | {doc}`04-biproportional-fitting` |
| $f(c_{ij})$ | deterrence function of a gravity model | {doc}`10-trip-distribution` |
| $\tau$, $\tau_i$, $\Gamma_j$ | overall, origin, and destination growth factors | {doc}`10-trip-distribution` |
| $t_{ij}$ | seed (prior or base-year) matrix in bi-proportional fitting | {doc}`04-biproportional-fitting` |
| $a_i$, $b_j$; $A_i$, $B_j$ | balancing factors of bi-proportional and gravity models | {doc}`04-biproportional-fitting` |
| $W\{T_{ij}\}$ | number of micro-states producing the matrix $\{T_{ij}\}$ (entropy maximization) | {doc}`04-biproportional-fitting` |
| $E$, $L$, $F$ | activity system, level of service, and flow in the demand–performance framework | {doc}`05-transportation-planning-process` |

## Networks and assignment

| Symbol | Meaning | First used in |
|---|---|---|
| $G = (N, A)$ | directed network: node set $N$, link set $A$ | {doc}`06-zoning-and-networks` |
| $a \in A$ | a link | {doc}`06-zoning-and-networks` |
| $x_a$, $\bx$ | flow on link $a$; vector of link flows | {doc}`06-zoning-and-networks` |
| $t_a(x_a)$ | link performance (travel time) function | {doc}`06-zoning-and-networks` |
| $t_a^0$, $c_a$ | free-flow travel time and capacity of link $a$ | {doc}`06-zoning-and-networks` |
| $r, s$; $q_{rs}$ | origin and destination nodes; demand between them | {doc}`13-user-equilibrium-assignment` |
| $K_{rs}$ | set of paths from $r$ to $s$ | {doc}`13-user-equilibrium-assignment` |
| $f_k^{rs}$, $c_k^{rs}$ | flow and travel time on path $k \in K_{rs}$ | {doc}`13-user-equilibrium-assignment` |
| $\delta_{a,k}^{rs}$ | 1 if link $a$ is on path $k$ of pair $rs$, 0 otherwise | {doc}`13-user-equilibrium-assignment` |
| $u_{rs}$ | minimum (equilibrium) travel time between $r$ and $s$ | {doc}`13-user-equilibrium-assignment` |
| $\by$ | auxiliary (all-or-nothing or stochastic-loading) link flows | {doc}`13-user-equilibrium-assignment` |
| $\tilde t_a(x_a)$ | marginal cost $t_a + x_at_a'(x_a)$ (system optimum) | {doc}`14-system-optimum-and-elastic-demand` |
| $\tau_a$ | link toll in time units (not to be confused with the growth factors $\tau_i$) | {doc}`14-system-optimum-and-elastic-demand` |
| $e_{rs}$, $\bar q_{rs}$ | excess demand and demand upper bound (elastic demand) | {doc}`14-system-optimum-and-elastic-demand` |
| $\theta$ | dispersion parameter of logit route choice (SUE) | {doc}`15-stochastic-user-equilibrium` |
| $s$, $t^*$ | bottleneck capacity and preferred arrival time (dynamic models) | {doc}`16-dynamic-assignment-and-simulation` |

## Choice models

| Symbol | Meaning | First used in |
|---|---|---|
| $C_n$ | choice set of decision maker $n$ | {doc}`11-discrete-choice-models` |
| $U_{in} = V_{in} + \varepsilon_{in}$ | utility of alternative $i$ for $n$: systematic part plus random part | {doc}`11-discrete-choice-models` |
| $P_n(i)$ | probability that $n$ chooses $i$ | {doc}`11-discrete-choice-models` |
| $\mu$ | scale parameter of Gumbel and logistic random terms | {doc}`01-probability-distributions` |
| $\btheta$, $\bbeta$ | parameters of a choice or regression model | {doc}`02-regression-and-hypothesis-tests` |

## Statistics

| Symbol | Meaning | First used in |
|---|---|---|
| $N$, $n$ | population and sample sizes | {doc}`07-travel-surveys-and-sampling` |
| $\bar{x}$, $s^2$ | sample mean and variance | {doc}`02-regression-and-hypothesis-tests` |
| $\mathrm{CV}$ | coefficient of variation $\sigma/\mu$ | {doc}`07-travel-surveys-and-sampling` |
| $z_{\alpha}$, $t_{\alpha,\nu}$ | upper-$\alpha$ quantiles of the standard normal and $t(\nu)$ distributions | {doc}`02-regression-and-hypothesis-tests` |
| $\mathit{SS}_T$, $\mathit{SS}_R$, $\mathit{SS}_E$ | total, regression, and error sums of squares | {doc}`02-regression-and-hypothesis-tests` |
| $R^2$, $\bar{R}^2$, $R_0^2$ | coefficient of determination, adjusted, and uncentered | {doc}`02-regression-and-hypothesis-tests` |
| $e_x$ | error (standard deviation) of a measured quantity $x$ | {doc}`08-errors-and-uncertainty` |
| $e_s$, $e_m$ | specification error and propagated measurement error of a model | {doc}`08-errors-and-uncertainty` |
| $w_Y$ | weight of choice-based sample stratum $Y$ (WESML) | {doc}`07-travel-surveys-and-sampling` |

## Optimization

| Symbol | Meaning | First used in |
|---|---|---|
| $f(\bx)$, $\Omega$ | objective function and feasible set | {doc}`03-nonlinear-optimization` |
| $\nabla f$, $\nabla^2 f$ | gradient and Hessian | {doc}`03-nonlinear-optimization` |
| $g_i \le 0$, $h_j = 0$ | inequality and equality constraints | {doc}`03-nonlinear-optimization` |
| $u_i$, $\lambda_j$ | KKT multipliers | {doc}`03-nonlinear-optimization` |
| $\mathcal{L}$ | Lagrangian (likelihood function in the choice-model chapters) | {doc}`03-nonlinear-optimization` |
| $\alpha$ | step size | {doc}`03-nonlinear-optimization` |
