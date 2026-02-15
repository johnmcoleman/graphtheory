from fastapi import APIRouter

router = APIRouter(prefix="/api/presets", tags=["presets"])

PRESET_GRAPHS = [
    {
        "id": "simple_unweighted",
        "name": "Simple Graph",
        "description": "A basic 6-node undirected graph. Great for learning BFS and DFS.",
        "category": "tutorial",
        "graph_data": {
            "nodes": [
                {"id": "A", "label": "A", "x": 100, "y": 200},
                {"id": "B", "label": "B", "x": 250, "y": 100},
                {"id": "C", "label": "C", "x": 250, "y": 300},
                {"id": "D", "label": "D", "x": 400, "y": 100},
                {"id": "E", "label": "E", "x": 400, "y": 300},
                {"id": "F", "label": "F", "x": 550, "y": 200},
            ],
            "edges": [
                {"id": "e1", "source": "A", "target": "B", "weight": 1},
                {"id": "e2", "source": "A", "target": "C", "weight": 1},
                {"id": "e3", "source": "B", "target": "D", "weight": 1},
                {"id": "e4", "source": "C", "target": "E", "weight": 1},
                {"id": "e5", "source": "D", "target": "F", "weight": 1},
                {"id": "e6", "source": "E", "target": "F", "weight": 1},
                {"id": "e7", "source": "B", "target": "E", "weight": 1},
            ],
        },
    },
    {
        "id": "weighted_graph",
        "name": "Weighted Road Network",
        "description": "A weighted graph representing a small road network. Perfect for Dijkstra's algorithm.",
        "category": "tutorial",
        "graph_data": {
            "nodes": [
                {"id": "S", "label": "S (Start)", "x": 50, "y": 200},
                {"id": "A", "label": "A", "x": 200, "y": 80},
                {"id": "B", "label": "B", "x": 200, "y": 320},
                {"id": "C", "label": "C", "x": 380, "y": 80},
                {"id": "D", "label": "D", "x": 380, "y": 320},
                {"id": "T", "label": "T (End)", "x": 530, "y": 200},
            ],
            "edges": [
                {"id": "e1", "source": "S", "target": "A", "weight": 4},
                {"id": "e2", "source": "S", "target": "B", "weight": 2},
                {"id": "e3", "source": "A", "target": "C", "weight": 5},
                {"id": "e4", "source": "A", "target": "D", "weight": 10},
                {"id": "e5", "source": "B", "target": "A", "weight": 1},
                {"id": "e6", "source": "B", "target": "D", "weight": 8},
                {"id": "e7", "source": "C", "target": "T", "weight": 3},
                {"id": "e8", "source": "D", "target": "T", "weight": 2},
                {"id": "e9", "source": "D", "target": "C", "weight": 1},
            ],
        },
    },
    {
        "id": "negative_weights",
        "name": "Graph with Negative Weights",
        "description": "A directed graph with negative edge weights (but no negative cycle). Ideal for Bellman-Ford.",
        "category": "tutorial",
        "graph_data": {
            "nodes": [
                {"id": "S", "label": "S", "x": 50, "y": 200},
                {"id": "A", "label": "A", "x": 200, "y": 80},
                {"id": "B", "label": "B", "x": 200, "y": 320},
                {"id": "C", "label": "C", "x": 380, "y": 80},
                {"id": "D", "label": "D", "x": 380, "y": 320},
                {"id": "T", "label": "T", "x": 530, "y": 200},
            ],
            "edges": [
                {"id": "e1", "source": "S", "target": "A", "weight": 6, "directed": True},
                {"id": "e2", "source": "S", "target": "B", "weight": 7, "directed": True},
                {"id": "e3", "source": "A", "target": "C", "weight": 5, "directed": True},
                {"id": "e4", "source": "A", "target": "B", "weight": -4, "directed": True},
                {"id": "e5", "source": "B", "target": "D", "weight": -3, "directed": True},
                {"id": "e6", "source": "C", "target": "T", "weight": -2, "directed": True},
                {"id": "e7", "source": "D", "target": "C", "weight": 4, "directed": True},
                {"id": "e8", "source": "D", "target": "T", "weight": 2, "directed": True},
            ],
        },
    },
    {
        "id": "binary_tree",
        "name": "Binary Tree",
        "description": "A complete binary tree with 4 levels. Compare how BFS and DFS traverse it differently!",
        "category": "tutorial",
        "graph_data": {
            "nodes": [
                {"id": "1", "label": "1", "x": 350, "y": 50},
                {"id": "2", "label": "2", "x": 200, "y": 150},
                {"id": "3", "label": "3", "x": 500, "y": 150},
                {"id": "4", "label": "4", "x": 125, "y": 250},
                {"id": "5", "label": "5", "x": 275, "y": 250},
                {"id": "6", "label": "6", "x": 425, "y": 250},
                {"id": "7", "label": "7", "x": 575, "y": 250},
                {"id": "8", "label": "8", "x": 80, "y": 350},
                {"id": "9", "label": "9", "x": 170, "y": 350},
                {"id": "10", "label": "10", "x": 230, "y": 350},
                {"id": "11", "label": "11", "x": 320, "y": 350},
                {"id": "12", "label": "12", "x": 380, "y": 350},
                {"id": "13", "label": "13", "x": 470, "y": 350},
                {"id": "14", "label": "14", "x": 530, "y": 350},
                {"id": "15", "label": "15", "x": 620, "y": 350},
            ],
            "edges": [
                {"id": "e1", "source": "1", "target": "2", "weight": 1},
                {"id": "e2", "source": "1", "target": "3", "weight": 1},
                {"id": "e3", "source": "2", "target": "4", "weight": 1},
                {"id": "e4", "source": "2", "target": "5", "weight": 1},
                {"id": "e5", "source": "3", "target": "6", "weight": 1},
                {"id": "e6", "source": "3", "target": "7", "weight": 1},
                {"id": "e7", "source": "4", "target": "8", "weight": 1},
                {"id": "e8", "source": "4", "target": "9", "weight": 1},
                {"id": "e9", "source": "5", "target": "10", "weight": 1},
                {"id": "e10", "source": "5", "target": "11", "weight": 1},
                {"id": "e11", "source": "6", "target": "12", "weight": 1},
                {"id": "e12", "source": "6", "target": "13", "weight": 1},
                {"id": "e13", "source": "7", "target": "14", "weight": 1},
                {"id": "e14", "source": "7", "target": "15", "weight": 1},
            ],
        },
    },
    {
        "id": "petersen",
        "name": "Petersen Graph",
        "description": "The famous Petersen graph — a classic example in graph theory. It's 3-regular, has 10 vertices and 15 edges, and is not planar.",
        "category": "famous",
        "graph_data": {
            "nodes": [
                {"id": "0", "label": "0", "x": 300, "y": 30},
                {"id": "1", "label": "1", "x": 557, "y": 217},
                {"id": "2", "label": "2", "x": 458, "y": 470},
                {"id": "3", "label": "3", "x": 142, "y": 470},
                {"id": "4", "label": "4", "x": 43, "y": 217},
                {"id": "5", "label": "5", "x": 300, "y": 130},
                {"id": "6", "label": "6", "x": 453, "y": 243},
                {"id": "7", "label": "7", "x": 393, "y": 393},
                {"id": "8", "label": "8", "x": 207, "y": 393},
                {"id": "9", "label": "9", "x": 147, "y": 243},
            ],
            "edges": [
                {"id": "e1", "source": "0", "target": "1", "weight": 1},
                {"id": "e2", "source": "1", "target": "2", "weight": 1},
                {"id": "e3", "source": "2", "target": "3", "weight": 1},
                {"id": "e4", "source": "3", "target": "4", "weight": 1},
                {"id": "e5", "source": "4", "target": "0", "weight": 1},
                {"id": "e6", "source": "0", "target": "5", "weight": 1},
                {"id": "e7", "source": "1", "target": "6", "weight": 1},
                {"id": "e8", "source": "2", "target": "7", "weight": 1},
                {"id": "e9", "source": "3", "target": "8", "weight": 1},
                {"id": "e10", "source": "4", "target": "9", "weight": 1},
                {"id": "e11", "source": "5", "target": "7", "weight": 1},
                {"id": "e12", "source": "5", "target": "8", "weight": 1},
                {"id": "e13", "source": "6", "target": "8", "weight": 1},
                {"id": "e14", "source": "6", "target": "9", "weight": 1},
                {"id": "e15", "source": "7", "target": "9", "weight": 1},
            ],
        },
    },
    {
        "id": "k33",
        "name": "Complete Bipartite K₃,₃",
        "description": "The complete bipartite graph K₃,₃. By Kuratowski's theorem, a graph is planar if and only if it doesn't contain K₅ or K₃,₃ as a subdivision.",
        "category": "famous",
        "graph_data": {
            "nodes": [
                {"id": "A1", "label": "A₁", "x": 150, "y": 100},
                {"id": "A2", "label": "A₂", "x": 300, "y": 100},
                {"id": "A3", "label": "A₃", "x": 450, "y": 100},
                {"id": "B1", "label": "B₁", "x": 150, "y": 350},
                {"id": "B2", "label": "B₂", "x": 300, "y": 350},
                {"id": "B3", "label": "B₃", "x": 450, "y": 350},
            ],
            "edges": [
                {"id": "e1", "source": "A1", "target": "B1", "weight": 1},
                {"id": "e2", "source": "A1", "target": "B2", "weight": 1},
                {"id": "e3", "source": "A1", "target": "B3", "weight": 1},
                {"id": "e4", "source": "A2", "target": "B1", "weight": 1},
                {"id": "e5", "source": "A2", "target": "B2", "weight": 1},
                {"id": "e6", "source": "A2", "target": "B3", "weight": 1},
                {"id": "e7", "source": "A3", "target": "B1", "weight": 1},
                {"id": "e8", "source": "A3", "target": "B2", "weight": 1},
                {"id": "e9", "source": "A3", "target": "B3", "weight": 1},
            ],
        },
    },
]

