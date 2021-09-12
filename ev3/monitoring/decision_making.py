#!/usr/bin/env python3

from monitor import *

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


# TODO: integrate problem size (difficulty) in decision

# returns a value between 0 and 1
# 0 -> solve directly on device
# 1 -> should be offloaded
# TODO: -1 -> no solution (and therefore) decision possible,
#  e.g. no connection and problem is bigger than (available) RAM
# a score (composite variable) is calculated based on multiple indicators (like battery level etc.)
def get_current_decision_value():
    status = get_current_status()
    if status.avg_rtt is None:
        return 0
    th = check_thresholds(status)
    if th is not None:
        return th
    return combine_values(normalize_values(status))


def check_thresholds(status):
    if status.battery_level < T_OFF_BATTERY_LEVEL:
        print('T_OFF_BATTERY_LEVEL undercut:', status.battery_level)
        return 1
    if status.battery_level > T_NOFF_BATTERY_LEVEL:
        print('T_NOFF_BATTERY_LEVEL exceeded:', status.battery_level)
        return 0
    if status.avg_rtt < T_OFF_CONNECTIVITY:
        print('T_OFF_CONNECTIVITY undercut:', status.avg_rtt)
        return 1
    if status.avg_rtt > T_NOFF_CONNECTIVITY:
        print('T_NOFF_CONNECTIVITY exceeded:', status.avg_rtt)
        return 0
    if status.cpu_usage > T_OFF_CPU_USAGE:
        print('T_OFF_CPU_USAGE exceeded:', status.cpu_usage)
        return 1
    if status.cpu_usage < T_NOFF_CPU_USAGE:
        print('T_NOFF_CPU_USAGE undercut:', status.cpu_usage)
        return 0
    if status.memory_usage > T_OFF_MEMORY_USAGE:
        print('T_OFF_MEMORY_USAGE exceeded:', status.memory_usage)
        return 1
    if status.memory_usage < T_NOFF_MEMORY_USAGE:
        print('T_NOFF_MEMORY_USAGE undercut:', status.memory_usage)
        return 0


def normalize_values(status):
    # battery level is already normalized (percentage)
    # cpu usage is already normalized (percentage)
    # memory usage is already normalized (percentage)

    # higher battery level should DECREASE score
    status.battery_level = 100 - status.battery_level
    # higher avg rtt should DECREASE score
    status.avg_rtt = 100 - (status.avg_rtt / TIMEOUT * 100)
    # higher cpu usage should INCREASE score
    # higher memory usage should INCREASE score
    return status


def combine_values(status):
    print(status.battery_level)
    print(status.avg_rtt)
    print(status.cpu_usage)
    print(status.memory_usage)
    return (status.battery_level * W_BATTERY_LEVEL +
            status.avg_rtt * W_CONNECTIVITY +
            status.cpu_usage * W_CPU_USAGE +
            status.memory_usage * W_MEMORY_USAGE) / 100


print(get_current_decision_value())
