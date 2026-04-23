"""
Algorithm Implementations, Graph Algorithms in Network Optimization

Team: Kartik Chaudhary, Askat Mendybaev, Devon Gardner
City: Tampa, Florida

Who did what:
Kartik implemented Dijkstra and wrote its complexity analysis.
Askat implemented Kruskal and the Union-Find helper class, plus its analysis.
Devon implemented BFS and DFS and their analyses.

All of us reviewed each other's code before the final submission.

We implemented four algorithms covering all three required categories:
  1. Traversal:     BFS (Devon) and DFS (Devon)
  2. Shortest Path: Dijkstra (Kartik)
  3. MST:           Kruskal (Askat)

Edge weights throughout are driving distances in miles on the Tampa road network.
"""

from collections import deque
import heapq
from typing import Optional
from graph import Graph


# =============================================================================
# 1. BREADTH-FIRST SEARCH (BFS)
#    Implemented by: Devon Gardner
# =============================================================================

"""
PSEUDOCODE - BFS:

BFS(G, source):
    for each vertex u in G.V:
        color[u] = WHITE
        dist[u]  = INFINITY
        parent[u] = NIL
    color[source] = GRAY
    dist[source]  = 0
    Q = empty queue
    ENQUEUE(Q, source)
    while Q is not empty:
        u = DEQUEUE(Q)
        for each neighbor v of u:
            if color[v] == WHITE:
                color[v]  = GRAY
                dist[v]   = dist[u] + 1
                parent[v] = u
                ENQUEUE(Q, v)
        color[u] = BLACK
    return dist, parent

Time Complexity:
    O(V + E)
    Every vertex is enqueued and dequeued exactly once: O(V)
    Every edge is examined once (twice for undirected): O(E)
    Best case = Worst case = O(V + E), BFS always visits everything reachable.

Space Complexity:
    O(V)
    dist[], parent[], color[] arrays each take O(V)
    Queue holds at most O(V) vertices

Best case: Target is the direct neighbor of source, found in 1 iteration.
           Still O(V + E) asymptotically because we initialize all vertices.
Worst case: Target is the farthest vertex, or graph is dense, so O(V + E).
"""


def bfs(graph: Graph, source: int) -> tuple[dict, dict]:
    """
    BFS from source. Returns (distances, parents).

    Devon's note: BFS is great for finding the fewest-hops path (unweighted),
    checking connectivity, and level-order exploration. In our Tampa network,
    BFS from Downtown Tampa tells us how many road-segments away each location
    is, regardless of mileage — useful for minimizing number of turns/stops.
    """
    dist = {v: float('inf') for v in range(graph.V)}
    parent = {v: None for v in range(graph.V)}
    visited = set()

    dist[source] = 0
    queue = deque([source])
    visited.add(source)

    order = []   # track visit order so we can print/analyze it

    while queue:
        u = queue.popleft()
        order.append(u)

        for v, _ in graph.adj[u]:    # BFS ignores weights
            if v not in visited:
                visited.add(v)
                dist[v] = dist[u] + 1
                parent[v] = u
                queue.append(v)

    return dist, parent, order


def bfs_path(graph: Graph, source: int, target: int) -> list[int]:
    """Reconstruct the fewest-hops path from source to target using BFS."""
    _, parent, _ = bfs(graph, source)
    if parent[target] is None and target != source:
        return []   # no path
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = parent[node]
    return path[::-1]


# =============================================================================
# 2. DEPTH-FIRST SEARCH (DFS)
#    Implemented by: Devon Gardner
# =============================================================================

"""
PSEUDOCODE - DFS:

DFS(G):
    for each vertex u in G.V:
        color[u] = WHITE
        parent[u] = NIL
    time = 0
    for each vertex u in G.V:
        if color[u] == WHITE:
            DFS-VISIT(G, u)

DFS-VISIT(G, u):
    time = time + 1
    disc[u] = time          (discovery time)
    color[u] = GRAY
    for each neighbor v of u:
        if color[v] == WHITE:
            parent[v] = u
            DFS-VISIT(G, v)
    color[u] = BLACK
    time = time + 1
    finish[u] = time        (finish time)

Time Complexity:
    O(V + E)
    Each vertex is discovered and finished exactly once: O(V)
    Each edge is examined once (twice for undirected): O(E)

Space Complexity:
    O(V)
    disc[], finish[], color[], parent[] arrays each take O(V)
    Recursive call stack depth up to O(V) in worst case (linear chain graph)

Best case: Source immediately finds a path or detects a cycle on the first branch.
Worst case: Graph is a long chain, so call stack depth reaches O(V).
"""


