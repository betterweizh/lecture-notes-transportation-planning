# Traffic Assignment IV: Dynamic Assignment and Simulation

## Overview

The static models of the previous chapters assume that the O-D flows and
the link travel times are constant over the modeled period. Peak-hour
congestion is not like that: queues build up and dissipate, a traveler who
leaves ten minutes earlier meets different conditions, and many travelers
adjust their departure time to avoid the worst of the peak. **Dynamic
traffic assignment (DTA)** adds the time dimension. This chapter states the
dynamic user equilibrium conditions, solves the simplest dynamic model —
Vickrey's bottleneck model of departure time choice — in closed form,
distinguishes instantaneous from experienced travel times, outlines the
general DTA algorithm, and introduces multi-agent simulation with MATSim.

:::{admonition} Learning objectives
:class: objectives
After completing this chapter, readers should be able to:

- state the dynamic user equilibrium conditions for route choice and for
  joint departure time and route choice;
- derive the equilibrium of the bottleneck model and compute its departure
  rates, queue, and costs;
- compute instantaneous and experienced route travel times and explain why
  the difference matters;
- describe the algorithmic framework of simulation-based DTA; and
- explain how an agent-based simulation such as MATSim represents demand and
  reaches a relaxed equilibrium.
:::

## Notation

| Symbol | Meaning |
|---|---|
| $N$ | number of commuters |
| $s$ | bottleneck capacity (vehicles per unit time) |
| $t^*$ | preferred (official) arrival time at work |
| $T(t)$ | queuing time of a commuter who departs at time $t$ |
| $Q(t)$ | queue length (vehicles) at time $t$ |
| $r(t)$ | departure rate at time $t$ |
| $\alpha$, $\beta$, $\gamma$ | value of travel time, unit cost of early and of late arrival |
| $\delta$ | $\beta\gamma/(\beta + \gamma)$ |
| $t_s$, $t_e$, $\tilde t$ | first and last departure times; departure time of the on-time arrival |
| $C(t)$ | generalized cost of a commuter who departs at $t$ |

## From static to dynamic equilibrium

The static user equilibrium (Wardrop's first principle) says that all used
paths of an O-D pair have equal and minimum travel time. Adding time gives
two dynamic versions:

- **Dynamic user equilibrium (DyUE) for route choice.** For each O-D pair
  and each departure time interval, all used paths have equal and minimum
  **experienced** travel time (generalized cost), and no traveler can
  reduce his or her experienced travel time by unilaterally changing route.
- **DyUE for departure time and route choice.** For each O-D pair, all used
  combinations of path and departure time have equal and minimum
  experienced generalized cost, which now includes the penalty of arriving
  earlier or later than desired.

Time introduces two effects that static models lack. On the **demand
side**, travelers who cannot get through in one interval spill over into
the next, so demand is no longer independent across intervals. On the
**supply side**, link travel times vary with the time at which a vehicle
enters the link, so the time of a path depends on when each of its links is
reached. Queues also spill back onto upstream links, which a separable
static cost function cannot represent.

## The bottleneck model

### Set-up

Vickrey's (1969) bottleneck model, developed by Arnott, de Palma, and
Lindsey (1990, 1993), is the simplest model of departure time choice and is
solved in closed form. $N$ identical commuters drive from home to work in
the morning peak. The trip is uncongested except at a single **bottleneck**
with capacity $s$: if vehicles arrive at the bottleneck faster than $s$, a
queue forms, served first-in-first-out (FIFO). All commuters want to arrive
at work at the same time $t^*$, and they pay a **schedule delay** penalty
for arriving early or late.

Setting the free-flow travel time to zero (which shifts all times but does
not affect the results), a commuter who departs at $t$ waits in the queue
for $T(t) = Q(t)/s$ and arrives at work at $t + T(t)$. The generalized cost
of the trip is

$$
C(t) =
\begin{cases}
\alpha T(t) + \beta\left[t^* - t - T(t)\right], & \text{early arrival}, \\
\alpha T(t) + \gamma\left[t + T(t) - t^*\right], & \text{late arrival},
\end{cases}
$$ (eq-16-bottleneck-cost)

where $\alpha$ is the value of travel time, $\beta$ the cost per unit time
of arriving early, and $\gamma$ the cost per unit time of arriving late.
Empirically $\beta < \alpha < \gamma$ (Small, 1982, found
$\beta \approx 0.6\alpha$ and $\gamma \approx 2.4\alpha$): arriving early is
less unpleasant than traveling, which is less unpleasant than arriving late.

### Equilibrium departure rates

At the departure time equilibrium, every commuter has the same cost, so
$C(t)$ is constant over the departure period $[t_s, t_e]$. For early
arrivals, $\diff C/\diff t = \alpha T' - \beta(1 + T') = 0$, and for
late arrivals $\alpha T' + \gamma(1 + T') = 0$:

