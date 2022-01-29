#!/bin/bash

add_latency () {
  ssh ubuntu@194.182.171.9 "sudo tc qdisc add dev eth0 root netem delay $1ms"
  ssh root@128.131.57.103 "sudo tc qdisc add dev ens3 root netem delay $1ms"
  ssh root@128.131.57.122 "sudo tc qdisc add dev ens3 root netem delay $1ms"
  ssh root@128.131.57.123 "sudo tc qdisc add dev ens3 root netem delay $1ms"
}

delete_latency() {
  ssh ubuntu@194.182.171.9 "sudo tc qdisc delete dev eth0 root netem delay $1ms"
  ssh root@128.131.57.103 "sudo tc qdisc delete dev ens3 root netem delay $1ms"
  ssh root@128.131.57.122 "sudo tc qdisc delete dev ens3 root netem delay $1ms"
  ssh root@128.131.57.123 "sudo tc qdisc delete dev ens3 root netem delay $1ms"
}

change_latency() {
    add_latency $1
    sleep 20
    delete_latency $1
}


while true
  do
    sleep 20
    change_latency 50
    change_latency 100
    change_latency 200
    change_latency 300
  done



