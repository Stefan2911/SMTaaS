#!/bin/bash
ssh robot@10.0.18 "python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/simple time 10 robot_only"
ssh robot@10.0.18 "python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/medium time 10 robot_only"
ssh robot@10.0.18 "python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/hard time 10 robot_only"
ssh robot@10.0.18 "python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/mixed time 10 robot_only"