#!/usr/bin/env python3
import logging
from enum import Enum

from src.monitoring.config.config import Config
from src.monitoring.monitor_connectivity import *
from src.monitoring.monitor_system_utilization import *

config = Config()

logging.basicConfig()
logger = logging.getLogger('monitor')
logger.setLevel(level=config.get_logging_level())


class Monitor:
    def __init__(self):
        self.battery_level = get_battery_percent()
        self.avg_rtt = get_rtt()
        self.cpu_usage = get_cpu_usage()
        self.used_ram = get_used_ram()
        self.available_ram = get_available_ram()
        self.memory_usage = get_memory_usage()
        self.disk_usage = get_disk_usage()
        self.traffic = get_traffic()

    def print_state(self):
        logger.info('battery level (in volts):', self.battery_level)
        logger.info('avg rtt (in ms):', self.avg_rtt)
        logger.info('CPU usage (in %):', self.cpu_usage)
        logger.info('used RAM (in Mb):', self.used_ram)
        logger.info('available RAM (in Mb):', self.available_ram)
        logger.info('memory usage (in %):', self.memory_usage)
        logger.info('disk usage (in %):', self.disk_usage)
        logger.info('traffic:', self.traffic)


class SimpleMonitor:
    def __init__(self, monitor):
        self.battery_level = self.__get_rating(monitor.battery_level, config.get_indicator_ranges('battery-level'))
        self.connectivity = self.__get_rating(monitor.avg_rtt, config.get_indicator_ranges('connectivity'))
        self.cpu_state = self.__get_rating(monitor.cpu_usage, config.get_indicator_ranges('cpu-usage'))
        self.memory_state = self.__get_rating(monitor.memory_usage, config.get_indicator_ranges('memory-usage'))

    def print_state(self):
        logger.info('battery level: %s', self.battery_level)
        logger.info('connectivity: %s', self.connectivity)
        logger.info('cpu state: %s', self.cpu_state)
        logger.info('memory state: %s', self.memory_state)

    def __get_rating(self, value, ranges):
        for rating in Rating:
            if ranges[rating.name]['start'] <= value <= ranges[rating.name]['end']:
                return rating


class Rating(Enum):
    poor = 0
    average = 1
    excellent = 2
    # TODO: could be extended with fair, good


def get_current_state(simple=False):
    if simple:
        return SimpleMonitor(Monitor())
    return Monitor()


def map_detailed_state(monitor, simple=False):
    if simple:
        return SimpleMonitor(monitor)
    return monitor


def get_number_of_rating_classes():
    return len(Rating)
