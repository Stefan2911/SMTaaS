import logging
from datetime import timedelta

from timeloop import Timeloop

from communication.rest.client import post_smt_problem
from config import *
from decision_making import get_current_decision_value
from smt.solver import call_solver

logger = logging.getLogger('main')
logger.setLevel(level=get_logging_level())

tl = Timeloop()

current_decision_value = get_current_decision_value()


@tl.job(interval=timedelta(seconds=get_update_interval()))
def update_decision_value():
    global current_decision_value
    current_decision_value = get_current_decision_value()
    logger.debug("updated decision value: %s", current_decision_value)


@tl.job(interval=timedelta(seconds=2))
def testing():
    test_file = "./smt/examples/simple.smt2"
    logger.debug("new smt_problem")
    if current_decision_value > get_offload_threshold():
        logger.debug("offload")
        logger.info(post_smt_problem(test_file, get_api_url()))
    else:
        logger.debug("solve on EV3")
        logger.info(call_solver(test_file, get_solver_installation_location()))


def on_created(event):
    file_path = event.src_path
    logger.debug("new smt_problem: %s", file_path)
    if current_decision_value > get_offload_threshold():
        logger.debug("offload")
        logger.info(post_smt_problem(file_path, get_api_url()).content)
    else:
        logger.debug("solve on EV3")
        logger.info(call_solver(file_path, get_solver_installation_location()))


if __name__ == "__main__":
    tl.start(block=False)
    # TODO: watchdog requires Python >= 3.6 which is currently not installed on EV3
    # watch_config()
    # patterns = ["*.smt2"]
    # ignore_patterns = None
    # ignore_directories = True
    # case_sensitive = True
    # my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

    # my_event_handler.on_created = on_created
    # my_observer = Observer()
    # my_observer.schedule(my_event_handler, DIRECTORY_TO_OBSERVE, recursive=False)

    # my_observer.start()
    # try:
    #    while True:
    #        time.sleep(1)
    # except KeyboardInterrupt:
    #    my_observer.stop()
    #    my_observer.join()