$$
T'(t) =
\begin{cases}
\dfrac{\beta}{\alpha - \beta} > 0, & \text{early arrivals}, \\[2ex]
-\dfrac{\gamma}{\alpha + \gamma} < 0, & \text{late arrivals}.
\end{cases}
$$

The queue grows while commuters arrive early and shrinks while they arrive
late. Since the queue changes at rate $Q'(t) = r(t) - s$ and
$T = Q/s$, we have $T' = r/s - 1$, so the **departure rate** is

$$
r(t) =
\begin{cases}
\dfrac{\alpha}{\alpha - \beta}\,s, & t_s \le t < \tilde t, \\[2ex]
\dfrac{\alpha}{\alpha + \gamma}\,s, & \tilde t \le t \le t_e,
\end{cases}
$$ (eq-16-bottleneck-rate)

higher than capacity before the departure time $\tilde t$ of the commuter
who arrives exactly on time, lower after it.

### Watershed times and equilibrium cost

The first commuter, departing at $t_s$, meets no queue and arrives early;
the last, departing at $t_e$, meets no queue either (the queue has just
cleared) and arrives late. Both have the equilibrium cost:

$$
\begin{aligned}
C &= \beta\left(t^* - t_s\right), \\
C &= \gamma\left(t_e - t^*\right) .
\end{aligned}
$$

The bottleneck works at capacity throughout the peak, so the $N$ commuters
pass in $t_e - t_s = N/s$. Solving these two equations,

$$
\begin{aligned}
t_s &= t^* - \frac{\gamma}{\beta + \gamma}\,\frac{N}{s}, \\
t_e &= t^* + \frac{\beta}{\beta + \gamma}\,\frac{N}{s}, \\
C &= \frac{\beta\gamma}{\beta + \gamma}\,\frac{N}{s} \\
&= \delta\,\frac{N}{s} .
\end{aligned}
$$ (eq-16-bottleneck-times)

The on-time commuter has only travel time cost,
$C = \alpha T(\tilde t) = \alpha(t^* - \tilde t)$. The queue is longest
when this commuter departs, so

$$
\begin{aligned}
\tilde t &= t^* - \frac{\delta}{\alpha}\,\frac{N}{s}, \\
Q_{\max} &= s\,T(\tilde t) \\
&= \frac{\delta}{\alpha}\,N
\end{aligned}
$$ (eq-16-bottleneck-queue)

{numref}`fig-16-bottleneck-cumulative` shows the cumulative departures and the
cumulative exits from the bottleneck; the horizontal distance between the
curves is a commuter's queuing time and the vertical distance is the queue.

```{figure} figures/16-bottleneck-cumulative.svg
:name: fig-16-bottleneck-cumulative
:width: 560px
:class: dark-light

Cumulative departures and exits at the bottleneck for the example of
{prf:ref}`ex-31-bottleneck` ($N = 5\,000$, $s = 2\,000$ veh/h). The shaded
area is the total queuing time.
```

### Total costs and pricing

Every commuter bears cost $\delta N/s$, so the **total cost** is
$\mathrm{TC} = \delta N^2/s$. It splits equally into total travel (queuing)
time cost and total schedule delay cost:

$$
\begin{aligned}
\mathrm{TTC} &= \frac{\delta N^2}{2s}, \\
\mathrm{SDC} &= \frac{\delta N^2}{2s}, \\
\mathrm{TC} &= \frac{\delta N^2}{s} .
\end{aligned}
$$ (eq-16-bottleneck-total)

The total cost grows with the **square** of demand: an extra commuter both
bears the equilibrium cost and lengthens the peak for everybody else. The
queuing time is pure waste. A **time-varying toll** that rises linearly from
zero at $t_s$ to $\delta N/s$ at $\tilde t$ and falls back to zero at $t_e$
replicates the queuing cost. Commuters then arrive at work at the same
times as before but depart at exactly the capacity rate $s$; the queue
disappears, the schedule delay cost is unchanged, and the total social cost
halves to $\delta N^2/(2s)$, with the former queuing cost collected as toll
revenue ({prf:ref}`ex-31-bottleneck`).

## Instantaneous and experienced travel times

In a dynamic network the travel time of a link depends on the time at which
a vehicle enters it. Two route travel times can then be computed for a
traveler departing at time $\tau$:

- The **instantaneous travel time (ITT)** adds the link times prevailing at
  the departure time $\tau$, as if the network state were frozen. It is
  what a traveler would estimate from a snapshot of current conditions
  (pre-trip information).