TUTORIALS = [
    {
        "id": "bfs_intro",
        "title": "Breadth-First Search (BFS)",
        "algorithm": "bfs",
        "preset_id": "simple_unweighted",
        "start_node": "A",
        "end_node": "F",
        "directed": False,
        "description": """**Breadth-First Search** explores a graph level by level, visiting all neighbors of a node before moving deeper.

**Key Properties:**
- Uses a **queue** (FIFO) data structure
- Finds the **shortest path** in unweighted graphs
- Time complexity: **O(V + E)**
- Space complexity: **O(V)**

**How it works:**
1. Start at the source node, add it to the queue
2. Dequeue a node, mark it as visited
3. Add all unvisited neighbors to the queue
4. Repeat until the queue is empty or target is found

Watch the animation to see BFS explore from node A to node F!""",
    },
    {
        "id": "dfs_intro",
        "title": "Depth-First Search (DFS)",
        "algorithm": "dfs",
        "preset_id": "simple_unweighted",
        "start_node": "A",
        "end_node": "F",
        "directed": False,
        "description": """**Depth-First Search** explores as far as possible along each branch before backtracking.

**Key Properties:**
- Uses a **stack** (LIFO) data structure (or recursion)
- Does NOT guarantee the shortest path
- Time complexity: **O(V + E)**
- Space complexity: **O(V)**

**How it works:**
1. Start at the source node, push it onto the stack
2. Pop a node, mark it as visited
3. Push all unvisited neighbors onto the stack
4. Repeat until the stack is empty or target is found

Compare with BFS — notice how DFS goes deep before going wide!""",
    },
    {
        "id": "dijkstra_intro",
        "title": "Dijkstra's Shortest Path",
        "algorithm": "dijkstra",
        "preset_id": "weighted_graph",
        "start_node": "S",
        "end_node": "T",
        "directed": False,
        "description": """**Dijkstra's Algorithm** finds the shortest path from a source to all other nodes in a weighted graph.

**Key Properties:**
- Uses a **priority queue** (min-heap)
- Works only with **non-negative** edge weights
- Time complexity: **O((V + E) log V)** with a binary heap
- Greedy approach: always processes the closest unvisited node

**How it works:**
1. Set distance to source = 0, all others = infinity
2. Extract the node with minimum distance
3. For each neighbor, check if going through this node gives a shorter path (relaxation)
4. If so, update the distance and predecessor
5. Repeat until all nodes are processed

Watch how Dijkstra finds the shortest path from S to T in this road network!""",
    },
    {
        "id": "bellman_ford_intro",
        "title": "Bellman-Ford Algorithm",
        "algorithm": "bellman_ford",
        "preset_id": "negative_weights",
        "start_node": "S",
        "end_node": "T",
        "directed": True,
        "description": """**Bellman-Ford** finds shortest paths even with **negative edge weights**, and can detect negative cycles.

**Key Properties:**
- Handles **negative weights** (unlike Dijkstra)
- Can detect **negative cycles**
- Time complexity: **O(V × E)**
- Performs V-1 rounds of edge relaxation

**How it works:**
1. Set distance to source = 0, all others = infinity
2. For V-1 rounds, relax ALL edges: if dist[u] + weight(u,v) < dist[v], update dist[v]
3. After V-1 rounds, check all edges once more — if any can still be relaxed, there's a negative cycle

This graph has negative edge weights. Watch how Bellman-Ford handles them!""",
    },
]


@router.get("/graphs")
def get_preset_graphs():
    return {"presets": PRESET_GRAPHS}


@router.get("/tutorials")
def get_tutorials():
    return {"tutorials": TUTORIALS}


@router.get("/graphs/{preset_id}")
def get_preset_graph(preset_id: str):
    for preset in PRESET_GRAPHS:
        if preset["id"] == preset_id:
            return preset
    return {"error": "Preset not found"}
