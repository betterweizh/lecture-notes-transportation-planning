# Sampling and Survey Design

This chapter works through the examples and problems of
{doc}`07-travel-surveys-and-sampling`.

## Efficiency of stratified sampling

:::{prf:example} Simple random versus stratified sampling
:label: ex-22-sampling-efficiency

The households of an area are classified by car ownership (with or without
a car) and size (up to four, or more than four residents). From historical
data the four cells contain the following shares of households:

| | Up to 4 residents | More than 4 residents |
|---|---|---|
| With car | 9 % | 16 % |
| Without car | 25 % | 50 % |

To estimate daily trip rates with 95 % confidence, $m$ observations are
required in every cell. How many households must be interviewed with simple
random sampling, and with stratified sampling?
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**Simple random sampling.** A random sample of $n$ households contains on
average $n$ times the cell share in each cell. The binding cell is the
smallest one (9 %), which needs $0.09\,n \ge m$:

$$
n = \frac{m}{0.09} \approx 11.1\,m .
$$

The other cells then receive $0.16n = 1.8m$, $0.25n = 2.8m$, and
$0.50n = 5.6m$ observations — far more than needed.

**Stratified sampling.** First carry out a cheap screening survey that only
asks each contacted household which cell it belongs to, and continue until
$m$ households of the rarest cell have been found (about $11.1m$ short
contacts). Then interview in detail $m$ households of each cell, selected at
random within the cell:

$$
n = m + m + m + m = 4m \ \ll\ 11.1\,m .
$$

The number of full (expensive) interviews falls by about 64 %. The saving
is real as long as a screening contact costs much less than a full
interview.
:::

## The three sampling methods compared

:::{prf:example} Joint distributions under three sampling methods
:label: ex-22-three-samples

In a population, travelers to work have low (LI) or high (HI) income and
use bus (B) or car (C). The population joint distribution
$\Pr(Y, X)$ is

| | LI | HI | Total |
|---|---|---|---|
| Bus | 0.45 | 0.15 | 0.60 |
| Car | 0.20 | 0.20 | 0.40 |
| Total | 0.65 | 0.35 | 1.00 |

Find the joint distribution in (a) a simple random sample, (b) a sample
stratified with 75 % low-income and 25 % high-income travelers, and (c) a
choice-based sample with 75 % bus users and 25 % car users. (d) For each
sample, compute the probability that a high-income traveler uses the car,
and (e) show how weighting corrects the choice-based sample.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**(a) Simple random sample.** By {eq}`eq-07-srs-joint`, the sample joint
distribution equals the population table.

**(b) Stratified sample.** By {eq}`eq-07-stratified-joint`,
$f(Y, X) = f(X)\Pr(Y \mid X) = f(X)\Pr(Y, X)/\Pr(X)$ with
$f(\mathrm{LI}) = 0.75$ and $f(\mathrm{HI}) = 0.25$. For example,

$$
\begin{aligned}
f(\mathrm{B}, \mathrm{LI}) &= 0.75 \times \frac{0.45}{0.65} = 0.519, \\
f(\mathrm{C}, \mathrm{HI}) &= 0.25 \times \frac{0.20}{0.35} = 0.143 .
\end{aligned}
$$

| | LI | HI | Total |
|---|---|---|---|
| Bus | 0.519 | 0.107 | 0.626 |
| Car | 0.231 | 0.143 | 0.374 |
| Total | 0.750 | 0.250 | 1.000 |

**(c) Choice-based sample.** Now $f(Y, X) = f(Y)\Pr(X \mid Y)
= f(Y)\Pr(Y, X)/\Pr(Y)$ with $f(\mathrm{B}) = 0.75$ and
$f(\mathrm{C}) = 0.25$. For example,

$$
\begin{aligned}
f(\mathrm{B}, \mathrm{LI}) &= 0.75 \times \frac{0.45}{0.60} = 0.5625, \\
f(\mathrm{C}, \mathrm{HI}) &= 0.25 \times \frac{0.20}{0.40} = 0.125 .
\end{aligned}
$$

| | LI | HI | Total |
|---|---|---|---|
| Bus | 0.5625 | 0.1875 | 0.750 |
| Car | 0.1250 | 0.1250 | 0.250 |
| Total | 0.6875 | 0.3125 | 1.000 |

**(d) Probability that a high-income traveler uses the car.**

$$
\begin{aligned}
\text{population / random sample:}\quad
\Pr(\mathrm{C} \mid \mathrm{HI}) &= \frac{0.20}{0.35} = 0.571, \\
\text{stratified sample:}\quad
f(\mathrm{C} \mid \mathrm{HI}) &= \frac{0.143}{0.250} = 0.571, \\
\text{choice-based sample:}\quad
f(\mathrm{C} \mid \mathrm{HI}) &= \frac{0.125}{0.3125} = 0.400 .
\end{aligned}
$$

The stratified sample reproduces the population conditional probability, as
{eq}`eq-07-stratified-property` predicts; the choice-based sample does not —
it under-represents car users, so a mode-choice model estimated from it
would under-predict car use.

