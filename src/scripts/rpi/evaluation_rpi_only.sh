#!/bin/bash
ssh pi@10.0.0.3 "python3.7 -m src.evaluation.evaluation time 10 robot_only /home/pi/src/smt/sets/evaluation/simple /home/pi/src/smt/sets/evaluation/medium /home/pi/src/smt/sets/evaluation/hard /home/pi/src/smt/sets/evaluation/mixed"