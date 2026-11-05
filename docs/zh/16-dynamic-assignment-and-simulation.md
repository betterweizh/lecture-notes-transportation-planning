# 交通分配（四）：动态分配与仿真

## 概述

前面各章的静态模型假设 O-D 流量和路段行程时间在所建模的时段内恒定不变。高峰时段的拥堵并非如此：排队形成又消散，早出发十分钟的出行者会遇到不同的状况，许多出行者调整出发时间以避开最拥堵的时段。**动态交通分配**（dynamic traffic assignment，DTA）引入了时间维度。本章阐述动态用户均衡条件，以闭式求解最简单的动态模型——Vickrey 的出发时间选择瓶颈模型——区分瞬时行程时间（instantaneous travel time）与实际经历行程时间（experienced travel time），概述一般的动态交通分配算法，并介绍基于 MATSim 的多智能体仿真。

:::{admonition} 学习目标
:class: objectives
学完本章后，读者应能够：

- 写出路径选择以及出发时间与路径联合选择的动态用户均衡条件；
- 推导瓶颈模型的均衡，并计算其出发率、排队长度和费用；
- 计算路径的瞬时行程时间和实际经历行程时间，并解释二者差别的重要性；
- 描述基于仿真的动态交通分配的算法框架；
- 解释 MATSim 等基于智能体的仿真如何表示需求并达到松弛均衡。
:::

## 符号说明

| 符号 | 含义 |
|---|---|
| $N$ | 通勤者人数 |
| $s$ | 瓶颈通行能力（单位时间车辆数） |
| $t^*$ | 期望（规定）的上班到达时间 |
| $T(t)$ | 在时刻 $t$ 出发的通勤者的排队时间 |
| $Q(t)$ | 时刻 $t$ 的排队长度（车辆数） |
| $r(t)$ | 时刻 $t$ 的出发率 |
| $\alpha$, $\beta$, $\gamma$ | 出行时间价值、早到和晚到的单位费用 |
| $\delta$ | $\beta\gamma/(\beta + \gamma)$ |
| $t_s$, $t_e$, $\tilde t$ | 最早和最晚出发时刻；准时到达者的出发时刻 |
| $C(t)$ | 在时刻 $t$ 出发的通勤者的广义费用 |

## 从静态均衡到动态均衡

静态用户均衡（Wardrop 第一原理）指出，一个 O-D 对的所有被使用路径具有相等且最小的行程时间。加入时间维度后，得到两种动态形式：

- **路径选择的动态用户均衡（DyUE）。** 对每个 O-D 对和每个出发时段，所有被使用路径的**实际经历**行程时间（广义费用）相等且最小，任何出行者都不能通过单方面改变路径来减少其实际经历的行程时间。
- **出发时间与路径选择的动态用户均衡。** 对每个 O-D 对，所有被使用的路径与出发时间组合具有相等且最小的实际经历广义费用，此时广义费用中还包括早于或晚于期望时刻到达的惩罚。

时间带来了静态模型所没有的两种效应。在**需求方面**，在某一时段内无法通过的出行者会溢出到下一时段，因此各时段的需求不再相互独立。在**供给方面**，路段行程时间随车辆进入路段的时刻而变化，因此路径时间取决于到达其各路段的时刻。排队还会向上游路段蔓延，而可分离的静态费用函数无法表示这一点。

## 瓶颈模型

### 模型设定

Vickrey（1969）的出发时间选择（departure time choice）瓶颈模型（bottleneck model）经 Arnott、de Palma 和 Lindsey（1990，1993）发展，是最简单的出发时间选择模型，可以闭式求解。$N$ 名相同的通勤者在早高峰从家开车去上班。除一个通行能力为 $s$ 的**瓶颈**外，出行都不拥堵：若车辆到达瓶颈的速率超过 $s$，就会形成排队，按先进先出（FIFO）的规则服务。所有通勤者都希望在同一时刻 $t^*$ 到达单位，早到或晚到都要付出**计划延误**（schedule delay）惩罚。

令自由流行程时间为零（这只是平移所有时间，不影响结果），在时刻 $t$ 出发的通勤者在队列中等待 $T(t) = Q(t)/s$，于 $t + T(t)$ 到达单位。出行的广义费用为

$$
C(t) =
\begin{cases}
\alpha T(t) + \beta\left[t^* - t - T(t)\right], & \text{早到}, \\
\alpha T(t) + \gamma\left[t + T(t) - t^*\right], & \text{晚到},
\end{cases}
$$ (eq-16-bottleneck-cost)

