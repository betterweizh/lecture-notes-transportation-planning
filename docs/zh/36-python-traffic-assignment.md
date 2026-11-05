# Python 实现：交通分配

## 概述

本章实现{doc}`13-user-equilibrium-assignment`、{doc}`14-system-optimum-and-elastic-demand`、{doc}`15-stochastic-user-equilibrium`和{doc}`16-dynamic-assignment-and-simulation`中的交通分配模型，并复现{doc}`28-examples-user-equilibrium`、{doc}`29-examples-system-optimum-and-elastic-demand`、{doc}`30-examples-stochastic-user-equilibrium`和{doc}`31-examples-dynamic-assignment`中的算例。一个小型的 `Network` 类存储路段和 O-D 需求；最短路径、全有全无加载、Frank–Wolfe 算法和相继平均法都建立在它之上。构建本书时不会运行这些代码；请将其复制到脚本或 notebook 中运行，并将输出结果与 `# Expected:` 注释相比较，这些注释与算例的结果一致。

:::{admonition} 学习目标
:class: objectives
学完本章后，读者应能够：

- 用可分离的路段阻抗函数表示网络，并用 Dijkstra 算法计算最短路径；
- 实现求解用户均衡的全有全无分配、Frank–Wolfe 算法和相继平均法，并用相对间隙监测收敛；
- 用边际成本函数求得系统最优，并计算边际成本收费；
- 求解弹性需求问题和分布–分配组合问题；
- 计算 Logit 和 Probit 随机加载，并用相继平均法求解 Logit 随机用户均衡；
- 计算瓶颈模型和时间依赖的行程时间。
:::

## 环境准备

代码使用 `numpy`、`scipy`（`optimize`、`stats`）和标准库模块 `heapq`；下面的代码块包含全部导入语句。

```python
import heapq

import numpy as np
from scipy import optimize, stats

np.set_printoptions(precision=3, suppress=True, linewidth=120)
```

## 网络类

本书中的每个路段阻抗函数都具有如下形式

$$
t_a(x_a) = A_a + B_a\,x_a^{P_a},
$$

它涵盖线性函数（$P_a = 1$）、{prf:ref}`ex-29-hw4-q1`中的二次函数（$P_a = 2$）以及 BPR 函数 $t_a^0[1 + \alpha(x_a/c_a)^\beta]$（取 $A_a = t_a^0$，$B_a = \alpha t_a^0/c_a^\beta$，$P_a = \beta$）。于是 Beckmann 积分和边际成本都有闭式解：

$$
\begin{aligned}
\int_0^{x_a} t_a(\omega)\,\diff\omega &= A_a x_a + \frac{B_a}{P_a + 1}\,x_a^{P_a + 1}, \\
\tilde t_a(x_a) &= t_a(x_a) + x_a t_a'(x_a) \\
&= A_a + (P_a + 1)\,B_a\,x_a^{P_a}.
\end{aligned}
$$

```python
class Network:
    """Directed network with link costs t_a(x_a) = A_a + B_a * x_a**P_a.

    Parameters
    ----------
    links : list of tuple
        One tuple (tail, head, A, B, P) per link; link a is the a-th tuple
        (0-based index).
    demand : dict
        O-D demand {(r, s): q_rs}.
    """

    def __init__(self, links, demand):
        if any(len(link) != 5 for link in links):
            raise ValueError("each link must be a tuple (tail, head, A, B, P)")
        self.tail = [link[0] for link in links]
        self.head = [link[1] for link in links]
        self.A = np.array([link[2] for link in links], float)
        self.B = np.array([link[3] for link in links], float)
        self.P = np.array([link[4] for link in links], float)
        if np.any(self.B < 0) or np.any(self.P <= 0):
            raise ValueError("link costs need B_a >= 0 and P_a > 0")
        self.demand = dict(demand)
        if any(q < 0 for q in self.demand.values()):
            raise ValueError("O-D demands must be non-negative")
        self.n_links = len(links)
        # adjacency lists: node -> list of (link, head)
        self.out = {}
        for a, (i, j) in enumerate(zip(self.tail, self.head)):
            self.out.setdefault(i, []).append((a, j))

    def cost(self, x):
        """Link travel times t_a(x_a)."""
        return self.A + self.B * x**self.P

    def marginal_cost(self, x):
        """Marginal costs t_a + x_a t_a', equation (eq-14-marginal-cost)."""
        return self.A + (self.P + 1) * self.B * x**self.P

    def beckmann(self, x):
        """Beckmann's objective, equation (eq-13-beckmann)."""
        return float(
            np.sum(self.A * x + self.B * x ** (self.P + 1) / (self.P + 1))
        )

    def tstt(self, x):
        """Total system travel time, equation (eq-14-tstt)."""
        return float(self.cost(x) @ x)
```

### 最短路径与全有全无分配

Dijkstra 算法（采用最小标号规则的{prf:ref}`alg-03-label-correcting`）用堆作为候选节点表。全有全无加载（{prf:ref}`alg-13-aon`）通过前驱路段回溯每个 O-D 对的最短路径，并把需求加到路径上的每条路段。

