import time

from src.decision.decision_mode import DecisionMode
from src.showcase.grid_moving import move_with_stops
from src.showcase.hamiltonian_with_smt_lib import solve_hamiltonian

graph_usecase = {
    0: [1, 4],
    1: [0, 2, 5],
    2: [1, 3, 6],
    3: [2, 7],
    4: [0, 5, 8],
    5: [1, 4, 6, 9],
    6: [2, 5, 7, 10],
    7: [3, 6, 11],
    8: [4, 9, 12],
    9: [5, 8, 10, 13],
    10: [6, 9, 11, 14],
    11: [7, 10, 15],
    12: [8, 13],
    13: [9, 12, 14],
    14: [10, 13, 15],
    15: [11, 14]
}

graph_usecase_simple = {
    0: [1, 3],
    1: [0, 2, 4],
    2: [1, 5],
    3: [0, 4, 6],
    4: [1, 3, 5, 7],
    5: [2, 4],
    6: [3, 7],
    7: [4, 6]
}

print('start')
start_time = time.time()
move_with_stops(solve_hamiltonian(graph_usecase_simple, decision_mode=DecisionMode.q_learning))
end_time = time.time()
print(end_time - start_time)
