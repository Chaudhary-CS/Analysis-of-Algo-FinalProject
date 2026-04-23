"""
Graph Algorithms in Network Optimization
Course: Analysis of Algorithms, Final Project

Team: Kartik Chaudhary, Askat Mendybaev, Devon Gardner
City: Tampa, Florida

Our thought process:
We are all in Tampa, so Kartik suggested modeling the city we actually live in.
Every location we picked is somewhere we have been to, which made it easy to
sanity-check edge weights. If the shortest path from Downtown to USF came out
to 2 miles we would know immediately something was wrong.

We mapped out 20 real Tampa landmarks and connected them based on how roads
actually run in the city (I-275, Dale Mabry, Hillsborough Ave, the Selmon
Expressway). Askat verified the approximate mile distances using Google Maps.

Devon pointed out this also makes the MST result meaningful. Kruskal's MST
tells us the minimum total road miles needed to connect all 20 Tampa locations,
which mirrors the kind of question a city planner or FDOT would actually ask.

Edge weights = road distance in miles (approximate driving distance).
Graph type: Weighted, Undirected.
"""


class Graph:
    """
    Adjacency-list representation of a weighted undirected graph.

    We chose adjacency list over adjacency matrix because our city graph
    is sparse — not every location has a direct road to every other location.
    Adjacency list gives us O(V + E) space vs O(V^2) for matrix, which matters
    when V is large and edges are few.
    """

    def __init__(self, num_vertices: int):
        self.V = num_vertices
        self.adj: dict[int, list[tuple[int, int]]] = {i: [] for i in range(num_vertices)}
        self.edges: list[tuple[int, int, int]] = []   # (weight, u, v) for Kruskal
        self.vertex_names: dict[int, str] = {}

    def add_vertex_name(self, v: int, name: str):
        self.vertex_names[v] = name

    def add_edge(self, u: int, v: int, weight: int):
        """Add an undirected weighted edge between u and v."""
        self.adj[u].append((v, weight))
        self.adj[v].append((u, weight))
        self.edges.append((weight, u, v))

    def get_name(self, v: int) -> str:
        return self.vertex_names.get(v, str(v))

    def print_graph(self):
        print("\n=== Tampa Road Network (Adjacency List) ===")
        for v in range(self.V):
            neighbors = [(self.get_name(u), f"{w}mi") for u, w in self.adj[v]]
            print(f"  [{v:2}] {self.get_name(v):<28}: {neighbors}")
        print(f"\n  Vertices: {self.V}  |  Edges: {len(self.edges)}")


