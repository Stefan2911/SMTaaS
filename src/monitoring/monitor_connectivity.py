#!/usr/bin/env python3

from pythonping import ping

from src.simulation.simulation import Simulation

TIMEOUT = 1  # in seconds

simulation = Simulation.get_instance()


def get_rtt(host='8.8.8.8'):
    rtt_avg_ms = ping(host, count=2, timeout=TIMEOUT).rtt_avg_ms
    return rtt_avg_ms + simulation.get_additional_latency(host)
