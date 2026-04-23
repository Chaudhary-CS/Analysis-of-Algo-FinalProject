"""
Experimental Analysis & Comparison
Course: Analysis of Algorithms — Final Project

Team: Kartik Chaudhary, Askat Mendybaev, Devon Gardner

--- Our Approach to the Experiments ---
Askat designed the experiment framework. We wanted to compare algorithms
across four dimensions:
  1. Execution time
  2. Memory usage (via tracemalloc)
  3. Small vs large graph sizes
  4. Sparse vs dense graphs

We run each algorithm multiple times and take the average to reduce
noise from Python's GC and timer resolution.

Graph sizes tested: 10, 20 (our real dataset), 50, 100 vertices
Densities tested: sparse (0.15), medium (0.30), dense (0.60)
"""

import time
import tracemalloc
import statistics
from graph import Graph, build_city_network, build_synthetic_graph
from algorithms import bfs, dfs, dijkstra, kruskal

RUNS = 10   # number of repetitions per measurement for averaging


# =============================================================================
# TIMING & MEMORY HELPERS
# =============================================================================

def measure_time(func, *args, runs: int = RUNS) -> tuple[float, float]:
    """
    Returns (mean_ms, stdev_ms) over `runs` executions.
    We average over multiple runs because Python's time.perf_counter
    has microsecond noise on short operations.
    """
    times = []
    for _ in range(runs):
        start = time.perf_counter()
        func(*args)
        end = time.perf_counter()
        times.append((end - start) * 1000)   # convert to ms
    return statistics.mean(times), statistics.stdev(times) if runs > 1 else 0.0


def measure_memory(func, *args) -> float:
    """
    Returns peak memory usage in KB for one execution.
    Uses Python's built-in tracemalloc.
    """
    tracemalloc.start()
    func(*args)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak / 1024   # bytes → KB


# =============================================================================
# EXPERIMENT 1: Algorithm comparison on our main city graph (20 nodes)
# =============================================================================

def experiment_main_graph() -> dict:
    """
    Run all four algorithms on our 20-node city network.
    Returns timing and memory results.
    """
    g = build_city_network()
    source = 0   # Downtown

    results = {}

    for name, func, args in [
        ("BFS",      bfs,      (g, source)),
        ("DFS",      dfs,      (g, source)),
        ("Dijkstra", dijkstra, (g, source)),
        ("Kruskal",  kruskal,  (g,)),
    ]:
        mean_t, std_t = measure_time(func, *args)
        mem_kb = measure_memory(func, *args)
        results[name] = {
            "time_mean_ms": round(mean_t, 4),
            "time_std_ms":  round(std_t, 4),
            "memory_kb":    round(mem_kb, 3),
            "vertices":     g.V,
            "edges":        len(g.edges),
        }

    return results


# =============================================================================
# EXPERIMENT 2: Scale test — vary graph size
# =============================================================================

def experiment_scale(sizes: list[int] = [10, 20, 50, 100]) -> dict:
    """
    Compare algorithm runtime as graph size grows (fixed density=0.30).

    This lets us see how each algorithm scales empirically and whether it
    matches our theoretical complexity predictions (BFS/DFS: O(V+E),
    Dijkstra: O((V+E)logV), Kruskal: O(E log E)).
    """
    results = {name: [] for name in ["BFS", "DFS", "Dijkstra", "Kruskal"]}

    for V in sizes:
        g = build_synthetic_graph(V, density=0.30)
        source = 0

        for name, func, args in [
            ("BFS",      bfs,      (g, source)),
            ("DFS",      dfs,      (g, source)),
            ("Dijkstra", dijkstra, (g, source)),
            ("Kruskal",  kruskal,  (g,)),
        ]:
            mean_t, _ = measure_time(func, *args)
            results[name].append({
                "V":          V,
                "E":          len(g.edges),
                "time_ms":    round(mean_t, 4),
            })

    return results


# =============================================================================
# EXPERIMENT 3: Sparse vs Dense comparison
# =============================================================================

def experiment_sparse_vs_dense(V: int = 50) -> dict:
    """
    Same vertex count (50), different densities.

    Sparse  → fewer edges → faster algorithms (less work per vertex)
    Dense   → many edges  → slower, especially for Dijkstra and Kruskal
              since both have edge-count-dependent complexity.

    We expected BFS/DFS to be less sensitive to density than Dijkstra/Kruskal.
    """
    densities = {
        "sparse": 0.10,
        "medium": 0.30,
        "dense":  0.65,
    }

    results = {}
    for label, density in densities.items():
        g = build_synthetic_graph(V, density=density, seed=99)
        source = 0
        row = {"V": V, "E": len(g.edges), "density_label": label, "density": density}

        for name, func, args in [
            ("BFS",      bfs,      (g, source)),
            ("DFS",      dfs,      (g, source)),
            ("Dijkstra", dijkstra, (g, source)),
            ("Kruskal",  kruskal,  (g,)),
        ]:
            mean_t, _ = measure_time(func, *args)
            row[f"{name}_ms"] = round(mean_t, 4)

        results[label] = row

    return results


