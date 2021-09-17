# on the basis of the decision value forward problem to solver on EV3 or offload it


import time
from datetime import timedelta

from timeloop import Timeloop
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

from ev3.communication.rest.client import post_smt_problem
from ev3.decision_making import get_current_decision_value
from ev3.smt.solver import call_solver

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
    print("updated decision value:", current_decision_value)


def on_created(event):
    file_path = event.src_path
    print("new smt_problem:", file_path)
    if current_decision_value > OFFLOAD_THRESHOLD:
        print("offload")
        print(post_smt_problem(file_path))
    else:
        print("solve on EV3")
        print(call_solver(file_path))


if __name__ == "__main__":
    patterns = ["*.smt2"]
    ignore_patterns = None
    ignore_directories = True
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

    my_event_handler.on_created = on_created
    my_observer = Observer()
    my_observer.schedule(my_event_handler, DIRECTORY_TO_OBSERVE, recursive=False)

    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