def dfs(graph: Graph, source: Optional[int] = None) -> tuple[dict, dict, list]:
    """
    Iterative DFS (we used iterative instead of recursive to avoid Python's
    default recursion limit of 1000 on large graphs).

    Devon's note: DFS is useful for detecting cycles, topological sort, and
    finding connected components. In our Tampa network, DFS from Downtown
    explores deep into one sub-region (e.g., South Tampa / Hyde Park) before
    backtracking — useful for full city reachability mapping.
    """
    visited = set()
    parent = {v: None for v in range(graph.V)}
    order = []

    start_nodes = [source] if source is not None else list(range(graph.V))

    for start in start_nodes:
        if start in visited:
            continue
        stack = [start]
        while stack:
            u = stack.pop()
            if u in visited:
                continue
            visited.add(u)
            order.append(u)
            for v, _ in reversed(graph.adj[u]):   # reversed to match recursive order
                if v not in visited:
                    if parent[v] is None:
                        parent[v] = u
                    stack.append(v)

    return visited, parent, order


# =============================================================================
# 3. DIJKSTRA'S ALGORITHM
#    Implemented by: Kartik Chaudhary
# =============================================================================

"""
PSEUDOCODE - Dijkstra (min-heap / priority queue):

Dijkstra(G, source):
    for each vertex u in G.V:
        dist[u]   = INFINITY
        parent[u] = NIL
    dist[source] = 0
    PQ = MIN-PRIORITY-QUEUE containing all vertices keyed by dist
    while PQ is not empty:
        u = EXTRACT-MIN(PQ)
        for each neighbor v of u with edge weight w(u,v):
            if dist[u] + w(u,v) < dist[v]:
                dist[v]   = dist[u] + w(u,v)    (RELAX)
                parent[v] = u
                DECREASE-KEY(PQ, v, dist[v])
    return dist, parent

Time Complexity (with binary min-heap):
    O((V + E) log V)
    EXTRACT-MIN costs O(log V), called V times:      O(V log V)
    DECREASE-KEY costs O(log V), called at most E times: O(E log V)
    Total: O((V + E) log V)

    With a Fibonacci heap this improves to O(E + V log V), but we used
    Python's heapq (binary heap) since it is simpler and sufficient.

Space Complexity:
    O(V + E)
    dist[] and parent[] arrays take O(V)
    Priority queue holds O(V) entries normally, up to O(E) with lazy deletion

Best case: Source equals target, return immediately, O(1).
Worst case: Dense graph, all edges relaxed, O((V + E) log V).

Note: Dijkstra requires non-negative edge weights. Tampa road distances
are always at least 1 mile, so this constraint is always satisfied.
"""


def dijkstra(graph: Graph, source: int) -> tuple[dict, dict]:
    """
    Dijkstra's shortest path from source to all vertices.

    Kartik's note: We chose Dijkstra over Bellman-Ford because Tampa road
    distances are all positive miles — no negative weights. Dijkstra is faster:
    O((V+E) log V) vs Bellman-Ford's O(VE). This is essentially what Google
    Maps runs (a variant of Dijkstra) when you ask for directions in Tampa.
    """
    dist = {v: float('inf') for v in range(graph.V)}
    parent = {v: None for v in range(graph.V)}
    dist[source] = 0

    # (distance, vertex) min-heap
    pq = [(0, source)]

    while pq:
        d, u = heapq.heappop(pq)

        # Lazy deletion: skip if we already found a shorter path to u
        if d > dist[u]:
            continue

        for v, weight in graph.adj[u]:
            new_dist = dist[u] + weight
            if new_dist < dist[v]:          # RELAX
                dist[v] = new_dist
                parent[v] = u
                heapq.heappush(pq, (new_dist, v))

    return dist, parent


def dijkstra_path(graph: Graph, source: int, target: int) -> tuple[list[int], int]:
    """Return (path, total_distance) from source to target."""
    dist, parent = dijkstra(graph, source)
    if dist[target] == float('inf'):
        return [], -1
    path = []
    node = target
    while node is not None:
        path.append(node)
        node = parent[node]
    return path[::-1], dist[target]


# =============================================================================
# 4. KRUSKAL'S ALGORITHM (Minimum Spanning Tree)
#    Implemented by: Askat Mendybaev
# =============================================================================

