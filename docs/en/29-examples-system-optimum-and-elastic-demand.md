# System Optimum, Elastic Demand, and Combined Models

This chapter works through the examples and problems of
{doc}`14-system-optimum-and-elastic-demand`. The code in
{doc}`36-python-traffic-assignment` reproduces the numbers.

## System optimum and pricing

:::{prf:example} UE and SO on two routes
:label: ex-29-so-two-route

For the two routes of {prf:ref}`ex-28-ue-two-route`,
$t_1 = 40 + 0.5\,x_1$ and $t_2 = 10 + 0.25\,x_2^2$, with $q = 10$:
(1) find the system optimum and compare its total travel time with the UE;
(2) compute the marginal-cost tolls and verify that they produce the SO.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**(1)** The marginal costs {eq}`eq-14-marginal-cost` are

$$
\begin{aligned}
\tilde t_1 &= 40 + 0.5x_1 + x_1(0.5) = 40 + x_1, \\
\tilde t_2 &= 10 + 0.25x_2^2 + x_2(0.5x_2) = 10 + 0.75\,x_2^2 .
\end{aligned}
$$

At $x_2 = 10$, $\tilde t_2 = 85 > \tilde t_1(0) = 40$, so both links are
used at the SO ({prf:ref}`thm-14-so-ue`):

$$
\begin{aligned}
40 + (10 - x_2) &= 10 + 0.75\,x_2^2 \\
0.75\,x_2^2 + x_2 - 40 &= 0 \\
x_2 &= \frac{-1 + \sqrt{1 + 120}}{1.5} = \frac{20}{3} = 6.667,
\end{aligned}
$$

and $x_1 = 3.333$. The travel times are $t_1 = 41.67$ and $t_2 = 21.11$,
so

$$
\mathrm{TSTT}^{\mathrm{SO}} = 3.333 \times 41.67 + 6.667 \times 21.11 = 279.63,
$$

compared with $\mathrm{TSTT}^{\mathrm{UE}} = 10 \times 35 = 350$ at the UE
$(0, 10)$. The SO saves 20 % of the total travel time, but it sends a third
of the travelers to the route that takes 41.67 instead of 21.11: they would
switch if they could, so the SO is not an equilibrium. The ratio
$350/279.63 = 1.25$ is the price of anarchy of this network.

**(2)** The tolls {eq}`eq-14-mc-toll` at the SO flows are

$$
\begin{aligned}
\tau_1 &= x_1\,t_1'(x_1) = 3.333 \times 0.5 = 1.67, \\
\tau_2 &= x_2\,t_2'(x_2) = 6.667 \times 0.5 \times 6.667 = 22.22 .
\end{aligned}
$$

With the tolls, the generalized times at the SO flows are
$41.67 + 1.67 = 43.33$ and $21.11 + 22.22 = 43.33$: equal, so the SO flows
are the user equilibrium of the tolled network. The heavy toll on the steep
link 2 pushes traffic to link 1.
:::

:::{prf:example} Braess's paradox
:label: ex-29-braess

In the network of {numref}`fig-14-braess-network`, $q_{14} = 6$, and the link
times are $t_1 = 50 + x_1$, $t_2 = 50 + x_2$, $t_3 = 10x_3$, $t_4 = 10x_4$.
(1) Find the UE and the SO, and the marginal-cost tolls. (2) A new link 5
from node 3 to node 2 is built, with $t_5 = 10 + x_5$. Find the new UE and
SO and comment.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**(1)** The two paths are A = links 1–4 and B = links 3–2. By symmetry the
UE splits the demand equally: $f_A = f_B = 3$, all link flows are 3, and
both paths take $50 + 3 + 10 \times 3 = 83$. The total system travel time is

$$
\begin{aligned}
\mathrm{TSTT} &= \sum_a x_at_a \\
&= 2 \times 3 \times 53 + 2 \times 3 \times 30 \\
&= 498 \\
&= 6 \times 83 .
\end{aligned}
$$

The marginal costs are $\tilde t_1 = 50 + 2x_1$, $\tilde t_2 = 50 + 2x_2$,
$\tilde t_3 = 20x_3$, $\tilde t_4 = 20x_4$. Equal marginal path costs,

$$
\begin{aligned}
50 + 2f_A + 20f_A &= 20f_B + 50 + 2f_B, \\
f_A + f_B &= 6,
\end{aligned}
$$

