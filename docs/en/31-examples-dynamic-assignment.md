# Dynamic Assignment and Simulation

This chapter works through the examples and problems of
{doc}`16-dynamic-assignment-and-simulation`. The code in
{doc}`36-python-traffic-assignment` reproduces the numbers.

## The bottleneck model

:::{prf:example} Morning commute through a bottleneck
:label: ex-31-bottleneck

$N = 5\,000$ commuters pass a bottleneck with capacity
$s = 2\,000$ cars/h. They all want to arrive at work at $t^* = $ 8:30. The
value of travel time is $\alpha = 20$, and the unit costs of early and late
arrival are $\beta = 10$ and $\gamma = 40$ (dollars per hour).

1. Find the first and last departure times, the departure time of the
   commuter who arrives on time, and the equilibrium cost per commuter.
2. Find the departure rates and the maximum queue.
3. Compute the total travel time cost, schedule delay cost, and total cost.
4. Describe the optimal time-varying toll and its effect.
5. What happens if the capacity is increased to 2 500 cars/h?
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

The peak lasts $N/s = 2.5$ h, and
$\delta = \beta\gamma/(\beta + \gamma) = 400/50 = 8$ dollars per hour.

**1.** By {eq}`eq-16-bottleneck-times` and {eq}`eq-16-bottleneck-queue`,

$$
\begin{aligned}
t_s &= t^* - \frac{\gamma}{\beta + \gamma}\frac{N}{s} = 8.5 - 0.8 \times 2.5 = 6.5 \ (\text{6:30}), \\
t_e &= t^* + \frac{\beta}{\beta + \gamma}\frac{N}{s} = 8.5 + 0.2 \times 2.5 = 9.0 \ (\text{9:00}), \\
\tilde t &= t^* - \frac{\delta}{\alpha}\frac{N}{s} = 8.5 - 0.4 \times 2.5 = 7.5 \ (\text{7:30}), \\
C &= \delta\,\frac{N}{s} = 8 \times 2.5 = 20 \text{ dollars}.
\end{aligned}
$$

Check: the first commuter arrives 2 h early and pays $10 \times 2 = 20$;
the last arrives 0.5 h late and pays $40 \times 0.5 = 20$; the on-time
commuter queues for 1 h and pays $20 \times 1 = 20$.

**2.** By {eq}`eq-16-bottleneck-rate`,

$$
r = \frac{\alpha}{\alpha - \beta}\,s = \frac{20}{10} \times 2\,000 = 4\,000 \text{ cars/h}
\quad \text{from 6:30 to 7:30},
$$

$$
r = \frac{\alpha}{\alpha + \gamma}\,s = \frac{20}{60} \times 2\,000 = 667 \text{ cars/h}
\quad \text{from 7:30 to 9:00}.
$$

The queue grows at $4\,000 - 2\,000 = 2\,000$ cars/h for one hour, so
the maximum queue, at 7:30, is

$$
Q_{\max} = \frac{\delta}{\alpha}\,N = 0.4 \times 5\,000 = 2\,000 \text{ cars},
$$

and it then shrinks at $2\,000 - 667 = 1\,333$ cars/h, vanishing at 9:00
({numref}`fig-16-bottleneck-cumulative`). Check:
$4\,000 \times 1 + (2\,000/3) \times 1.5 = 5\,000$ commuters.

**3.** The total queuing time is the area between the cumulative curves:
$\tfrac{1}{2} \times 1 \times 2\,000 + \tfrac{1}{2} \times 1.5 \times 2\,000 = 2\,500$
vehicle-hours. Hence

$$
\begin{aligned}
\mathrm{TTC} &= 20 \times 2\,500 = 50\,000 = \frac{\delta N^2}{2s}, \\
\mathrm{SDC} &= 50\,000, \\
\mathrm{TC} &= 100\,000 = N \times C .
\end{aligned}
$$

