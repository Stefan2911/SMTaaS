#!/bin/bash
ssh robot@10.0.18 "python3 -m src.decision.reinforcement_learning.q_learning.decision_making"

ssh pi@10.0.0.16 "./change_latency.sh 100"
ssh pi@10.0.0.19 "./change_latency.sh 100"
ssh robot@10.0.18 "python3 -m src.decision.reinforcement_learning.q_learning.decision_making"

ssh pi@10.0.0.16 "./change_latency.sh 200"
ssh pi@10.0.0.19 "./change_latency.sh 200"
ssh robot@10.0.18 "python3 -m src.decision.reinforcement_learning.q_learning.decision_making"

ssh pi@10.0.0.16 "sudo tc qdisc del dev wlan0 root"
ssh pi@10.0.0.19 "sudo tc qdisc del dev wlan0 root"