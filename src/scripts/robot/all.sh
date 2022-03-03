#!/bin/bash
# simulation is done on application level

# training q_learning
ssh robot@10.0.18 "python3 -m src.decision.reinforcement_learning.q_learning.decision_making"

# evaluation robot only
ssh robot@10.0.18 "python3 -m src.evaluation.evaluation time 5 robot_only /home/pi/src/smt/sets/evaluation/simple /home/pi/src/smt/sets/evaluation/medium /home/pi/src/smt/sets/evaluation/hard /home/pi/src/smt/sets/evaluation/mixed"

# evaluation cloud only
ssh robot@10.0.18 "python3 -m src.evaluation.evaluation time 5 cloud_only /home/pi/src/smt/sets/evaluation/simple /home/pi/src/smt/sets/evaluation/medium /home/pi/src/smt/sets/evaluation/hard /home/pi/src/smt/sets/evaluation/mixed"

# evaluation q_learning
ssh robot@10.0.18 "python3 -m src.evaluation.evaluation time 5 q_learning /home/pi/src/smt/sets/evaluation/simple /home/pi/src/smt/sets/evaluation/medium /home/pi/src/smt/sets/evaluation/hard /home/pi/src/smt/sets/evaluation/mixed"
