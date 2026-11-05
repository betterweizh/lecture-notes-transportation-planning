# Zoning and Network Coding

This chapter works through the examples and problems of
{doc}`06-zoning-and-networks`.

## Designing a zoning system

:::{prf:example} Zoning Punggol Town
:label: ex-21-punggol-zoning

Punggol is a new town in north-eastern Singapore with an area of about
$3.74~\mathrm{km}^2$ and, in 2019, about 187 800 residents living mostly in
public (HDB) housing, organized in a number of residential districts around
a town center with a rail (MRT/LRT) station and a mall.

(a) Propose a zoning system of traffic analysis zones (TAZs) for a 2020
transportation planning study of the town.

(b) Choose one TAZ and discuss its likely trip productions and attractions.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**(a) Number of zones.** Start with the quantitative rules of thumb of
NCHRP Report 716 (see {ref}`sec-06-zoning-rules`).

*Residents per zone* between 1 200 and 3 000:

$$
\frac{187\,800}{3\,000} \approx 63
\ \le\ \text{number of zones}\ \le\
\frac{187\,800}{1\,200} \approx 157 .
$$

*Area per zone* between $0.65$ and $2.59~\mathrm{km}^2$:

$$
\frac{3.74}{2.59} \approx 1.4
\ \le\ \text{number of zones}\ \le\
\frac{3.74}{0.65} \approx 5.8 .
$$

*Trips per zone* below 15 000 per day: assuming for illustration about two
person trips per resident per day, the town generates about 375 600 trips,
so at least $375\,600/15\,000 = 25.04$, that is 26, zones are needed.

The rules contradict each other — the population rule asks for 63–157 zones,
the area rule for 2–5, the trip rule for at least 26 — because they were calibrated for low-density US
cities. In a high-density town the area rule must be dropped; the population
and trip rules are closer to practice in Singapore, whose strategic models
use roughly 5 000 residents per zone (about 1 170 zones for 5.7 million
people), which would give about 38 zones for Punggol.

**Zone boundaries.** Apply the qualitative criteria:

1. *Compatibility with statistical units.* Build zones from Singapore's
   planning subzones and housing precincts so that census and housing data
   can be attached directly.
2. *Homogeneity.* Keep residential precincts, the town center (mall,
   transport hub, offices), schools, parks, and industrial land in separate
   zones.
3. *Boundaries.* Use the waterway, the park connector, and the expressway
   corridor as natural boundaries; avoid splitting a housing precinct along
   its access road.
4. *Access.* Give each zone a centroid at its center of activity (for
   example the main block cluster or the mall), connected to the network at
   its real access points and, for public transport, to the nearest LRT
   station.
5. *Hierarchy.* Number zones by district so that they can be aggregated.

A reasonable design for a town-level strategic study is therefore a
hierarchical system of about **14 coarse zones** — one per residential
district, plus the town center, the industrial/creative cluster, and the
large parks — each subdivided into two or three subzones (roughly 30–40 in
total) for detailed local studies. Any number in this range is defensible
if the reasoning above is followed; there is no unique answer.

**(b) Productions and attractions of a residential TAZ.** Take a zone
containing several HDB blocks, a neighborhood center with a supermarket and
food court, and two primary schools.

- *Productions* (home end of home-based trips): HB work trips by employed
  residents, HB education trips by students, HB shopping and leisure trips,
  and escort trips (parents taking children to school). They are driven by
  the number of households, household size, workers, students, income, and
  car ownership.
- *Attractions* (non-home end): education trips to the two schools
  (enrollment, staff), shopping and dining trips to the neighborhood center
  (retail floor space, employment), and work trips of the employees of the
  schools and shops.
- *Non-home-based trips* (e.g., from the MRT station to the shops on the
  way home) are produced where they start.

Because the zone is mainly residential, its daily productions exceed its
attractions. Productions and attractions carry no direction, however: in the
morning peak most home-based trips *leave* the zone (origins exceed
destinations), and in the evening peak the same trips return, so
destinations exceed origins.
:::

## Coding a signalized junction

:::{prf:example} Network representation of a signalized junction
:label: ex-21-junction-coding

A four-arm signalized junction in Singapore has three-lane approaches; on
each approach two lanes serve the through movement and one lane serves the
right turn, and left turns use a separate slip lane that is not controlled
by the signal.

(a) Represent the junction as a directed graph that allows the effect of the
signal control to be modeled, assuming a reasonable signal plan.

(b) Using the BPR function
$t_a(x_a) = t_a^0\left[1 + 0.15\left(x_a/c_a\right)^4\right]$ and a lane
capacity of 1 800 passenger cars per hour (pcu/h), formulate a travel time
function for each link and explain how its parameters are obtained.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