```python
def dijkstra(net, t, origin):
    """Shortest-path labels and predecessor links from one origin.

    Parameters
    ----------
    net : Network
        The network.
    t : numpy.ndarray
        Non-negative link costs.
    origin : int
        Origin node.

    Returns
    -------
    label : dict
        Shortest-path cost of every reachable node.
    pred : dict
        Last link of the shortest path to every reachable node.
    """
    if np.any(np.asarray(t) < 0):
        raise ValueError("Dijkstra's algorithm needs non-negative link costs")
    label = {origin: 0.0}
    pred = {origin: None}
    heap = [(0.0, origin)]
    done = set()
    while heap:
        d, i = heapq.heappop(heap)
        if i in done:
            continue
        done.add(i)
        for a, j in net.out.get(i, []):
            if d + t[a] < label.get(j, np.inf) - 1e-12:
                label[j] = d + t[a]
                pred[j] = a
                heapq.heappush(heap, (label[j], j))
    return label, pred


def path_links(net, pred, dest):
    """Links of the shortest path to `dest`, read back from `pred`."""
    links, j = [], dest
    while pred[j] is not None:
        a = pred[j]
        links.append(a)
        j = net.tail[a]
    return links[::-1]


def all_or_nothing(net, t, demand=None):
    """All-or-nothing assignment, algorithm (alg-13-aon).

    Parameters
    ----------
    net : Network
        The network.
    t : numpy.ndarray
        Fixed link costs.
    demand : dict, optional
        O-D demand {(r, s): q_rs}; the network's demand by default.

    Returns
    -------
    y : numpy.ndarray
        Link flows.
    u : dict
        Shortest-path cost of every O-D pair.
    """
    demand = net.demand if demand is None else demand
    y = np.zeros(net.n_links)
    u = {}
    for r in sorted({o for o, _ in demand}):
        label, pred = dijkstra(net, t, r)
        for (o, s), q in demand.items():
            if o != r:
                continue
            if s not in label:
                raise ValueError(f"destination {s} cannot be reached from {r}")
            u[(o, s)] = label[s]
            y[path_links(net, pred, s)] += q
    return y, u
```

全章使用{numref}`fig-13-six-node-network`的六节点网络，需求为 $q_{12} = 100$ 和 $q_{56} = 50$。用自由流加载和{prf:ref}`ex-28-ue-aon`检验这些函数：

```python
# links (tail, head, A, B, P) with t_a = A + B x**P
six_node_links = [
    (1, 2, 3.0, 0.5, 1),
    (1, 3, 1.0, 2.0, 1),
    (4, 2, 0.5, 1.0, 1),
    (3, 4, 1.0, 0.5, 1),
    (5, 3, 2.0, 0.5, 1),
    (5, 6, 4.0, 1.0, 1),
    (4, 6, 1.0, 0.5, 1),
]
six_node = Network(six_node_links, demand={(1, 2): 100, (5, 6): 50})

y, u = all_or_nothing(six_node, six_node.cost(np.zeros(7)))
print("AON at free flow:", y, {k: float(v) for k, v in u.items()})

# network of the AON example, loaded with the link times t = (1, 2, 3, 9, 1)
aon_net = Network(
    [
        (1, 3, 0, 0, 1),
        (2, 3, 0, 0, 1),
        (3, 4, 0, 0, 1),
        (3, 4, 0, 0, 1),
        (4, 5, 0, 0, 1),
    ],
    {(1, 5): 2, (2, 5): 3},
)
y, u = all_or_nothing(aon_net, np.array([1.0, 2.0, 3.0, 9.0, 1.0]))
print("AON example:", y, {k: float(v) for k, v in u.items()})
# Expected: AON at free flow: [0. 100. 100. 100. 0. 50. 0.]
#           {(1, 2): 2.5, (5, 6): 4.0}
#           AON example: [2. 3. 5. 0. 5.] {(1, 5): 5.0, (2, 5): 6.0}
```

## 用户均衡

### Frank–Wolfe 算法

线搜索沿 $\bx + \alpha(\by - \bx)$ 最小化 Beckmann 目标函数；其导数 {eq}`eq-13-fw-line-search` 关于 $\alpha$ 单调递增，因此根据其符号进行二分是安全的。**相对间隙** {eq}`eq-13-relative-gap` 衡量流量离均衡有多远。传入 `cost=net.marginal_cost`，同一段代码就变成了系统最优求解器（{prf:ref}`thm-14-so-ue`）。

```python
def bisection(dz, lo=0.0, hi=1.0, tol=1e-10):
    """Root of an increasing function dz on [lo, hi] by bisection.

    Returns the end point lo or hi if dz does not change sign on the
    interval.
    """
    if not lo < hi:
        raise ValueError("bisection needs lo < hi")
    if dz(hi) <= 0:
        return hi
    if dz(lo) >= 0:
        return lo
    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if dz(mid) > 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


def frank_wolfe(net, cost=None, tol=1e-6, max_iter=1000, verbose=0):
    """Frank-Wolfe method, algorithm (alg-13-fw-ue).

    Parameters
    ----------
    net : Network
        The network.
    cost : callable, optional
        Link cost function: net.cost (default) gives the user equilibrium,
        net.marginal_cost the system optimum.
    tol : float
        Stop when the relative gap (eq-13-relative-gap) is below tol.
    max_iter : int
        Maximum number of iterations.
    verbose : int
        Number of iterations to print.

    Returns
    -------
    x : numpy.ndarray
        Link flows.
    n : int
        Number of iterations.
    gap : float
        Relative gap of x.
    """
    if tol <= 0 or max_iter < 1:
        raise ValueError("tol must be positive and max_iter at least 1")
    cost = net.cost if cost is None else cost
    # step 1: initialization, AON at free-flow times
    x, _ = all_or_nothing(net, cost(np.zeros(net.n_links)))
    for n in range(1, max_iter + 1):
        # step 2: update the link times
        t = cost(x)
        # step 3: direction finding
        y, _ = all_or_nothing(net, t)
        # step 6 (checked before the move): relative gap of x
        gap = t @ (x - y) / (t @ x)
        if gap < tol:
            break
        d = y - x
        # step 4: line search on the derivative (eq-13-fw-line-search)
        alpha = bisection(lambda a: cost(x + a * d) @ d)
        if n <= verbose:
            print(
                f"n={n} x={x.round(2)} y={y} alpha={alpha:.4f} "
                f"z={net.beckmann(x):.2f} gap={gap:.4f}"
            )
        # step 5: move
        x = x + alpha * d
    return x, n, gap


x_ue, n, gap = frank_wolfe(six_node, verbose=4)
print("UE flows:", x_ue.round(3), "iterations:", n, f"gap: {gap:.1e}")
print("link times:", six_node.cost(x_ue).round(3))
# Expected: alpha = 0.8737, 0.3491, 0.0226, 0.0010;
#           z = 19200.00, 3931.22, 3549.88, 3539.81;
#           gap = 0.9209, 0.2964, 0.1348, 0.0048
#           UE flows: [89.615 10.385 10.385 28.308 17.923 32.077 17.923]
#           iterations: 19 gap: 3.7e-07
#           link times: [47.808 21.769 10.885 15.154 10.962 36.077 9.962]
```

