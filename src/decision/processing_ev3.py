import logging
import time
from enum import Enum

import src.decision.heuristic.decision_making
import src.decision.reinforcement_learning.q_learning.decision_making
from src.config.config import Config

config = Config()

logging.basicConfig()
logger = logging.getLogger('main')
logger.setLevel(level=config.get_logging_level())


class DecisionMode(Enum):
    heuristic = 0
    q_learning = 1


def process(smt_problem, decision_mode=DecisionMode.q_learning):
    start_process_time = time.time()
    if decision_mode == DecisionMode.heuristic:
        result = src.decision.heuristic.decision_making.process(smt_problem)
    else:
        result = src.decision.reinforcement_learning.q_learning.decision_making.process(smt_problem)
    end_process_time = time.time()
    logger.debug('needed time for processing (in s): %s', end_process_time - start_process_time)
    return result