**(e) Weighting.** By {eq}`eq-07-weight`,

$$
\begin{aligned}
w_{\mathrm{B}} &= \frac{\Pr(\mathrm{B})}{f(\mathrm{B})} = \frac{0.60}{0.75} = 0.8, \\
w_{\mathrm{C}} &= \frac{\Pr(\mathrm{C})}{f(\mathrm{C})} = \frac{0.40}{0.25} = 1.6 .
\end{aligned}
$$

Applying {eq}`eq-07-choice-based-weights` to the high-income column of the
choice-based sample,

$$
\begin{aligned}
\Pr(\mathrm{C} \mid \mathrm{HI})
&= \frac{w_{\mathrm{C}}\, f(\mathrm{C}, \mathrm{HI})}
        {w_{\mathrm{B}}\, f(\mathrm{B}, \mathrm{HI}) + w_{\mathrm{C}}\, f(\mathrm{C}, \mathrm{HI})} \\
&= \frac{1.6 \times 0.125}{0.8 \times 0.1875 + 1.6 \times 0.125}
 = \frac{0.200}{0.350} = 0.571,
\end{aligned}
$$

and $\Pr(\mathrm{B} \mid \mathrm{HI}) = 0.150/0.350 = 0.429$: the weights
recover the population probabilities exactly.
:::

## Sizes of subpopulations

:::{prf:example} Mode shares from on-mode surveys
:label: ex-22-subpopulation-shares

In an area of 180 000 inhabitants, the average income is \$33 600 per year
and average car ownership is 0.44 cars per household. Small on-mode surveys
give the following averages for the users of each mode:

| Mode | Income (\$/year) | Car ownership (cars/household) |
|---|---|---|
| Car | 78 000 | 1.15 |
| Bus | 14 400 | 0.05 |
| Metro | 38 400 | 0.85 |

Estimate the share $F_m$ of the population using each mode.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

The population averages are weighted averages of the mode averages, with the
unknown shares as weights, and the shares sum to one:

$$
\begin{aligned}
78\,000\,F_1 + 14\,400\,F_2 + 38\,400\,F_3 &= 33\,600, \\
1.15\,F_1 + 0.05\,F_2 + 0.85\,F_3 &= 0.44, \\
F_1 + F_2 + F_3 &= 1 .
\end{aligned}
$$

Eliminate $F_3 = 1 - F_1 - F_2$ from the first two equations:

$$
\begin{aligned}
39\,600\,F_1 - 24\,000\,F_2 &= -4\,800, \\
0.30\,F_1 - 0.80\,F_2 &= -0.41 .
\end{aligned}
$$

Multiplying the second equation by 30 000 and subtracting it from the first
gives $30\,600\,F_1 = 7\,500$, so

$$
\begin{aligned}
F_1 &= 0.2451, \\
F_2 &= \frac{0.41 + 0.30 F_1}{0.80} = 0.6044, \\
F_3 &= 1 - F_1 - F_2 = 0.1505 .
\end{aligned}
$$

With 180 000 inhabitants there are about 44 100 car users, 108 800 bus
users, and 27 100 metro users. *Check:*
$78\,000(0.2451) + 14\,400(0.6044) + 38\,400(0.1505) = 33\,600$ and
$1.15(0.2451) + 0.05(0.6044) + 0.85(0.1505) = 0.440$.
:::

## Sample sizes

:::{prf:example} Sample size for a mean trip rate
:label: ex-22-household-sample-size

The number of daily trips per household is to be estimated with a relative
error of 5 % at 90 % confidence. Studies in three similar cities report
coefficients of variation of 0.86, 1.07, and 1.05. (a) How many households
must be surveyed? (b) How many must be contacted if the response rate is
25 %? (c) What would a 10 % error at 95 % confidence require?
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**(a)** Take $\mathrm{CV} \approx (0.86 + 1.07 + 1.05)/3 = 0.99 \approx 1.0$
and $z_{0.05} = 1.645$. By {eq}`eq-07-sample-size-cv`,

$$
\begin{aligned}
n &= \frac{z_{\alpha/2}^2\,\mathrm{CV}^2}{E^2} \\
&= \frac{1.645^2 \times 1.0^2}{0.05^2} = 1\,082.4 ,
\end{aligned}
$$

so about 1 100 completed household surveys give trip rates within 5 % of the
true mean, 90 % of the time. The population size does not matter as long as
it is much larger than the sample.

**(b)** With a 25 % response rate, about $1\,083/0.25 \approx 4\,330$
households must be contacted — and the analyst should check whether
non-respondents travel differently from respondents.

**(c)** With $E = 0.10$ and $z_{0.025} = 1.96$,
$n = 1.96^2/0.1^2 \times \mathrm{CV}^2 = 384.2\,\mathrm{CV}^2$, that is
385 households for $\mathrm{CV} = 1.0$: doubling the acceptable error while raising the
confidence level still cuts the sample to about a third.
:::

