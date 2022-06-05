import os
import re
import tempfile

from src.decision.decision_mode import DecisionMode
from src.decision.processing_ev3 import process


# Input a graph as an adjacency list, e.g. {0:[1,2], 1:[2], 2:[1,0]}.
def fill_temporary_file(graph, temp_file):
    temp_file.writelines("(set-option :produce-models true)\n")
    temp_file.writelines("(set-logic QF_LIA)\n")
    number_of_vertices = len(graph)
    for i in range(number_of_vertices):
        declaration = "(declare-const v" + str(i) + " Int)\n"
        temp_file.writelines(declaration)
    temp_file.write("(assert (= v0 0))\n")
    for i in range(number_of_vertices):
        or_conditions = ""
        for j in graph.get(i):
            or_conditions = or_conditions + "(= v" + str(j) + " (mod (+ v" + str(i) + " 1) " + str(
                number_of_vertices) + "))"
        if or_conditions != "":
            or_assert = "(assert (or" + or_conditions + "))\n"
            temp_file.writelines(or_assert)
    temp_file.writelines("(check-sat)\n")
    temp_file.writelines("(get-model)\n")


graph = {
    0: [1, 4, 5],
    1: [0, 7, 2],
    2: [1, 9, 3],
    3: [2, 11, 4],
    4: [3, 13, 0],
    5: [0, 14, 6],
    6: [5, 16, 7],
    7: [6, 8, 1],
    8: [7, 17, 9],
    9: [8, 10, 2],
    10: [9, 18, 11],
    11: [10, 3, 12],
    12: [11, 19, 13],
    13: [12, 14, 4],
    14: [13, 15, 5],
    15: [14, 16, 19],
    16: [6, 17, 15],
    17: [16, 8, 18],
    18: [10, 19, 17],
    19: [18, 12, 15]
}

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


def solve_hamiltonian(graph_simple):
    temp = tempfile.TemporaryFile(mode="w+t", delete=False)
    try:
        fill_temporary_file(graph_simple, temp)
        temp.close()
        # result = subprocess.run(["C:\\Users\\Acer\\Desktop\\cvc4.exe", temp.name, '--lang', 'smtlib'], check=True,
        #                         stdout=subprocess.PIPE, universal_newlines=True).stdout
        result = process(temp.name, decision_mode=DecisionMode.q_learning)
        nodes_as_strings = re.findall("v\d+", result)
        order_as_strings = re.findall(" \d+", result)
        nodes = [0] * len(nodes_as_strings)
        for i in range(len(order_as_strings)):
            nodes[int(order_as_strings[i])] = int(nodes_as_strings[i][1:])
        print(nodes)
    finally:
        os.remove(temp.name)

# solve_hamiltonian(graph_simple)
