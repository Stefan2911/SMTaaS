#!/usr/bin/env python3

from pythonping import ping

TIMEOUT = 1  # in seconds


def get_rtt(host='8.8.8.8'):
    rtt_avg_ms = ping(host, count=2, timeout=TIMEOUT).rtt_avg_ms
    return rtt_avg_ms
