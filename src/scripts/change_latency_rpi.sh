#!/bin/bash
sudo tc qdisc del dev wlan0 root
sudo tc qdisc add dev wlan0 root handle 1: prio
sudo tc qdisc add dev wlan0 parent 1:3 handle 30: netem delay "$1"ms
sudo tc filter add dev wlan0 protocol ip parent 1:0 prio 3 u32 match ip dst 10.0.0.18/32 flowid 1:3