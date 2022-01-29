#!/bin/bash

evaluate () {
  ssh robot@10.0.18 "python3 -m src.evaluation.evaluation time 10 cloud_only /home/robot/src/smt/sets/evaluation/simple /home/robot/src/smt/sets/evaluation/medium /home/robot/src/smt/sets/evaluation/hard /home/robot/src/smt/sets/evaluation/mixed"
}

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

evaluate_with_additional_latency() {
  echo "$1 ms additional latency"
  add_latency "$1"
  evaluate
  delete_latency "$1"
}

echo "0ms additional latency"
evaluate

evaluate_with_additional_latency 50
evaluate_with_additional_latency 100
evaluate_with_additional_latency 200
evaluate_with_additional_latency 300