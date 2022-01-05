#!/usr/bin/env python

import psutil
from ev3dev2.power import PowerSupply

CONVERSION_FACTOR = 1048576  # Byte to MegaByte

psutil.cpu_percent(interval=None)


def get_cpu_usage():
    return psutil.cpu_percent(interval=None)


def get_used_ram():
    return psutil.virtual_memory().used / CONVERSION_FACTOR


def get_available_ram():
    return psutil.virtual_memory().available / CONVERSION_FACTOR


def get_memory_usage():
    return psutil.virtual_memory().percent


def get_disk_usage():
    return psutil.disk_usage('/').percent


# DOES NOT WORK ON EV3
def get_battery_level():
    sensors_battery = psutil.sensors_battery()
    if sensors_battery is None:
        return 100  # if no battery is installed, there must be permanent power supply
    return sensors_battery.percent


def get_battery_level_ev3():
    # not sure why, but I need to multiply measured_voltage with 10 otherwise it is below min_voltage
    return (((PowerSupply().measured_voltage * 10) - PowerSupply().min_voltage) /
            (PowerSupply().max_voltage - PowerSupply().min_voltage)) * 100


def get_traffic():
    return (psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv) / CONVERSION_FACTOR
