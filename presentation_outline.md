# Presentation Outline
**Graph Algorithms in Network Optimization**
Course: Analysis of Algorithms, Final Project
Team: Kartik Chaudhary, Askat Mendybaev, Devon Gardner
City: Tampa, Florida

Total slides: 10


## Slide 1: Title Slide (Kartik presents)

**Graph Algorithms in Network Optimization**
Tampa Road Network Case Study

Team: Kartik Chaudhary, Askat Mendybaev, Devon Gardner
Course: Analysis of Algorithms
Date: Spring 2026


## Slide 2: Problem Statement and Motivation (Kartik presents)

Why Tampa? We are all students here, so we used the city we actually live in. Every location is somewhere we have been, which let us verify results intuitively.

Two core questions we wanted to answer:
1. What is the shortest driving route between any two Tampa locations? (Dijkstra)
2. What is the minimum total road mileage to connect all 20 Tampa areas? (Kruskal)
3. Is every part of Tampa reachable from Downtown? (BFS / DFS)

Real applications: GPS navigation, FDOT infrastructure planning, emergency vehicle routing from Tampa General Hospital.


## Slide 3: Graph Model (Kartik presents)

Our graph has 20 vertices (real Tampa locations) and 37 edges (road connections).

Show the vertex table: Downtown Tampa, TPA Airport, USF, Tampa General, International Plaza, Riverwalk, Ybor City, John Germany Library, Raymond James Stadium, Tampa Museum of Art, Port of Tampa Bay, Westshore District, New Tampa, South Tampa, Brandon, Westchase, Channelside, Tampa Convention Center, Seminole Heights, Hyde Park Village.

Graph type: Weighted and Undirected.
Weighted because we need real driving distances (miles) for GPS routing.
Undirected because Tampa roads go both ways.
Representation: Adjacency list, chosen over adjacency matrix because our graph is sparse (37 edges vs 190 for a complete graph).

Askat verified every edge weight using Google Maps.


## Slide 4: Algorithm 1 and 2, BFS and DFS (Devon presents)

BFS (Breadth-First Search):
Explores level by level using a queue. Finds the path with fewest hops (ignoring weights).
Tampa result: Downtown to Brandon = 3 hops via Downtown to Tampa General to South Tampa to Brandon.
Time: O(V + E). Space: O(V).

DFS (Depth-First Search):
Explores as deep as possible before backtracking. Implemented iteratively using a stack.
Tampa result: All 20 locations confirmed reachable from Downtown (20/20 vertices reached).
Time: O(V + E). Space: O(V).

Key point: Both BFS and DFS ignore edge weights. That is fine for connectivity checks but wrong for GPS routing.


## Slide 5: Algorithm 3, Dijkstra's Shortest Path (Kartik presents)

Dijkstra's Algorithm:
Uses a min-heap priority queue. Finds shortest weighted path from source to all vertices.
Requires non-negative edge weights. Tampa road distances are always at least 1 mile, so this holds.
Time: O((V+E) log V) with binary heap. Space: O(V + E).

Tampa results from Downtown:
- To TPA Airport: 10 miles via Dale Mabry (Raymond James Stadium to Westshore to Airport)
- To USF: 7 miles via N Ashley Dr to Library to Bruce B Downs
- To Brandon: 20 miles via Riverwalk to Hyde Park to South Tampa to Selmon Expressway
- To Westchase: 12 miles via Dale Mabry

Key insight: Without the Downtown to Raymond James Stadium edge (Dale Mabry), Dijkstra routed Downtown to Airport as 42 miles via USF and New Tampa. Adding that one road dropped it to 10 miles. One missing edge can completely break shortest-path results.


## Slide 6: Algorithm 4, Kruskal's Minimum Spanning Tree (Askat presents)

Kruskal's Algorithm:
Sort all edges by weight. Add edges to MST one at a time if they connect two different components.
Uses Union-Find with path compression and union by rank for near O(1) per operation.
Time: O(E log E). Space: O(V + E).

Tampa MST result:
19 road segments, total cost of 65 miles to connect all 20 Tampa locations.

Selected MST edges:
- Downtown to Riverwalk, Museum of Art, Channelside, Convention Center (all 1 mile each)
- Airport to International Plaza (2 miles)
- South Tampa to Brandon (15 miles)

Why Kruskal over Prim? Kruskal is more natural to implement with Union-Find and performs better on sparse graphs. Our Tampa graph has 37 edges, which is sparse.


## Slide 7: Complexity Summary (Devon presents)

