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

ssh pi@10.0.0.16 "python3.7 -m src.decision.reinforcement_learning.q_learning.decision_making"

echo "latency 100ms"
add_latency 100
ssh pi@10.0.0.16 "python3.7 -m src.decision.reinforcement_learning.q_learning.decision_making"
delete_latency 100

echo "latency 250ms"
add_latency 250
ssh pi@10.0.0.16 "python3.7 -m src.decision.reinforcement_learning.q_learning.decision_making"
delete_latency 250