其中 $\alpha$ 为出行时间价值，$\beta$ 为单位时间早到的费用，$\gamma$ 为单位时间晚到的费用。实证上 $\beta < \alpha < \gamma$（Small（1982）得到 $\beta \approx 0.6\alpha$，$\gamma \approx 2.4\alpha$）：早到不如出行那样令人不快，而出行又不如晚到那样令人不快。

### 均衡出发率

在出发时间均衡状态下，每名通勤者的费用相同，因此 $C(t)$ 在出发时段 $[t_s, t_e]$ 内为常数。对早到者，$\diff C/\diff t = \alpha T' - \beta(1 + T') = 0$；对晚到者，$\alpha T' + \gamma(1 + T') = 0$：

$$
T'(t) =
\begin{cases}
\dfrac{\beta}{\alpha - \beta} > 0, & \text{早到者}, \\[2ex]
-\dfrac{\gamma}{\alpha + \gamma} < 0, & \text{晚到者}.
\end{cases}
$$

通勤者早到时排队增长，晚到时排队缩短。由于排队的变化率为 $Q'(t) = r(t) - s$，且 $T = Q/s$，有 $T' = r/s - 1$，因此**出发率**为

$$
r(t) =
\begin{cases}
\dfrac{\alpha}{\alpha - \beta}\,s, & t_s \le t < \tilde t, \\[2ex]
\dfrac{\alpha}{\alpha + \gamma}\,s, & \tilde t \le t \le t_e,
\end{cases}
$$ (eq-16-bottleneck-rate)

在准时到达者的出发时刻 $\tilde t$ 之前高于通行能力，之后低于通行能力。

### 分界时刻与均衡费用

第一名通勤者在 $t_s$ 出发，没有遇到排队，早到；最后一名在 $t_e$ 出发，也没有遇到排队（队列恰好消散），晚到。二者都承担均衡费用：

$$
\begin{aligned}
C &= \beta\left(t^* - t_s\right), \\
C &= \gamma\left(t_e - t^*\right) .
\end{aligned}
$$

在整个高峰期间瓶颈都以通行能力运行，因此 $N$ 名通勤者在 $t_e - t_s = N/s$ 内通过。联立这两个方程，得

$$
\begin{aligned}
t_s &= t^* - \frac{\gamma}{\beta + \gamma}\,\frac{N}{s}, \\
t_e &= t^* + \frac{\beta}{\beta + \gamma}\,\frac{N}{s}, \\
C &= \frac{\beta\gamma}{\beta + \gamma}\,\frac{N}{s} \\
&= \delta\,\frac{N}{s} .
\end{aligned}
$$ (eq-16-bottleneck-times)

准时到达的通勤者只有出行时间费用，$C = \alpha T(\tilde t) = \alpha(t^* - \tilde t)$。该通勤者出发时排队最长，因此

$$
\begin{aligned}
\tilde t &= t^* - \frac{\delta}{\alpha}\,\frac{N}{s}, \\
Q_{\max} &= s\,T(\tilde t) \\
&= \frac{\delta}{\alpha}\,N
\end{aligned}
$$ (eq-16-bottleneck-queue)

{numref}`fig-16-bottleneck-cumulative`给出了累计出发曲线和累计驶离瓶颈曲线；两条曲线之间的水平距离是一名通勤者的排队时间，垂直距离是排队长度。

```{figure} figures/16-bottleneck-cumulative.svg
:name: fig-16-bottleneck-cumulative
:width: 560px
:class: dark-light

{prf:ref}`ex-31-bottleneck`算例（$N = 5\,000$，$s = 2\,000$ 辆/小时）中瓶颈处的累计出发曲线和累计驶离曲线。阴影面积为总排队时间。
```

### 总费用与收费

每名通勤者承担的费用为 $\delta N/s$，因此**总费用**为 $\mathrm{TC} = \delta N^2/s$。它在总出行（排队）时间费用和总计划延误费用之间平分：

$$
\begin{aligned}
\mathrm{TTC} &= \frac{\delta N^2}{2s}, \\
\mathrm{SDC} &= \frac{\delta N^2}{2s}, \\
\mathrm{TC} &= \frac{\delta N^2}{s} .
\end{aligned}
$$ (eq-16-bottleneck-total)

