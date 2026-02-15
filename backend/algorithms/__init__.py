from algorithms.bfs import run_bfs
from algorithms.dfs import run_dfs
from algorithms.dijkstra import run_dijkstra
from algorithms.bellman_ford import run_bellman_ford

ALGORITHMS = {
    "bfs": run_bfs,
    "dfs": run_dfs,
    "dijkstra": run_dijkstra,
    "bellman_ford": run_bellman_ford,
}
