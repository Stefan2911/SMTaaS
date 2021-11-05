import logging
import time
from datetime import timedelta

from timeloop import Timeloop
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from src.communication.rest.client import Client
from src.decision.heuristic.decision_making import get_current_decision_value
from src.ev3.config.config import Config
from src.ev3.smt.solver import call_solver

config = Config()

logging.basicConfig()
logger = logging.getLogger('main')
logger.setLevel(level=config.get_logging_level())

tl = Timeloop()

client = Client()


@tl.job(interval=timedelta(seconds=2))
def testing():
    test_file = "src/smt/examples/simple.smt2"
    logger.debug("new smt_problem")
    if get_current_decision_value(test_file) == 1:
        logger.debug("offload")
        logger.info(client.post_smt_problem_offload(test_file))
    else:
        logger.debug("solve on EV3")
        logger.info(call_solver(test_file))


def on_created(event):
    file_path = event.src_path
    logger.debug("new smt_problem: %s", file_path)
    if get_current_decision_value(file_path) == 1:
        logger.debug("offload")
        logger.info(client.post_smt_problem_offload(file_path).content)
    else:
        logger.debug("solve on EV3")
        logger.info(call_solver(file_path))


if __name__ == "__main__":
    tl.start(block=False)
    patterns = ["*.smt2"]
    ignore_patterns = None
    ignore_directories = True
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

    my_event_handler.on_created = on_created
    my_observer = Observer()
    my_observer.schedule(my_event_handler, config.get_directory_to_observe(), recursive=False)

    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