总费用随需求的**平方**增长：一名新增通勤者既承担均衡费用，又延长了所有其他人的高峰时段。排队时间纯属浪费。**时变收费**从 $t_s$ 时的零线性上升到 $\tilde t$ 时的 $\delta N/s$，再线性下降到 $t_e$ 时的零，它恰好复制了排队费用。此时通勤者到达单位的时刻与以前相同，但恰好以通行能力 $s$ 的速率出发；排队消失，计划延误费用不变，社会总费用减半为 $\delta N^2/(2s)$，原来的排队费用转化为收费收入（{prf:ref}`ex-31-bottleneck`）。

## 瞬时行程时间与实际经历行程时间

在动态网络中，路段的行程时间取决于车辆进入该路段的时刻。对在时刻 $\tau$ 出发的出行者，可以计算两种路径行程时间：

- **瞬时行程时间**（instantaneous travel time，ITT）将出发时刻 $\tau$ 的各路段时间相加，就好像网络状态被冻结了一样。它是出行者根据当前状况的快照（出行前信息）所作的估计。
- **实际经历行程时间**（experienced travel time，ETT）跟随车辆计算：每条路段的时间是车辆实际进入该路段时的时间，它取决于前面各路段的时间。这是出行者实际经历的行程时间。

对于由路段 $a_1, a_2, \ldots, a_m$ 组成、路段时间 $t_a(\tau)$ 依赖于进入时刻的路径，

$$
\begin{aligned}
\mathrm{ITT}(\tau) &= \sum_{i=1}^{m} t_{a_i}(\tau), \\
\mathrm{ETT}(\tau) &= \tau_m - \tau, \\
\tau_0 &= \tau, \\
\tau_i &= \tau_{i-1} + t_{a_i}(\tau_{i-1}), \quad i = 1, \ldots, m .
\end{aligned}
$$ (eq-16-itt-ett)

拥堵加剧时，瞬时行程时间低估实际经历的时间；拥堵消散时则高估。按瞬时行程时间最短的路径，按实际经历行程时间可能远非最短（{prf:ref}`ex-31-itt-ett`）。动态用户均衡是以实际经历时间定义的，因此动态交通分配需要**时间依赖最短路径**。若路段时间满足先进先出（较晚进入绝不会较早离开），则以到达时刻为标号的 Dijkstra 算法仍然适用：在最早到达 $i$ 的时刻扫描路段 $(i, j)$（Dreyfus，1969）。

## 动态交通分配

### 算法框架

静态分配和动态分配共有三个核心步骤：寻找最短路径、将出行分配到路径上、检验收敛。在静态分配中，最短路径在整个时段内都相同，加载是一种矩阵运算；在动态交通分配中，最短路径随出发时段而变化，加载是一次交通仿真。基于仿真的动态交通分配按如下方式迭代（Chiu 等，2011）：

1. **网络加载。** 用交通仿真（路段模型、排队、信号、溢流）使车辆沿其被分配的路径移动，并记录随时间变化的路段行程时间和延误。车辆遵循先进先出；到达过程在很小的仿真时间步（秒）上离散化。
2. **更新路径集。** 对每个 O-D 对和每个分配时段（分钟），用第 1 步得到的实际经历行程时间计算时间依赖最短路径，并将其加入路径集。
3. **调整路径。** 将每个 O-D 对、每个时段中的部分车辆从较慢的路径转移到较快的路径：采用相继平均法、梯度投影法，或基于起点和基于丛的方法。
4. **收敛检验。** 计算动态相对间隙，即对所有出发时段的实际经历时间求和的 {eq}`eq-13-relative-gap` 的对应形式；若足够小则停止，否则返回第 1 步。

这一过程是启发式的：与 Beckmann 模型不同，动态均衡没有一般的凸规划表述，其存在性和唯一性都得不到保证，收敛性只能通过经验检验。动态交通分配用于在走廊和子区域上评价静态模型无法反映的运营措施——事件管理、施工区、匝道控制、信号配时、管理车道以及分时段收费——其需求往往取自静态的区域模型（Sloboden 等，2012）。

## 多智能体交通仿真

### 基于智能体的需求

基于智能体的模型更进一步，将每个出行者模拟为一个具有每日**计划**（plan）的**智能体**（agent）：计划是一串带有地点和时间的活动（家、工作、购物、家），由带有交通方式和路径的出行连接起来。需求不再是 O-D 矩阵，而是智能体选择的结果。**MATSim**（Multi-Agent Transport Simulation）是由苏黎世联邦理工学院和柏林工业大学的 K. W. Axhausen 和 K. Nagel 开发的开源 Java 框架，正是基于这一思想（Horni、Nagel 和 Axhausen，2016；<https://www.matsim.org>）。