对于线性阻抗函数，均衡也可以精确求出：每条路径的流量要么为零，要么使各路径费用相等。{prf:ref}`ex-28-ue-six-node`基于路径的解验证了 Frank–Wolfe 算法的结果：

```python
# unknowns f2 (path 1-3-4-2) and g2 (path 5-3-4-6); f1 = 100 - f2, g1 = 50 - g2
M = np.array([[4.0, 0.5], [0.5, 2.5]])
rhs = np.array([50.5, 50.0])
f2, g2 = np.linalg.solve(M, rhs)
print(
    "path flows:",
    round(100 - f2, 3),
    round(f2, 3),
    round(50 - g2, 3),
    round(g2, 3),
)
# Expected: path flows: 89.615 10.385 32.077 17.923
```

### 相继平均法

相继平均法（{prf:ref}`alg-13-msa-ue`）用预先确定的步长 $1/n$ 代替线搜索：

```python
def msa(net, cost=None, n_iter=100, verbose=0):
    """Method of successive averages, algorithm (alg-13-msa-ue).

    Parameters
    ----------
    net : Network
        The network.
    cost : callable, optional
        Link cost function (net.cost by default).
    n_iter : int
        Number of iterations.
    verbose : int
        Number of iterations to print.

    Returns
    -------
    numpy.ndarray
        Link flows after n_iter iterations.
    """
    if n_iter < 1:
        raise ValueError("n_iter must be at least 1")
    cost = net.cost if cost is None else cost
    x, _ = all_or_nothing(net, cost(np.zeros(net.n_links)))
    for n in range(1, n_iter + 1):
        y, _ = all_or_nothing(net, cost(x))
        if n <= verbose:
            print(f"n={n} x={x.round(2)} y={y} z={net.beckmann(x):.2f}")
        x = x + (y - x) / n
    return x


print("MSA, 1000 iterations:", msa(six_node, n_iter=1000, verbose=4).round(3))
# Expected: z = 19200.00, 4250.00, 6881.25, 4580.56 in the first four
#           iterations
#           MSA, 1000 iterations: [89.6 10.4 10.4 28.3 17.9 32.1 17.9]
```

### 采用 BPR 函数的三路段算例

{prf:ref}`ex-28-ue-fw-three-link`中的 BPR 算例有一个 O-D 对和三条平行路段，$t_a = t_a^0[1 + 0.15(x_a/c_a)^4]$：

```python
t0, cap = np.array([10.0, 20.0, 25.0]), np.array([2.0, 4.0, 3.0])
bpr = Network(
    [(1, 2, t0[a], 0.15 * t0[a] / cap[a] ** 4, 4) for a in range(3)],
    {(1, 2): 10},
)

x_fw, n, gap = frank_wolfe(bpr, tol=1e-8, verbose=6)
print(
    "UE:",
    x_fw.round(3),
    "times:",
    bpr.cost(x_fw).round(3),
    "z =",
    round(bpr.beckmann(x_fw), 2),
)
print(
    "MSA after 12 and 1000 iterations:",
    msa(bpr, n_iter=12).round(2),
    msa(bpr, n_iter=1000).round(3),
)
# Expected: alpha = 0.5965, 0.1611, 0.0356, 0.0204, 0.0072, 0.0054;
#           z = 1975.00, 197.40, 189.99, 189.45, 189.36, 189.34;
#           gap = 0.9789, 0.2824, 0.1190, 0.0315, 0.0233, 0.0083
#           UE: [3.583 4.645 1.772] times: [25.456 25.456 25.456] z = 189.33
#           MSA after 12 and 1000 iterations: [3.33 5. 1.67] [3.58 4.65 1.77]
```

### 含两个 O-D 对的五路段网络

在{prf:ref}`ex-28-hw4-q2-due`的网络中，路段 1–5 分别为 $1 \to 2$、$3 \to 2$、$1 \to 3$、$3 \to 4$ 和 $4 \to 2$，$t_a = 1 + 0.15\,x_a/a$：

```python
hw4 = Network(
    [
        (1, 2, 1, 0.15 / 1, 1),
        (3, 2, 1, 0.15 / 2, 1),
        (1, 3, 1, 0.15 / 3, 1),
        (3, 4, 1, 0.15 / 4, 1),
        (4, 2, 1, 0.15 / 5, 1),
    ],
    {(1, 2): 20, (3, 2): 60},
)

x_hw4, n, gap = frank_wolfe(hw4, tol=1e-4, max_iter=5000, verbose=3)
print("FW:", x_hw4.round(3), "after", n, "iterations; gap", f"{gap:.1e}")
_, u = all_or_nothing(hw4, hw4.cost(x_hw4))
print("O-D costs:", {k: round(float(v), 4) for k, v in u.items()})

# exact solution: pair 1-2 uses link 1 only; pair 3-2 splits between link 2
# and links 4-5
y45 = 3.5 / (0.075 + 0.0375 + 0.03)
print("exact:", 20, round(60 - y45, 4), 0, round(y45, 4), round(y45, 4))
# Expected: alpha = 0.2941, 0.1526, 0.1546
#           FW: [19.973 35.448 0.027 24.579 24.579] after 3269 iterations;
#           gap 1.0e-04
#           O-D costs: {(1, 2): 3.996, (3, 2): 3.6586}
#           exact: 20 35.4386 0 24.5614 24.5614
```