**4.** A toll that rises linearly from 0 at 6:30 to
$\delta N/s = 20$ dollars at 7:30 and falls linearly to 0 at 9:00 charges
each commuter exactly the queuing cost he or she would otherwise bear.
Commuters then depart at the capacity rate of 2 000 cars/h, nobody
queues, and everybody arrives at the same time as before. Each commuter
still pays 20 dollars (toll plus schedule delay), but the 50 000 dollars of
queuing time become toll revenue: the social cost halves to 50 000.

**5.** With $s = 2\,500$, $N/s = 2$ h: the peak runs from
$8.5 - 1.6 = 6.9$ (6:54) to $8.5 + 0.4 = 8.9$ (8:54), the cost per commuter
falls to $8 \times 2 = 16$ dollars, and the total cost to
$8 \times 5\,000^2/2\,500 = 80\,000$, a 20 % reduction. The maximum queue,
$\delta N/\alpha = 2\,000$ cars, does not change: it depends on demand,
not capacity.
:::

## Instantaneous and experienced travel times

:::{prf:example} Time-dependent route travel times
:label: ex-31-itt-ett

A network has the links (1, 2), (2, 4), (4, 6), (2, 5), (5, 6), (1, 3), and
(3, 5), and three routes from node 1 to node 6: A = 1–2–4–6,
B = 1–2–5–6, and C = 1–3–5–6. The travel time of each link depends on the
minute at which a vehicle enters it:

| Entry minute | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| (1, 2) | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| (2, 4) | 1 | 2 | 3 | 3 | 2 | 2 | 1 |
| (4, 6) | 1 | 3 | 5 | 6 | 5 | 4 | 3 |
| (2, 5) | 2 | 3 | 3 | 2 | 2 | 2 | 2 |
| (5, 6) | 1 | 2 | 2 | 1 | 1 | 1 | 1 |
| (1, 3) | 2 | 1 | 1 | 1 | 1 | 1 | 1 |
| (3, 5) | 2 | 2 | 1 | 1 | 1 | 1 | 1 |

For departures at minutes 1 and 2, compute the instantaneous and
experienced travel times of the three routes and find the shortest route by
each measure.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**Departure at minute 1.** The ITT adds the column of minute 1
({eq}`eq-16-itt-ett`):

$$
\begin{aligned}
\mathrm{ITT}_A &= 1 + 1 + 1 = 3, \\
\mathrm{ITT}_B &= 1 + 2 + 1 = 4, \\
\mathrm{ITT}_C &= 2 + 2 + 1 = 5 .
\end{aligned}
$$

The ETT follows the vehicle. On route A it enters (1, 2) at minute 1
(time 1), (2, 4) at minute 2 (time 2), and (4, 6) at minute 4 (time 6),
arriving at minute 10:

$$
\begin{aligned}
\mathrm{ETT}_A &= 1 + 2 + 6 = 9, \\
\mathrm{ETT}_B &= 1 + 3 + 1 = 5 \quad (\text{entries at minutes } 1, 2, 5), \\
\mathrm{ETT}_C &= 2 + 1 + 1 = 4 \quad (\text{entries at minutes } 1, 3, 4).
\end{aligned}
$$

Route A is the shortest by ITT (3) but the longest by ETT (9): it runs into
the congestion that builds up on (4, 6). The time-dependent shortest route
is C, with 4 minutes.

**Departure at minute 2.**

$$
\begin{aligned}
\mathrm{ITT}_A &= 1 + 2 + 3 = 6, \\
\mathrm{ITT}_B &= 1 + 3 + 2 = 6, \\
\mathrm{ITT}_C &= 1 + 2 + 2 = 5, \\
\mathrm{ETT}_A &= 1 + 3 + 4 = 8 \quad (\text{entries } 2, 3, 6), \\
\mathrm{ETT}_B &= 1 + 3 + 1 = 5 \quad (\text{entries } 2, 3, 6), \\
\mathrm{ETT}_C &= 1 + 1 + 1 = 3 \quad (\text{entries } 2, 3, 4).
\end{aligned}
$$

