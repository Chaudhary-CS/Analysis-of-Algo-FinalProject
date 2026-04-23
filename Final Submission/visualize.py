"""
Graph Visualizations, Tampa Road Network
Course: Analysis of Algorithms, Final Project

Team: Kartik Chaudhary, Askat Mendybaev, Devon Gardner

Run this file to generate all graph diagrams as PNG images:
    python3 visualize.py

Generates:
    fig1_tampa_network.png      - Full Tampa road network
    fig2_mst.png                - Minimum Spanning Tree highlighted
    fig3_bfs_dfs.png            - BFS and DFS traversal order
    fig4_dijkstra_path.png      - Dijkstra shortest paths from Downtown
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import networkx as nx
from graph import build_city_network
from algorithms import kruskal, bfs, dfs, dijkstra

# ── Approximate Tampa geographic positions (x = east/west, y = north/south) ──
# Spread downtown cluster so labels don't overlap
POSITIONS = {
    0:  (5.5,  5.0),   # Downtown Tampa       - center
    1:  (1.0,  7.0),   # Tampa Intl Airport   - northwest
    2:  (7.5,  9.5),   # USF                  - north
    3:  (5.2,  2.0),   # Tampa General        - south of downtown
    4:  (1.8,  6.0),   # International Plaza  - northwest
    5:  (4.0,  5.8),   # Riverwalk            - west of downtown
    6:  (7.2,  5.5),   # Ybor City            - east of downtown
    7:  (5.5,  6.8),   # John Germany Library - north of downtown
    8:  (3.0,  6.5),   # Raymond James        - west
    9:  (4.2,  4.5),   # Museum of Art        - southwest of downtown
    10: (7.0,  3.8),   # Port of Tampa Bay    - southeast
    11: (2.2,  5.5),   # Westshore District   - west
    12: (8.5, 11.0),   # New Tampa            - far north
    13: (4.0,  1.5),   # South Tampa          - far south
    14: (11.0, 4.5),   # Brandon              - far east
    15: (0.2,  6.0),   # Westchase            - far west
    16: (6.5,  4.5),   # Channelside          - east of downtown
    17: (6.8,  3.2),   # Convention Center    - south of downtown
    18: (6.5,  7.8),   # Seminole Heights     - north
    19: (3.5,  2.8),   # Hyde Park Village    - south
}

# Color by area type
NODE_COLORS = {
    # Downtown core
    0: "#2B6CB0", 5: "#2B6CB0", 7: "#2B6CB0", 9: "#2B6CB0",
    16: "#2B6CB0", 17: "#2B6CB0",
    # Neighborhoods
    6: "#276749", 18: "#276749", 19: "#276749", 3: "#276749", 13: "#276749",
    # Suburbs
    12: "#C05621", 14: "#C05621", 15: "#C05621",
    # Commercial / Transport / Education
    1: "#6B46C1", 4: "#6B46C1", 8: "#6B46C1", 10: "#6B46C1",
    11: "#6B46C1", 2: "#6B46C1",
}

AREA_LABELS = {
    "Downtown Core":          "#2B6CB0",
    "Neighborhoods":          "#276749",
    "Suburbs":                "#C05621",
    "Commercial / Transport": "#6B46C1",
}

SHORT_NAMES = {
    0:  "Downtown",
    1:  "TPA Airport",
    2:  "USF",
    3:  "Tampa General",
    4:  "Intl Plaza",
    5:  "Riverwalk",
    6:  "Ybor City",
    7:  "Library",
    8:  "RayJay Stadium",
    9:  "Museum of Art",
    10: "Port",
    11: "Westshore",
    12: "New Tampa",
    13: "South Tampa",
    14: "Brandon",
    15: "Westchase",
    16: "Channelside",
    17: "Convention Ctr",
    18: "Seminole Hts",
    19: "Hyde Park",
}


def build_nx_graph():
    """Convert our Graph class to a NetworkX graph."""
    g = build_city_network()
    G = nx.Graph()
    for v in range(g.V):
        G.add_node(v, label=SHORT_NAMES[v])
    for weight, u, v in g.edges:
        G.add_edge(u, v, weight=weight)
    return G, g


def draw_base(ax, G, node_colors, edge_color="#AAAAAA", edge_width=1.4,
              edge_alpha=0.65, show_edge_labels=True, title=""):
    colors = [node_colors.get(v, "#888888") for v in G.nodes()]

    nx.draw_networkx_nodes(G, POSITIONS, ax=ax, node_color=colors,
                           node_size=700, alpha=0.95)

    # Labels positioned slightly above each node so they don't overlap the circle
    label_pos = {v: (x, y + 0.35) for v, (x, y) in POSITIONS.items()}
    nx.draw_networkx_labels(G, label_pos,
                            labels={v: SHORT_NAMES[v] for v in G.nodes()},
                            ax=ax, font_size=6.5, font_color="#1A202C", font_weight="bold")

    nx.draw_networkx_edges(G, POSITIONS, ax=ax, edge_color=edge_color,
                           width=edge_width, alpha=edge_alpha)

    if show_edge_labels:
        edge_labels = {(u, v): f"{d['weight']}mi" for u, v, d in G.edges(data=True)}
        nx.draw_networkx_edge_labels(G, POSITIONS, edge_labels=edge_labels,
                                     ax=ax, font_size=5.8, font_color="#555555",
                                     bbox=dict(boxstyle="round,pad=0.15",
                                               facecolor="white", alpha=0.7, edgecolor="none"))
    ax.set_title(title, fontsize=13, fontweight="bold", pad=12)
    ax.axis("off")


# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 1: Full Tampa Road Network
# ─────────────────────────────────────────────────────────────────────────────

def fig1_full_network():
    G, g = build_nx_graph()
    fig, ax = plt.subplots(figsize=(15, 11))
    fig.patch.set_facecolor("#F7FAFC")
    ax.set_facecolor("#F7FAFC")

    draw_base(ax, G, NODE_COLORS, title="Tampa Road Network (20 Vertices, 37 Edges)")

    # Legend
    patches = [mpatches.Patch(color=c, label=l) for l, c in AREA_LABELS.items()]
    ax.legend(handles=patches, loc="lower left", fontsize=8,
              framealpha=0.85, edgecolor="#CCCCCC")

    # Annotation
    ax.text(0.01, 0.99,
            "Weighted, Undirected\nEdge weights = driving miles (Google Maps)",
            transform=ax.transAxes, fontsize=7.5, va="top",
            color="#555555", style="italic")

    plt.tight_layout()
    plt.savefig("fig1_tampa_network.png", dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close()
    print("  Saved: fig1_tampa_network.png")


# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 2: MST Highlighted
# ─────────────────────────────────────────────────────────────────────────────

def fig2_mst():
    G, g = build_nx_graph()
    mst_edges, total = kruskal(g)
    mst_set = {(min(u, v), max(u, v)) for u, v, _ in mst_edges}
    mst_edge_data = {(min(u, v), max(u, v)): w for u, v, w in mst_edges}

    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    fig.patch.set_facecolor("#F7FAFC")

    # Left: full graph (faded)
    ax = axes[0]
    ax.set_facecolor("#F7FAFC")
    draw_base(ax, G, NODE_COLORS, edge_color="#CCCCCC", edge_width=0.8,
              edge_alpha=0.4, show_edge_labels=False,
              title="Full Tampa Road Network")

    # Right: MST only
    ax = axes[1]
    ax.set_facecolor("#F7FAFC")
    colors = [NODE_COLORS.get(v, "#888888") for v in G.nodes()]
    nx.draw_networkx_nodes(G, POSITIONS, ax=ax, node_color=colors,
                           node_size=700, alpha=0.95)
    lpos = {v: (x, y + 0.35) for v, (x, y) in POSITIONS.items()}
    nx.draw_networkx_labels(G, lpos,
                            labels={v: SHORT_NAMES[v] for v in G.nodes()},
                            ax=ax, font_size=6.5, font_color="#1A202C", font_weight="bold")

    # Non-MST edges (faded)
    non_mst = [(u, v) for u, v in G.edges()
               if (min(u, v), max(u, v)) not in mst_set]
    nx.draw_networkx_edges(G, POSITIONS, edgelist=non_mst, ax=ax,
                           edge_color="#DDDDDD", width=0.7, alpha=0.4)

    # MST edges (highlighted)
    mst_el = [(u, v) for u, v in G.edges()
              if (min(u, v), max(u, v)) in mst_set]
    nx.draw_networkx_edges(G, POSITIONS, edgelist=mst_el, ax=ax,
                           edge_color="#C53030", width=2.8, alpha=0.9)

    # MST edge labels
    mst_labels = {(u, v): f"{mst_edge_data.get((min(u,v),max(u,v)),'?')}mi"
                  for u, v in mst_el}
    nx.draw_networkx_edge_labels(G, POSITIONS, edge_labels=mst_labels,
                                 ax=ax, font_size=5.5, font_color="#C53030",
                                 bbox=dict(boxstyle="round,pad=0.1",
                                           facecolor="white", alpha=0.6, edgecolor="none"))

    ax.set_title(f"Kruskal MST  |  19 edges  |  {total} miles total",
                 fontsize=12, fontweight="bold", pad=10)
    ax.axis("off")

    mst_patch = mpatches.Patch(color="#C53030", label=f"MST edges ({total} mi total)")
    faded_patch = mpatches.Patch(color="#DDDDDD", label="Non-MST edges")
    ax.legend(handles=[mst_patch, faded_patch], loc="lower left",
              fontsize=8, framealpha=0.85, edgecolor="#CCCCCC")

    plt.tight_layout()
    plt.savefig("fig2_mst.png", dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close()
    print("  Saved: fig2_mst.png")


# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 3: BFS vs DFS Traversal Order
# ─────────────────────────────────────────────────────────────────────────────

def fig3_traversals():
    G, g = build_nx_graph()
    _, _, bfs_order = bfs(g, source=0)
    _, _, dfs_order = dfs(g, source=0)

    fig, axes = plt.subplots(1, 2, figsize=(16, 8))
    fig.patch.set_facecolor("#F7FAFC")

    for ax, order, algo_name, color in [
        (axes[0], bfs_order, "BFS", "#2B6CB0"),
        (axes[1], dfs_order, "DFS", "#276749"),
    ]:
        ax.set_facecolor("#F7FAFC")
        rank = {v: i + 1 for i, v in enumerate(order)}

        node_colors = []
        for v in G.nodes():
            if v == 0:
                node_colors.append("#E53E3E")     # source = red
            else:
                frac = rank.get(v, len(order)) / len(order)
                if algo_name == "BFS":
                    r = int(43 + (1 - frac) * (155))
                    node_colors.append(f"#{r:02X}6C{0xB0:02X}")
                else:
                    r = int(39 + (1 - frac) * 120)
                    node_colors.append(f"#27{r:02X}49")

        node_colors = [NODE_COLORS.get(v, "#888888") for v in G.nodes()]

        nx.draw_networkx_nodes(G, POSITIONS, ax=ax, node_color=node_colors,
                               node_size=700, alpha=0.9)

        # Name above node
        lpos = {v: (x, y + 0.35) for v, (x, y) in POSITIONS.items()}
        nx.draw_networkx_labels(G, lpos,
                                labels={v: SHORT_NAMES[v] for v in G.nodes()},
                                ax=ax, font_size=6.5, font_color="#1A202C", font_weight="bold")

        # Step number below node
        spos = {v: (x, y - 0.45) for v, (x, y) in POSITIONS.items()}
        nx.draw_networkx_labels(G, spos,
                                labels={v: f"#{rank[v]}" for v in G.nodes()},
                                ax=ax, font_size=7.0, font_color="#E53E3E", font_weight="bold")

        nx.draw_networkx_edges(G, POSITIONS, ax=ax, edge_color="#BBBBBB",
                               width=1.0, alpha=0.5)

        ax.set_title(
            f"{algo_name} Traversal from Downtown Tampa\nVisit order: 1 = first visited",
            fontsize=11, fontweight="bold", pad=10)
        ax.axis("off")

        # Show order as text
        order_text = " -> ".join(f"#{i+1} {SHORT_NAMES[v]}" for i, v in enumerate(order))
        ax.text(0.01, 0.01, f"Order: {order_text}",
                transform=ax.transAxes, fontsize=5, va="bottom",
                color="#555555", wrap=True,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white",
                          alpha=0.7, edgecolor="none"))

    source_patch = mpatches.Patch(color="#E53E3E", label="Source (Downtown Tampa)")
    axes[0].legend(handles=[source_patch], loc="upper right", fontsize=8,
                   framealpha=0.85, edgecolor="#CCCCCC")

    plt.tight_layout()
    plt.savefig("fig3_bfs_dfs.png", dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close()
    print("  Saved: fig3_bfs_dfs.png")


# ─────────────────────────────────────────────────────────────────────────────
# FIGURE 4: Dijkstra Shortest Paths from Downtown
# ─────────────────────────────────────────────────────────────────────────────

def fig4_dijkstra():
    from algorithms import dijkstra_path
    G, g = build_nx_graph()
    dist, parent = dijkstra(g, source=0)

    # Reconstruct all shortest-path edges used
    path_edges = set()
    for target in range(1, g.V):
        if dist[target] != float('inf'):
            node = target
            while parent[node] is not None:
                u, v = parent[node], node
                path_edges.add((min(u, v), max(u, v)))
                node = parent[node]

    fig, ax = plt.subplots(figsize=(13, 10))
    fig.patch.set_facecolor("#F7FAFC")
    ax.set_facecolor("#F7FAFC")

    # All edges faded
    non_path = [(u, v) for u, v in G.edges()
                if (min(u, v), max(u, v)) not in path_edges]
    nx.draw_networkx_edges(G, POSITIONS, edgelist=non_path, ax=ax,
                           edge_color="#DDDDDD", width=0.7, alpha=0.4)

    # Shortest path tree edges
    path_el = [(u, v) for u, v in G.edges()
               if (min(u, v), max(u, v)) in path_edges]
    nx.draw_networkx_edges(G, POSITIONS, edgelist=path_el, ax=ax,
                           edge_color="#2B6CB0", width=2.5, alpha=0.85)

    # Nodes colored by distance bucket
    max_dist = max(d for d in dist.values() if d != float('inf'))
    node_colors = []
    for v in G.nodes():
        if v == 0:
            node_colors.append("#E53E3E")
        else:
            frac = dist.get(v, max_dist) / max_dist
            g_val = int(108 + (1 - frac) * 100)
            node_colors.append(f"#2B{g_val:02X}B0")

    # (nodes drawn inside fig4 with offsets below)

    nx.draw_networkx_nodes(G, POSITIONS, ax=ax, node_color=node_colors,
                           node_size=700, alpha=0.95)

    # Name above node
    label_pos = {v: (x, y + 0.35) for v, (x, y) in POSITIONS.items()}
    nx.draw_networkx_labels(G, label_pos,
                            labels={v: SHORT_NAMES[v] for v in G.nodes()},
                            ax=ax, font_size=6.5, font_color="#1A202C", font_weight="bold")

    # Distance below node
    dist_pos = {v: (x, y - 0.45) for v, (x, y) in POSITIONS.items()}
    dist_labels = {v: f"{dist[v]}mi" if v != 0 else "source" for v in G.nodes()}
    nx.draw_networkx_labels(G, dist_pos, labels=dist_labels, ax=ax,
                            font_size=6.0, font_color="#C53030", font_weight="bold")

    ax.set_title("Dijkstra Shortest Paths from Downtown Tampa\n"
                 "Blue edges = shortest path tree. Node labels show driving distance.",
                 fontsize=11, fontweight="bold", pad=10)
    ax.axis("off")

    src_patch = mpatches.Patch(color="#E53E3E", label="Source: Downtown Tampa")
    path_patch = mpatches.Patch(color="#2B6CB0", label="Shortest path tree edges")
    ax.legend(handles=[src_patch, path_patch], loc="lower left",
              fontsize=8, framealpha=0.85, edgecolor="#CCCCCC")

    plt.tight_layout()
    plt.savefig("fig4_dijkstra.png", dpi=150, bbox_inches="tight",
                facecolor=fig.get_facecolor())
    plt.close()
    print("  Saved: fig4_dijkstra.png")


# ─────────────────────────────────────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\nGenerating Tampa graph visualizations...")
    fig1_full_network()
    fig2_mst()
    fig3_traversals()
    fig4_dijkstra()
    print("\nAll figures saved. Include them in your report and presentation.")
    print("  fig1_tampa_network.png  - Full road network (use in Section 3 / 4 of report)")
    print("  fig2_mst.png            - MST comparison (use in Section 5.4)")
    print("  fig3_bfs_dfs.png        - BFS vs DFS traversal (use in Section 5.1 / 5.2)")
    print("  fig4_dijkstra.png       - Dijkstra shortest paths (use in Section 5.3)")
