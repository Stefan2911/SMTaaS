#!/bin/bash

add_latency () {
  ssh pi@10.0.0.1 "sudo tc qdisc add dev eth0 root netem delay $1ms"
  ssh pi@10.0.0.3 "sudo tc qdisc add dev eth0 root netem delay $1ms"
}

delete_latency() {
  ssh pi@10.0.0.1 "sudo tc qdisc delete dev eth0 root netem delay $1ms"
  ssh pi@10.0.0.3 "sudo tc qdisc delete dev eth0 root netem delay $1ms"
}

change_latency() {
    add_latency $1
    sleep 20
    delete_latency $1
}


while true
  do
    sleep 20
    change_latency 100
    change_latency 200
    change_latency 300
    change_latency 400
  done



