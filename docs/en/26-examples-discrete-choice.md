# Modal Split: Discrete Choice

This chapter works through the examples and problems of
{doc}`11-discrete-choice-models`, including estimation and sampling
problems. The code in {doc}`35-python-mode-choice` reproduces the numbers.

## Binary logit

:::{prf:example} Car or transit between two towns
:label: ex-26-dc-binary

Commuters between two towns choose between car and transit with utilities

$$
\begin{aligned}
U_{\mathrm{car}} &= 0.5 - 0.25\,T_{\mathrm{car}} - 0.42\,E_{\mathrm{car}} - 1.25\,C_{\mathrm{car}} + \varepsilon_{\mathrm{car}}, \\
U_{\mathrm{transit}} &= -0.25\,T_{\mathrm{transit}} - 0.42\,E_{\mathrm{transit}} - 1.25\,C_{\mathrm{transit}} + \varepsilon_{\mathrm{transit}},
\end{aligned}
$$

where $T$ is in-vehicle time (min), $E$ access time (min), $C$ cost (S\$),
and the disturbances are i.i.d. Gumbel with $\mu = 1$. The average values
are $T = (25, 30)$, $E = (5, 8)$, $C = (3, 1)$ for (car, transit).

(1) Compute the mode shares. (2) Recompute them if a S\$1 toll is added to
the car cost. (3) Compute the direct elasticity of the car share with
respect to the car cost, and the implied value of in-vehicle time.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**(1)** The systematic utilities are

$$
\begin{aligned}
V_{\mathrm{car}} &= 0.5 - 0.25 \times 25 - 0.42 \times 5 - 1.25 \times 3 = -11.60, \\
V_{\mathrm{transit}} &= -0.25 \times 30 - 0.42 \times 8 - 1.25 \times 1 = -12.11,
\end{aligned}
$$

so by {eq}`eq-11-binary-logit`

$$
\begin{aligned}
P(\mathrm{car}) &= \frac{1}{1 + e^{V_{\mathrm{transit}} - V_{\mathrm{car}}}} \\
&= \frac{1}{1 + e^{-0.51}} \\
&= 0.625, \\
P(\mathrm{transit}) &= 0.375 .
\end{aligned}
$$

**(2)** The toll lowers the car utility by $1.25 \times 1 = 1.25$:
$V^*_{\mathrm{car}} = -12.85$, so

$$
P^*(\mathrm{car}) = \frac{1}{1 + e^{-12.11 + 12.85}} = \frac{1}{1 + e^{0.74}} = 0.323,
$$

and the transit share rises to 0.677.

**(3)** By {eq}`eq-11-direct-elasticity`,

$$
\begin{aligned}
E^{P(\mathrm{car})}_{C_{\mathrm{car}}} &= \beta_C\,C_{\mathrm{car}}\left[1 - P(\mathrm{car})\right] \\
&= -1.25 \times 3 \times 0.375 = -1.41 :
\end{aligned}
$$

a 1 % increase in the car cost reduces the car share by about 1.4 %. The
value of in-vehicle time is $\beta_T/\beta_C = 0.25/1.25 = $ S\$0.20 per
minute (S\$12 per hour), and access time is valued
$0.42/0.25 = 1.7$ times as highly as in-vehicle time.
:::

## Maximum likelihood

:::{prf:example} Likelihood and maximum likelihood estimation
:label: ex-26-dc-likelihood

Six travelers choose between two public transport modes A and B:

| Traveler | Age | Time by A (min) | Time by B (min) | Choice |
|---|---|---|---|---|
| 1 | 35 | 15.4 | 58.2 | A |
| 2 | 45 | 14.2 | 31.0 | B |
| 3 | 37 | 19.6 | 43.6 | A |
| 4 | 42 | 50.8 | 59.9 | A |
| 5 | 32 | 55.5 | 33.8 | B |
| 6 | 15 | not available | 48.4 | B |

The utilities are