## 系统最优与 Braess 悖论

收费 {eq}`eq-14-mc-toll` 等于系统最优流量下的 $x_at_a'(x_a)$；网络取自{prf:ref}`ex-29-braess`：

```python
braess_links = [
    (1, 2, 50, 1, 1),
    (3, 4, 50, 1, 1),
    (1, 3, 0, 10, 1),
    (2, 4, 0, 10, 1),
]
braess = Network(braess_links, {(1, 4): 6})
braess5 = Network(braess_links + [(3, 2, 10, 1, 1)], {(1, 4): 6})

for name, net in (("without link 5", braess), ("with link 5", braess5)):
    x_ue, *_ = frank_wolfe(net, tol=1e-10, max_iter=20000)
    x_so, *_ = frank_wolfe(
        net, cost=net.marginal_cost, tol=1e-10, max_iter=20000
    )
    # marginal-cost toll x_a t_a'(x_a) at the SO flows
    toll = x_so * net.B * net.P * x_so ** (net.P - 1)
    print(
        f"{name}: UE {x_ue.round(2)} TSTT {net.tstt(x_ue):.1f} | "
        f"SO {x_so.round(2)} TSTT {net.tstt(x_so):.1f} | toll {toll.round(2)}"
    )
# Expected: without link 5: UE [3. 3. 3. 3.] TSTT 498.0 |
#           SO [3. 3. 3. 3.] TSTT 498.0 | toll [3. 3. 30. 30.]
#           with link 5: UE [2. 2. 4. 4. 2.] TSTT 552.0 |
#           SO [3. 3. 3. 3. 0.] TSTT 498.0 | toll [3. 3. 30. 30. 0.]
```

{prf:ref}`ex-29-so-two-route`的两路径网络表明，系统最优可能使用用户均衡中空置的路径：

```python
two_route = Network([(1, 2, 40, 0.5, 1), (1, 2, 10, 0.25, 2)], {(1, 2): 10})
x_ue, *_ = frank_wolfe(two_route, tol=1e-12)
x_so, *_ = frank_wolfe(two_route, cost=two_route.marginal_cost, tol=1e-12)
print(
    "UE:",
    x_ue.round(3),
    two_route.tstt(x_ue),
    " SO:",
    x_so.round(3),
    round(two_route.tstt(x_so), 2),
)
# Expected: UE: [0. 10.] 350.0  SO: [3.333 6.667] 279.63
```

### 作为需求函数的 DUE 与 SO

DUE 和 SO 取决于需求 $q$；对若干取值检验{prf:ref}`ex-29-hw4-q1`的闭式解（各列依次为：DUE 下用 Frank–Wolfe 算法和用公式求得的 $x_1$，以及 SO 下的相应结果）：

```python
def hw4_q1(q):
    """Flow x_1 at the DUE and SO, numerically and by the closed forms."""
    net = Network(
        [(1, 2, 1.5, 0.5, 2), (1, 2, 1.0, 2.0, 1), (2, 3, 4.0, 1.0, 1)],
        {(1, 3): q},
    )
    x_ue, *_ = frank_wolfe(net, tol=1e-12, max_iter=20000)
    x_so, *_ = frank_wolfe(
        net, cost=net.marginal_cost, tol=1e-12, max_iter=20000
    )
    ue_formula = max(np.sqrt(4 * q + 3) - 2, 0)
    so_formula = max((np.sqrt(24 * q + 13) - 4) / 3, 0)
    return x_ue[0], ue_formula, x_so[0], so_formula


for q in (0.2, 1, 4, 10):
    print(q, np.round(hw4_q1(q), 4))
# Expected: 0.2 [0. 0. 0.073 0.073]
#           1 [0.646 0.646 0.694 0.694]
#           4 [2.359 2.359 2.147 2.147]
#           10 [4.557 4.557 3.969 3.969]
```

## 弹性需求

超额需求重构 {eq}`eq-14-excess-demand` 增加一条从 $r$ 到 $s$ 的虚拟路段，其费用为 $W_{rs}(e_{rs}) = D_{rs}^{-1}(\bar q_{rs} - e_{rs})$；扩展网络上的固定需求为上界 $\bar q_{rs}$。对于线性反需求函数 $D^{-1}(q) = a - bq$，$W(e) = a - b\bar q + b\,e$ 同样具有 $A + Be$ 的形式。算例为{prf:ref}`ex-29-elastic-demand`：

```python
def elastic_network(links, inverse_demand, q_bar):
    """Augment `links` with one excess-demand link per O-D pair.

    Parameters
    ----------
    links : list of tuple
        Links (tail, head, A, B, P) of the real network.
    inverse_demand : dict
        {(r, s): (a, b)} for the inverse demand D^-1(q) = a - b q.
    q_bar : dict
        Upper bound {(r, s): q_bar_rs} on the demand.

    Returns
    -------
    Network
        Augmented network with the fixed demand q_bar.
    """
    if set(inverse_demand) != set(q_bar):
        raise ValueError("inverse_demand and q_bar need the same O-D pairs")
    if any(b <= 0 for _, b in inverse_demand.values()):
        raise ValueError("the inverse demand must be decreasing (b > 0)")
    dummy = [
        (r, s, a - b * q_bar[(r, s)], b, 1)
        for (r, s), (a, b) in inverse_demand.items()
    ]
    return Network(list(links) + dummy, q_bar)


net = elastic_network([(1, 2, 1, 1, 1)], {(1, 2): (5, 1)}, {(1, 2): 5})
x, *_ = frank_wolfe(net, tol=1e-12)
print(
    "link flow:",
    round(x[0], 4),
    " excess demand:",
    round(x[1], 4),
    " demand q = q_bar - e:",
    round(5 - x[1], 4),
)
# Expected: link flow: 2.0  excess demand: 3.0  demand q = q_bar - e: 2.0
```

