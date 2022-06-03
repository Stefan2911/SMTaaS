import itertools
import random

vertices = [1, 2, 3, 4, 5, 6, 7, 8, 9]
direct_connections = {
    1: [2, 4],
    2: [1, 3, 5],
    3: [2, 6],
    4: [1, 5, 7],
    5: [2, 4, 6, 8],
    6: [3, 5, 9],
    7: [4, 8],
    8: [5, 7, 9],
    9: [6, 8]
}
connection_costs = {
    1: [0, 1, 2, 1, 2, 3, 2, 3, 4],
    2: [1, 0, 1, 2, 1, 2, 3, 2, 3],
    3: [2, 1, 0, 3, 2, 1, 4, 3, 2],
    4: [1, 2, 3, 0, 1, 2, 1, 2, 3],
    5: [2, 1, 2, 1, 0, 1, 2, 1, 2],
    6: [3, 2, 1, 2, 1, 0, 3, 2, 1],
    7: [2, 3, 4, 1, 2, 3, 0, 1, 2],
    8: [3, 2, 3, 2, 1, 2, 1, 0, 1],
    9: [4, 3, 2, 3, 2, 1, 2, 1, 0]
}
cost_of_all_connections = 1


def calculate_costs(start, v1, v2, v3):
    return connection_costs.get(start)[v1 - 1] \
           + connection_costs.get(v1)[v2 - 1] \
           + connection_costs.get(v2)[v3 - 1] \
           + connection_costs.get(v3)[start - 1]


def is_minimum_distance(start, destinations, minimum):
    # start - g1 - g2 - g3 - start
    # start - g1 - g3 - g2 - start
    # start - g2 - g1 - g3 - start
    # start - g2 - g3 - g1 - start
    # start - g3 - g1 - g2 - start
    # start - g3 - g2 - g1 - start
    for permutation in itertools.permutations([destinations[0], destinations[1], destinations[2]]):
        if calculate_costs(start, permutation[0], permutation[1], permutation[2]) <= minimum:
            return permutation
    return None


min_distance = 4
max_distance = 8


def find_shortest_path(start, destinations):
    min = min_distance
    while min <= max_distance:
        shortest_path = is_minimum_distance(start, destinations, min)

        if shortest_path is not None:
            return shortest_path
        min = min + 1
    return None


def create_shortest_path_problem():
    sample = random.sample(vertices, 3)
    print("stops: ", sample)
    print("shortest path: ", find_shortest_path(1, sample))


create_shortest_path_problem()
