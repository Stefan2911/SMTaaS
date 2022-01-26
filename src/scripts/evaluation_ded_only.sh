#!/bin/bash

evaluate () {
  ssh robot@10.0.18 "python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/simple time 10 ded_only"
  ssh robot@10.0.18 "python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/medium time 10 ded_only"
  ssh robot@10.0.18 "python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/hard time 10 ded_only"
  ssh robot@10.0.18 "python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/mixed time 10 ded_only"
}

evaluate_with_additional_latency(){
  echo "$1 ms additional latency"
  ssh pi@10.0.0.16 "./change_latency.sh $1"
  ssh pi@10.0.0.19 "./change_latency.sh $1"
  evaluate
}
ssh pi@10.0.0.16 "sudo tc qdisc del dev eth0 root"
ssh pi@10.0.0.19 "sudo tc qdisc del dev eth0 root"

echo "0ms additional latency"
evaluate

evaluate_with_additional_latency 50
evaluate_with_additional_latency 100
evaluate_with_additional_latency 200
evaluate_with_additional_latency 300

ssh pi@10.0.0.16 "sudo tc qdisc del dev eth0 root"
ssh pi@10.0.0.19 "sudo tc qdisc del dev eth0 root"