## 分布–分配组合模型

Evans 算法（{prf:ref}`alg-14-evans`）求解组合模型 {eq}`eq-14-combined-da`。每次迭代计算最短路径费用 $u_{rs}$，用这些费用求解双约束重力模型（辅助出行矩阵 $\bv$），对 $\bv$ 进行全有全无加载（辅助路段流量 $\by$），再以一个共同步长同时移动出行矩阵和路段流量，该步长由对下式的线搜索确定：

$$
z(\bx, \bq) = \sum_a \int_0^{x_a} t_a(\omega)\,\diff\omega
+ \frac{1}{\beta}\sum_{r, s} q_{rs}\left(\ln q_{rs} - 1\right).
$$

算例为{prf:ref}`ex-29-combined-da`：

```python
def gravity(O, D, cost, beta, n_iter=500):
    """Doubly constrained gravity model (eq-14-combined-da-solution).

    Parameters
    ----------
    O, D : numpy.ndarray
        Trip productions and attractions (equal totals).
    cost : numpy.ndarray
        O-D costs u_rs, one row per origin.
    beta : float
        Dispersion parameter, beta > 0.
    n_iter : int
        Number of balancing (Furness) iterations.

    Returns
    -------
    numpy.ndarray
        Trip matrix q_rs = A_r O_r B_s D_s exp(-beta u_rs).
    """
    if beta <= 0:
        raise ValueError("beta must be positive")
    if not np.isclose(O.sum(), D.sum()):
        raise ValueError("productions and attractions must have equal totals")
    F = np.exp(-beta * cost)
    B = np.ones(len(D))
    for _ in range(n_iter):
        A = 1.0 / (F @ (B * D))
        B = 1.0 / ((A * O) @ F)
    return (A * O)[:, None] * (B * D)[None, :] * F


def evans(net, origins, dests, O, D, beta, n_iter=500, verbose=0):
    """Evans's algorithm for combined distribution and assignment.

    Parameters
    ----------
    net : Network
        The network (its own demand is not used).
    origins, dests : list of int
        Origin and destination nodes, in the order of O and D.
    O, D : numpy.ndarray
        Trip productions and attractions.
    beta : float
        Dispersion parameter of the gravity model.
    n_iter : int
        Number of iterations.
    verbose : int
        Number of iterations to print.

    Returns
    -------
    x : numpy.ndarray
        Link flows.
    q : numpy.ndarray
        Trip matrix.
    u : numpy.ndarray
        Shortest-path costs at the last iteration.
    """
    if len(origins) != len(O) or len(dests) != len(D):
        raise ValueError("one production per origin, one attraction per dest")
    ods = [(r, s) for r in origins for s in dests]

    def costs_and_aon(t, trips):
        y, u = all_or_nothing(
            net, t, {od: q for od, q in zip(ods, trips.ravel())}
        )
        return y, np.array([[u[(r, s)] for s in dests] for r in origins])

    # step 1: gravity model and AON at free-flow times
    t_free = net.cost(np.zeros(net.n_links))
    _, u = costs_and_aon(t_free, np.ones((len(O), len(D))))
    q = gravity(O, D, u, beta)
    x, _ = costs_and_aon(t_free, q)
    for n in range(1, n_iter + 1):
        # step 2: shortest-path costs at the current flows
        _, u = costs_and_aon(net.cost(x), q)
        # step 3: auxiliary trip matrix and auxiliary link flows
        v = gravity(O, D, u, beta)
        y, _ = costs_and_aon(net.cost(x), v)
        dx, dq = y - x, v - q

        # step 4: line search; the upper end below 1 keeps q > 0
        def dz(a):
            return (
                net.cost(x + a * dx) @ dx
                + np.sum(np.log(q + a * dq) * dq) / beta
            )

        alpha = bisection(dz, 0.0, 1.0 - 1e-9)
        if n <= verbose:
            print(
                f"n={n} u={u.ravel().round(2)}"
                f" v={v.ravel().round(2)} alpha={alpha:.4f}"
            )
        # step 5: move
        x, q = x + alpha * dx, q + alpha * dq
    return x, q, u


# the demand is now a variable
comb = Network(six_node_links, {})
x, q, u = evans(
    comb,
    origins=[1, 5],
    dests=[2, 6],
    O=np.array([100.0, 50.0]),
    D=np.array([75.0, 75.0]),
    beta=0.1,
    n_iter=5000,
    verbose=2,
)
print("trip matrix:", q.round(2).tolist())
print("link flows:", x.round(2))
print("O-D costs:", u.round(2).tolist())
q_check = gravity(np.array([100.0, 50.0]), np.array([75.0, 75.0]), u, 0.1)
print("gravity model at these costs:", q_check.round(2).tolist())
# Expected: n=1 u=[3. 290.5 153.5 29.] v=[75. 25. 0. 50.] alpha=0.9875
#           n=2 u=[40.03 80.66 17.72 29.94] v=[69.2 30.8 5.8 44.2]
#           alpha=0.1986
#           trip matrix: [[72.51, 27.49], [2.49, 47.51]]
#           link flows: [72.51 27.49 2.49 36.99 9.5 40.5 34.5]
#           O-D costs: [[39.26, 93.72], [29.23, 44.49]]
#           gravity model at these costs: [[72.51, 27.49], [2.49, 47.51]]
```

## 随机用户均衡

### 路径枚举与 Logit 加载

