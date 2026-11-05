# Zoning Systems, Networks, and Data

## Overview

A transport model cannot work with every household, building, and street of
a city. It represents space by a **zoning system** — a set of traffic
analysis zones whose activities are concentrated at notional points called
centroids — and represents the transport system by a **network** of nodes
and links whose costs depend on the flows they carry. This chapter defines
these objects, gives practical rules for designing them, introduces the
link performance functions used in traffic assignment, and reviews the data
a travel demand model needs.

:::{admonition} Learning objectives
:class: objectives
After completing this chapter, readers should be able to:

- define the study area, external cordon, traffic analysis zones (TAZs),
  centroids, and centroid connectors;
- apply rules of thumb and criteria for designing a zoning system;
- distinguish productions/attractions from origins/destinations and write
  the two balance equations of a trip matrix;
- represent a road network, including a signalized junction, as a directed
  graph;
- write the BPR link performance function and derive the capacity of a
  signal-controlled movement; and
- list the data needed to build, calibrate, and validate a demand model.
:::

## Notation

| Symbol | Meaning |
|---|---|
| $z$ | number of zones |
| $O_i$ | trips produced by / originating in zone $i$ during the period |
| $D_j$ | trips attracted to / destined for zone $j$ during the period |
| $T_{ij}$ | trips from zone $i$ to zone $j$ during the period |
| $T$ | total number of trips, $T = \sum_i\sum_j T_{ij}$ |
| $G = (N, A)$ | directed graph with node set $N$ and link set $A \subseteq N\times N$ |
| $x_a$ | flow on link $a \in A$ (vehicles or pcu per hour) |
| $t_a(x_a)$ | travel time on link $a$ as a function of its flow |
| $t_a^0$, $c_a$ | free-flow travel time and capacity of link $a$ |
| $\alpha$, $\beta$ | parameters of the BPR function |
| $s$, $n_a$ | saturation flow per lane; number of lanes of movement $a$ |
| $g_a$, $C$ | effective green time of movement $a$; signal cycle length |

## The study area and zoning system

### Study area and cordons

The **study area** is the region whose travel is modeled in detail. Its
boundary is the **external cordon**. The choice depends on the decision
context and the type of trips of interest:

- for strategic studies, the area should contain the origin and destination
  of most trips, although this is not always possible for small urban areas;
- for traffic management studies of a local area, what matters is whether
  the changes caused by the schemes being tested can be modeled;
- the study area should be somewhat larger than the area directly affected
  by the schemes, so that re-routing and changes of destination are captured
  inside the model; and
- political boundaries are of secondary importance: the area that matters is
  the one that will be affected over the planning horizon, which is often
  larger than the one named in the project brief.

The rest of the world is represented by a small number of **external
zones**, usually one for each major road or rail corridor crossing the
cordon. Inside the study area, **screen lines** — artificial divides that
follow natural or man-made barriers with few crossing points (a river, a
railway, an expressway) — and internal cordons are used to count traffic
and check the model.

### Traffic analysis zones and centroids

Socioeconomic data (households, population, employment, land use) are
organized into geographic units called **traffic analysis zones (TAZs)**.
All activities of a zone are assumed to be concentrated at a single point,
its **centroid**. The centroid is a notional point that does not need to
coincide with the geometric center of the zone; it should reflect the center
of activity. Centroids are attached to the network by **centroid
connectors**, which represent the average cost (time, distance) of reaching
the network from the zone and should join it at the natural access and
egress points of the zone.

The number of zones is a trade-off. Many small zones reduce the
**aggregation error** caused by concentrating all activity at the centroid,
but they require more data, produce sparse trip matrices, and increase
computing time. Typical studies use from a few hundred to a few thousand
zones; for example, Singapore's strategic model has been run with about
1 170 zones for some 5.7 million residents (about 4 900 people per zone),
and the Dallas–Fort Worth model with 4 875 zones for 6.5 million people
(about 1 330 per zone).

(sec-06-zoning-rules)=
### Rules of thumb and design criteria

The NCHRP Report 716 guidelines (United States) suggest that, where
possible,

- each TAZ should contain more than 1 200 and fewer than 3 000 residents;
- each TAZ should generate fewer than 15 000 person trips per day; and
- each TAZ should cover one quarter to one square mile, that is about
  $0.65$ to $2.59~\mathrm{km}^2$.

