#!/usr/bin/env python3
import logging
import time
from enum import Enum

from src.config.config import Config
from src.monitoring.monitor_battery_level_ev3 import get_battery_level_ev3
from src.monitoring.monitor_connectivity import *
from src.monitoring.monitor_system_utilization import *

config = Config()

logging.basicConfig()
logger = logging.getLogger('monitor')
logger.setLevel(level=config.get_logging_level())


def _get_transmission_cost(problem_size):
    return problem_size * config.get_uplink_cost()


class Monitor:
    def __init__(self, problem_size):
        if config.is_simulation_active():
            self.battery_level = config.get_simulated_value('battery-level')
            self.avg_rtt = config.get_simulated_value('avg-rtt')
            self.cpu_usage = config.get_simulated_value('cpu-usage')
            self.used_ram = config.get_simulated_value('used-ram')
            self.available_ram = config.get_simulated_value('available-ram')
            self.memory_usage = config.get_simulated_value('memory-usage')
            self.disk_usage = config.get_simulated_value('disk-usage')
            self.traffic = config.get_simulated_value('traffic')
            self.transmission_cost = config.get_simulated_value('transmission-cost')
        else:
            start = time.time()
            self.battery_level = get_battery_percent()
            logger.debug('needed time for getting battery level: %s', time.time() - start)
            start = time.time()
            self.avg_rtt = get_rtt()
            logger.debug('needed time for getting rtt: %s', time.time() - start)
            start = time.time()
            self.cpu_usage = get_cpu_usage()
            logger.debug('needed time for getting cpu usage: %s', time.time() - start)
            start = time.time()
            self.used_ram = get_used_ram()
            logger.debug('needed time for getting used ram: %s', time.time() - start)
            start = time.time()
            self.available_ram = get_available_ram()
            logger.debug('needed time for getting available ram: %s', time.time() - start)
            start = time.time()
            self.memory_usage = get_memory_usage()
            logger.debug('needed time for getting memory usage: %s', time.time() - start)
            start = time.time()
            self.disk_usage = get_disk_usage()
            logger.debug('needed time for getting disk usage: %s', time.time() - start)
            start = time.time()
            self.traffic = get_traffic()
            logger.debug('needed time for getting traffic: %s', time.time() - start)
            start = time.time()
            self.transmission_cost = _get_transmission_cost(problem_size)
            logger.debug('needed time for getting transmission cost: %s', time.time() - start)

    def log_state(self):
        logger.info('battery level (in volts): %f', self.battery_level)
        logger.info('avg rtt (in ms): %f', self.avg_rtt)
        logger.info('CPU usage (percentage): %f', self.cpu_usage)
        logger.info('used RAM (in Mb): %f', self.used_ram)
        logger.info('available RAM (in Mb): %f', self.available_ram)
        logger.info('memory usage (percentage): %f', self.memory_usage)
        logger.info('disk usage (percentage): %f', self.disk_usage)
        logger.info('traffic: %f', self.traffic)
        logger.info('transmission cost: %f', self.transmission_cost)


class SimpleMonitor:
    def __init__(self, monitor):
        self.battery_level = self.__get_rating(monitor.battery_level, config.get_indicator_ranges('battery-level'))
        self.connectivity = self.__get_rating(monitor.avg_rtt, config.get_indicator_ranges('connectivity'))
        self.cpu_state = self.__get_rating(monitor.cpu_usage, config.get_indicator_ranges('cpu-usage'))
        self.memory_state = self.__get_rating(monitor.memory_usage, config.get_indicator_ranges('memory-usage'))
        self.transmission_cost = self.__get_rating(monitor.transmission_cost,
                                                   config.get_indicator_ranges('transmission-cost'))

    def log_state(self):
        logger.info('battery level: %s', self.battery_level)
        logger.info('connectivity: %s', self.connectivity)
        logger.info('cpu state: %s', self.cpu_state)
        logger.info('memory state: %s', self.memory_state)
        logger.info('transmission cost: %s', self.transmission_cost)

    def __get_rating(self, value, ranges):
        for rating in Rating:
            if ranges[rating.name]['start'] <= value <= ranges[rating.name]['end']:
                return rating
        return Rating.poor


class EV3Monitor(Monitor):
    def __init__(self, problem_size):
        super().__init__(problem_size)
        if config.is_simulation_active():
            self.battery_level = config.get_simulated_value('battery-level')
        else:
            self.battery_level = get_battery_level_ev3()


class Rating(Enum):
    poor = 0
    average = 1
    excellent = 2


def get_current_state(problem_size, simple=False):
    if simple:
        if config.is_ev3():
            return SimpleMonitor(EV3Monitor(problem_size))
        else:
            return SimpleMonitor(Monitor(problem_size))
    else:
        if config.is_ev3():
            return EV3Monitor(problem_size)
        else:
            return Monitor(problem_size)


def map_detailed_state(monitor, simple=False):
    if simple:
        return SimpleMonitor(monitor)
    return monitor


def get_number_of_rating_classes():
    return len(Rating)