Logit 加载 {eq}`eq-15-logit-sue` 需要每个 O-D 对的路径集。对于小型网络，可以用深度优先搜索枚举无环路径；路段–路径关联矩阵 $\bDelta$ 将路径流量映射为路段流量。算例为{prf:ref}`ex-30-sue-logit-loading`：

```python
def enumerate_paths(net, origin, dest):
    """All acyclic paths from origin to dest, as lists of link indices."""
    paths, stack = [], [(origin, [], {origin})]
    while stack:
        i, links, seen = stack.pop()
        if i == dest:
            paths.append(links)
            continue
        for a, j in net.out.get(i, []):
            if j not in seen:
                stack.append((j, links + [a], seen | {j}))
    return sorted(paths, key=lambda p: (len(p), p))


class PathSet:
    """Enumerated paths of all O-D pairs and the incidence matrix Delta.

    Parameters
    ----------
    net : Network
        The network; its demand defines the O-D pairs.
    """

    def __init__(self, net):
        self.net = net
        self.ods = list(net.demand)
        self.paths = [
            (od, p) for od in self.ods for p in enumerate_paths(net, *od)
        ]
        for od in self.ods:
            if not any(o == od for o, _ in self.paths):
                raise ValueError(f"O-D pair {od} has no path")
        self.Delta = np.zeros((net.n_links, len(self.paths)))
        for k, (_, p) in enumerate(self.paths):
            self.Delta[p, k] = 1.0

    def logit_loading(self, t, theta):
        """Logit loading, equation (eq-15-logit-sue), at fixed link times t.

        Returns the link flows x and the path flows f.
        """
        if theta <= 0:
            raise ValueError("the dispersion parameter theta must be positive")
        c = self.Delta.T @ t
        f = np.zeros(len(self.paths))
        for od in self.ods:
            k = [i for i, (o, _) in enumerate(self.paths) if o == od]
            # subtract the minimum for numerical stability
            e = np.exp(-theta * (c[k] - c[k].min()))
            f[k] = self.net.demand[od] * e / e.sum()
        return self.Delta @ f, f


ps = PathSet(Network(six_node_links, {(1, 2): 10, (5, 6): 5}))
print([p for _, p in ps.paths])
x, f = ps.logit_loading(ps.net.cost(np.zeros(7)), theta=1.0)
print("logit loading at free flow:", f.round(4), x.round(4))
# Expected: [[0], [1, 3, 2], [5], [4, 3, 6]]
#           logit loading at free flow: [3.775 6.225 2.5 2.5]
#           [3.775 6.225 6.225 8.725 2.5 2.5 2.5]
```

### 求解 Logit 随机用户均衡的相继平均法

算法为{prf:ref}`alg-15-msa-sue`，算例为{prf:ref}`ex-30-sue-msa`：

```python
def msa_sue(ps, theta, n_iter=1000, verbose=0):
    """MSA for the logit-based SUE, algorithm (alg-15-msa-sue).

    Parameters
    ----------
    ps : PathSet
        Paths and network.
    theta : float
        Dispersion parameter.
    n_iter : int
        Number of iterations.
    verbose : int
        Number of iterations to print.

    Returns
    -------
    numpy.ndarray
        Link flows after n_iter iterations.
    """
    if n_iter < 1:
        raise ValueError("n_iter must be at least 1")
    # step 1: logit loading at free-flow times
    x, _ = ps.logit_loading(ps.net.cost(np.zeros(ps.net.n_links)), theta)
    for n in range(1, n_iter + 1):
        # steps 2 and 3: logit loading at the current times
        y, _ = ps.logit_loading(ps.net.cost(x), theta)
        # step 4: move with step 1/n
        x_new = x + (y - x) / n
        if n <= verbose:
            change = np.sqrt(np.sum((x_new - x) ** 2)) / x.sum()
            print(
                f"n={n} t={ps.net.cost(x).round(2)} y={y.round(2)}"
                f" x={x_new.round(2)} crit={change:.4f}"
            )
        x = x_new
    return x


ps6 = PathSet(six_node)
x_sue = msa_sue(ps6, theta=1.0, n_iter=3000, verbose=3)
print("logit SUE (theta = 1):", x_sue.round(3))
print("path flows:", ps6.logit_loading(six_node.cost(x_sue), 1.0)[1].round(3))
# Expected: n=1 t=[21.88 125.49 62.75 44.62 14.5 29. 13.5]
#           y=[100. 0. 0. 0. 0. 50. 0.] crit=0.4478
#           n=2 x=[50. 50. 50. 75. 25. 25. 25.] crit=0.8165
#           n=3 x=[66.67 33.33 33.33 50. 16.67 33.33 16.67] crit=0.1361
#           logit SUE (theta = 1): [89.106 10.894 10.894 28.944 18.05 31.95
#           18.05]
#           path flows: [89.106 10.894 31.95 18.05]
```

相继平均法的不动点使 Fisk 函数 {eq}`eq-15-fisk` 取得最小值（{prf:ref}`thm-15-fisk`）。用 SciPy 直接最小化可以验证这一点：

```python
def fisk(ps, theta):
    """Minimize Fisk's function (eq-15-fisk) over the path flows.

    The path flows are written f = q_rs * softmax(w), so the minimization
    over w has no constraints. Returns the link flows and the path flows.
    """
    if theta <= 0:
        raise ValueError("the dispersion parameter theta must be positive")
    od_of = np.array([ps.ods.index(od) for od, _ in ps.paths])
    q = np.array([ps.net.demand[od] for od in ps.ods])

    def flows(w):
        f = np.empty_like(w)
        for i in range(len(ps.ods)):
            e = np.exp(w[od_of == i] - w[od_of == i].max())
            f[od_of == i] = q[i] * e / e.sum()
        return f

    def z(w):
        f = flows(w)
        return np.sum(f * np.log(f) - f) / theta + ps.net.beckmann(
            ps.Delta @ f
        )

    res = optimize.minimize(
        z, np.zeros(len(ps.paths)), method="BFGS", options={"gtol": 1e-10}
    )
    return ps.Delta @ flows(res.x), flows(res.x)


print("Fisk:", fisk(ps6, 1.0)[0].round(3))
# Expected: Fisk: [89.106 10.894 10.894 28.944 18.05 31.95 18.05]
```

