#!/bin/bash
# simulation is done on application level

# training q_learning
ssh pi@10.0.0.3 "python3.7 -m src.decision.reinforcement_learning.q_learning.decision_making"

# training dqn
ssh pi@10.0.0.3 "python3.7 -m src.decision.reinforcement_learning.deep_q_network.decision_making"

# evaluation rpi only
ssh pi@10.0.0.3 "python3.7 -m src.evaluation.evaluation_rpi time 5 robot_only /home/pi/src/smt/sets/evaluation/simple /home/pi/src/smt/sets/evaluation/medium /home/pi/src/smt/sets/evaluation/hard /home/pi/src/smt/sets/evaluation/mixed"

# evaluation cloud only
ssh pi@10.0.0.3 "python3.7 -m src.evaluation.evaluation_rpi time 5 cloud_only /home/pi/src/smt/sets/evaluation/simple /home/pi/src/smt/sets/evaluation/medium /home/pi/src/smt/sets/evaluation/hard /home/pi/src/smt/sets/evaluation/mixed"

# evaluation q_learning
ssh pi@10.0.0.3 "python3.7 -m src.evaluation.evaluation_rpi time 5 q_learning /home/pi/src/smt/sets/evaluation/simple /home/pi/src/smt/sets/evaluation/medium /home/pi/src/smt/sets/evaluation/hard /home/pi/src/smt/sets/evaluation/mixed"

# evaluation dqn
ssh pi@10.0.0.3 "python3.7 -m src.evaluation.evaluation_rpi time 5 dqn /home/pi/src/smt/sets/evaluation/simple /home/pi/src/smt/sets/evaluation/medium /home/pi/src/smt/sets/evaluation/hard /home/pi/src/smt/sets/evaluation/mixed"