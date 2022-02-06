#!/bin/bash

../change_cloud_latency_periodically.sh &
latency_task=$!
ssh pi@10.0.0.3 "python3.7 -m src.decision.reinforcement_learning.deep_q_network.decision_making"
kill $latency_task
