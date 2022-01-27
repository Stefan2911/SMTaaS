#!/bin/bash
ssh pi@10.0.16 "python3.7 -m src.evaluation.evaluation /home/pi/src/smt/sets/evaluation/simple time 10 robot_only"
ssh pi@10.0.16 "python3.7 -m src.evaluation.evaluation /home/pi/src/smt/sets/evaluation/medium time 10 robot_only"
ssh pi@10.0.16 "python3.7 -m src.evaluation.evaluation /home/pi/src/smt/sets/evaluation/hard time 10 robot_only"
ssh pi@10.0.16 "python3.7 -m src.evaluation.evaluation /home/pi/src/smt/sets/evaluation/mixed time 10 robot_only"