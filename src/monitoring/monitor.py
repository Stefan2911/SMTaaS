#!/usr/bin/env python3
import logging
from datetime import timedelta

from timeloop import Timeloop

from src.config.config import Config
from src.monitoring.monitor_connectivity import *

config = Config()
training_active = config.is_training_active()

tl = Timeloop()

logging.basicConfig()
logger = logging.getLogger('monitor')
logger.setLevel(level=config.get_logging_level())


class State:
    def __init__(self):
        self.offload_cost = 0
        self.problem_complexity = 0
        self.avg_rtt_list = [0] * len(config.get_connectivity_checking_hosts())


class ExtendedMonitor(State):
    def __init__(self):
        super().__init__()
        connectivity_checking_hosts = config.get_connectivity_checking_hosts()
        for i, host in enumerate(connectivity_checking_hosts):
            self.avg_rtt_list[i] = get_rtt(host)


class Monitor(State):
    def __init__(self):
        super().__init__()
        self.avg_rtt_list[0] = get_rtt(config.get_connectivity_checking_host())

    def log_state(self):
        logger.info('avg rtt (in ms): %f', self.avg_rtt_list[0])
        logger.info('problem complexity: %f', self.problem_complexity)


@tl.job(interval=timedelta(seconds=config.get_state_update_period()))
def update_state():
    global global_monitor
    if config.get_decision_mode() == 'deep_q_network':
        global_monitor = ExtendedMonitor()
    else:
        global_monitor = Monitor()


global_monitor = None
update_state()


def get_monitor():
    if training_active:
        update_state()
    return global_monitor


if training_active == False:
    tl.start()
