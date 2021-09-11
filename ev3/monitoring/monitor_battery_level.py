#!/usr/bin/env python3

from ev3dev2.power import PowerSupply


def get_battery_level():
    return PowerSupply().measured_volts
