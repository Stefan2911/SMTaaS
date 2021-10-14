#!/usr/bin/env python3

from src.monitoring.monitor_connectivity import *
from src.monitoring.monitor_system_utilization import *


class Monitor:
    def __init__(self):
        self.battery_level = get_battery_percent()
        self.avg_rtt = get_rtt()
        self.cpu_usage = get_cpu_usage()
        self.used_ram = get_used_ram()
        self.available_RAM = get_available_RAM()
        self.memory_usage = get_memory_usage()
        self.disk_usage = get_disk_usage()

    def print_state(self):
        print('battery level (in volts):', self.battery_level)
        print('avg rtt (in ms):', self.avg_rtt)
        print('CPU usage (in %):', self.cpu_usage)
        print('Used RAM (in Mb):', self.used_ram)
        print('Available RAM (in Mb):', self.available_RAM)
        print('Memory usage (in %):', self.memory_usage)
        print('Disk usage (in %):', self.disk_usage)


def get_current_state():
    return Monitor()