give $f_A = f_B = 3$: the SO coincides with the UE because of the symmetry.
The tolls are $\tau_1 = \tau_2 = 3 \times 1 = 3$ and
$\tau_3 = \tau_4 = 3 \times 10 = 30$.

**(2)** With link 5 there is a third path, C = links 3–5–4. Let
$f_A = f_B = f$ (by symmetry) and $f_C = 6 - 2f$; then
$x_1 = x_2 = f$, $x_3 = x_4 = 6 - f$, $x_5 = 6 - 2f$, and the path times are

$$
\begin{aligned}
c_A = c_B &= 50 + f + 10(6 - f) = 110 - 9f, \\
c_C &= 10(6 - f) + 10 + (6 - 2f) + 10(6 - f) = 136 - 22f .
\end{aligned}
$$

At the UE all three paths are used: $110 - 9f = 136 - 22f$, so $f = 2$ and
$f_C = 2$. The link flows are $(2, 2, 4, 4, 2)$ and every path takes **92**:

$$
\mathrm{TSTT} = 6 \times 92 = 552 > 498 .
$$

Every traveler is 9 time units worse off. At the old flows (3 on each of
links 1–4) path C would take only $30 + 10 + 30 = 70 < 83$, so travelers
move to it, overloading links 3 and 4, which are shared with paths A and B.

The SO does not change: at $\bx = (3, 3, 3, 3, 0)$ the marginal path costs
are $56 + 60 = 116$ for A and B and $60 + 10 + 60 = 130$ for C, so C stays
unused and $\mathrm{TSTT} = 498$. With the tolls of part (1) and
$\tau_5 = 0$, path C costs $(30 + 30) + 10 + (30 + 30) = 130$ against
$53 + 3 + 30 + 30 = 116$ for A, and the tolled UE is the SO. The new link
is useless in the SO and harmful in the UE: the UE's total travel time is
$552/498 = 1.11$ times the optimum.
:::

## Equilibrium and optimum as functions of demand

:::{prf:example} DUE and SO with a nonlinear link function
:label: ex-29-hw4-q1

In the network of {numref}`fig-29-parallel-links-network`, links 1 and 2 join node 1
to node 2 and link 3 joins node 2 to node 3. The link times are

$$
\begin{aligned}
t_1 &= 1.5 + 0.5\,x_1^2, \\
t_2 &= 1 + 2\,x_2, \\
t_3 &= 4 + x_3,
\end{aligned}
$$

and the demand from 1 to 3 is $q \ge 0$.
(1) Find the DUE link flows and the DUE travel time from 1 to 3.
(2) Find the SO link flows and the travel times of the two paths at the SO.

```{figure} figures/29-parallel-links-network.svg
:name: fig-29-parallel-links-network
:width: 400px
:class: dark-light

Two parallel links followed by a common link: one O-D pair from node 1 to node 3.
```
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

Both paths use link 3, so $x_3 = q$ and the route choice is between links 1
and 2, with $x_1 + x_2 = q$.

**(1) DUE.** At zero flow, $t_2(0) = 1 < t_1(0) = 1.5$, so link 2 is used
first. It carries all the demand while $t_2(q) = 1 + 2q \le 1.5$, that is,
for $q \le 1/4$. Then

$$
\begin{aligned}
x_1 &= 0, \\
x_2 &= q, \\
x_3 &= q, \\
u &= t_2 + t_3 = 1 + 2q + 4 + q = 3q + 5 .
\end{aligned}
$$

For $q > 1/4$ both links are used, and $t_1 = t_2$:

$$
\begin{aligned}
1.5 + 0.5\,x_1^2 &= 1 + 2\,(q - x_1) \\
x_1^2 + 4x_1 + 1 - 4q &= 0 \\
x_1 &= \sqrt{4q + 3} - 2 ,
\end{aligned}
$$

so

$$
\begin{aligned}
x_1 &= \sqrt{4q + 3} - 2, \\
x_2 &= q + 2 - \sqrt{4q + 3}, \\
x_3 &= q, \\
u &= 1 + 2x_2 + 4 + q = 3q + 9 - 2\sqrt{4q + 3} .
\end{aligned}
$$

