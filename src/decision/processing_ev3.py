from enum import Enum

import src.decision.heuristic.decision_making
import src.decision.reinforcement_learning.q_learning.decision_making


class DecisionMode(Enum):
    heuristic = 0
    q_learning = 1


def process(smt_problem, decision_mode=DecisionMode.q_learning):
    if decision_mode == DecisionMode.heuristic:
        return src.decision.heuristic.decision_making.process(smt_problem)
    else:
        return src.decision.reinforcement_learning.q_learning.decision_making.process(smt_problem)