# =============================================================================
# EXPERIMENT 4: Memory usage across graph sizes
# =============================================================================

def experiment_memory(sizes: list[int] = [10, 20, 50, 100]) -> dict:
    """
    Track peak memory (KB) for each algorithm at different graph sizes.

    All four algorithms are O(V) or O(V+E) in space, so we expect
    memory to grow roughly linearly with graph size.
    """
    results = {name: [] for name in ["BFS", "DFS", "Dijkstra", "Kruskal"]}

    for V in sizes:
        g = build_synthetic_graph(V, density=0.30)
        source = 0

        for name, func, args in [
            ("BFS",      bfs,      (g, source)),
            ("DFS",      dfs,      (g, source)),
            ("Dijkstra", dijkstra, (g, source)),
            ("Kruskal",  kruskal,  (g,)),
        ]:
            mem_kb = measure_memory(func, *args)
            results[name].append({"V": V, "memory_kb": round(mem_kb, 3)})

    return results


# =============================================================================
# PRINT RESULTS (formatted tables)
# =============================================================================

def _separator(width=70):
    print("─" * width)


def print_experiment_main(results: dict):
    print("\n" + "=" * 70)
    print("EXPERIMENT 1 — All Algorithms on Our 20-Node City Network")
    print("=" * 70)
    print(f"  {'Algorithm':<12} {'Avg Time (ms)':<16} {'Std Dev (ms)':<14} {'Peak Memory (KB)'}")
    _separator()
    for algo, r in results.items():
        print(f"  {algo:<12} {r['time_mean_ms']:<16.4f} {r['time_std_ms']:<14.4f} {r['memory_kb']:.3f}")
    print(f"\n  Graph: {results['BFS']['vertices']} vertices, {results['BFS']['edges']} edges")


def print_experiment_scale(results: dict):
    print("\n" + "=" * 70)
    print("EXPERIMENT 2 — Scaling: Runtime vs Graph Size (density=0.30)")
    print("=" * 70)
    sizes = [r["V"] for r in results["BFS"]]
    edges = [r["E"] for r in results["BFS"]]

    header = f"  {'V':>5}  {'E':>6}  " + "  ".join(f"{a:<12}" for a in ["BFS(ms)", "DFS(ms)", "Dijkstra(ms)", "Kruskal(ms)"])
    print(header)
    _separator()
    for i, V in enumerate(sizes):
        row = f"  {V:>5}  {edges[i]:>6}  "
        for algo in ["BFS", "DFS", "Dijkstra", "Kruskal"]:
            row += f"  {results[algo][i]['time_ms']:<12.4f}"
        print(row)


def print_experiment_sparse_dense(results: dict):
    print("\n" + "=" * 70)
    print("EXPERIMENT 3 — Sparse vs Dense Graphs (V=50)")
    print("=" * 70)
    print(f"  {'Type':<8} {'Edges':>6}  {'BFS(ms)':<12} {'DFS(ms)':<12} {'Dijkstra(ms)':<14} {'Kruskal(ms)'}")
    _separator()
    for label, r in results.items():
        print(f"  {label:<8} {r['E']:>6}  {r['BFS_ms']:<12.4f} {r['DFS_ms']:<12.4f} {r['Dijkstra_ms']:<14.4f} {r['Kruskal_ms']:.4f}")


def print_experiment_memory(results: dict):
    print("\n" + "=" * 70)
    print("EXPERIMENT 4 — Peak Memory Usage (KB) vs Graph Size")
    print("=" * 70)
    sizes = [r["V"] for r in results["BFS"]]
    header = f"  {'V':>5}  " + "  ".join(f"{a:<14}" for a in ["BFS(KB)", "DFS(KB)", "Dijkstra(KB)", "Kruskal(KB)"])
    print(header)
    _separator()
    for i, V in enumerate(sizes):
        row = f"  {V:>5}  "
        for algo in ["BFS", "DFS", "Dijkstra", "Kruskal"]:
            row += f"  {results[algo][i]['memory_kb']:<14.3f}"
        print(row)


def run_all_experiments() -> dict:
    """Run all experiments and return raw data for use in the canvas."""
    print("\n>>> Running experiments (each algorithm averaged over 10 runs)...")

    exp1 = experiment_main_graph()
    print("  [1/4] Main graph done.")

    exp2 = experiment_scale()
    print("  [2/4] Scale test done.")

    exp3 = experiment_sparse_vs_dense()
    print("  [3/4] Sparse/dense done.")

    exp4 = experiment_memory()
    print("  [4/4] Memory test done.")

    print_experiment_main(exp1)
    print_experiment_scale(exp2)
    print_experiment_sparse_dense(exp3)
    print_experiment_memory(exp4)

    return {"exp1": exp1, "exp2": exp2, "exp3": exp3, "exp4": exp4}


if __name__ == "__main__":
    run_all_experiments()