Route C is the shortest by both measures, but its ITT (5) overstates the
actual time (3), because links (3, 5) and (5, 6) clear by the time the
vehicle gets there. A traveler who chooses routes from a snapshot of current conditions
can be badly misled when conditions change during the trip; dynamic
equilibrium is defined on experienced times.

The link times satisfy FIFO — for every link, a later entry never leads to
an earlier exit — so the time-dependent Dijkstra search in
{doc}`36-python-traffic-assignment` finds route C for both departures.
:::

## Agent-based simulation

:::{prf:example} Travel time smoothing and plan scores
:label: ex-31-matsim-scores

Ten agents live in zone 1 and work in zone 3, starting at interval 40. They
can drive on link 1–3 directly or on links 1–2 and 2–3. The link travel
times (in intervals) depend on the number $n$ of agents on the link:
$t_{13} = 10 + 2n$, $t_{12} = 6 + n$, $t_{23} = 5 + 0.5n$. A plan is scored
with $-1$ per interval of travel, $-2$ per interval of early arrival, and
$-3$ per interval of late arrival. Expected link times are smoothed with
weights 0.4, 0.3, 0.2, and 0.1 on the current and the three previous
iterations, normalized over the iterations available, with free-flow times
standing in for the iteration before the first. Replanning chooses the
route and departure time that maximize the expected score without planning
to arrive late.

In iteration 0, all agents execute plan 1: depart at interval 30 on link
1–3. In iteration 1, eight agents execute the new plan and two keep plan 1.
Compute the scores, the smoothed link times, and the new plans.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**Iteration 0.** With 10 agents on link 1–3, $t_{13} = 30$, so they arrive
at interval 60, 20 intervals late:

$$
\text{score of plan 1} = -30 - 3 \times 20 = -90 .
$$

Links 1–2 and 2–3 are empty (times 6 and 5). The smoothed times are

$$
\begin{aligned}
\hat t_{13} &= \frac{0.4 \times 30 + 0.3 \times 10}{0.7} = 21.43, \\
\hat t_{12} &= 6, \\
\hat t_{23} &= 5 .
\end{aligned}
$$

The best response uses links 1–2–3 (expected time 11 < 21.43) and departs
at interval 29 to arrive exactly at 40: **plan 2**, expected score $-11$.

**Iteration 1.** Eight agents execute plan 2 and two execute plan 1. The
link times are $t_{13} = 10 + 2 \times 2 = 14$,
$t_{12} = 6 + 8 = 14$, and $t_{23} = 5 + 0.5 \times 8 = 9$. The scores are

$$
\begin{aligned}
\text{plan 1:}&\quad \text{depart 30, arrive 44:} \quad -14 - 3 \times 4 = -26, \\
\text{plan 2:}&\quad \text{depart 29, arrive 52:} \quad -23 - 3 \times 12 = -59,
\end{aligned}
$$

and the average executed score is
$(2 \times (-26) + 8 \times (-59))/10 = -52.4$, up from $-90$. The smoothed
times are

$$
\begin{aligned}
\hat t_{13} &= \frac{0.4 \times 14 + 0.3 \times 30 + 0.2 \times 10}{0.9} = 18.44, \\
\hat t_{12} &= \frac{0.4 \times 14 + 0.3 \times 6 + 0.2 \times 6}{0.9} = 9.56, \\
\hat t_{23} &= \frac{0.4 \times 9 + 0.3 \times 5 + 0.2 \times 5}{0.9} = 6.78 .
\end{aligned}
$$

Route 1–2–3 is still expected to be quicker ($16.33 < 18.44$). To arrive
no later than 40 the agent departs at interval 23, arriving at 39.33,
0.67 intervals early: **plan 3**, expected score
$-16.33 - 2 \times 0.67 = -17.67$.

The loop continues: agents spread over routes and departure times until the
average score stabilizes. Smoothing prevents the oscillation that would
result if every agent reacted to the last iteration's times alone (all
agents would leave link 1–3 at once, as in an AON assignment); it plays the
role of the step size in MSA.
:::
