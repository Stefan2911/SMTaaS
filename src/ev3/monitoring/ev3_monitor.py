#!/usr/bin/env python3
from src.ev3.monitoring.monitor_battery_level import get_battery_level
from src.monitoring.monitor import Monitor


class EV3Monitor(Monitor):
    def __init__(self):
        super().__init__()
        self.battery_level = get_battery_level()