$$
\begin{aligned}
V_A &= \beta_0 + \beta_1 t_A + \beta_2\,\mathrm{Age}_{<20} + \beta_3\,\mathrm{Age}_{>40}, \\
V_B &= \beta_1 t_B,
\end{aligned}
$$

where the age dummies equal 1 for travelers younger than 20 and older than
40, respectively. (a) Write the choice probabilities and compute the
likelihood at $(\beta_0, \beta_1, \beta_2, \beta_3) = (0.5, -0.1, 0.1, -0.1)$.
(b) Find the maximum likelihood estimates and $\rho^2$.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**Which observations count.** Traveler 6 has only mode B available; the
choice is certain and contributes $\ln 1 = 0$ to the log-likelihood. As a
consequence, the only traveler younger than 20 is not used and **$\beta_2$
cannot be estimated** from these data.

**(a) Probabilities.** With $V_A - V_B = \beta_0 + \beta_1(t_A - t_B) + \beta_3\mathrm{Age}_{>40}$,

$$
\begin{aligned}
P_1(A) &= \frac{1}{1 + \exp\left(-\beta_0 + 42.8\beta_1\right)}, \\
P_2(B) &= \frac{1}{1 + \exp\left(\beta_0 - 16.8\beta_1 + \beta_3\right)}, \\
P_3(A) &= \frac{1}{1 + \exp\left(-\beta_0 + 24.0\beta_1\right)}, \\
P_4(A) &= \frac{1}{1 + \exp\left(-\beta_0 + 9.1\beta_1 - \beta_3\right)}, \\
P_5(B) &= \frac{1}{1 + \exp\left(\beta_0 + 21.7\beta_1\right)} .
\end{aligned}
$$

At $(0.5, -0.1, 0.1, -0.1)$:

$$
\begin{aligned}
P_1(A) &= 0.9917, \\
P_2(B) &= 0.1111, \\
P_3(A) &= 0.9478, \\
P_4(A) &= 0.7875, \\
P_5(B) &= 0.8416,
\end{aligned}
$$

and the likelihood is their product,
$\mathcal{L} = 0.0692$ ($LL = -2.671$). Other parameter values give
$\mathcal{L} = 3.64\times 10^{-4}$ at $(0, -0.5, 0.5, -0.5)$ and
$2.49\times 10^{-43}$ at $(0, 1, 0.5, -0.5)$: the likelihood measures how
well each set of parameters reproduces the observed choices.

**(b) Maximum likelihood.** Maximizing
$LL = \ln P_1(A) + \ln P_2(B) + \ln P_3(A) + \ln P_4(A) + \ln P_5(B)$ over
$(\beta_0, \beta_1, \beta_3)$ with Newton–Raphson from zero gives

$$
\begin{aligned}
\hat\beta_0 &= -0.037, \\
\hat\beta_1 &= -0.102~\text{per minute}, \\
\hat\beta_3 &= -1.28, \\
LL(\hat\bbeta) &= -2.016 .
\end{aligned}
$$

The equally-likely model has $LL(\bzero) = 5\ln 0.5 = -3.466$, so

$$
\rho^2 = 1 - \frac{-2.016}{-3.466} = 0.418 .
$$

The time coefficient has the expected negative sign. The standard errors
from the inverse Hessian, however, are 2.41, 0.094, and 2.95, so with five
observations no coefficient is significant ($|t| < 1.1$); the example only
illustrates the method.
:::

## Applications of choice models

:::{prf:example} Choice with a uniformly distributed income
:label: ex-26-hw3-q3

Travelers choose between modes $a$ and $b$ with travel times $t_a$ and $t_b$
and utilities

$$
\begin{aligned}
U_a &= \alpha t_a + \beta I, \\
U_b &= \alpha t_b,
\end{aligned}
$$

where $\alpha = -0.5$, $\beta = 1.5\times 10^{-4}$, and the income $I$ is
uniformly distributed between 5 000 and 25 000 (density
$0.5\times 10^{-4}$). (a) Find the probability of choosing $a$ as a function
of $t_b - t_a$. (b) Sketch it.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**(a)** For an individual, $a$ is chosen if $U_a \ge U_b$:

$$
\alpha t_a + \beta I \ge \alpha t_b
\iff I \ge \frac{\alpha(t_b - t_a)}{\beta} = -\frac{10^4}{3}\left(t_b - t_a\right) =: I^{*}.
$$

Here income plays the role of the random term. Since
$I \sim \mathcal{U}(5\,000, 25\,000)$,

$$
P_a = \Prob(I \ge I^{*}) =
\begin{cases}
1, & I^{*} \le 5\,000, \\[2pt]
\dfrac{25\,000 - I^{*}}{20\,000}, & 5\,000 < I^{*} < 25\,000, \\[6pt]
0, & I^{*} \ge 25\,000 .
\end{cases}
$$

In terms of $\Delta = t_b - t_a$ (minutes),
$I^{*} \le 5\,000 \iff \Delta \ge -1.5$ and
$I^{*} \ge 25\,000 \iff \Delta \le -7.5$,
so

$$
P_a(\Delta) =
\begin{cases}
1, & \Delta \ge -1.5, \\[2pt]
1.25 + \dfrac{\Delta}{6}, & -7.5 < \Delta < -1.5, \\[6pt]
0, & \Delta \le -7.5 .
\end{cases}
$$

**(b)** The graph of $P_a$ against $\Delta$ is a ramp: zero up to
$\Delta = -7.5$, rising linearly with slope $1/6$ per minute, and equal to
one from $\Delta = -1.5$ onwards; $P_a = 0.5$ at $\Delta = -4.5$. Because
of the income bonus, everybody chooses $a$ unless it is more than 1.5 min
slower, and nobody chooses it if it is more than 7.5 min slower.

This is the **linear probability model** {eq}`eq-11-linear-probability`: a
uniformly distributed random term produces a linear ramp with kinks.
:::

:::{prf:example} A nested logit model
:label: ex-26-hw3-q4

Car (c), shared taxi (st), and mass transit (mt) form the upper level of a
nested logit model; mass transit is a nest containing bus (b) and
underground (u). The utilities are

$$
\begin{aligned}
V_c &= -0.03\,t_c - 0.15\,c_c + 1.30, \\
V_{st} &= -0.03\,t_{st} - 0.15\,c_{st} - 0.25, \\
V_b &= -0.04\,t_b - 0.02\,c_b + 0.6, \\
V_u &= -0.04\,t_u - 0.02\,c_u, \\
V_{mt} &= 0.60\,\mathrm{EMU}, \\
\mathrm{EMU} &= \ln\left(e^{V_b} + e^{V_u}\right),
\end{aligned}
$$

with $\mu = 1$ and the average values

| | Car | Shared taxi | Bus | Underground |
|---|---|---|---|---|
| Time $t$ | 4.5 | 5.5 | 7.5 | 5.4 |
| Cost/income $c$ | 23.0 | 15.0 | 5.5 | 3.6 |

Compute the probability of each mode.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**Lower nest.**

$$
\begin{aligned}
V_b &= -0.04 \times 7.5 - 0.02 \times 5.5 + 0.6 = 0.190, \\
V_u &= -0.04 \times 5.4 - 0.02 \times 3.6 = -0.288,
\end{aligned}
$$

$$
\begin{aligned}
P(b \mid mt) &= \frac{e^{0.190}}{e^{0.190} + e^{-0.288}} = 0.617, \\
P(u \mid mt) &= 0.383,
\end{aligned}
$$

and $\mathrm{EMU} = \ln(e^{0.190} + e^{-0.288}) = 0.672$.

**Upper level.**

$$
\begin{aligned}
V_c &= -0.03 \times 4.5 - 0.15 \times 23 + 1.30 = -2.285, \\
V_{st} &= -0.03 \times 5.5 - 0.15 \times 15 - 0.25 = -2.665, \\
V_{mt} &= 0.60 \times 0.672 = 0.403,
\end{aligned}
$$