- The **experienced travel time (ETT)** follows the vehicle: the time of
  each link is the time prevailing when the vehicle actually enters it,
  which depends on the times of the previous links. It is the travel time
  the traveler actually experiences.

For a route of links $a_1, a_2, \ldots, a_m$ with entry-time-dependent link
times $t_a(\tau)$,

$$
\begin{aligned}
\mathrm{ITT}(\tau) &= \sum_{i=1}^{m} t_{a_i}(\tau), \\
\mathrm{ETT}(\tau) &= \tau_m - \tau, \\
\tau_0 &= \tau, \\
\tau_i &= \tau_{i-1} + t_{a_i}(\tau_{i-1}), \quad i = 1, \ldots, m .
\end{aligned}
$$ (eq-16-itt-ett)

When congestion is building up, the ITT underestimates the time actually
experienced; when it is dissipating, it overestimates it. A route that is
shortest by ITT can be far from shortest by ETT ({prf:ref}`ex-31-itt-ett`).
The dynamic user equilibrium is defined on experienced times, so DTA needs
**time-dependent shortest paths**. If link times satisfy FIFO (entering
later never means leaving earlier), Dijkstra's algorithm still works with
labels that are arrival times: a link $(i, j)$ is scanned at the earliest
arrival time at $i$ (Dreyfus, 1969).

## Dynamic traffic assignment

### Algorithmic framework

Static and dynamic assignment share three core procedures: finding shortest
paths, assigning trips to paths, and checking convergence. In static
assignment the shortest paths are the same over the whole period and loading
is a matrix operation; in DTA they change from one departure interval to the
next, and loading is a traffic simulation. A simulation-based DTA iterates
as follows (Chiu et al., 2011):

1. **Network loading.** Move the vehicles along their assigned paths with a
   traffic simulation (link models, queues, signals, spillback), and record
   the time-varying link travel times and delays. Vehicles follow FIFO;
   arrivals are discretized in small simulation intervals (seconds).
2. **Path set update.** For each O-D pair and assignment interval (minutes),
   compute the time-dependent shortest path with the experienced travel
   times of step 1 and add it to the path set.
3. **Path adjustment.** Shift some vehicles of each O-D pair and interval
   from slower to faster paths: MSA, gradient projection, or origin- and
   bush-based methods.
4. **Convergence check.** Compute a dynamic relative gap, the analogue of
   {eq}`eq-13-relative-gap` with experienced times summed over all departure
   intervals; stop if it is small enough, otherwise return to step 1.

The procedure is heuristic: unlike Beckmann's program, the dynamic
equilibrium has no general convex formulation, its existence and
uniqueness are not guaranteed, and convergence is checked empirically.
DTA is used to evaluate operational measures that static models cannot
capture — incident management, work zones, ramp metering, signal timing,
managed lanes, and time-of-day pricing — on corridors and sub-areas, often
with demand taken from a static regional model (Sloboden et al., 2012).

## Multi-agent transport simulation

### Agent-based demand

