import os
import re

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


def solve_hamiltonian(graph, decision_mode):
    temp = open("temp.smt2", "w+t")
    try:
        fill_temporary_file(graph, temp)
        temp.close()
        result = process(temp.name, decision_mode)
        nodes_as_strings = re.findall("v\d+", result)
        order_as_strings = re.findall(" \d+", result)
        nodes = [0] * len(nodes_as_strings)
        for i in range(len(order_as_strings)):
            nodes[int(order_as_strings[i])] = int(nodes_as_strings[i][1:])
        return nodes
    finally:
        os.remove(temp.name)
