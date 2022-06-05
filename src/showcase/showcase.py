from src.showcase.grid_moving import move_with_stops
from src.showcase.hamiltonian_with_smt_lib import solve_hamiltonian

graph_simple = {
    0: [1, 3],
    1: [0, 2, 4],
    2: [1, 5],
    3: [0, 4, 6],
    4: [1, 3, 5, 7],
    5: [2, 4],
    6: [3, 7],
    7: [4, 6]
}

move_with_stops(solve_hamiltonian(graph_simple))
