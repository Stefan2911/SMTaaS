#!/bin/bash
ssh robot@10.0.18 "python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/simple time 10 cloud_only;
python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/medium time 10 cloud_only;
python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/hard time 10 cloud_only;
python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/mixed time 10 cloud_only"

ssh ubuntu@194.182.171.9 "sudo tc qdisc add dev eth0 root netem delay 50ms"
ssh -t pantelis@128.131.57.103 "sudo tc qdisc add dev ens3 root netem delay 50ms"
ssh -t pantelis@128.131.57.122 "sudo tc qdisc add dev ens3 root netem delay 50ms"
ssh -t pantelis@128.131.57.123 "sudo tc qdisc add dev ens3 root netem delay 50ms"
ssh robot@10.0.18 "python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/simple time 10 cloud_only;
python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/medium time 10 cloud_only;
python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/hard time 10 cloud_only;
python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/mixed time 10 cloud_only"
ssh ubuntu@194.182.171.9 "sudo tc qdisc delete dev eth0 root netem delay 50ms"
ssh -t pantelis@128.131.57.103 "sudo tc qdisc delete dev ens3 root netem delay 50ms"
ssh -t pantelis@128.131.57.122 "sudo tc qdisc delete dev ens3 root netem delay 50ms"
ssh -t pantelis@128.131.57.123 "sudo tc qdisc delete dev ens3 root netem delay 50ms"

ssh ubuntu@194.182.171.9 "sudo tc qdisc add dev eth0 root netem delay 100ms"
ssh -t pantelis@128.131.57.103 "sudo tc qdisc add dev ens3 root netem delay 100ms"
ssh -t pantelis@128.131.57.122 "sudo tc qdisc add dev ens3 root netem delay 100ms"
ssh -t pantelis@128.131.57.123 "sudo tc qdisc add dev ens3 root netem delay 100ms"
ssh robot@10.0.18 "python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/simple time 10 cloud_only;
python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/medium time 10 cloud_only;
python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/hard time 10 cloud_only;
python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/mixed time 10 cloud_only"
ssh ubuntu@194.182.171.9 "sudo tc qdisc delete dev eth0 root netem delay 100ms"
ssh -t pantelis@128.131.57.103 "sudo tc qdisc delete dev ens3 root netem delay 100ms"
ssh -t pantelis@128.131.57.122 "sudo tc qdisc delete dev ens3 root netem delay 100ms"
ssh -t pantelis@128.131.57.123 "sudo tc qdisc delete dev ens3 root netem delay 100ms"

ssh ubuntu@194.182.171.9 "sudo tc qdisc add dev eth0 root netem delay 200ms"
ssh -t pantelis@128.131.57.103 "sudo tc qdisc add dev ens3 root netem delay 200ms"
ssh -t pantelis@128.131.57.122 "sudo tc qdisc add dev ens3 root netem delay 200ms"
ssh -t pantelis@128.131.57.123 "sudo tc qdisc add dev ens3 root netem delay 200ms"
ssh robot@10.0.18 "python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/simple time 10 cloud_only;
python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/medium time 10 cloud_only;
python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/hard time 10 cloud_only;
python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/mixed time 10 cloud_only"
ssh ubuntu@194.182.171.9 "sudo tc qdisc delete dev eth0 root netem delay 200ms"
ssh -t pantelis@128.131.57.103 "sudo tc qdisc delete dev ens3 root netem delay 200ms"
ssh -t pantelis@128.131.57.122 "sudo tc qdisc delete dev ens3 root netem delay 200ms"
ssh -t pantelis@128.131.57.123 "sudo tc qdisc delete dev ens3 root netem delay 200ms"

ssh ubuntu@194.182.171.9 "sudo tc qdisc add dev eth0 root netem delay 300ms"
ssh -t pantelis@128.131.57.103 "sudo tc qdisc add dev ens3 root netem delay 300ms"
ssh -t pantelis@128.131.57.122 "sudo tc qdisc add dev ens3 root netem delay 300ms"
ssh -t pantelis@128.131.57.123 "sudo tc qdisc add dev ens3 root netem delay 300ms"
ssh robot@10.0.18 "python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/simple time 10 cloud_only;
python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/medium time 10 cloud_only;
python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/hard time 10 cloud_only;
python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/mixed time 10 cloud_only"
ssh ubuntu@194.182.171.9 "sudo tc qdisc delete dev eth0 root netem delay 300ms"
ssh -t pantelis@128.131.57.103 "sudo tc qdisc delete dev ens3 root netem delay 300ms"
ssh -t pantelis@128.131.57.122 "sudo tc qdisc delete dev ens3 root netem delay 300ms"
ssh -t pantelis@128.131.57.123 "sudo tc qdisc delete dev ens3 root netem delay 300ms"