#!/usr/bin/env python3

import logging

from src.decision.heuristic.config.config import Config
from src.monitoring.monitor import *

config = Config()

logging.basicConfig()
logger = logging.getLogger('decision_making')
logger.setLevel(level=config.get_logging_level())


# returns a value between 0 and 1
# 0 -> solve directly on device
# 1 -> should be offloaded
# TODO: maybe integrate problem size (difficulty) in decision
# a score (composite variable) is calculated based on multiple indicators (like battery level etc.)
# this is a heuristic based solution
def get_current_decision_value():
    state = get_current_state()
    indicator_configuration = config.get_indicator_configuration()
    th = check_thresholds(state, indicator_configuration)
    if th is not None:
        return th
    combined_value = combine_values(normalize_values(state), indicator_configuration)
    if combined_value > config.get_offload_threshold():
        return 1
    else:
        return 0


def check_thresholds(status, indicator_configuration):
    value = check_battery_level_threshold(status, indicator_configuration['battery-level'])
    if value is not None:
        return value
    value = check_connectivity_threshold(status, indicator_configuration['connectivity'])
    if value is not None:
        return value
    value = check_cpu_usage_threshold(status, indicator_configuration['cpu-usage'])
    if value is not None:
        return value
    value = check_memory_usage_threshold(status, indicator_configuration['memory-usage'])
    if value is not None:
        return value
    return None


def check_battery_level_threshold(status, battery_configuration):
    if status.battery_level < battery_configuration['offloading-threshold']:
        logger.debug('battery-level offloading-threshold %s undercut: %s',
                     battery_configuration['offloading-threshold'], status.battery_level)
        return 1
    if status.battery_level > battery_configuration['locally-threshold']:
        logger.debug('battery-level locally-threshold %s exceeded: %s', battery_configuration['locally-threshold'],
                     status.battery_level)
        return 0
    return None


def check_connectivity_threshold(status, connectivity_configuration):
    if status.avg_rtt is None:  # No connection
        logger.debug('No connection')
        return 0
    if status.avg_rtt < connectivity_configuration['offloading-threshold']:
        logger.debug('connectivity offloading-threshold %s undercut: %s',
                     connectivity_configuration['offloading-threshold'], status.avg_rtt)
        return 1
    if status.avg_rtt > connectivity_configuration['locally-threshold']:
        logger.debug('connectivity locally-threshold %s exceeded: %s', connectivity_configuration['locally-threshold'],
                     status.avg_rtt)
        return 0
    return None


def check_cpu_usage_threshold(status, cpu_configuration):
    if status.cpu_usage > cpu_configuration['offloading-threshold']:
        logger.debug('cpu-usage offloading-threshold %s exceeded: %s', cpu_configuration['offloading-threshold'],
                     status.cpu_usage)
        return 1
    if status.cpu_usage < cpu_configuration['locally-threshold']:
        logger.debug('cpu-usage locally-threshold %s undercut: %s', cpu_configuration['locally-threshold'],
                     status.cpu_usage)
        return 0
    return None


def check_memory_usage_threshold(status, memory_configuration):
    if status.memory_usage > memory_configuration['offloading-threshold']:
        logger.debug('memory-usage offloading-threshold %s exceeded: %s', memory_configuration['offloading-threshold'],
                     status.memory_usage)
        return 1
    if status.memory_usage < memory_configuration['locally-threshold']:
        logger.debug('memory-usage locally-threshold %s undercut: %s', memory_configuration['locally-threshold'],
                     status.memory_usage)
        return 0
    return None


def normalize_values(status):
    # battery level is already normalized (percentage)
    # cpu usage is already normalized (percentage)
    # memory usage is already normalized (percentage)

    # higher battery level should DECREASE score
    status.battery_level = 100 - status.battery_level
    # higher avg rtt should DECREASE score
    # TODO: adapt TIMEOUT definition
    status.avg_rtt = 100 - (status.avg_rtt / TIMEOUT * 100)
    # higher cpu usage should INCREASE score
    # higher memory usage should INCREASE score
    return status


def combine_values(status, configuration):
    logger.debug("normalized battery level value: %s", status.battery_level)
    logger.debug("normalized avg_rtt value: %s", status.avg_rtt)
    logger.debug("normalized cpu usage value: %s", status.cpu_usage)
    logger.debug("normalized memory usage value: %s", status.memory_usage)
    return (status.battery_level * configuration['battery-level']['weight'] +
            status.avg_rtt * configuration['connectivity']['weight'] +
            status.cpu_usage * configuration['cpu-usage']['weight'] +
            status.memory_usage * configuration['memory-usage']['weight']) / 100