# EV3

### Global Installation steps:

* `pip3.9 install -r requirements.txt`

### Monitoring EV3

In the following there is a short description about system states, which act as parameters for our decision making
algorithm.

##### Installation steps:

* There is an issue with root privileges: https://github.com/alessandromaggio/pythonping/issues/27. To solve the issue
  the following steps are necessary:
    * `sudo apt-get install libcap2-bin`
    * `sudo setcap cap_net_raw+ep $(which python3.9)` (depends on used python version)

#### Battery Level

To get the information about the battery level, we use the generic interface PowerSupply.
See: https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/power-supply.html

The `psutil` module also provides a possibility to get information about the battery level. But these functions are not
supported by the EV3 system.

#### Connectivity

##### speedtest

The `speedtest` module provides methods to get information about the upload and download speed. Due to the limited EV3
system the following error occurs and `pythonping` is the way to go.

Error: `speedtest.SpeedtestCLIError: Insufficient memory to pre-allocate upload data. Please use --no-pre-allocate`

##### pythonping (the way to go)

There are two additional installation steps necessary (see installation steps above). The function delivers the average
round trip time (rtt).

#### System Utilization

The `psutil` module provides information about CPU usage etc. See: https://psutil.readthedocs.io/en/latest/

## CVC4 - Installation on EV3

To install CVC4 multiple steps are necessary, which are explained in the following.

### Cross-Compiling

To create the CVC4 binary I did a cross-compiling-procedure with the provided docker container:
https://www.ev3dev.org/docs/tutorials/using-docker-to-cross-compile/

1. `sudo apt-get update`
2. `export CC=arm-linux-gnueabi-gcc `
3. `export CXX=arm-linux-gnueabi-g++`
4. `sudo apt-get install python3:armel`
5. `sudo apt-get install libgmp3-dev:armel`
6. `sudo apt install python-pip`
7. `pip install toml`
8. `sudo apt install default-jdk:armel`
9. Cross-compile antlr
   dependency: `./configure CC=arm-linux-gnueabi-gcc CXX=arm-linux-gnueabi-g++ --prefix=/src/LIBANTLR3C_INSTALL_DIR`
10. `./configure.sh production --antlr-dir=/src/LIBANTLR3C_INSTALL_DIR/libantlr3c-3.4 --gmp-dir=/usr/lib/arm-linux-gnueabi --static --static-binary`

For details see: https://hackmd.io/@EzPfmI1gT8S-9pvnJOhNlg/Skago80uO

# Edge

## RaspberryPi Setup

processor name: ARMv7 Processor rev 3 (v7l)

Linux raspberrypi 5.10.63-v7l+ #1459 SMP Wed Oct 6 16:41:57 BST 2021 armv7l GNU/Linux

### Install Python 3.7

For the armv7l architecture there are only prebuilt pytorch packages for python 3.7 or lower. The default python version
of RaspbianOS is 3.9. Therefore we need to install Python3.7.

1. `sudo apt update`
2. `sudo apt-get install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev`
3. `sudo apt-get install libopenblas-dev libblas-dev m4 cmake python3-dev python3-yaml python3-setuptools libffi-dev libatlas-base-dev`
4. `python3.7 -m pip install --upgrade pip`
5. `wget https://www.python.org/downloads/release/python-3712/`
6. `tar -zxvf Python-3.7.12.tgz`
7. `cd Python-3.7.12`
8. `./configure --enable-optimizations`
9. `sudo make altinstall`
10. `pip3.7 install -r requirements.txt`

### Monitoring Change:

* There is an issue with root privileges: https://github.com/alessandromaggio/pythonping/issues/27. To solve the issue
  the following steps are necessary:
    * `sudo apt-get install libcap2-bin`
    * `sudo setcap cap_net_raw+ep $(which python3.7)` (depends on used python version)

### PyTorch Installation

`pip3.7 install torch-1.7.0a0-cp37-cp37m-linux_armv7l.whl.whl`

