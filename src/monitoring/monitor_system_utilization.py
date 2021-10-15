#!/usr/bin/env python

import psutil

CONVERSION_FACTOR = 1048576  # Byte to MegaByte


def get_cpu_usage():
    return psutil.cpu_percent(interval=1)


def get_used_ram():
    return psutil.virtual_memory().used / CONVERSION_FACTOR


def get_available_ram():
    return psutil.virtual_memory().available / CONVERSION_FACTOR


def get_memory_usage():
    return psutil.virtual_memory().percent


def get_disk_usage():
    return psutil.disk_usage('/').percent


# DOES NOT WORK ON EV3
def get_battery_percent():
    sensors_battery = psutil.sensors_battery()
    if sensors_battery is None:
        return None
    return sensors_battery.percent


# DOES NOT WORK ON EV3
def get_battery_power_plugged():
    sensors_battery = psutil.sensors_battery()
    if sensors_battery is None:
        return None
    return sensors_battery.power_plugged


def get_traffic():
    return (psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv) / CONVERSION_FACTOR