Agent-based models go one step further and simulate every traveler as an
**agent** with a daily **plan**: a chain of activities (home, work,
shopping, home) with locations and times, connected by trips with modes and
routes. Demand is not an O-D matrix but the result of the agents' choices.
**MATSim** (Multi-Agent Transport Simulation), developed at ETH Zurich and
TU Berlin by K. W. Axhausen and K. Nagel, is an open-source Java framework
built on this idea (Horni et al., 2016;
<https://www.matsim.org>).

### Inputs and the MATSim loop

The inputs are a multimodal **network** (nodes, links with length,
free-flow speed, capacity, and lanes; transit schedules), a synthetic
**population** with attributes (age, car availability, and so on) and an
initial plan for every agent, and the **scoring** parameters — the marginal
utilities of performing activities, of traveling by each mode, of waiting,
and of arriving late.

MATSim then iterates a **co-evolutionary** loop:

1. **Mobility simulation (mobsim).** Each agent executes one plan, selected
   from its memory, for example with a logit model of the plan scores. All
   plans are executed simultaneously on the network, with queues at
   capacity-restricted links.
2. **Scoring.** The executed plan of each agent is scored with a utility
   function: utility of performing activities minus disutility of travel,
   minus penalties for late arrival or early departure.
3. **Replanning.** A share of the agents modify a plan — departure times,
   routes (time-dependent best response to the travel times of the last
   iteration, often smoothed by successive averaging), modes — and add it to
   their memory; plans with low scores are eventually deleted.

The loop stops after a given number of iterations, or when the average
score of the executed plans stabilizes. The result is a **relaxed
equilibrium**: no agent can improve its score by changing its plan, within
the choice dimensions offered by replanning. It is a stochastic user
equilibrium over complete daily plans rather than single trips. {prf:ref}`ex-31-matsim-scores` traces two iterations
of the loop for ten agents, including the smoothing of link travel times
across iterations, which plays the role of the MSA step size.

### Outputs

MATSim writes an **events file** listing every event of the simulated day
(an agent leaves an activity, enters or leaves a link, boards a vehicle,
starts an activity) with time, agent, vehicle, and link; a **plans file**
with the final plans of all agents and their scores; and summary statistics
and graphs (average score by iteration, mode shares, trip durations, and
departures, arrivals, and agents en route over the day). Because each agent
is tracked, the results can be aggregated in any way — link volumes by
minute, travel times of a population group, the users of a new road — and
animated with the visualizer. The price is effort: synthetic populations,
detailed networks, and calibration of the scoring function, and run times
of hours for large regions.

## Summary and Common Mistakes

### Summary

- The dynamic user equilibrium equalizes **experienced** travel costs for
  each departure interval (route choice) or across departure times
  (departure time and route choice).
- In the bottleneck model with cost {eq}`eq-16-bottleneck-cost`, the
  departure rate {eq}`eq-16-bottleneck-rate` is $\alpha s/(\alpha - \beta)$
  before and $\alpha s/(\alpha + \gamma)$ after the on-time departure;
  every commuter bears the cost $\delta N/s$ {eq}`eq-16-bottleneck-times`,
  the queue peaks at $\delta N/\alpha$ {eq}`eq-16-bottleneck-queue`, and the
  total cost $\delta N^2/s$ is split equally between queuing and schedule
  delay {eq}`eq-16-bottleneck-total`
  ({numref}`fig-16-bottleneck-cumulative`).
- ITT uses the network state at departure; ETT follows the vehicle
  {eq}`eq-16-itt-ett`.
- Simulation-based DTA iterates network loading, time-dependent shortest
  paths, and path adjustment; MATSim extends the idea to agents with daily
  activity plans and reaches a relaxed equilibrium.

### Common mistakes

- **Using instantaneous travel times to evaluate a dynamic equilibrium.**
  The equilibrium is defined on experienced times; ITT misjudges routes
  whenever conditions change during the trip.
- **Forgetting the FIFO requirement of time-dependent shortest-path
  algorithms.** The Dijkstra-type search with arrival-time labels is exact
  only if entering a link later never means leaving it earlier.
- **Assuming that the bottleneck queue would disappear if commuters "just
  left earlier".** At equilibrium the queue is the price that allocates the
  scarce arrival times close to $t^*$; only a time-varying toll removes it.
- **Forgetting that the total cost of the bottleneck grows with the square
  of $N$.** Each extra commuter bears the equilibrium cost and lengthens the
  peak for everybody else.
- **Treating a simulation-based equilibrium as unique and exact.** Results
  vary with the random seed and the number of iterations; report several
  runs.

## References

- Vickrey, W. S. (1969). Congestion theory and transport investment.
  *American Economic Review*, *59*(2), 251–260.
- Arnott, R., de Palma, A., & Lindsey, R. (1990). Economics of a bottleneck.
  *Journal of Urban Economics*, *27*(1), 111–130.
- Arnott, R., de Palma, A., & Lindsey, R. (1993). A structural model of
  peak-period congestion: A traffic bottleneck with elastic demand.
  *American Economic Review*, *83*(1), 161–179.
- Small, K. A. (1982). The scheduling of consumer activities: Work trips.
  *American Economic Review*, *72*(3), 467–479.
- Dreyfus, S. E. (1969). An appraisal of some shortest-path algorithms.
  *Operations Research*, *17*(3), 395–412.
- Chiu, Y.-C., Bottom, J., Mahut, M., Paz, A., Balakrishna, R., Waller, T.,
  & Hicks, J. (2011). *Dynamic Traffic Assignment: A Primer*. Transportation
  Research Circular E-C153. Transportation Research Board.
- Sloboden, J., Lewis, J., Alexiadis, V., Chiu, Y.-C., & Nava, E. (2012).
  *Traffic Analysis Toolbox Volume XIV: Guidebook on the Utilization of
  Dynamic Traffic Assignment in Modeling* (FHWA-HOP-13-015). Federal Highway
  Administration.
- Horni, A., Nagel, K., & Axhausen, K. W. (Eds.). (2016). *The Multi-Agent
  Transport Simulation MATSim*. Ubiquity Press.
  <https://doi.org/10.5334/baw>
