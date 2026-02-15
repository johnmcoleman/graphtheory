# Graph Theory Visualizer

An interactive web app for visualizing graph theory algorithms. Built with FastAPI + Vue.js 3 + Cytoscape.js.

## Features

- **Interactive Graph Editor** — Click to add nodes and edges, set weights, toggle directed mode
- **Algorithm Visualization** — Step-by-step animated playback of graph algorithms
- **Guided Tutorials** — Learn BFS, DFS, Dijkstra's, and Bellman-Ford with curated examples
- **Preset Graphs** — Famous graphs (Petersen, K₃,₃) and tutorial-ready examples
- **Save & Share** — Save graphs to the database and share via unique URLs

## Algorithms

| Algorithm | Category | Weights | Description |
|-----------|----------|---------|-------------|
| BFS | Traversal | No | Breadth-first exploration using a queue |
| DFS | Traversal | No | Depth-first exploration using a stack |
| Dijkstra | Shortest Path | Non-negative | Greedy shortest path with priority queue |
| Bellman-Ford | Shortest Path | Any (detects negative cycles) | V-1 rounds of edge relaxation |

## Tech Stack

- **Backend**: Python, FastAPI, SQLAlchemy, SQLite
- **Frontend**: Vue.js 3 (Composition API), Vite, Pinia, Cytoscape.js
- **Database**: SQLite (file-based, zero config)

## Getting Started

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

The API runs at `http://localhost:8000`. API docs at `http://localhost:8000/docs`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The dev server runs at `http://localhost:5173` and proxies API requests to the backend.

### Production Build

```bash
cd frontend
npm run build
# The FastAPI app serves the built frontend from frontend/dist/
cd ../backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Project Structure

```
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── database.py          # SQLAlchemy setup
│   ├── models.py            # Database models
│   ├── schemas.py           # Pydantic schemas
│   ├── algorithms/          # Algorithm implementations
│   │   ├── bfs.py
│   │   ├── dfs.py
│   │   ├── dijkstra.py
│   │   └── bellman_ford.py
│   └── routers/             # API routes
│       ├── graphs.py        # CRUD for saved graphs
│       ├── algorithms.py    # Algorithm execution
│       └── presets.py       # Preset graphs & tutorials
├── frontend/
│   ├── src/
│   │   ├── components/      # Vue components
│   │   ├── views/           # Page views
│   │   ├── stores/          # Pinia state management
│   │   ├── api/             # API client
│   │   └── router/          # Vue Router config
│   └── ...
└── README.md
```
