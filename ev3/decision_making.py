#!/usr/bin/env python3

import logging

from monitoring.monitor import *

logging.basicConfig(level=logging.DEBUG)

# TODO: maybe extract constants in configuration file (e.g. yaml)

# Thresholds which decide immediately to offload or not
# TODO: define
# T_OFF = Threshold-Offloading, T_NOFF = Threshold-Not-Offloading
# in %

T_OFF_BATTERY_LEVEL = 40
T_NOFF_BATTERY_LEVEL = 95

# rtt in ms
T_OFF_CONNECTIVITY = 1
T_NOFF_CONNECTIVITY = 80

# in %
T_OFF_CPU_USAGE = 80
T_NOFF_CPU_USAGE = 1

# in %
T_OFF_MEMORY_USAGE = 80
T_NOFF_MEMORY_USAGE = 5

# Parameter weights
W_BATTERY_LEVEL = 0.25
W_CONNECTIVITY = 0.25
W_CPU_USAGE = 0.25
W_MEMORY_USAGE = 0.25


# TODO: maybe integrate problem size (difficulty) in decision, if decision value is calculated for each problem?

# returns a value between 0 and 1
# 0 -> solve directly on device
# 1 -> should be offloaded
# TODO: -1 -> no solution (and therefore) decision possible,
#  e.g. no connection and problem is bigger than (available) RAM
# a score (composite variable) is calculated based on multiple indicators (like battery level etc.)
def get_current_decision_value():
    status = get_current_status()
    th = check_thresholds(status)
    if th is not None:
        return th
    return combine_values(normalize_values(status))


def check_thresholds(status):
    value = check_battery_level_threshold(status)
    if value is not None:
        return value
    value = check_connectivity_threshold(status)
    if value is not None:
        return value
    value = check_cpu_usage_threshold(status)
    if value is not None:
        return value
    value = check_battery_level_threshold(status)
    if value is not None:
        return value
    return None


def check_battery_level_threshold(status):
    if status.battery_level < T_OFF_BATTERY_LEVEL:
        logging.debug('T_OFF_BATTERY_LEVEL undercut: %s', status.battery_level)
        return 1
    if status.battery_level > T_NOFF_BATTERY_LEVEL:
        logging.debug('T_NOFF_BATTERY_LEVEL exceeded: %s', status.battery_level)
        return 0
    return None


def check_connectivity_threshold(status):
    if status.avg_rtt is None:  # No connection
        return 0
    if status.avg_rtt < T_OFF_CONNECTIVITY:
        logging.debug('T_OFF_CONNECTIVITY undercut: %s', status.avg_rtt)
        return 1
    if status.avg_rtt > T_NOFF_CONNECTIVITY:
        logging.debug('T_NOFF_CONNECTIVITY exceeded: %s', status.avg_rtt)
        return 0
    return None


def check_cpu_usage_threshold(status):
    if status.cpu_usage > T_OFF_CPU_USAGE:
        logging.debug('T_OFF_CPU_USAGE exceeded: %s', status.cpu_usage)
        return 1
    if status.cpu_usage < T_NOFF_CPU_USAGE:
        logging.debug('T_NOFF_CPU_USAGE undercut: %s', status.cpu_usage)
        return 0
    return None


def check_memory_usage_threshold(status):
    if status.memory_usage > T_OFF_MEMORY_USAGE:
        logging.debug('T_OFF_MEMORY_USAGE exceeded: %s', status.memory_usage)
        return 1
    if status.memory_usage < T_NOFF_MEMORY_USAGE:
        logging.debug('T_NOFF_MEMORY_USAGE undercut: %s', status.memory_usage)
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


def combine_values(status):
    logging.debug("normalized battery level value: %s", status.battery_level)
    logging.debug("normalized avg_rtt value: %s", status.avg_rtt)
    logging.debug("normalized cpu usage value: %s", status.cpu_usage)
    logging.debug("normalized memory usage value: %s", status.memory_usage)
    return (status.battery_level * W_BATTERY_LEVEL +
            status.avg_rtt * W_CONNECTIVITY +
            status.cpu_usage * W_CPU_USAGE +
            status.memory_usage * W_MEMORY_USAGE) / 100