These rules were written for US cities and conflict with each other in
very dense cities, where 3 000 residents may live in a single housing block
(see {prf:ref}`ex-21-punggol-zoning`). The following qualitative criteria,
compiled by Ortúzar and Willumsen from practical studies, are more general:

1. Zones must be small enough for the aggregation error to be acceptable.
   It is convenient to start with many small zones and aggregate them later.
2. The zoning system must be compatible with administrative divisions,
   especially census zones, so that data can be attached to zones. This is
   the most important criterion.
3. Zones should be as homogeneous as possible in land use and population
   (for example, income); areas that differ strongly should not be merged
   even if they are small.
4. Zone boundaries must be compatible with cordons, screen lines, and
   previous zoning systems. Using main roads as boundaries is common
   (NCHRP), but it makes it ambiguous to which zone trips with ends on the
   road belong; many modelers therefore prefer boundaries along the
   "backs" of activity, such as rivers, rail lines, or the rear of
   frontage development.
5. The shape of a zone should make it easy to define its centroid
   connectors; a zone should be the natural catchment area of the network
   nodes it connects to.
6. Zones need not be of equal area; if anything they should be of similar
   size in travel-time units, so zones are smaller in congested central
   areas.

A **hierarchical** zoning system (subzones within zones within districts
within sectors), with a numbering scheme in which leading digits identify
the higher levels, allows each analysis to be carried out at the right level
of detail.

## Trip ends and the trip matrix

### Productions and attractions, origins and destinations

A trip has two ends. Two conventions for labeling them are used, and
confusing them is a common source of error.

- **Origin and destination** describe the direction of travel: a trip goes
  *from* its origin *to* its destination.
- **Production and attraction** describe the land use that causes the trip.
  For a **home-based (HB)** trip, the home end is the *production* and the
  other end is the *attraction*, whatever the direction of travel. For a
  **non-home-based (NHB)** trip, the production is the origin and the
  attraction is the destination.

A morning trip from home to work and the evening return trip are two trips
with opposite origins and destinations, but both are *produced* at home and
*attracted* to work. Trip generation models
({doc}`09-trip-generation`) forecast productions and attractions, typically for
a whole day; a **production–attraction (P–A) matrix** is then converted into
an **origin–destination (O-D) matrix** for a specific period (for example
the morning peak hour) using the share of each purpose traveling in each
direction during that period.

### The balance equations

Let $T_{ij}$ be the number of trips from zone $i$ to zone $j$ during the
period. The **trip matrix** $[T_{ij}]_{z\times z}$ has row sums equal to
the trips leaving each zone and column sums equal to the trips arriving at
each zone:

$$
\sum_{j=1}^{z} T_{ij} = O_i, \qquad i = 1,\ldots,z,
$$ (eq-06-row-balance)

$$
\sum_{i=1}^{z} T_{ij} = D_j, \qquad j = 1,\ldots,z.
$$ (eq-06-column-balance)

Summing either set gives the total number of trips,

$$
\begin{aligned}
T &= \sum_{i=1}^{z} O_i \\
&= \sum_{j=1}^{z} D_j \\
&= \sum_{i=1}^{z}\sum_{j=1}^{z} T_{ij}.
\end{aligned}
$$ (eq-06-total-trips)

One purpose of the demand model is to estimate the trip matrix of the
planning year from base-year data. Trip generation estimates $O_i$ and
$D_j$; trip distribution fills the matrix subject to
{eq}`eq-06-row-balance`–{eq}`eq-06-column-balance`.

## Network representation

### Directed graphs

A road network is coded as a **directed graph** $G = (N, A)$, where $N$ is
the set of nodes (junctions, centroids, and shape points) and

$$
A \subseteq N \times N = \{(i, j) : i \in N,\ j \in N\}
$$

is the set of directed **links**. A two-way road between nodes $i$ and $j$
is coded as two links, $(i, j)$ and $(j, i)$. Links fall into three groups:

- **normal links**, representing road segments between junctions;
- **intersection (turning) links**, representing movements through a
  junction when turning delays matter; and
- **centroid connectors**, joining centroids to the network. Centroids must
  not be used as through nodes; in practice paths are prevented from passing
  through a centroid.

For example, the network with nodes $N = \{1, 2, 3, 4, 5\}$ and links

$$
\begin{aligned}
A = \{&(1,2), (1,3), (1,4), (1,5), (2,3), (2,5), \\
      &(3,2), (3,4), (4,3), (4,5), (5,2), (5,4)\}
\end{aligned}
$$

has 5 nodes and 12 links; if node 1 is a centroid, the links leaving it are
centroid connectors.

