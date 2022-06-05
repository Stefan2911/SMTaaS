import src.decision.reinforcement_learning.deep_q_network.decision_making
import src.decision.reinforcement_learning.q_learning.decision_making
from src.decision.decision_mode import DecisionMode
from src.smt.smt_solver.native.solver import call_solver


def process(smt_problem, decision_mode):
    if decision_mode == DecisionMode.deep_q_network:
        return src.decision.reinforcement_learning.deep_q_network.decision_making.process(smt_problem)
    elif decision_mode == DecisionMode.q_learning:
        return src.decision.reinforcement_learning.q_learning.decision_making.process(smt_problem)
    else:
        return call_solver(smt_problem)
