#!/bin/bash
ssh robot@10.0.18 "python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/simple time 10 ded_only;
python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/medium time 10 ded_only;
python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/hard time 10 ded_only;
python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/mixed time 10 ded_only"

ssh pi@10.0.0.16 "./change_latency.sh 50"
ssh pi@10.0.0.19 "./change_latency.sh 50"
ssh robot@10.0.18 "python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/simple time 10 ded_only;
python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/medium time 10 ded_only;
python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/hard time 10 ded_only;
python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/mixed time 10 ded_only"

ssh pi@10.0.0.16 "./change_latency.sh 100"
ssh pi@10.0.0.19 "./change_latency.sh 100"
ssh robot@10.0.18 "python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/simple time 10 ded_only;
python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/medium time 10 ded_only;
python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/hard time 10 ded_only;
python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/mixed time 10 ded_only"

ssh pi@10.0.0.16 "./change_latency.sh 200"
ssh pi@10.0.0.19 "./change_latency.sh 200"
ssh robot@10.0.18 "python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/simple time 10 ded_only;
python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/medium time 10 ded_only;
python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/hard time 10 ded_only;
python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/mixed time 10 ded_only"

ssh pi@10.0.0.16 "./change_latency.sh 300"
ssh pi@10.0.0.19 "./change_latency.sh 300"
ssh robot@10.0.18 "python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/simple time 10 ded_only;
python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/medium time 10 ded_only;
python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/hard time 10 ded_only;
python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/mixed time 10 ded_only"

ssh pi@10.0.0.16 "sudo tc qdisc del dev wlan0 root"
ssh pi@10.0.0.19 "sudo tc qdisc del dev wlan0 root"