The purpose of traffic assignment is to load the O-D matrix onto the links
of this graph and obtain the link flows $x_a$, $a \in A$, according to a
route-choice principle ({doc}`13-user-equilibrium-assignment`).

### Coding junctions

A junction can be coded in two ways ({numref}`fig-06-junction-coding`):

1. **As a single node.** All movements share the node, so the model cannot
   distinguish the delay of a left turn from that of a right turn or a
   through movement. This is adequate for strategic models of large areas.
2. **As an expanded junction.** Each approach is split into an entry node
   and an exit node, and each permitted movement is a separate **turning
   link** with its own capacity and delay. Banned turns are simply omitted.
   This is needed when signal control or turning delays matter.

```{figure} figures/06-junction-coding.svg
:name: fig-06-junction-coding
:width: 640px
:class: dark-light

Two ways of coding a four-arm junction with left-hand traffic. (a) A
single node $J$: all turning movements share one node. (b) An expanded
junction: each approach has an external node (N, E, S, W), an entry node,
and an exit node, and every movement is a separate turning link. Only the
three movements from the west entry node $W^{\mathrm{in}}$ are drawn: left
to $N^{\mathrm{out}}$, through to $E^{\mathrm{out}}$, and right to
$S^{\mathrm{out}}$.
```

### Link performance functions

Traffic assignment needs, for every link, a **link performance (cost–flow)
function** $t_a(x_a)$ that gives the travel time as a function of flow. It
must be increasing in $x_a$ to represent congestion. The most widely used is
the **Bureau of Public Roads (BPR)** function (Bureau of Public Roads, 1964),

$$
\begin{aligned}
t_a(x_a) &= t_a^0\left[1 + \alpha\left(\frac{x_a}{c_a}\right)^{\beta}\right], \\
\alpha &= 0.15, \\
\beta &= 4,
\end{aligned}
$$ (eq-06-bpr)

where $t_a^0$ is the free-flow travel time and $c_a$ the "practical"
capacity of the link. At $x_a = c_a$ the travel time is
$1.15\,t_a^0$. The parameters $\alpha$ and $\beta$ can be recalibrated for
local conditions. Because {eq}`eq-06-bpr` is defined for all $x_a \ge 0$, the
assigned flow may exceed $c_a$; the function then grows steeply but stays
finite, which keeps assignment algorithms stable.

Other common forms are Davidson's (1966) function, which tends to infinity
as the flow approaches capacity, and the conical delay functions of Spiess
(1990). In practice links
carry a **generalized cost** that combines time, distance-based operating
cost, and tolls in common (time or money) units.

### Capacity of signal-controlled movements

At a signalized junction, a movement can discharge only during its green
time. If the saturation flow per lane is $s$ (for example $1\,800$
passenger cars per hour of green, a typical prevailing value; the Highway
Capacity Manual starts from a base value of $1\,900$ and adjusts it for local
conditions), the movement has $n_a$ lanes, the effective
green time is $g_a$, and the cycle length is $C$, then

$$
c_a = s \cdot n_a \cdot \frac{g_a}{C}.
$$ (eq-06-signal-capacity)

The ratio $g_a/C$ is the **green ratio** (or green split). Using
{eq}`eq-06-signal-capacity` as the capacity in the BPR function of each turning
link makes the link performance functions reflect the signal plan;
alternatively, an average signal delay can be added to $t_a^0$, for example
the uniform delay term of Webster (1958),
$d = C(1 - g_a/C)^2 / \{2[1 - (g_a/C)\,X]\}$, where $X = x_a/c_a$ is the
degree of saturation.

### Public transport networks

Public transport networks are more complex because services run along fixed
sequences of links (lines or routes) with frequencies and timetables. Their
coding requires stops and stations, lines with their stop sequences and
headways, access and egress links (walking), transfer links, and fare
rules. Most transit routes run on the road network, so the road network is
coded first and transit lines are coded on top of it.

## Data for travel demand modeling

The quality of the input data limits the quality of any model. Data
availability and accuracy, the ability to update them periodically, and the
possibility of forecasting them are the main criteria for selecting the
variables of a model.

### Socioeconomic and land-use data

- **Population and households.** Censuses are the most complete source.
  Singapore's Census of Population is conducted every ten years and
  combines administrative registers with a large sample enumeration of
  households; the US decennial census provides block-level counts that can
  be aggregated to zones.
