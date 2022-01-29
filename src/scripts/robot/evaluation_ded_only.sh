#!/bin/bash

evaluate () {
  ssh robot@10.0.18 "python3 -m time 10 ded_only src.evaluation.evaluation src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/simple /home/robot/src/smt/sets/evaluation/medium /home/robot/src/smt/sets/evaluation/hard /home/robot/src/smt/sets/evaluation/mixed"
}

evaluate_with_additional_latency(){
  echo "$1 ms additional latency"
  ssh pi@10.0.0.1 "./change_latency.sh $1"
  ssh pi@10.0.0.3 "./change_latency.sh $1"
  evaluate
}
ssh pi@10.0.0.1 "sudo tc qdisc del dev eth0 root"
ssh pi@10.0.0.3 "sudo tc qdisc del dev eth0 root"

echo "0ms additional latency"
evaluate

evaluate_with_additional_latency 50
evaluate_with_additional_latency 100
evaluate_with_additional_latency 200
evaluate_with_additional_latency 300

ssh pi@10.0.0.1 "sudo tc qdisc del dev eth0 root"
ssh pi@10.0.0.3 "sudo tc qdisc del dev eth0 root"