### 输入与 MATSim 循环

输入包括：多方式**网络**（节点；具有长度、自由流速度、通行能力和车道数的路段；公交时刻表），带有属性（年龄、小汽车可用性等）且每个智能体都有初始计划的合成**人口**，以及**评分**参数——进行活动、乘坐各种方式出行、等待和晚到的边际效用。

然后 MATSim 迭代一个**协同演化**循环：

1. **移动仿真（mobsim）。** 每个智能体执行从其记忆中选出的一个计划，例如根据计划评分用 Logit 模型选择。所有计划在网络上同时执行，在通行能力受限的路段上形成排队。
2. **评分。** 用效用函数对每个智能体所执行的计划评分：进行活动的效用减去出行的负效用，再减去晚到或早退的惩罚。
3. **重新规划。** 一部分智能体修改某个计划——出发时间、路径（针对上一次迭代行程时间的时间依赖最优响应，常通过相继平均加以平滑）、交通方式——并将其加入记忆；评分低的计划最终被删除。

循环在达到给定的迭代次数后，或在所执行计划的平均评分趋于稳定时停止。其结果是一种**松弛均衡**（relaxed equilibrium）：在重新规划所提供的选择维度内，没有智能体能够通过改变计划来提高其评分。这是针对完整的每日计划（而非单次出行）的随机用户均衡。{prf:ref}`ex-31-matsim-scores`追踪了十个智能体的两次循环迭代，包括跨迭代对路段行程时间的平滑，它所起的作用相当于相继平均法中的步长。

### 输出

MATSim 输出：一个**事件文件**，列出所模拟的一天中的每个事件（智能体离开某活动、进入或离开某路段、登上车辆、开始某活动）及其时间、智能体、车辆和路段；一个**计划文件**，包含所有智能体的最终计划及其评分；以及汇总统计和图表（各次迭代的平均评分、方式分担率、出行时长，以及一天中的出发、到达和在途智能体数）。由于每个智能体都被追踪，结果可以按任何方式汇总——按分钟计的路段流量、某一人群的出行时间、新道路的使用者——并可以用可视化工具制作动画。代价是工作量：合成人口、详细的网络、评分函数的标定，以及大区域数小时的运行时间。

## 本章回顾

### 小结

- 动态用户均衡使每个出发时段内（路径选择）或各出发时刻之间（出发时间与路径选择）的**实际经历**出行费用相等。
- 在费用为 {eq}`eq-16-bottleneck-cost` 的瓶颈模型中，准时出发者之前的出发率 {eq}`eq-16-bottleneck-rate` 为 $\alpha s/(\alpha - \beta)$，之后为 $\alpha s/(\alpha + \gamma)$；每名通勤者承担的费用为 $\delta N/s$ {eq}`eq-16-bottleneck-times`，最大排队为 $\delta N/\alpha$ {eq}`eq-16-bottleneck-queue`，总费用 $\delta N^2/s$ 在排队和计划延误之间平分 {eq}`eq-16-bottleneck-total`（{numref}`fig-16-bottleneck-cumulative`）。
- 瞬时行程时间使用出发时刻的网络状态；实际经历行程时间跟随车辆计算 {eq}`eq-16-itt-ett`。
- 基于仿真的动态交通分配迭代进行网络加载、时间依赖最短路径和路径调整；MATSim 将这一思想推广到具有每日活动计划的智能体，并达到松弛均衡。

### 常见错误

- **用瞬时行程时间评价动态均衡。** 均衡是以实际经历时间定义的；只要出行过程中状况发生变化，瞬时行程时间就会误判路径。
- **忘记时间依赖最短路径算法对先进先出的要求。** 以到达时刻为标号的 Dijkstra 类搜索只有在“较晚进入路段绝不会较早离开”时才是精确的。
- **认为只要通勤者“早点出发”，瓶颈排队就会消失。** 在均衡状态下，排队是分配接近 $t^*$ 的稀缺到达时刻的代价；只有时变收费才能消除排队。
- **忘记瓶颈模型的总费用随 $N$ 的平方增长。** 每名新增通勤者既承担均衡费用，又延长了所有其他人的高峰时段。
- **把基于仿真的均衡当作唯一且精确的结果。** 结果随随机数种子和迭代次数而变化；应报告多次运行的结果。

## 参考文献

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
