from enum import Enum

import src.decision.reinforcement_learning.deep_q_network.decision_making
import src.decision.reinforcement_learning.q_learning.decision_making


class DecisionMode(Enum):
    q_learning = 1
    deep_q_network = 2


def process(smt_problem, decision_mode=DecisionMode.q_learning):
    if decision_mode == DecisionMode.deep_q_network:
        return src.decision.reinforcement_learning.deep_q_network.decision_making.process(smt_problem)
    else:
        return src.decision.reinforcement_learning.q_learning.decision_making.process(smt_problem)