$$
\begin{aligned}
P_c &= \frac{e^{-2.285}}{e^{-2.285} + e^{-2.665} + e^{0.403}} = 0.061, \\
P_{st} &= 0.042, \\
P_{mt} &= 0.897 .
\end{aligned}
$$

**Unconditional probabilities.**

$$
\begin{aligned}
P_b &= 0.897 \times 0.617 = 0.554, \\
P_u &= 0.897 \times 0.383 = 0.343 .
\end{aligned}
$$

| Mode | Car | Shared taxi | Bus | Underground |
|---|---|---|---|---|
| Probability | 0.061 | 0.042 | 0.554 | 0.343 |

The structural parameter 0.60 lies in $(0, 1]$, as required: bus and
underground share unobserved attributes (both are mass transit), so an
improvement of the bus draws proportionally more from the underground than
from the car.
:::

:::{prf:example} Correcting a model estimated on a choice-based sample
:label: ex-26-hw3-q5

A binary logit model ($\mu = 1$) for car and bus was estimated on a sample
from one sector of a city:

$$
\begin{aligned}
V_c &= 3.0 - 0.25\,t_c - 0.4\,e_c - 0.1\,c_c, \\
V_b &= -0.25\,t_b - 0.4\,e_b - 0.1\,c_b,
\end{aligned}
$$

with in-vehicle time $t$ (min), access time $e$ (min), and cost $c$; the
average values are $t = (25, 40)$, $e = (5, 8)$, $c = (140, 50)$ for
(car, bus). In the sample, 220 chose car and 630 bus; in the whole
population, 17 000 chose car and 69 000 bus.

(a) What correction must be applied to the model? (b) By what percentage
does the probability of choosing car change if bus fares rise by 25 %?
(c) What if car costs rise by 100 %?
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**Diagnosis.** With the average data,

$$
\begin{aligned}
V_c &= 3.0 - 6.25 - 2.0 - 14.0 = -19.25, \\
V_b &= -10.0 - 3.2 - 5.0 = -18.20,
\end{aligned}
$$

so $P_c = 1/(1 + e^{1.05}) = 0.259$. This equals the car share of the
*sample*, $H_c = 220/850 = 0.259$, but the population share is
$Q_c = 17\,000/86\,000 = 0.198$. The sample over-represents car users — a
choice-based sample — and the model inherits the bias.

**(a) Correction.** For a logit model with alternative-specific constants
estimated on a choice-based sample, only the constants are biased. By
{eq}`eq-11-asc-correction`, with the bus constant normalized to zero,

$$
\begin{aligned}
K_c' &= K_c - \ln\frac{H_c}{Q_c} + \ln\frac{H_b}{Q_b} \\
&= 3.0 - \ln\frac{0.2588}{0.1977} + \ln\frac{0.7412}{0.8023} \\
&= 3.0 - 0.2695 - 0.0793 = 2.651,
\end{aligned}
$$

and the corrected model is

$$
\begin{aligned}
V_c &= 2.651 - 0.25\,t_c - 0.4\,e_c - 0.1\,c_c, \\
V_b &= -0.25\,t_b - 0.4\,e_b - 0.1\,c_b .
\end{aligned}
$$

Check: now $V_c = -19.599$ and $P_c = 1/(1 + e^{1.399}) = 0.198 = Q_c$.

**(b) Bus fare +25 %.** $c_b = 62.5$, so $V_b = -19.45$ and

$$
P_c = \frac{1}{1 + e^{-19.45 + 19.599}} = \frac{1}{1 + e^{0.149}} = 0.463,
$$

an increase of $0.463/0.198 - 1 = 134\,\%$. The response is large because
the fare rise lowers the bus utility by 1.25, while the two modes differed
by only 1.4 utility units.

**(c) Car cost +100 %.** $c_c = 280$, so $V_c = 2.651 - 6.25 - 2.0 - 28.0 = -33.60$
and $P_c = 1/(1 + e^{15.40}) = 2.1\times 10^{-7}$: virtually everybody would
take the bus.
:::