- **Employment.** Accurate employment by zone is harder to obtain than
  household data: jobs move, establishments are reported at the company
  rather than the site level, and there is no census-like control total at
  small geographic levels. Official labor statistics and establishment
  registers are the usual sources.
- **Land use.** Floor space by use (residential, retail, office, industrial,
  education), school enrollment, parking supply.

### Travel data

Household interview travel surveys are the main source of information on
travel behavior ({doc}`07-travel-surveys-and-sampling`). Singapore's Land
Transport Authority conducts its Household Interview Travel Survey (HITS)
every four to five years using a one-day trip diary for every household
member. A household survey provides

- **household data:** location, size, age and sex of members, structure,
  workers, occupations, places of work and study, vehicle ownership, and
  income; and
- **trip data:** origin and destination, purpose, mode or modes, start and
  end times, and cost.

Such data allow trips to be linked into **tours** and support activity-based
models as well as trip-based ones.

### Network and validation data

Road networks are coded consistently with the zoning system, more finely in
developed areas with small zones and more coarsely elsewhere. Link
attributes include length, number of lanes, free-flow speed, capacity, and
the link performance function; node attributes include junction type and
signal plans. Open data such as OpenStreetMap can provide the geometry, but
attributes must be checked.

Independent data are needed for **validation**: traffic counts on screen
lines and cordons, public transport boardings, and observed travel times.
A model is validated by comparing modeled and observed values for data
that were not used to calibrate it.

## Summary and Common Mistakes

### Summary

- Space is represented by zones and centroids; the zoning system must
  balance aggregation error against data and computing costs
  ({ref}`sec-06-zoning-rules`).
- Productions and attractions describe the land use that causes a trip,
  origins and destinations its direction; the two coincide only for
  non-home-based trips.
- Trip matrices satisfy the row-sum (origin) and column-sum (destination)
  balance equations {eq}`eq-06-row-balance` and {eq}`eq-06-column-balance`,
  so that all margins add up to the same total {eq}`eq-06-total-trips`.
- Networks are directed graphs; junctions can be expanded into turning
  links ({numref}`fig-06-junction-coding`); links carry increasing cost–flow
  functions such as the BPR function {eq}`eq-06-bpr`, whose capacity at a
  signal follows from {eq}`eq-06-signal-capacity`.
- Socioeconomic, travel, network, and validation data each play a distinct
  role in building a model.

### Common mistakes

- **Using production–attraction tables as if they were origin–destination
  tables for a specific period.** A P–A table records home-based trips at
  their home end in both directions; it must be converted with directional
  factors for the period before assignment.
- **Placing centroids at the geometric center of a zone and connecting them
  to the nearest node.** The centroid should sit at the center of activity
  and its connectors at the real access points; otherwise route choice and
  link loads near the zone are distorted.
- **Letting paths pass through centroids or centroid connectors.** A
  centroid is not a junction; through paths over connectors create
  artificial short cuts and must be blocked.
- **Coding a signalized junction as a single node when the study is about
  junction operation.** A single node cannot give different delays to
  different turning movements; use an expanded junction with turning
  links.

## References

- Ortúzar, J. de D., & Willumsen, L. G. (2011). *Modelling Transport* (4th
  ed.), Section 3.5 (Network and zoning systems). Wiley.
  <https://doi.org/10.1002/9781119993308>
- Cambridge Systematics et al. (2012). *Travel Demand Forecasting:
  Parameters and Techniques* (NCHRP Report 716), Chapter 3. Transportation
  Research Board. <https://doi.org/10.17226/14665>
- Sheffi, Y. (1985). *Urban Transportation Networks: Equilibrium Analysis
  with Mathematical Programming Methods*, Chapter 1. Prentice-Hall.
- Transportation Research Board. (2016). *Highway Capacity Manual: A guide
  for multimodal mobility analysis* (6th ed.), Chapter 19 (Signalized
  intersections). The National Academies Press.
- Bureau of Public Roads. (1964). *Traffic assignment manual*. U.S.
  Department of Commerce, Urban Planning Division.
- Davidson, K. B. (1966). A flow travel time relationship for use in
  transportation planning. *Proceedings of the 3rd Australian Road Research
  Board Conference*, *3*(1), 183–194.
- Spiess, H. (1990). Conical volume-delay functions. *Transportation
  Science*, *24*(2), 153–158. <https://doi.org/10.1287/trsc.24.2.153>
- Webster, F. V. (1958). *Traffic signal settings* (Road Research Technical
  Paper No. 39). Her Majesty's Stationery Office.
