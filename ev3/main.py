import logging
from datetime import timedelta

from timeloop import Timeloop

from communication.rest.client import post_smt_problem
from decision_making import get_current_decision_value
from smt.solver import call_solver

logging.basicConfig(level=logging.DEBUG)

# in the following directory the SMT problems are added
DIRECTORY_TO_OBSERVE = "/home/robot/develop/smt/watch"

# how often a new decision value is calculated
UPDATE_DECISION_VALUE_INTERVAL = 5

# TODO: define value when problem should be offloaded
OFFLOAD_THRESHOLD = 0.5

tl = Timeloop()

current_decision_value = 0.5


@tl.job(interval=timedelta(seconds=UPDATE_DECISION_VALUE_INTERVAL))
def update_decision_value():
    global current_decision_value
    current_decision_value = get_current_decision_value()
    logging.debug("updated decision value: %s", current_decision_value)


@tl.job(interval=timedelta(seconds=0.5))
def testing():
    test_file = "./smt/examples/simple.smt2"
    logging.debug("new smt_problem")
    if current_decision_value > OFFLOAD_THRESHOLD:
        logging.debug("offload")
        logging.info(post_smt_problem(test_file))
    else:
        logging.debug("solve on EV3")
        logging.info(call_solver(test_file))


def on_created(event):
    file_path = event.src_path
    logging.debug("new smt_problem: %s", file_path)
    if current_decision_value > OFFLOAD_THRESHOLD:
        logging.debug("offload")
        logging.info(post_smt_problem(file_path))
    else:
        logging.debug("solve on EV3")
        logging.info(call_solver(file_path))


if __name__ == "__main__":
    tl.start(block=True)
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