def build_city_network() -> Graph:
    """
    Our 20-node Tampa road network dataset.

    Kartik, Askat, and Devon all live/study in Tampa so we used real locations
    and approximate Google Maps driving distances (in miles). We traced routes
    along actual Tampa roads — I-275, Dale Mabry Hwy, Hillsborough Ave,
    the Selmon Expressway, Bruce B Downs Blvd — not straight-line distances.

    Askat verified every edge weight against Google Maps and flagged anything
    that looked wrong. Devon drew the graph on paper first to make sure it
    was fully connected before we coded it up.

    Vertices (Tampa locations):
        0  Downtown Tampa          1  Tampa Intl Airport (TPA)
        2  USF (Univ. of S. Fla.) 3  Tampa General Hospital
        4  International Plaza     5  Riverwalk / Curtis Hixon
        6  Ybor City               7  John Germany Public Library
        8  Raymond James Stadium   9  Tampa Museum of Art
       10  Port of Tampa Bay      11  Westshore District
       12  New Tampa              13  South Tampa
       14  Brandon                15  Westchase
       16  Channelside            17  Tampa Convention Center
       18  Seminole Heights       19  Hyde Park Village
    """
    locations = [
        "Downtown Tampa",        # 0  — central hub, Channelside Dr / Ashley Dr
        "Tampa Intl Airport",    # 1  — TPA, off I-275 North
        "USF",                   # 2  — University of South Florida, Bruce B Downs
        "Tampa General Hosp.",   # 3  — Davis Islands, close to downtown
        "International Plaza",   # 4  — Bay St, near airport
        "Riverwalk",             # 5  — Curtis Hixon Waterfront Park
        "Ybor City",             # 6  — Historic District, E 7th Ave
        "John Germany Library",  # 7  — 900 N Ashley Dr
        "Raymond James Stadium", # 8  — Dale Mabry Hwy
        "Tampa Museum of Art",   # 9  — N Ashley Dr, downtown waterfront
        "Port of Tampa Bay",     # 10 — Garrison Channel
        "Westshore District",    # 11 — Business/commercial hub near airport
        "New Tampa",             # 12 — Bruce B Downs / I-75 north
        "South Tampa",           # 13 — Bayshore Blvd area
        "Brandon",               # 14 — Suburbs east via I-75/Crosstown
        "Westchase",             # 15 — Suburbs west, Linebaugh Ave
        "Channelside",           # 16 — Waterfront, next to downtown
        "Tampa Convention Ctr",  # 17 — S Franklin St, waterfront
        "Seminole Heights",      # 18 — N Florida Ave, hip neighborhood
        "Hyde Park Village",     # 19 — S Dakota Ave, walkable shops
    ]

    g = Graph(20)
    for i, name in enumerate(locations):
        g.add_vertex_name(i, name)

    # (u, v, distance_miles)
    # All distances are approximate driving miles along real Tampa roads.
    # We used Google Maps to verify each one — Askat spot-checked every edge.
    road_edges = [
        # Downtown Tampa (0) — central hub with spokes to nearby areas
        (0, 17, 1),   # Downtown → Convention Center (S Franklin St, 5 min walk)
        (0, 16, 1),   # Downtown → Channelside (same waterfront strip)
        (0, 9,  1),   # Downtown → Museum of Art (N Ashley Dr)
        (0, 6,  2),   # Downtown → Ybor City (I-4 East, 5 min)
        (0, 18, 3),   # Downtown → Seminole Heights (N Florida Ave)
        (0, 3,  3),   # Downtown → Tampa General (Davis Islands Blvd)
        (0, 5,  1),   # Downtown → Riverwalk (literally the same waterfront)

        # Tampa International Airport (1) — near Westshore, accessible from I-275
        (1, 11, 3),   # Airport → Westshore District (George J Bean Pkwy)
        (1, 4,  2),   # Airport → International Plaza (Westshore Blvd, 5 min)
        (1, 15, 9),   # Airport → Westchase (Linebaugh Ave west)

        # USF (2) — north end of Tampa, Bruce B Downs
        (2, 12, 8),   # USF → New Tampa (Bruce B Downs north)
        (2, 18, 5),   # USF → Seminole Heights (N Florida Ave / Fowler)
        (2, 7,  4),   # USF → John Germany Library (I-275 south)

        # Tampa General Hospital (3) — Davis Islands, close to South Tampa
        (3, 13, 3),   # Tampa General → South Tampa (Bayshore Blvd)
        (3, 19, 2),   # Tampa General → Hyde Park Village (Rome Ave)

        # International Plaza (4) — Bay St, Westshore area
        (4, 11, 2),   # International Plaza → Westshore (walking distance)
        (4, 8,  4),   # International Plaza → Raymond James Stadium (Dale Mabry)

        # Riverwalk (5) — Curtis Hixon, basically downtown
        (5, 9,  1),   # Riverwalk → Museum of Art (same block)
        (5, 19, 2),   # Riverwalk → Hyde Park Village (Bayshore)

        # Ybor City (6) — E 7th Ave, historic district
        (6, 10, 2),   # Ybor City → Port of Tampa (Adamo Dr / Channelside Dr)
        (6, 18, 3),   # Ybor City → Seminole Heights (N 22nd St)

        # John Germany Library (7) — N Ashley Dr, near downtown
        (7, 9,  2),   # Library → Museum of Art (N Ashley Dr, same stretch)
        (7, 17, 2),   # Library → Convention Center (S Ashley Dr south)
        (7, 18, 5),   # Library → Seminole Heights (N Florida Ave)

        # Raymond James Stadium (8) — Dale Mabry, Westshore
        (0, 8,  4),   # Downtown → Raymond James Stadium (Dale Mabry Hwy, ~4 mi south)
        (8, 11, 3),   # Stadium → Westshore District (Dale Mabry / Cypress)
        (8, 15, 8),   # Stadium → Westchase (Hillsborough Ave west)

        # Tampa Museum of Art (9) — downtown waterfront
        (9, 17, 1),   # Museum → Convention Center (S Franklin St)

        # Port of Tampa Bay (10) — Garrison Channel / Channelside
        (10, 16, 2),  # Port → Channelside (Channelside Dr)
        (10, 17, 2),  # Port → Convention Center (S Franklin / Garrison)

        # Westshore District (11) — I-275 / Cypress St
        (11, 15, 10), # Westshore → Westchase (Hillsborough Ave west)

        # New Tampa (12) — Bruce B Downs / I-75 north suburbs
        (12, 14, 18), # New Tampa → Brandon (I-75 south to I-4 east)
        (12, 15, 18), # New Tampa → Westchase (Gunn Hwy / Van Dyke Rd)

        # South Tampa (13) — Bayshore Blvd area
        (13, 19, 2),  # South Tampa → Hyde Park Village (S Dakota Ave)
        (13, 14, 15), # South Tampa → Brandon (Selmon Expressway)

        # Brandon (14) — east suburbs, I-75 / Crosstown
        (14, 15, 22), # Brandon → Westchase (I-4 to I-275 north, Hillsborough)

        # Channelside (16) — waterfront, east of downtown
        (16, 17, 1),  # Channelside → Convention Center (S Franklin St)
    ]

    for u, v, w in road_edges:
        g.add_edge(u, v, w)

    return g


def build_synthetic_graph(num_vertices: int, density: float = 0.3, seed: int = 42) -> Graph:
    """
    Generate a synthetic graph for experimental analysis.

    We use this to test our algorithms at different sizes (small=10, large=50)
    and different densities (sparse=0.15, dense=0.6).

    density: probability that any two vertices share an edge.
    Weights are pseudo-random integers between 1 and 50.
    """
    import random
    random.seed(seed)

    g = Graph(num_vertices)
    for i in range(num_vertices):
        g.add_vertex_name(i, f"Node_{i}")

    # Guarantee connectivity first: build a random spanning tree
    vertices = list(range(num_vertices))
    random.shuffle(vertices)
    for i in range(1, num_vertices):
        u = vertices[i - 1]
        v = vertices[i]
        w = random.randint(1, 50)
        g.add_edge(u, v, w)

    # Then add extra edges based on density
    existing = {(min(u, v), max(u, v)) for _, u, v in g.edges}
    for u in range(num_vertices):
        for v in range(u + 1, num_vertices):
            if (u, v) not in existing and random.random() < density:
                w = random.randint(1, 50)
                g.add_edge(u, v, w)
                existing.add((u, v))

    return g