**(a) Directed graph.** Expand the junction as in
{numref}`fig-06-junction-coding`(b). For each approach $\ell \in \{N, E, S, W\}$
create an **entry node** $\ell^{\mathrm{in}}$ and an **exit node**
$\ell^{\mathrm{out}}$, and an external node $\ell^{\mathrm{ext}}$ at the
upstream end of the road. The link set is:

- 8 **normal links**: $(\ell^{\mathrm{ext}}, \ell^{\mathrm{in}})$ and
  $(\ell^{\mathrm{out}}, \ell^{\mathrm{ext}})$ for each approach;
- 12 **turning links**: from each entry node to the exit nodes of the other
  three approaches — left, through, and right (U-turns are not coded).

The graph has $3 \times 4 = 12$ nodes and $8 + 12 = 20$ links. With
left-hand traffic, from the west entry the left turn goes to $N^{\mathrm{out}}$,
the through movement to $E^{\mathrm{out}}$, and the right turn to
$S^{\mathrm{out}}$.

**Signal plan.** Assume a four-phase plan with cycle length $C = 120$ s:

| Phase | Movements | Green $g$ (s) | Amber (s) |
|---|---|---|---|
| A | north and south through | 42 | 3 |
| B | north and south right turns | 12 | 3 |
| C | east and west through | 42 | 3 |
| D | east and west right turns | 12 | 3 |

The phases sum to $42 + 12 + 42 + 12 + 4\times 3 = 120$ s. Left turns on
slip lanes run continuously.

**(b) Link performance functions.** Each link receives the BPR function with
its own free-flow time and capacity. Take the effective green time equal to
the displayed green (the amber time used by vehicles roughly offsets the
start-up lost time), so that the green ratios are

$$
\begin{aligned}
\frac{g}{C} &= \frac{42}{120} = 0.35 \ \ \text{(through)}, \\
\frac{g}{C} &= \frac{12}{120} = 0.10 \ \ \text{(right turn)}.
\end{aligned}
$$

By {eq}`eq-06-signal-capacity`, $c_a = s\, n_a\, g_a/C$ with
$s = 1\,800$ pcu/h per lane:

| Link type | Lanes $n_a$ | $g_a/C$ | Capacity $c_a$ (pcu/h) |
|---|---|---|---|
| through movement | 2 | 0.35 | $1\,800 \times 2 \times 0.35 = 1\,260$ |
| right turn | 1 | 0.10 | $1\,800 \times 1 \times 0.10 = 180$ |
| left turn (slip lane, unsignalized) | 1 | 1 | 1 800 |
| approach and exit roads | 3 | 1 | 5 400 |

The travel time function of, say, the west-to-east through movement is then

$$
t_{W\to E}(x) = t^0_{W\to E}\left[1 + 0.15\left(\frac{x}{1\,260}\right)^{4}\right],
$$

where $t^0$ is the free-flow time to cross the junction (length of the
movement divided by the free-flow speed). The free-flow times of normal
links come from their lengths and speed limits.

**Remarks.**

- The BPR function with a reduced capacity captures the *capacity* effect
  of the signal but not the *average delay* that even an uncongested
  vehicle suffers at a red light. A better formulation adds a fixed signal
  delay to $t^0$, for example Webster's uniform delay
  $C(1 - g/C)^2/[2(1 - (g/C)X)]$, which for $X \to 0$ is
  $120(1 - 0.35)^2/2 \approx 25$ s for the through movements and
  $120(1 - 0.10)^2/2 \approx 49$ s for the right turns.
- The right-turn capacity of 180 pcu/h is very low; if right-turn demand is
  high, the green split should be revised, which is exactly the kind of
  change the expanded coding allows the model to evaluate.
:::

## Network elements

:::{prf:example} Counting the elements of a coded network
:label: ex-21-graph-elements

A road network has nodes $N = \{1, 2, 3, 4, 5\}$, where node 1 is the
centroid of a zone, and links

$$
\begin{aligned}
A = \{&(1,2), (1,3), (1,4), (1,5), (2,3), (2,5), \\
      &(3,2), (3,4), (4,3), (4,5), (5,2), (5,4)\}.
\end{aligned}
$$

Classify the links and identify the two-way roads.
:::

:::{dropdown} Solution
:class-container: solution
:animate: fade-in

There are $\lvert N\rvert = 5$ nodes and $\lvert A\rvert = 12$ links.

- The four links leaving node 1, $(1,2), (1,3), (1,4), (1,5)$, are
  **centroid connectors**. Since no link enters node 1, the centroid is
  coded only as an origin; for the zone to attract trips, the reverse
  connectors $(2,1), \ldots, (5,1)$ would have to be added.
- The other eight links are normal links. The pairs $\{(2,3),(3,2)\}$,
  $\{(3,4),(4,3)\}$, $\{(4,5),(5,4)\}$, and $\{(2,5),(5,2)\}$ are the two
  directions of four two-way roads forming the ring $2-3-4-5-2$.

Paths between other zones must not pass through node 1, which in planning
software is ensured by marking it as a centroid.
:::
