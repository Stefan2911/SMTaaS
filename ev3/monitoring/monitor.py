#!/usr/bin/env python3

from .monitor_battery_level import *
from .monitor_connectivity import *
from .monitor_system_utilization import *


class Monitor:
    def __init__(self):
        self.battery_level = get_battery_level()
        self.avg_rtt = get_rtt()
        self.cpu_usage = get_cpu_usage()
        self.used_ram = get_used_ram()
        self.available_RAM = get_available_RAM()
        self.memory_usage = get_memory_usage()
        self.disk_usage = get_disk_usage()


def print_status():
    m = Monitor()
    print('battery level (in volts):', m.battery_level)
    print('avg rtt (in ms):', m.avg_rtt)
    print('CPU usage (in %):', m.cpu_usage)
    print('Used RAM (in Mb):', m.used_ram)
    print('Available RAM (in Mb):', m.available_RAM)
    print('Memory usage (in %):', m.memory_usage)
    print('Disk usage (in %):', m.disk_usage)


def get_current_status():
    return Monitor()
