# Bi-proportional Fitting

This chapter works through the examples and problems of
{doc}`04-biproportional-fitting`: balancing a matrix to new margins,
detecting infeasible targets, and the entropy-maximizing interpretation of
the balanced matrix. Applications to trip distribution are solved in
{doc}`25-examples-trip-distribution`, and the code in
{doc}`32-python-foundations` reproduces the numbers.

## Matrix balancing

:::{prf:example} Updating a matrix to new margins
:label: ex-20-bp-ras

A $3 \times 3$ matrix observed in a base year,

$$
\bt = \begin{bmatrix} 20 & 10 & 10 \\ 10 & 30 & 10 \\ 10 & 10 & 40 \end{bmatrix},
$$

has row totals $(40, 50, 60)$ and column totals $(40, 50, 60)$. New totals
are known: rows $\mathbf{O} = (50, 60, 70)$ and columns
$\mathbf{D} = (40, 60, 80)$. (a) Check consistency. (b) Balance the matrix
with algorithm I to a relative tolerance of $10^{-4}$. (c) Give the
balancing factors and verify that the result preserves the cross-product
ratios of the seed. (d) Show that perturbing the result while keeping its
margins increases the information distance from the seed.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**(a)** $\sum_i O_i = 180 = \sum_j D_j$: the targets are consistent, and
the seed is strictly positive, so a unique balanced matrix exists.

**(b)** *Iteration 1, row step.* The row totals of the seed are 40, 50,
and 60, so the rows are multiplied by $50/40 = 1.25$, $60/50 = 1.2$, and
$70/60 = 1.1667$:

$$
\bT' = \begin{bmatrix} 25.00 & 12.50 & 12.50 \\ 12.00 & 36.00 & 12.00 \\ 11.67 & 11.67 & 46.67 \end{bmatrix} .
$$

*Column step.* The column totals are now 48.67, 60.17, and 71.17, so the
columns are multiplied by $40/48.67$, $60/60.17$, and $80/71.17$:

$$
\bT^{(1)} = \begin{bmatrix} 20.55 & 12.47 & 14.05 \\ 9.86 & 35.90 & 13.49 \\ 9.59 & 11.63 & 52.46 \end{bmatrix} .
$$

The row totals are now $(47.07, 59.25, 73.68)$, with a largest relative
error of $\lvert 73.68 - 70\rvert/70 = 5.9\,\%$. Repeating,

| $r$ | Row totals after the column step | Largest relative error |
|---|---|---|
| 1 | (47.065, 59.253, 73.682) | 0.0587 |
| 2 | (49.664, 59.659, 70.677) | 0.0097 |
| 3 | (49.956, 59.912, 70.133) | 0.0019 |
| 4 | (49.993, 59.980, 70.027) | 0.0004 |
| 5 | (49.999, 59.996, 70.006) | 0.00008 |

and after five iterations

$$
\bT = \begin{bmatrix} 21.43 & 13.15 & 15.42 \\ 9.80 & 36.09 & 14.11 \\ 8.77 & 10.76 & 50.48 \end{bmatrix} .
$$

**(c)** Algorithm II, started from $b_j = 1$, produces the same matrices
and, at convergence, the factors

$$
\begin{aligned}
\ba &= (1.338,\ 1.224,\ 1.095), \\
\bb &= (0.801,\ 0.983,\ 1.152),
\end{aligned}
$$

for example $T_{13} = 1.338 \times 1.152 \times 10 = 15.42$. The factors
are defined up to a common scale; only the products $a_ib_j$ matter. The
cross-product ratio of rows 1, 2 and columns 1, 2 is
$t_{11}t_{22}/(t_{12}t_{21}) = 20 \times 30/(10 \times 10) = 6$ in the seed
and

$$
\frac{T_{11}T_{22}}{T_{12}T_{21}} = \frac{21.43 \times 36.09}{13.15 \times 9.80} = 6.00
$$

in the balanced matrix: the association pattern of the seed is unchanged.

**(d)** The information distance {eq}`eq-04-bp-information` of the balanced
matrix (after five iterations) from the seed is $I(\bT, \bt) = 4.460$. Adding the
margin-preserving perturbation

