# Errors and Uncertainty

This chapter works through the examples and problems of
{doc}`08-errors-and-uncertainty`.

## Error propagation through basic operations

:::{prf:example} Sums, differences, products, ratios, and powers
:label: ex-23-error-operations

Two independent variables are measured as $x = 10 \pm 1$ and $y = 8 \pm 1$
(relative errors 10 % and 12.5 %). Compute the value, absolute error, and
relative error of $z = x + y$, $x - y$, $xy$, $x/y$, and $x^2$.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

Apply {eq}`eq-08-error-propagation-indep`,
$e_z^2 = (\partial z/\partial x)^2 e_x^2 + (\partial z/\partial y)^2 e_y^2$.

*Addition*, $z = 18$: both derivatives are 1, so

$$
\begin{aligned}
e_z &= \sqrt{1^2 + 1^2} = 1.41, \\
\frac{e_z}{z} &= \frac{1.41}{18} = 7.9\,\%.
\end{aligned}
$$

*Subtraction*, $z = 2$: the derivatives are $1$ and $-1$, so again
$e_z = 1.41$, but

$$
\frac{e_z}{z} = \frac{1.41}{2} = 70.7\,\%.
$$

*Multiplication*, $z = 80$: $\partial z/\partial x = y = 8$ and
$\partial z/\partial y = x = 10$, so

$$
\begin{aligned}
e_z &= \sqrt{8^2 \times 1^2 + 10^2 \times 1^2} = \sqrt{164} = 12.8, \\
\frac{e_z}{z} &= \sqrt{0.10^2 + 0.125^2} = 16.0\,\%.
\end{aligned}
$$

*Division*, $z = 1.25$: $\partial z/\partial x = 1/y = 0.125$ and
$\partial z/\partial y = -x/y^2 = -0.156$, so

$$
\begin{aligned}
e_z &= \sqrt{0.125^2 + 0.156^2} = 0.200, \\
\frac{e_z}{z} &= 16.0\,\%.
\end{aligned}
$$

*Power*, $z = x^2 = 100$: $\partial z/\partial x = 2x = 20$, so

$$
\begin{aligned}
e_z &= 20 \times 1 = 20, \\
\frac{e_z}{z} &= 2 \times 10\,\% = 20\,\%.
\end{aligned}
$$

| Operation | $z$ | $e_z$ | $e_z/z$ |
|---|---|---|---|
| $x + y$ | 18 | 1.41 | 7.9 % |
| $x - y$ | 2 | 1.41 | 70.7 % |
| $xy$ | 80 | 12.8 | 16.0 % |
| $x/y$ | 1.25 | 0.20 | 16.0 % |
| $x^2$ | 100 | 20 | 20.0 % |

The sum has a smaller relative error than either input; the difference of
two similar numbers is almost meaningless; products and ratios combine the
relative errors; the power doubles the relative error. These are the rules
of thumb of {doc}`08-errors-and-uncertainty`.
:::

## Which data are worth improving?

:::{prf:example} The value of better data
:label: ex-23-value-better-data

A model $z = xy + w$ uses three independent inputs measured as
$x = 100 \pm 10$, $y = 50 \pm 5$, and $w = 200 \pm 50$. The marginal costs of
improving each measurement are \$5.00 to improve $x$ to $100 \pm 9$, \$6.00
to improve $y$ to $50 \pm 4$, and \$0.02 to improve $w$ to $200 \pm 49$.
Which measurement should be improved first?
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**Current error.** The partial derivatives are
$\partial z/\partial x = y = 50$, $\partial z/\partial y = x = 100$, and
$\partial z/\partial w = 1$, so

$$
\begin{aligned}
e_z^2 &= 50^2 \times 10^2 + 100^2 \times 5^2 + 1^2 \times 50^2 \\
&= 250\,000 + 250\,000 + 2\,500 = 502\,500,
\end{aligned}
$$

and $e_z = 708.87$.