At $q = 1/4$, $\sqrt{4q + 3} = 2$ and the two branches meet. For $q = 10$,
for example, $x_1 = 4.557$, $x_2 = 5.443$, and $u = 25.89$.

**(2) SO.** The marginal costs are

$$
\begin{aligned}
\tilde t_1 &= 1.5 + 1.5\,x_1^2, \\
\tilde t_2 &= 1 + 4\,x_2, \\
\tilde t_3 &= 4 + 2\,x_3 .
\end{aligned}
$$

Link 2 alone is optimal while $\tilde t_2(q) = 1 + 4q \le \tilde t_1(0) = 1.5$,
that is, for $q \le 1/8$. Then $x_1 = 0$, $x_2 = x_3 = q$, and the path
times are

$$
\begin{aligned}
c_{\text{link 1}} &= t_1(0) + t_3(q) = 5.5 + q, \\
c_{\text{link 2}} &= t_2(q) + t_3(q) = 5 + 3q .
\end{aligned}
$$

For $q > 1/8$, $\tilde t_1 = \tilde t_2$:

$$
\begin{aligned}
1.5 + 1.5\,x_1^2 &= 1 + 4\,(q - x_1) \\
3x_1^2 + 8x_1 + 1 - 8q &= 0 \\
x_1 &= \frac{\sqrt{24q + 13} - 4}{3},
\end{aligned}
$$

and $x_2 = q - x_1$, $x_3 = q$. Substituting, the path travel times are

$$
\begin{aligned}
c_{\text{link 1}} &= 1.5 + 0.5\,x_1^2 + 4 + q \\
&= \frac{64}{9} + \frac{7}{3}\,q - \frac{4}{9}\sqrt{24q + 13}, \\
c_{\text{link 2}} &= 1 + 2\,x_2 + 4 + q \\
&= \frac{23}{3} + 3q - \frac{2}{3}\sqrt{24q + 13} .
\end{aligned}
$$

They are not equal: at the SO the marginal costs are equal, not the travel
times. For $q = 10$: $x_1 = 3.969$, $x_2 = 6.031$; the path times are 23.38
via link 1 and 27.06 via link 2, and the total travel time is 255.99,
against 258.85 at the DUE.
:::

## Elastic demand

:::{prf:example} Elastic demand on a single link
:label: ex-29-elastic-demand

One O-D pair is connected by a single link with $t(x) = 1 + x$. The inverse
demand function is $D^{-1}(q) = 5 - q$. (1) Solve the equilibrium with
elastic demand directly and from the program {eq}`eq-14-elastic`. (2) Solve it
with the excess-demand network, first with $\bar q = 5$ and then with
$\bar q = 8$.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**(1)** At equilibrium the travel time equals the inverse demand,
$1 + q = 5 - q$, so $q = x = 2$ and $u = 3$. From {eq}`eq-14-elastic`, with
$x = q$,

$$
\begin{aligned}
z(q) &= \int_0^q (1 + \omega)\,\diff\omega - \int_0^q (5 - \omega)\,\diff\omega \\
&= q^2 - 4q,
\end{aligned}
$$

which is minimized at $q = 2$.

**(2)** With $\bar q = D(0) = 5$, the excess-demand function is
$W(e) = D^{-1}(5 - e) = e$. The augmented network has the real link
($1 + x$) and a dummy link ($e$) in parallel, with fixed demand 5. Both are
used, so

$$
\begin{aligned}
1 + x &= e, \\
x + e &= 5,
\end{aligned}
\quad\Longrightarrow\quad
\begin{aligned}
x &= 2, \\
e &= 3,
\end{aligned}
$$

with common time 3: two trips are made and three are suppressed. With
$\bar q = 8$, $W(e) = 5 - (8 - e) = e - 3$, and
$1 + x = e - 3$, $x + e = 8$ give $x = 2$, $e = 6$, time 3 again. The upper
bound changes the excess demand but not the solution.
:::

## Combined distribution and assignment

:::{prf:example} Evans's algorithm on the six-node network
:label: ex-29-combined-da

In the network of {prf:ref}`ex-28-ue-six-node`, origins 1 and 5 produce
$O_1 = 100$ and $O_5 = 50$ trips, and destinations 2 and 6 attract
$D_2 = D_6 = 75$. The trips are distributed by a doubly constrained gravity
model with $\beta = 0.1$ and assigned by Wardrop's principle. Perform the
initialization and the first iteration of Evans's algorithm by hand, and
check the converged solution.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