$$
\bP = \begin{bmatrix} 1 & -1 & 0 \\ -1 & 1 & 0 \\ 0 & 0 & 0 \end{bmatrix}
$$

gives $I(\bT + \bP, \bt) = 4.588$, and subtracting it
gives $I(\bT - \bP, \bt) = 4.584$. Both are larger, as
{prf:ref}`thm-04-bp-information` requires: among all matrices with these
margins, the balanced one is closest to the seed.
:::

:::{prf:example} Targets incompatible with the zero cells
:label: ex-20-bp-infeasible

The seed $\bt = \begin{bmatrix} 5 & 0 \\ 3 & 2 \end{bmatrix}$ has a
structural zero in cell (1, 2). Balance it (a) to rows $(4, 6)$ and columns
$(8, 2)$, and (b) to rows $(6, 4)$ and columns $(3, 7)$.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

Because $T_{12} = 0$, row 1 can only send its total to column 1, so
$T_{11} = O_1$, $T_{21} = D_1 - O_1$, and $T_{22} = D_2$.

**(a)** $T_{11} = 4$, $T_{21} = 8 - 4 = 4$, $T_{22} = 2$: all non-negative,
and row 2 sums to $4 + 2 = 6 = O_2$. A balanced matrix exists, and the
iterations converge to

$$
\bT = \begin{bmatrix} 4 & 0 \\ 4 & 2 \end{bmatrix} .
$$

**(b)** The same reasoning gives $T_{11} = 6$, but column 1 can hold only
$D_1 = 3$: no matrix with this zero pattern has the required margins,
although the totals are consistent ($6 + 4 = 3 + 7$). The iterations
cannot converge. Cell (2, 1) shrinks towards zero, and the matrix
approaches a cycle between

$$
\begin{bmatrix} 6 & 0 \\ 0 & 4 \end{bmatrix}
\ \text{after each row step}
\qquad\text{and}\qquad
\begin{bmatrix} 3 & 0 \\ 0 & 7 \end{bmatrix}
\ \text{after each column step}.
$$

The column totals are met after every column step, but the row totals stay
at $(3, 7)$ instead of $(6, 4)$: the convergence test of
{prf:ref}`alg-04-biprop-1` never succeeds, which signals the infeasibility.
:::

## Entropy maximization

:::{prf:example} Most probable distribution
:label: ex-20-bp-entropy

(a) Six commuters leave one zone for two destinations. Which split between
the destinations is most probable when nothing else is known? (b) Show that
the maximum-entropy matrix with given row and column totals and no seed is
$T_{ij} = O_iD_j/N$.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**(a)** The split $(T_1, T_2)$ is realized by $W = 6!/(T_1!\,T_2!)$
micro-states:

| $(T_1, T_2)$ | (6,0) | (5,1) | (4,2) | (3,3) | (2,4) | (1,5) | (0,6) |
|---|---|---|---|---|---|---|---|
| $W$ | 1 | 6 | 15 | **20** | 15 | 6 | 1 |

The even split is most probable (20 of the $2^6 = 64$ micro-states). With
more commuters the distribution of $W$ becomes ever more concentrated
around the maximum, which justifies using the most probable meso-state as a
forecast.

**(b)** From the derivation in {doc}`04-biproportional-fitting`,
$T_{ij} = a_ib_j$. Imposing the constraints,
$\sum_j a_ib_j = a_i\sum_j b_j = O_i$ and $\sum_i a_ib_j = b_j\sum_i a_i = D_j$,
so $a_i = O_i/\sum_j b_j$ and $b_j = D_j/\sum_i a_i$. Then

$$
\begin{aligned}
T_{ij} &= a_ib_j \\
&= \frac{O_i D_j}{\sum_j b_j \sum_i a_i} \\
&= \frac{O_iD_j}{N},
\end{aligned}
$$

because $\sum_{ij}a_ib_j = N$. Every row is distributed in proportion to
the column totals — the "independence" matrix of contingency tables. For a
trip matrix without cost information, every origin sends trips to
destinations in proportion to their attractions.
:::