**Marginal improvement rates.** By {eq}`eq-08-marginal-improvement`,

$$
\begin{aligned}
\frac{\partial e_z}{\partial e_x} &= \frac{y^2 e_x}{e_z} \\
&= \frac{2\,500 \times 10}{708.87} = 35.27, \\
\frac{\partial e_z}{\partial e_y} &= \frac{x^2 e_y}{e_z} \\
&= \frac{10\,000 \times 5}{708.87} = 70.53, \\
\frac{\partial e_z}{\partial e_w} &= \frac{1 \times e_w}{e_z} = \frac{50}{708.87} = 0.0705 .
\end{aligned}
$$

**Cost per unit reduction of $e_z$.** Divide each marginal cost by the
corresponding rate:

$$
\begin{aligned}
\frac{5.00}{35.27} &= \$0.142, \\
\frac{6.00}{70.53} &= \$0.085, \\
\frac{0.02}{0.0705} &= \$0.284 .
\end{aligned}
$$

Improving $y$ is the cheapest way to reduce the output error: it is worth
doing if a unit reduction of $e_z$ is worth at least \$0.085. Improving $w$,
although the cheapest measurement, is the worst option because $w$ hardly
affects $z$.

*Check with the actual improvements.* Recomputing $e_z$ with each improved
input gives 674.54 ($x$ improved), 642.26 ($y$ improved), and 708.80
($w$ improved), that is reductions of 34.3, 66.6, and 0.07 for \$5, \$6,
and \$0.02 — the same ranking.
:::

## Simple or complex model?

:::{prf:example} Model complexity and data quality
:label: ex-23-simple-vs-complex

A naïve model forecasts a quantity with a 30 % error, mostly due to poor
specification. A "perfect" model without specification error is available:
$z = x_1 x_2 x_3 x_4 x_5$, a product of five independent variables, each
measured with the same relative error. Which model should be used
(a) if the data have a 10 % measurement error, and (b) if the data have a
20 % measurement error and the naïve model's error is 40 %?
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

For a product of independent variables, relative errors add in quadrature:

$$
\begin{aligned}
\frac{e_z}{z} &= \sqrt{\sum_{i=1}^{5}\left(\frac{e_{x_i}}{x_i}\right)^2} \\
&= \sqrt{5}\,\frac{e_x}{x}.
\end{aligned}
$$

**(a)** $e_z/z = \sqrt{5}\times 0.10 = 22.4\,\% < 30\,\%$: the complex
model is better.

**(b)** $e_z/z = \sqrt{5}\times 0.20 = 44.7\,\% > 40\,\%$: the naïve model
is better.

With good data the detailed model wins; with poor data its five noisy inputs
make it worse than a crude model. This is the trade-off of
{numref}`fig-08-error-vs-complexity`.
:::

## Errors in population forecasts

:::{prf:example} Forecasting population
:label: ex-23-hw1-q3

The population of an area must be forecast for 2020. Reliable census data
exist for 1990 and 2000:

$$
\begin{aligned}
P_{1990} &= 25\,000 \pm 500, \\
P_{2000} &= 26\,000 \pm 300 .
\end{aligned}
$$

The growth-factor model $P_n = P_b\, t^{d}$ is used, where $P_n$ is the
population in the forecast year $n$, $P_b$ the population in the base year
$b$, $t$ the growth rate per decade, and $d = (n - b)/10$ the number of
decades extrapolated. The census data are independent and, at first, the
model is assumed to have no specification error.

(a) With what accuracy can the 2020 population be forecast?

(b) A 2010 census value is offered, $P_{2010} = 27\,500 \pm 850$, less
accurate than the previous ones. Is it worth using?

(c) Repeat the analysis assuming that the specification error of the model
is proportional to $d$ and equal to $10d\,\%$.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**(a) Base year 2000.** The growth rate per decade is
$t = P_{2000}/P_{1990}$ and $d = 2$, so