"""
PSEUDOCODE - Kruskal:

Kruskal(G):
    A = empty set                    (MST edges)
    for each vertex v in G.V:
        MAKE-SET(v)
    sort G.E by weight ascending
    for each edge (u, v) in sorted G.E:
        if FIND-SET(u) != FIND-SET(v):   (u and v in different components)
            A = A union {(u, v)}
            UNION(u, v)
    return A

Union-Find with Path Compression and Union by Rank:

MAKE-SET(x):    parent[x] = x;  rank[x] = 0

FIND-SET(x):    if x != parent[x]:
                    parent[x] = FIND-SET(parent[x])   (path compression)
                return parent[x]

UNION(x, y):    rx = FIND-SET(x);  ry = FIND-SET(y)
                if rx == ry: return
                if rank[rx] < rank[ry]: swap(rx, ry)
                parent[ry] = rx
                if rank[rx] == rank[ry]: rank[rx] += 1

Time Complexity:
    O(E log E), dominated by sorting the edges
    Sorting edges: O(E log E)
    V MAKE-SET calls: O(V)
    E FIND-SET and UNION calls with path compression and union by rank
    cost nearly O(E * alpha(V)) where alpha is the inverse Ackermann function,
    which is effectively O(1) for all practical V.
    Total: O(E log E)

    Since E <= V^2, log E = O(log V), so this is also written as O(E log V).

Space Complexity:
    O(V + E)
    parent[] and rank[] arrays: O(V)
    Sorted edge list: O(E)

Best case: Edges are already in sorted order. Sorting still runs, so O(E log E) always.
Worst case: Dense graph with E = O(V^2) gives O(V^2 log V).
"""


class UnionFind:
    """
    Disjoint Set Union (Union-Find) with path compression and union by rank.
    Askat's note: This makes Kruskal fast. Without it, FIND would be O(V) per
    call in the worst case (long chains). With path compression + union by rank,
    amortized cost per operation is nearly O(1).
    """

    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])   # path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        """Merge the sets containing x and y. Returns False if already same set."""
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True


def kruskal(graph: Graph) -> tuple[list[tuple[int, int, int]], int]:
    """
    Kruskal's MST. Returns (mst_edges, total_weight).

    Askat's note: We chose Kruskal over Prim because Kruskal is more
    intuitive to implement with Union-Find, and it performs better on
    sparse graphs (O(E log E) vs Prim's O((V+E) log V) with a min-heap).
    Since our Tampa graph is sparse (~38 edges on 20 nodes), Kruskal fits.

    In Tampa context: the MST gives the minimum total road miles needed
    to connect all 20 Tampa locations — the kind of answer FDOT (Florida
    Department of Transportation) would want when planning minimal new
    road infrastructure to connect underserved areas.
    """
    uf = UnionFind(graph.V)
    sorted_edges = sorted(graph.edges)    # sort by weight (index 0)

    mst_edges = []
    total_weight = 0

    for weight, u, v in sorted_edges:
        if uf.union(u, v):
            mst_edges.append((u, v, weight))
            total_weight += weight
            if len(mst_edges) == graph.V - 1:   # MST has V-1 edges
                break

    return mst_edges, total_weight


# =============================================================================
# HELPER: Print results nicely
# =============================================================================

def print_bfs_results(graph: Graph, source: int):
    print(f"\n{'='*60}")
    print(f"BFS from '{graph.get_name(source)}'")
    print(f"{'='*60}")
    dist, parent, order = bfs(graph, source)
    print(f"  Visit order: {' → '.join(graph.get_name(v) for v in order)}")
    print(f"\n  Hop distances from {graph.get_name(source)}:")
    for v in range(graph.V):
        d = dist[v]
        d_str = str(d) if d != float('inf') else "unreachable"
        print(f"    {graph.get_name(v):<28}: {d_str} hops")


def print_dfs_results(graph: Graph, source: int):
    print(f"\n{'='*60}")
    print(f"DFS from '{graph.get_name(source)}'")
    print(f"{'='*60}")
    visited, parent, order = dfs(graph, source)
    print(f"  Visit order: {' → '.join(graph.get_name(v) for v in order)}")
    print(f"  Total vertices reached: {len(visited)}")


def print_dijkstra_results(graph: Graph, source: int):
    print(f"\n{'='*60}")
    print(f"Dijkstra Shortest Paths from '{graph.get_name(source)}'")
    print(f"{'='*60}")
    dist, _ = dijkstra(graph, source)
    for v in range(graph.V):
        d = dist[v]
        d_str = f"{d} mi" if d != float('inf') else "unreachable"
        path, _ = dijkstra_path(graph, source, v)
        path_str = " → ".join(graph.get_name(n) for n in path)
        print(f"  To {graph.get_name(v):<28}: {d_str:<12}  Path: {path_str}")


def print_kruskal_results(graph: Graph):
    print(f"\n{'='*60}")
    print(f"Kruskal's Minimum Spanning Tree")
    print(f"{'='*60}")
    mst_edges, total = kruskal(graph)
    for u, v, w in mst_edges:
        print(f"  {graph.get_name(u):<28} to {graph.get_name(v):<28}  ({w} mi)")
    print(f"\n  Total MST weight: {total} mi  ({len(mst_edges)} edges, {graph.V} vertices)")