### 五路段网络上的 Logit 随机用户均衡

算例为{prf:ref}`ex-30-hw4-q2-sue`：

```python
ps_hw4 = PathSet(hw4)
print([p for _, p in ps_hw4.paths])
x_sue = msa_sue(ps_hw4, theta=0.1, n_iter=5000, verbose=3)
print(
    "SUE:",
    x_sue.round(3),
    " path flows:",
    ps_hw4.logit_loading(hw4.cost(x_sue), 0.1)[1].round(3),
)
# Expected: [[0], [2, 1], [2, 3, 4], [1], [3, 4]]
#           n=1 t=[2.1 3.86 1.63 2.29 2.04] y=[8.36 36.66 11.64 34.98 34.98]
#           crit=0.0171
#           n=2 x=[8.3 36.82 11.7 34.88 34.88] crit=0.0018
#           n=3 x=[8.28 36.86 11.72 34.86 34.86] crit=0.0005
#           SUE: [8.255 36.917 11.745 34.829 34.829]
#           path flows: [8.255 6.044 5.702 30.873 29.127]
```

### Probit 加载：精确解与蒙特卡洛模拟

对于两条路径，Probit 选择概率是一个正态分布函数值 {eq}`eq-15-probit-two-paths`（{prf:ref}`ex-30-sue-probit-loading`）；一般情况下，通过对路段时间进行蒙特卡洛模拟并进行全有全无加载来估计（{prf:ref}`alg-15-monte-carlo-loading`、{prf:ref}`ex-30-sue-monte-carlo`）。模拟得到的流量取决于随机数生成器和种子，因此其他运行结果在小数点后第二位会有所不同。

```python
# standard deviations of the link times
sd = np.array([0.3, 0.1, 0.1, 0.2, 0.4, 0.6, 0.1])
p12 = stats.norm.cdf(
    -0.5 / np.sqrt(sd[0] ** 2 + sd[1] ** 2 + sd[2] ** 2 + sd[3] ** 2)
)
print(
    "P(path 1 of pair 1-2) =",
    round(p12, 5),
    " flows:",
    round(10 * p12, 4),
    round(10 * (1 - p12), 4),
)

net_small = Network(six_node_links, {(1, 2): 10, (5, 6): 5})
t_free = net_small.cost(np.zeros(7))


def monte_carlo_loading(net, t_mean, sd, n_draws, seed=0):
    """Monte Carlo probit loading, algorithm (alg-15-monte-carlo-loading).

    Draws normal link times with means t_mean and standard deviations sd,
    loads all-or-nothing, and returns the running average of the link flows
    after n_draws draws.
    """
    if n_draws < 1:
        raise ValueError("n_draws must be at least 1")
    rng = np.random.default_rng(seed)
    x = np.zeros(net.n_links)
    for n in range(1, n_draws + 1):
        # AON with sampled link times
        y, _ = all_or_nothing(net, t_mean + rng.normal(0.0, sd))
        # running average
        x += (y - x) / n
    return x


for n_draws in (100, 1000, 10000):
    print(
        n_draws, monte_carlo_loading(net_small, t_free, sd, n_draws).round(3)
    )
# Expected: P(path 1 of pair 1-2) = 0.09835  flows: 0.9835 9.0165
#           100 [1.1 8.9 8.9 11.25 2.35 2.65 2.35]
#           1000 [0.94 9.06 9.06 11.62 2.56 2.44 2.56]
#           10000 [0.984 9.016 9.016 11.503 2.487 2.513 2.487]
```

### 感知时间服从均匀分布

算例为{prf:ref}`ex-30-hw4-q3`：

```python
# perceived times (t1, t2) of links 1 and 2 in the ten draws
draws = [
    (3.004, 4.004),
    (4.691, 6.675),
    (3.580, 6.215),
    (5.426, 5.629),
    (4.755, 6.699),
    (4.440, 5.799),
    (4.051, 5.336),
    (5.688, 6.420),
    (5.469, 4.980),
    (5.240, 5.677),
]
x = np.zeros(2)
for n, (t1, t2) in enumerate(draws, start=1):
    y = np.array([2.0, 0.0]) if t1 < t2 else np.array([0.0, 2.0])
    x += (y - x) / n
    print(n, t1, t2, y, x.round(3))
print("exact:", round(2 * 7 / 9, 3), round(2 * 2 / 9, 3))

rng = np.random.default_rng(1)
t1, t2 = rng.uniform(3, 6, 100_000), rng.uniform(4, 7, 100_000)
print("100 000 draws: P(link 1) =", round((t1 < t2).mean(), 3))
# Expected: x = [2. 0.] for n = 1, ..., 8, [1.778 0.222] at n = 9,
#           [1.8 0.2] at n = 10
#           exact: 1.556 0.444
#           100 000 draws: P(link 1) = 0.778
```

## 动态模型

### 瓶颈模型

下面的函数对{prf:ref}`ex-31-bottleneck`计算式 {eq}`eq-16-bottleneck-rate` 至式 {eq}`eq-16-bottleneck-total`：