| Algorithm | Time | Space | Best Case | Worst Case |
|---|---|---|---|---|
| BFS | O(V+E) | O(V) | Target is immediate neighbor | Full graph explored |
| DFS | O(V+E) | O(V) | Target on first branch | Linear chain graph |
| Dijkstra | O((V+E) log V) | O(V+E) | Source = target | Dense graph O(V^2 log V) |
| Kruskal | O(E log E) | O(V+E) | Edges already sorted | Dense graph O(V^2 log V) |

Note: Dijkstra only works with non-negative weights. Bellman-Ford handles negative weights at O(VE).
Note: Kruskal requires sorting all edges upfront, which is expensive on dynamic graphs.


## Slide 8: Experimental Results (Askat presents)

We ran four experiments, each averaged over 10 runs using Python's time.perf_counter and tracemalloc for memory.

Experiment 1, Tampa graph (20 nodes, 37 edges):
BFS 0.0087ms, DFS 0.0090ms, Dijkstra 0.0109ms, Kruskal 0.0204ms.
All under 0.025ms. Differences are not meaningful at this size.

Experiment 2, Scale test (V from 10 to 100, density 0.30):
At V = 100: BFS 0.0855ms, DFS 0.1785ms, Dijkstra 0.2269ms, Kruskal 0.3684ms.
BFS and DFS scale linearly. Dijkstra's log factor shows. Kruskal steepens as E grows with V^2.

Experiment 3, Sparse vs Dense (V = 50):
Sparse (164 edges): Kruskal 0.0581ms. Dense (822 edges): Kruskal 0.1492ms.
Kruskal is most sensitive to density. BFS is least sensitive.

Experiment 4, Memory:
All algorithms grow linearly in memory with V, confirming O(V) space.


## Slide 9: Discussion and Insights (Devon presents)

Which algorithm performed best?
For Tampa specifically: Dijkstra is most practically valuable because it answers the question people actually have (how do I get there?). BFS and DFS are fastest at O(V+E) but can only answer connectivity questions, not distance questions.

When to use each:
- BFS: subway transfers, social network hops, connectivity checks
- DFS: detecting cycles in dependency graphs, topological sort, finding all connected components
- Dijkstra: GPS navigation, network packet routing (OSPF uses Dijkstra)
- Kruskal: laying fiber cables, building water pipe networks, road infrastructure with minimum cost

Limitations:
- BFS/DFS ignore weights entirely
- Dijkstra breaks on negative weights; use Bellman-Ford
- Kruskal is not efficient on dynamic graphs where edges change frequently; Prim's works better there


## Slide 10: Conclusion and Demo (All three present)

What we built:
A Tampa road network with 20 real locations and 37 Google Maps verified road connections.
Four fully implemented and tested graph algorithms covering all three required categories.
Four experiments comparing runtime, memory, scale, and density.

Key results:
- BFS: Downtown to Brandon in 3 hops
- DFS: All 20 Tampa locations confirmed reachable
- Dijkstra: Downtown to Airport = 10 miles via Dale Mabry
- Kruskal: Minimum 65-mile network connects all of Tampa

Live demo: run python3 main.py

Takeaway: Algorithm choice depends entirely on what question you are answering. There is no universally best option. The Tampa network gave us a real dataset to test that principle against.


## Speaker Notes

Kartik speaks on: slides 1, 2, 3, 5 (problem, graph model, Dijkstra)
Askat speaks on: slides 6, 8 (Kruskal, experiments)
Devon speaks on: slides 4, 7, 9 (BFS/DFS, complexity, discussion)
All three speak on slide 10 conclusion

Anticipated questions and answers:

Q: Why not use Bellman-Ford instead of Dijkstra?
A: Bellman-Ford handles negative weights but runs at O(VE), which is significantly slower than Dijkstra's O((V+E) log V). Since all Tampa road distances are positive, Dijkstra is the correct and more efficient choice.

Q: Why adjacency list over adjacency matrix?
A: Our graph has 20 vertices but only 37 edges. A complete graph would have 190 edges. Adjacency list takes O(V + E) space while adjacency matrix takes O(V^2). For sparse graphs like ours, adjacency list is more memory-efficient.

Q: Why Kruskal over Prim?
A: Both give the same MST. We chose Kruskal because Union-Find is straightforward to implement and Kruskal performs better on sparse graphs. Prim's with a Fibonacci heap is better for very dense graphs or dynamic graphs.

Q: How did you verify the edge weights?
A: Askat verified each weight using Google Maps driving distance. We used approximate driving miles rather than straight-line distances because Tampa's geography (Davis Islands, the Hillsborough River, Tampa Bay) forces significant road detours.
