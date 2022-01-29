#!/bin/bash
echo "additional latency 0ms"
ssh robot@10.0.18 "python3 -m src.decision.reinforcement_learning.q_learning.decision_making"

echo "additional latency 100ms"
ssh pi@10.0.0.1 "./change_latency.sh 100"
ssh pi@10.0.0.3 "./change_latency.sh 100"
ssh robot@10.0.18 "python3 -m src.decision.reinforcement_learning.q_learning.decision_making"

echo "additional latency 150ms"
ssh pi@10.0.0.1 "./change_latency.sh 150"
ssh pi@10.0.0.3 "./change_latency.sh 150"
ssh robot@10.0.18 "python3 -m src.decision.reinforcement_learning.q_learning.decision_making"

echo "additional latency 200ms"
ssh pi@10.0.0.1 "./change_latency.sh 200"
ssh pi@10.0.0.3 "./change_latency.sh 200"
ssh robot@10.0.18 "python3 -m src.decision.reinforcement_learning.q_learning.decision_making"

echo "additional latency 300ms"
ssh pi@10.0.0.1 "./change_latency.sh 300"
ssh pi@10.0.0.3 "./change_latency.sh 300"
ssh robot@10.0.18 "python3 -m src.decision.reinforcement_learning.q_learning.decision_making"

ssh pi@10.0.0.1 "sudo tc qdisc del dev eth0 root"
ssh pi@10.0.0.3 "sudo tc qdisc del dev eth0 root"