:::{prf:example} Sample size for a roadside interview survey
:label: ex-22-roadside-sample-size

At a roadside interview station, the share of vehicles traveling between a
given O-D pair is to be estimated with an absolute error of at most
$e = 0.1$ at 95 % confidence. Find the conservative sample size for flows of
$N = 100$, 500, 1 000, 2 000, 5 000, and 10 000 vehicles in the survey
period.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

With $e/z_{\alpha/2} = 0.1/1.96 = 0.05102$, so
$(e/z_{\alpha/2})^2 = 0.002603$, formula {eq}`eq-07-sample-size-conservative`
gives

$$
n^{*} = \frac{0.25}{0.002603 + 0.25/N}.
$$

| Flow $N$ (veh/period) | 100 | 500 | 1 000 | 2 000 | 5 000 | 10 000 |
|---|---|---|---|---|---|---|
| $n^*$ (rounded up) | 49 | 81 | 88 | 92 | 95 | 96 |
| sampling rate $n^*/N$ | 49 % | 16 % | 8.8 % | 4.6 % | 1.9 % | 1.0 % |

The sample size approaches $0.25/0.002603 = 96.04$, that is 97, as $N$ grows: for busy
roads a small sampling rate suffices, while on quiet roads a large fraction
of vehicles must be stopped.
:::

## Population shares from two samples

:::{prf:example} Stratified and choice-based samples
:label: ex-22-hw1-q4

Two samples of a population are classified by income and mode (car, bus,
underground). The stratified (by income) sample has the joint distribution

| Mode | Low income | Medium income | High income |
|---|---|---|---|
| Car | 3.33 % | 18.00 % | 20.00 % |
| Bus | 33.34 % | 7.20 % | 4.00 % |
| Underground | 3.33 % | 4.80 % | 6.00 % |
| Total | 40.00 % | 30.00 % | 30.00 % |

and the choice-based sample has

| Mode | Low income | Medium income | High income | Total |
|---|---|---|---|---|
| Car | 6.67 % | 20.00 % | 13.33 % | 40.00 % |
| Bus | 17.24 % | 2.07 % | 0.69 % | 20.00 % |
| Underground | 16.67 % | 13.33 % | 10.00 % | 40.00 % |

(a) The income shares of the population are 60 %, 25 %, and 15 %. Find the
joint distribution of a random sample. (b) Compute the weighting factors
needed to estimate a mode-choice model from the choice-based sample with
software written for random samples.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**(a)** In a sample stratified by income, the conditional mode shares within
each income group equal those of the population
({eq}`eq-07-stratified-property`), so

$$
\Pr(Y, X) = \Pr(X)\,\Pr(Y \mid X) = \Pr(X)\,\frac{f(Y, X)}{f(X)} .
$$

For low income, $\Pr(X) / f(X) = 0.60/0.40 = 1.5$; for medium income,
$0.25/0.30 = 0.8\overline{3}$; for high income, $0.15/0.30 = 0.5$. Hence

$$
\begin{aligned}
\Pr(\text{car}, \text{low}) &= 1.5 \times 3.33\,\% = 5.0\,\%, \\
\Pr(\text{bus}, \text{medium}) &= 0.8\overline{3} \times 7.20\,\% = 6.0\,\%, \\
\Pr(\text{underground}, \text{high}) &= 0.5 \times 6.00\,\% = 3.0\,\%,
\end{aligned}
$$

and so on. (The 3.33 % and 33.34 % entries are the rounded values of
$40\,\% \times 1/12$ and $40\,\% \times 10/12$, so the low-income entries
are exactly 5 %, 50 %, and 5 %.)

| Mode | Low income | Medium income | High income | Total |
|---|---|---|---|---|
| Car | 5.0 % | 15.0 % | 10.0 % | 30.0 % |
| Bus | 50.0 % | 6.0 % | 2.0 % | 58.0 % |
| Underground | 5.0 % | 4.0 % | 3.0 % | 12.0 % |
| Total | 60.0 % | 25.0 % | 15.0 % | 100 % |

**(b)** The population mode shares are the row totals of (a), and the sample
shares are the row totals of the choice-based table. By {eq}`eq-07-weight`,

$$
\begin{aligned}
w_{\text{car}} &= \frac{0.30}{0.40} = 0.75, \\
w_{\text{bus}} &= \frac{0.58}{0.20} = 2.90, \\
w_{\text{underground}} &= \frac{0.12}{0.40} = 0.30 .
\end{aligned}
$$

Each observation is weighted by the factor of its chosen mode in the
log-likelihood (WESML). Bus users, under-sampled relative to the population,
receive weights above one.

*Consistency check.* The choice-based table should equal
$f(Y)\Pr(X \mid Y)$. For example,
$f(\text{bus}, \text{low}) = 0.20 \times 0.50/0.58 = 17.24\,\%$ and
$f(\text{car}, \text{medium}) = 0.40 \times 0.15/0.30 = 20.00\,\%$, in
agreement with the data, so both samples come from the population found in
(a).
:::
