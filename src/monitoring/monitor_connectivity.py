#!/usr/bin/env python3

from pythonping import ping

# TODO: adapt TIMEOUT definition
TIMEOUT = 100  # in MS


def get_rtt(host='8.8.8.8'):
    rtt_avg_ms = ping(host, size=10, count=3, timeout=TIMEOUT / 1000).rtt_avg_ms
    return rtt_avg_ms
