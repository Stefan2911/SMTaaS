#!/usr/bin/env python3
import logging

from src.monitoring.monitor_connectivity import *
from src.monitoring.monitor_system_utilization import *

logging.basicConfig()
logger = logging.getLogger('monitor')
logger.setLevel(level=logging.INFO)


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
        logger.info('Used RAM (in Mb):', self.used_ram)
        logger.info('Available RAM (in Mb):', self.available_ram)
        logger.info('Memory usage (in %):', self.memory_usage)
        logger.info('Disk usage (in %):', self.disk_usage)
        logger.info('Traffic:', self.traffic)


def get_current_state():
    return Monitor()
