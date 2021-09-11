#!/usr/bin/env python3

from monitor_battery_level import *
from monitor_connectivity import *
from monitor_system_utilization import *

print('battery level (in volts): ', get_battery_level())

print('connectivity')
print('avg rtt (in ms): ', get_rtt())

print('system utilization')
print('CPU usage (in %): ', get_cpu_usage())
print('Used RAM (in Mb): ', get_used_ram())
print('Available Virtual Memory (in Mb):', get_available_virtual_memory())
print('Disk Usage (in %):', get_disk_usage())
