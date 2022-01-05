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


class Monitor:
    def __init__(self):
        if config.is_simulation_active():
            self.battery_level = config.get_simulated_value('battery-level')
            self.avg_rtt = config.get_simulated_value('avg-rtt')
            self.cpu_usage = config.get_simulated_value('cpu-usage')
            self.memory_usage = config.get_simulated_value('memory-usage')
            self.traffic = config.get_simulated_value('traffic')
            self.offload_cost = config.get_simulated_value('offload-cost')
            # currently not used information
            # self.used_ram = config.get_simulated_value('used-ram')
            # self.available_ram = config.get_simulated_value('available-ram')
            # self.disk_usage = config.get_simulated_value('disk-usage')
        else:
            if config.is_ev3():
                self.battery_level = get_battery_level_ev3()
            else:
                self.battery_level = get_battery_level()
            self.avg_rtt = get_rtt(config.get_connectivity_checking_host())
            self.cpu_usage = get_cpu_usage()
            self.memory_usage = get_memory_usage()
            self.traffic = get_traffic()
            self.offload_cost = 0
            # currently not used information
            # self.used_ram = get_used_ram()
            # self.available_ram = get_available_ram()
            # self.disk_usage = get_disk_usage()

    def log_state(self):
        logger.info('battery level (in volts): %f', self.battery_level)
        logger.info('avg rtt (in ms): %f', self.avg_rtt)
        logger.info('CPU usage (percentage): %f', self.cpu_usage)
        logger.info('memory usage (percentage): %f', self.memory_usage)
        logger.info('traffic: %f', self.traffic)
        logger.info('offload cost: %f', self.offload_cost)
        # currently not used information
        # logger.info('used RAM (in Mb): %f', self.used_ram)
        # logger.info('available RAM (in Mb): %f', self.available_ram)
        # logger.info('disk usage (percentage): %f', self.disk_usage)


class SimpleMonitor:
    def __init__(self, monitor):
        self.battery_level = self.__get_rating(monitor.battery_level, config.get_indicator_ranges('battery-level'))
        self.connectivity = self.__get_rating(monitor.avg_rtt, config.get_indicator_ranges('connectivity'))
        self.cpu_state = self.__get_rating(monitor.cpu_usage, config.get_indicator_ranges('cpu-usage'))
        self.memory_state = self.__get_rating(monitor.memory_usage, config.get_indicator_ranges('memory-usage'))
        self.offload_cost = self.__get_rating(monitor.offload_cost,
                                              config.get_indicator_ranges('offload-cost'))

    def log_state(self):
        logger.info('battery level: %s', self.battery_level)
        logger.info('connectivity: %s', self.connectivity)
        logger.info('cpu state: %s', self.cpu_state)
        logger.info('memory state: %s', self.memory_state)
        logger.info('offload cost: %s', self.offload_cost)

    def __get_rating(self, value, ranges):
        for rating in Rating:
            if ranges[rating.name]['start'] <= value <= ranges[rating.name]['end']:
                return rating
        return Rating.poor


class Rating(Enum):
    poor = 0
    average = 1
    excellent = 2


@tl.job(interval=timedelta(seconds=config.get_state_update_period()))
def update_state():
    global global_monitor
    global global_simple_monitor
    global_monitor = Monitor()
    global_simple_monitor = SimpleMonitor(global_monitor)


global_monitor = None
global_simple_monitor = None
update_state()


def get_monitor():
    return global_monitor


def get_simple_monitor():
    return global_simple_monitor


def get_number_of_rating_classes():
    return len(Rating)
