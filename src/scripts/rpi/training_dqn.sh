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

train_with_additional_latency() {
  echo "$1 ms additional latency"
  add_latency "$1"
  ssh pi@10.0.0.3 "python3.7 -m src.decision.reinforcement_learning.deep_q_network.decision_making"
  delete_latency "$1"
}

#echo "additional latency 0ms"
../change_cloud_latency_periodically.sh &
latency_task=$!
ssh pi@10.0.0.3 "python3.7 -m src.decision.reinforcement_learning.deep_q_network.decision_making"
kill $latency_task

#train_with_additional_latency 50
#train_with_additional_latency 100
#train_with_additional_latency 200
#train_with_additional_latency 300