The four O-D pairs have the paths: $1 \to 2$: link 1 or links 2–4–3;
$1 \to 6$: links 2–4–7; $5 \to 2$: links 5–4–3; $5 \to 6$: link 6 or links
5–4–7.

**Initialization.** The free-flow shortest-path times are
$u_{12} = 2.5$, $u_{16} = 3$, $u_{52} = 3.5$, and $u_{56} = 4$. Because
$u_{12} - u_{16} = u_{52} - u_{56}$, the deterrence matrix
$\exp(-\beta u_{rs})$ is the product of a row and a column factor, and the
gravity model gives the independent matrix
$q_{rs} = O_rD_s/150$:

$$
\bq^{(1)} = \begin{bmatrix} 50 & 50 \\ 25 & 25 \end{bmatrix} .
$$

Assigning it AON (the two paths of $5 \to 6$ tie at 4; the direct link is
taken) gives $\bx^{(1)} = (0, 100, 75, 125, 25, 25, 50)$.

**Iteration 1.** The link times are
$\bt^{(1)} = (3, 201, 75.5, 63.5, 14.5, 29, 26)$, and the shortest-path
times are

$$
\begin{aligned}
u_{12} &= 3, \\
u_{16} &= 201 + 63.5 + 26 = 290.5, \\
u_{52} &= 14.5 + 63.5 + 75.5 = 153.5, \\
u_{56} &= 29 .
\end{aligned}
$$

The gravity model with these times concentrates the trips on the cheap
pairs:
$\bv^{(1)} = \begin{bmatrix} 75 & 25 \\ 0 & 50 \end{bmatrix}$
($v_{52} \approx 2 \times 10^{-16}$), and its AON assignment is
$\by^{(1)} = (75, 25, 0, 25, 0, 50, 25)$. The line search on
$z(\bx, \bq)$ gives $\alpha_1 = 0.9875$, so

$$
\begin{aligned}
\bq^{(2)} &= \begin{bmatrix} 74.69 & 25.31 \\ 0.31 & 49.69 \end{bmatrix}, \\
\bx^{(2)} &= (74.06,\ 25.94,\ 0.94,\ 26.25,\ 0.31,\ 49.69,\ 25.31) .
\end{aligned}
$$

**Converged solution.** After a few thousand iterations,

$$
\begin{aligned}
\bq^* &= \begin{bmatrix} 72.513 & 27.487 \\ 2.487 & 47.513 \end{bmatrix}, \\
\bx^* &= (72.513,\ 27.487,\ 2.487,\ 36.990,\ 9.503,\ 40.497,\ 34.503),
\end{aligned}
$$

with link times $(39.257, 55.974, 2.987, 19.495, 6.751, 44.497, 18.251)$.
*Wardrop's conditions:* for $1 \to 2$, link 1 takes 39.257 and path 2–4–3
takes $55.974 + 19.495 + 2.987 = 78.456$, so only link 1 is used
($x_3 = 2.487$ is the $5 \to 2$ flow). For $5 \to 6$, link 6 takes 44.497
and path 5–4–7 takes $6.751 + 19.495 + 18.251 = 44.497$: both are used, the
second with $x_5 - q_{52} = 7.016$ trips. *Gravity condition:* in a doubly
constrained gravity model the cross-product ratio of a $2 \times 2$ matrix
depends only on the costs,

$$
\begin{aligned}
\frac{q_{12}\,q_{56}}{q_{16}\,q_{52}} &= \exp\left[-\beta\left(u_{12} + u_{56} - u_{16} - u_{52}\right)\right] .
\end{aligned}
$$

With $(u_{12}, u_{16}, u_{52}, u_{56}) = (39.257, 93.720, 29.233, 44.497)$,
the left side is $72.513 \times 47.513/(27.487 \times 2.487) = 50.40$ and
the right side is $\exp(0.1 \times 39.199) = 50.40$. The trip matrix is the
gravity model evaluated at the equilibrium times, as
{eq}`eq-14-combined-da-solution` requires. Compared with the free-flow
distribution $\bq^{(1)}$, congestion on the shared link 4 discourages the
"crossing" trips $1 \to 6$ and $5 \to 2$.
:::
