#!/usr/bin/env python3

# import speedtest
from pythonping import ping

# s = speedtest.Speedtest()
# CONVERSION_FACTOR = 1048576  # Byte to MegaByte


# def get_down_speed():
#    return round(s.download()) / CONVERSION_FACTOR


# def get_up_speed():
#    return round(s.upload()) / CONVERSION_FACTOR

# TODO: adapt TIMEOUT definition
TIMEOUT = 100  # in MS


# if request timed out -> no connection
def get_rtt(host='8.8.8.8'):
    rtt_avg_ms = ping(host, size=10, count=3, timeout=TIMEOUT / 1000).rtt_avg_ms
    return rtt_avg_ms