$$
\begin{aligned}
P_{2020} &= P_{2000}\left(\frac{P_{2000}}{P_{1990}}\right)^{2} \\
&= \frac{P_{2000}^{3}}{P_{1990}^{2}} \\
&= \frac{26\,000^3}{25\,000^2} = 28\,121.6 .
\end{aligned}
$$

The partial derivatives are

$$
\begin{aligned}
\frac{\partial P_{2020}}{\partial P_{2000}} &= \frac{3P_{2000}^{2}}{P_{1990}^{2}} = 3.2448, \\
\frac{\partial P_{2020}}{\partial P_{1990}} &= -\frac{2P_{2000}^{3}}{P_{1990}^{3}} = -2.2497,
\end{aligned}
$$

so by {eq}`eq-08-error-propagation-indep`

$$
\begin{aligned}
e_{P_{2020}}^2 &= 3.2448^2 \times 300^2 + 2.2497^2 \times 500^2 \\
&= 947\,585 + 1\,265\,319 = 2\,212\,904,
\end{aligned}
$$

giving $P_{2020} = 28\,122 \pm 1\,488$, a relative error of
$1\,488/28\,122 = 5.29\,\%$.

**(b) Base year 2010.** Using the latest decade for the growth rate,
$t = P_{2010}/P_{2000}$ and $d = 1$:

$$
\begin{aligned}
P_{2020} &= P_{2010}\,\frac{P_{2010}}{P_{2000}} = \frac{P_{2010}^{2}}{P_{2000}} \\
&= \frac{27\,500^2}{26\,000} = 29\,086.5 .
\end{aligned}
$$

With
$\partial P_{2020}/\partial P_{2010} = 2P_{2010}/P_{2000} = 2.1154$ and
$\partial P_{2020}/\partial P_{2000} = -P_{2010}^2/P_{2000}^2 = -1.1187$,

$$
\begin{aligned}
e_{P_{2020}}^2 &= 2.1154^2 \times 850^2 + 1.1187^2 \times 300^2 \\
&= 3\,233\,081 + 112\,637 = 3\,345\,717,
\end{aligned}
$$

giving $P_{2020} = 29\,087 \pm 1\,829$, a relative error of 6.29 %.
Ignoring specification error, the less accurate 2010 value **increases**
the forecast error (6.29 % > 5.29 %), so it is not worth using.

**(c) With specification error.** Write the true population as
$TP_{2020} = P_{2020} + D$, where $D$ has mean zero and standard deviation
$e_s$ (the specification error), independent of the data error. By
{eq}`eq-08-forecast-error`, $e_{TP} = \sqrt{e_{P_{2020}}^2 + e_s^2}$.

- Model (a) extrapolates $d = 2$ decades, so $e_s = 0.20 \times 28\,122 = 5\,624$:

  $$
  \begin{aligned}
  e_{TP} &= \sqrt{1\,488^2 + 5\,624^2} = 5\,818, \\
  \frac{e_{TP}}{P_{2020}} &= \frac{5\,818}{28\,122} = 20.7\,\%.
  \end{aligned}
  $$

- Model (b) extrapolates $d = 1$ decade, so $e_s = 0.10 \times 29\,087 = 2\,909$:

  $$
  \begin{aligned}
  e_{TP} &= \sqrt{1\,829^2 + 2\,909^2} = 3\,436, \\
  \frac{e_{TP}}{P_{2020}} &= \frac{3\,436}{29\,087} = 11.8\,\%.
  \end{aligned}
  $$

Once specification error is taken into account, the shorter extrapolation
dominates and the 2010 census **is** worth using, despite its larger
measurement error.

*Alternative model for (b).* One could also estimate the growth rate from
1990 to 2010, $t = (P_{2010}/P_{1990})^{1/2}$, so that
$P_{2020} = P_{2010}^{3/2}/P_{1990}^{1/2} = 28\,842 \pm 1\,368$ (4.74 %);
with specification error ($d = 1$) the total relative error is 11.1 %, even
slightly better.
:::
