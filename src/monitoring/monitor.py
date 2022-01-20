#!/usr/bin/env python3
import logging
from datetime import timedelta
from enum import Enum

from timeloop import Timeloop

from src.config.config import Config
from src.monitoring.monitor_connectivity import *
from src.monitoring.monitor_system_utilization import *

config = Config()

tl = Timeloop()

logging.basicConfig()
logger = logging.getLogger('monitor')
logger.setLevel(level=config.get_logging_level())


class State:
    def __init__(self):
        self.offload_cost = 0
        self.problem_complexity = 0


class Monitor(State):
    def __init__(self):
        super().__init__()
        if config.is_simulation_active():
            self.avg_rtt = config.get_simulated_value('avg-rtt')
            self.cpu_usage = config.get_simulated_value('cpu-usage')
            self.memory_usage = config.get_simulated_value('memory-usage')
            self.traffic = config.get_simulated_value('traffic')
            super.offload_cost = config.get_simulated_value('offload-cost')
            super.problem_complexity = config.get_simulated_value('problem-complexity')
        else:
            self.avg_rtt = get_rtt(config.get_connectivity_checking_host())
            self.cpu_usage = get_cpu_usage()
            self.memory_usage = get_memory_usage()
            self.traffic = get_traffic()

    def log_state(self):
        logger.info('avg rtt (in ms): %f', self.avg_rtt)
        logger.info('CPU usage (percentage): %f', self.cpu_usage)
        logger.info('memory usage (percentage): %f', self.memory_usage)
        logger.info('traffic: %f', self.traffic)
        logger.info('offload cost: %f', self.offload_cost)
        logger.info('problem complexity: %f', self.problem_complexity)


def get_rating(value, ranges):
    if ranges is None or value is None:
        return Rating.poor
    for rating in Rating:
        if ranges[rating.name]['start'] <= value <= ranges[rating.name]['end']:
            return rating
    return Rating.poor


class SimpleMonitor(State):
    def __init__(self, monitor):
        super().__init__()
        self.connectivity = get_rating(monitor.avg_rtt, config.get_indicator_ranges('connectivity'))
        self.cpu_state = get_rating(monitor.cpu_usage, config.get_indicator_ranges('cpu-usage'))
        self.memory_state = get_rating(monitor.memory_usage, config.get_indicator_ranges('memory-usage'))

    def log_state(self):
        logger.info('connectivity: %s', self.connectivity)
        logger.info('cpu state: %s', self.cpu_state)
        logger.info('memory state: %s', self.memory_state)
        logger.info('offload cost: %s', self.offload_cost)
        logger.info('problem complexity: %s', self.problem_complexity)


class Rating(Enum):
    poor = 0
    average = 1
    excellent = 2


@tl.job(interval=timedelta(seconds=config.get_state_update_period()))
def update_state():
    global global_monitor
    global_monitor = Monitor()


global_monitor = None
update_state()


def get_monitor():
    return global_monitor


def get_number_of_rating_classes():
    return len(Rating)


tl.start()