### SMT-Solver installation

`sudo apt install cvc4`

# Cloud

### Setup

1. Connect via ssh
2. `sudo apt-get update`
3. `sudo apt install docker.io`
4. `sudo docker pull stefanh96/master-thesis:latest`
5. `sudo docker run -p 5000:5000 stefanh96/master-thesis:latest`
6. Open necessary ports to make service reachable remotely

# Evaluation

* Copy/Deploy evaluation & training sets on robot

### Robot only (Edge only)

1. Start on robot: `python3 -m src.evaluation.edge_only <problem-directory> <set repitition>`
    * e.g. `python3 -m src.evaluation.edge_only /home/robot/develop/src/smt/sets/evaluation/simple 10`

### Dedicated Edge Device (DED only / RaspberryPi only)

1. Define instances in always_offload.py
2. RaspberryPi's:
    * Set `solver-location` in `src/smt/smt_solver/config/config.yaml` to `/usr/bin/cvc4`
    * Set `final-node` in `src/smt/smt_solver/config/config.yaml` to `True`
    * Start: `python3.7 -m src.smt.smt_solver.native.main`
3. Start on robot: `python3 -m src.evaluation.always_offload <problem-directory> <set repitition>`
    * e.g. `python3 -m src.evaluation.always_offload /home/robot/develop/src/smt/sets/evaluation/simple 10`

### Cloud only

1. Define instances in always_offload.py
2. Start on Cloud-VMs: `sudo docker run stefanh96/master-thesis:latest`
3. Start on robot `python3 -m src.evaluation.always_offload <problem-directory> <set repitition>`
    * e.g. `python3 -m src.evaluation.always_offload /home/robot/develop/src/smt/sets/evaluation/simple 10`

### Q-Learning

1. Define model in `src/decision/reinforcement_learning/config.yaml`
2. Upload config `src/decision/reinforcement_learning/config.yaml` to RaspberryPis and EV3
3. Set `solver/instances` in `src/decision/reinforcement_learning/config.yaml` on RaspberryPis and EV3
4. RaspberryPi's:
    * Set `solver-location` in `src/smt/smt_solver/config/config.yaml` to `/usr/bin/cvc4`
    * Set `final-node` in `src/smt/smt_solver/config/config.yaml` to `False`
    * Set `decision-mode` in `src/smt/smt_solver/config/config.yaml` to `q-learning`
    * Start: `python3.7 -m src.smt.smt_solver.native.main`
5. Start on Cloud-VMs: `sudo docker run stefanh96/master-thesis:latest`
6. Start on robot: `python3 -m src.evaluation.always_offload <problem-directory> <set repitition> <decision-mode>`
    * e.g. `python3 -m src.evaluation.with_decision /home/robot/develop/src/smt/sets/evaluation/simple 10 q_learning`

### Q-Learning (EV3) & DQN (RaspberryPis)

1. Define model in `src/decision/reinforcement_learning/config.yaml`
2. Upload config `src/decision/reinforcement_learning/config.yaml` to RaspberryPis and EV3
3. Set `solver/instances` in `src/decision/reinforcement_learning/config.yaml` on RaspberryPis and EV3
4. RaspberryPi's:
    * Set `solver-location` in `src/smt/smt_solver/config/config.yaml` to `/usr/bin/cvc4`
    * Set `final-node` in `src/smt/smt_solver/config/config.yaml` to `False`
    * Set `decision-mode` in `src/smt/smt_solver/config/config.yaml` to `deep_q_network`
    * Start: `python3.7 -m src.smt.smt_solver.native.main`
5. Start on Cloud-VMs: `sudo docker run stefanh96/master-thesis:latest`
6. Start on robot: `python3 -m src.evaluation.always_offload <problem-directory> <set repitition> <decision-mode>`
    * e.g. `python3 -m src.evaluation.with_decision /home/robot/develop/src/smt/sets/evaluation/simple 10 q_learning`