:::{prf:example} Specifying a likelihood from stated-preference data
:label: ex-26-hw3-q6

A stated-preference survey of six choices between modes A and B gave:

| Person | Time A (min) | Cost A (S\$) | Time B (min) | Cost B (S\$) | Salary $s$ (S\$1000/month) | Choice |
|---|---|---|---|---|---|---|
| 1 | 10 | 1.8 | 15 | 1.0 | 3.0 | B |
| 2 | 10 | 1.8 | 15 | 1.0 | 4.0 | A |
| 3 | 5 | 4.0 | 20 | 0.8 | 3.5 | B |
| 4 | 5 | 4.0 | 20 | 0.8 | 6.0 | A |
| 5 | 8 | 3.0 | 18 | 0.9 | 4.5 | B |
| 6 | 8 | 3.0 | 18 | 0.9 | 6.5 | A |

(a) Define linear utility functions. (b) Write the log-likelihood function
for estimating them by maximum likelihood.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**(a) Utilities.** Time and cost are attributes of both modes and get
generic coefficients; salary does not vary across modes, so it can enter
only one utility, together with a single constant:

$$
\begin{aligned}
V_A^n &= \beta_0 + \beta_t\,t_A^n + \beta_c\,c_A^n + \beta_s\,s^n, \\
V_B^n &= \beta_t\,t_B^n + \beta_c\,c_B^n .
\end{aligned}
$$

**(b) Log-likelihood.** With binary logit,
$P_A^n = 1/[1 + \exp(V_B^n - V_A^n)]$ and $P_B^n = 1 - P_A^n$, where

$$
V_A^n - V_B^n = \beta_0 + \beta_t\left(t_A^n - t_B^n\right) + \beta_c\left(c_A^n - c_B^n\right) + \beta_s s^n .
$$

The differences are $(t_A - t_B, c_A - c_B) = (-5, 0.8)$ for persons 1–2,
$(-15, 3.2)$ for persons 3–4, and $(-10, 2.1)$ for persons 5–6. The observed
choices are B, A, B, A, B, A, so

$$
\begin{aligned}
LL(\beta_0, \beta_t, \beta_c, \beta_s)
&= \ln P_B^1 + \ln P_A^2 + \ln P_B^3 + \ln P_A^4 + \ln P_B^5 + \ln P_A^6 \\
&= -\ln\left(1 + e^{\beta_0 - 5\beta_t + 0.8\beta_c + 3.0\beta_s}\right)
   - \ln\left(1 + e^{-\beta_0 + 5\beta_t - 0.8\beta_c - 4.0\beta_s}\right) \\
&\quad - \ln\left(1 + e^{\beta_0 - 15\beta_t + 3.2\beta_c + 3.5\beta_s}\right)
   - \ln\left(1 + e^{-\beta_0 + 15\beta_t - 3.2\beta_c - 6.0\beta_s}\right) \\
&\quad - \ln\left(1 + e^{\beta_0 - 10\beta_t + 2.1\beta_c + 4.5\beta_s}\right)
   - \ln\left(1 + e^{-\beta_0 + 10\beta_t - 2.1\beta_c - 6.5\beta_s}\right).
\end{aligned}
$$

**Can it be maximized?** Not with these data. Within each pair of persons
the attributes are identical and the richer person chooses A, so some
parameter vector classifies all six choices correctly — for example
$(\beta_0, \beta_t, \beta_c, \beta_s) = (-10.43, 0, -2.86, 3.43)$ makes
$V_A - V_B$ negative for persons 1, 3, 5 and positive for 2, 4, 6.
Multiplying such a vector by an ever larger factor drives every probability
of the observed choice towards one and $LL$ towards 0, so the maximum is
not attained (**perfect separation**). Estimation requires more, and more
varied, responses — in SP practice each respondent answers several choice
tasks — or fewer parameters.
:::
