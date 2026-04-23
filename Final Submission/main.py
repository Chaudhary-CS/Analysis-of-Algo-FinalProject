"""
Main Runner, Graph Algorithms in Network Optimization
Course: Analysis of Algorithms, Final Project

Team: Kartik Chaudhary, Askat Mendybaev, Devon Gardner

Run this file to see all algorithm results and experiments.
    python3 main.py
"""

from graph import build_city_network
from algorithms import (
    print_bfs_results,
    print_dfs_results,
    print_dijkstra_results,
    print_kruskal_results,
    dijkstra_path,
    bfs_path,
)
from analysis import run_all_experiments


def print_header():
    print("\n" + "#" * 70)
    print("#  GRAPH ALGORITHMS IN NETWORK OPTIMIZATION")
    print("#  Analysis of Algorithms, Final Project")
    print("#  Team: Kartik Chaudhary, Askat Mendybaev, Devon Gardner")
    print("#  City: Tampa, Florida")
    print("#" * 70)


def section(title: str):
    print(f"\n\n{'━'*70}")
    print(f"  {title}")
    print(f"{'━'*70}")


def main():
    print_header()

    # Build the graph
    section("TAMPA ROAD NETWORK DATASET (20 Real Locations)")
    g = build_city_network()
    g.print_graph()

    # BFS
    section("ALGORITHM 1: Breadth-First Search (BFS)")
    print("\n  Practical use: How many road segments from Downtown Tampa to each location?")
    print_bfs_results(g, source=0)

    # BFS path example: Downtown to Brandon (furthest suburb)
    path = bfs_path(g, source=0, target=14)
    print(f"\n  BFS fewest-hops path: Downtown Tampa to Brandon")
    print(f"  Path: {' -> '.join(g.get_name(v) for v in path)}  ({len(path)-1} hops)")

    # DFS
    section("ALGORITHM 2: Depth-First Search (DFS)")
    print("\n  Practical use: Confirm all Tampa locations are reachable from Downtown.")
    print_dfs_results(g, source=0)

    # Dijkstra
    section("ALGORITHM 3: Dijkstra's Shortest Path")
    print("\n  Practical use: GPS routing, shortest driving miles from Downtown Tampa.")
    print_dijkstra_results(g, source=0)

    # Highlight: Downtown to Westchase (longest suburban route)
    path, dist = dijkstra_path(g, source=0, target=15)
    print(f"\n  Shortest path: Downtown Tampa to Westchase")
    print(f"  Path : {' -> '.join(g.get_name(v) for v in path)}")
    print(f"  Distance: {dist} miles")

    # Kruskal
    section("ALGORITHM 4: Kruskal's Minimum Spanning Tree")
    print("\n  Practical use: Minimum total road miles to connect all 20 Tampa locations.")
    print("\n  This is the answer FDOT would want for minimum-cost infrastructure planning.")
    print_kruskal_results(g)

    # Experimental Analysis
    section("EXPERIMENTAL ANALYSIS AND COMPARISON")
    run_all_experiments()

    # Summary
    section("DISCUSSION SUMMARY")
    print("""
  Q1: Which algorithm performed best and why?
      For traversal tasks (reachability, connectivity), BFS and DFS are fastest
      at O(V+E) because they do not maintain any priority structure. BFS was
      slightly faster than DFS in practice since deque operations are marginally
      faster than stack push/pop on Python lists for large graphs.

      For shortest path, Dijkstra is the right tool for weighted graphs.
      On our sparse 20-node Tampa graph it runs extremely fast, but runtime
      grows more noticeably on dense graphs due to more heap operations.

      Kruskal is excellent for MST on sparse graphs like ours. On dense
      graphs, sorting E edges dominates and runtime grows as O(E log E).

  Q2: When to use each algorithm?
      BFS:      fewest hops (unweighted shortest path), connectivity check,
                level-order exploration (e.g., social network degrees of separation)
      DFS:      cycle detection, topological sort, connected components, maze solving
      Dijkstra: GPS shortest path (positive weights), network routing
      Kruskal:  minimum cost infrastructure (cables, pipes, roads)

  Q3: Limitations?
      BFS/DFS:  ignore edge weights; BFS gives wrong "shortest" path on weighted graphs
      Dijkstra: fails with negative edge weights (use Bellman-Ford instead)
      Kruskal:  requires sorting all edges upfront; less efficient on very dense graphs

  Q4: Observations from experiments?
      BFS and DFS times scaled nearly linearly with V+E, matching O(V+E) theory.
      Dijkstra was slower than BFS/DFS due to heap overhead, but the difference
      was only noticeable at V=100+.
      Kruskal was most sensitive to edge count: going from sparse to dense
      caused the biggest relative slowdown for Kruskal compared to the others.
      Memory usage for all algorithms grew linearly with V, confirming O(V) space.
    """)

    print("\n" + "#" * 70)
    print("#  END OF PROJECT OUTPUT")
    print("#" * 70 + "\n")


if __name__ == "__main__":
    main()
