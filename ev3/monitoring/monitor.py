#!/usr/bin/env python3

from monitor_battery_level import *
from monitor_connectivity import *
from monitor_system_utilization import *


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
    print('battery level (in volts):', get_battery_level())
    print('avg rtt (in ms):', get_rtt())
    print('CPU usage (in %):', get_cpu_usage())
    print('Used RAM (in Mb):', get_used_ram())
    print('Available RAM (in Mb):', get_available_RAM())
    print('Memory usage (in %):', get_memory_usage())
    print('Disk usage (in %):', get_disk_usage())


def get_current_status():
    return Monitor()