```python
def bottleneck(N, s, t_star, alpha, beta, gamma):
    """Equilibrium of Vickrey's bottleneck model (times in hours).

    Parameters
    ----------
    N : float
        Number of commuters.
    s : float
        Bottleneck capacity (vehicles per hour).
    t_star : float
        Preferred arrival time (hours).
    alpha, beta, gamma : float
        Value of travel time and unit costs of early and late arrival,
        0 < beta < alpha and gamma > 0.

    Returns
    -------
    dict
        Departure times, cost per commuter, departure rates, maximum queue,
        and total costs (eq-16-bottleneck-times to eq-16-bottleneck-total).
    """
    if N <= 0 or s <= 0:
        raise ValueError("N and s must be positive")
    if not 0 < beta < alpha or gamma <= 0:
        raise ValueError("the model needs 0 < beta < alpha and gamma > 0")
    delta = beta * gamma / (beta + gamma)
    return {
        # first and last departures, departure of the on-time arrival
        "t_s": t_star - gamma / (beta + gamma) * N / s,
        "t_e": t_star + beta / (beta + gamma) * N / s,
        "t_tilde": t_star - delta / alpha * N / s,
        "cost": delta * N / s,
        "r_early": alpha * s / (alpha - beta),
        "r_late": alpha * s / (alpha + gamma),
        "max_queue": delta / alpha * N,
        "TTC": delta * N**2 / (2 * s),
        "SDC": delta * N**2 / (2 * s),
        "TC": delta * N**2 / s,
    }


def clock(h):
    """Clock time h:mm of a time h in hours."""
    return f"{int(h)}:{round(60 * (h - int(h))):02d}"


res = bottleneck(N=5000, s=2000, t_star=8.5, alpha=20, beta=10, gamma=40)
print(
    {
        k: (clock(v) if k.startswith("t_") else round(v, 1))
        for k, v in res.items()
    }
)
# Expected: t_s 6:30, t_e 9:00, t_tilde 7:30, cost 20.0, r_early 4000.0,
#           r_late 666.7, max_queue 2000.0, TTC 50000.0, SDC 50000.0,
#           TC 100000.0
```

### 瞬时行程时间与实际经历行程时间

{prf:ref}`ex-31-itt-ett`中的路段行程时间取决于车辆进入路段的分钟。瞬时行程时间将出发时刻的各路段时间相加；实际经历行程时间则跟随车辆穿过网络 {eq}`eq-16-itt-ett`。时间依赖的 Dijkstra 搜索（在先进先出条件下有效）可以找到最早到达的路径。

```python
# link: travel time when entering at minute 1, 2, ..., 7
tt = {
    (1, 2): [1, 1, 1, 1, 1, 1, 1],
    (2, 4): [1, 2, 3, 3, 2, 2, 1],
    (4, 6): [1, 3, 5, 6, 5, 4, 3],
    (2, 5): [2, 3, 3, 2, 2, 2, 2],
    (5, 6): [1, 2, 2, 1, 1, 1, 1],
    (1, 3): [2, 1, 1, 1, 1, 1, 1],
    (3, 5): [2, 2, 1, 1, 1, 1, 1],
}


def time_of(link, minute):
    """Travel time of `link` for a vehicle entering at `minute` (>= 1)."""
    if minute < 1:
        raise ValueError("entry minutes start at 1")
    return tt[link][min(minute, 7) - 1]


def itt(route, dep):
    """Instantaneous travel time of a route (sequence of nodes)."""
    return sum(time_of(link, dep) for link in zip(route, route[1:]))


def ett(route, dep):
    """Experienced travel time of a route (sequence of nodes)."""
    now = dep
    for link in zip(route, route[1:]):
        now += time_of(link, now)
    return now - dep


def td_dijkstra(origin, dest, dep):
    """Earliest-arrival route in a FIFO time-dependent network.

    Returns the route (list of nodes) and its experienced travel time.
    """
    arrival, pred, heap = {origin: dep}, {origin: None}, [(dep, origin)]
    while heap:
        t, i = heapq.heappop(heap)
        if i == dest:
            break
        for a, b in tt:
            if a == i and t + time_of((a, b), t) < arrival.get(b, np.inf):
                arrival[b], pred[b] = t + time_of((a, b), t), i
                heapq.heappush(heap, (arrival[b], b))
    if dest not in arrival:
        raise ValueError(f"node {dest} cannot be reached from {origin}")
    route, j = [dest], dest
    while pred[j] is not None:
        j = pred[j]
        route.append(j)
    return route[::-1], arrival[dest] - dep


routes = [(1, 2, 4, 6), (1, 2, 5, 6), (1, 3, 5, 6)]
for dep in (1, 2):
    print(
        f"departure {dep}:",
        {r: (itt(r, dep), ett(r, dep)) for r in routes},
        " TD-shortest:",
        td_dijkstra(1, 6, dep),
    )
# Expected: departure 1: (ITT, ETT) = (3, 9), (4, 5), (5, 4);
#           TD-shortest: ([1, 3, 5, 6], 4)
#           departure 2: (ITT, ETT) = (6, 8), (6, 5), (5, 3);
#           TD-shortest: ([1, 3, 5, 6], 3)
```

## 小结

- 一个采用 $t_a = A_a + B_ax_a^{P_a}$ 的 `Network` 类即可支持用户均衡、系统最优（边际成本，{prf:ref}`thm-14-so-ue`）、弹性需求（虚拟路段，{eq}`eq-14-excess-demand`）和组合模型。
- 全有全无加载是主力工具：它是 Frank–Wolfe 算法和相继平均法的方向，是 Evans 算法的子问题，也是蒙特卡洛 Probit 加载的基本构件。
- Frank–Wolfe 算法起初收敛很快，接近解时则很慢；相继平均法更简单，但对确定性用户均衡收敛更慢，它是随机加载的首选方法。
- 实用软件（以及 AequilibraE 等 Python 软件包）在含数千条路段的网络上采用相同的思想和更快的算法——共轭 Frank–Wolfe 算法、基于丛的方法；<https://github.com/bstabler/TransportationNetworks> 上的 TNTP 基准网络是检验本章代码的良好平台。
