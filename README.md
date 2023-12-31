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

#### Ubuntu based VM:

1. Connect via ssh
2. `sudo apt-get update`
3. `sudo apt install docker.io`
4. `sudo docker pull <imagename>`
5. `sudo docker run -p 5000:5000 <imagename>`
6. Open necessary ports to make service reachable remotely

#### CentOS based VM:

1. Connect via ssh
2. `sudo yum update`
3. `sudo yum install docker`
4. (Maybe necessary: `systemctl start docker`)
5. `sudo docker pull <imagename>` and select docker.io repository
6. `sudo docker run -p 5000:5000 <imagename>`
7. `sudo systemctl disable --now firewalld.service`

### VM's

1. Install ppp on RaspberryPi's/EV3: `sudo apt-get install ppp`
2. `sudo pppd updetach noauth silent nodeflate pty "/usr/bin/ssh root@128.131.57.123 /usr/sbin/pppd nodetach notty noauth" ipparam vpn 10.10.10.1:10.10.20.1`
3. `sudo pppd updetach noauth silent nodeflate pty "/usr/bin/ssh root@128.131.57.122 /usr/sbin/pppd nodetach notty noauth" ipparam vpn 10.10.10.2:10.10.20.2`
4. `sudo pppd updetach noauth silent nodeflate pty "/usr/bin/ssh root@128.131.57.103 /usr/sbin/pppd nodetach notty noauth" ipparam vpn 10.10.10.3:10.10.20.3`

On other RPi use:

1. `sudo pppd updetach noauth silent nodeflate pty "/usr/bin/ssh root@128.131.57.123 /usr/sbin/pppd nodetach notty noauth" ipparam vpn 10.10.10.4:10.10.20.4`
2. `sudo pppd updetach noauth silent nodeflate pty "/usr/bin/ssh root@128.131.57.122 /usr/sbin/pppd nodetach notty noauth" ipparam vpn 10.10.10.5:10.10.20.5`
3. `sudo pppd updetach noauth silent nodeflate pty "/usr/bin/ssh root@128.131.57.103 /usr/sbin/pppd nodetach notty noauth" ipparam vpn 10.10.10.6:10.10.20.6`

To kill processes: `sudo pkill -f pppd`

It is important that IP addresses are not used twice!

# Evaluation

### Get information about setup

* Get information about RAM: `cat /proc/meminfo`
* Get information about disk space: `df -h`
* Get information about CPU('s): `cat /proc/cpuinfo` or `lscpu`
* Get information about OS: `cat /etc/os-release` and `cat /proc/version`

### General

* Copy/Deploy evaluation & training sets on robot
* Configuration file is located in: `src/config/config.yaml`
* Set `smt.solver-location` to solver location e.g. `/usr/bin/cvc4`
* Set `monitoring.connectivity.hosts` to hosts which are randomly chosen for connectivity check (possible improvement
  would be to add a state for each offload instance)
* Set `evaluation.cloud-instances` and `evaluation.ded-instances`
* Set `smt.decision-mode` to `q_learning` or `deep_q_network`

### Evaluation CLI on robot:

`python3 -m src.evaluation.evaluation <problem-directories> <goal> <set repetition> <approach>`
Goals: `time`
Approaches: `robot_only`, `ded_only`, `cloud_only`, `q_learning`
If goal is `time` 3rd parameter is set repetition

### Evaluation CLI on RPi's:

`python3 -m src.evaluation.evaluation_rpi <problem-directories> <goal> <set repetition> <approach>`
Goals: `time`
Approaches: `rpi_only`, `cloud_only`, `q_learning`, `dqn`
If goal is `time` 3rd parameter is set repetition

### Evaluation automation:

Use scripts in `sm/scripts`. You need to copy public key to not have to enter the password:
`cat C:\Users\Acer\.ssh\id_rsa.pub | ssh user@host 'cat >> .ssh/authorized_keys'`

### Robot only (Edge only)

1.
   1. Goal time: Start on
      robot: `python3 -m src.evaluation.evaluation time <set repetition> robot_only <problem-directories>`
      * e.g. `python3 -m src.evaluation.evaluation time 5 robot_only /home/robot/src/smt/sets/evaluation/simple `

### Dedicated Edge Device (DED only / RaspberryPi only)

1. Configure instances `evaluation.ded-instances`
2. RaspberryPi's:
   * Set `smt.decision-mode` to `None`
   * Start: `python3.7 -m src.smt.smt_solver.native.main`
3.
   1. Goal time: Start on
      robot `python3 -m src.evaluation.evaluation_rpi time <set repetition> ded_only <problem-directories> `
      * e.g. `python3 -m src.evaluation.evaluation_rpi time 5 ded_only /home/robot/src/smt/sets/evaluation/simple`

### Cloud only

1. Configure instances `evaluation.cloud-instances`
2. Start on Cloud-VMs: `sudo docker run <imagename>`
3.
   1. Goal time: Start on
      robot `python3 -m src.evaluation.evaluation time <set repetition> cloud_only <problem-directories>`
      *
      e.g. `python3 -m src.evaluation.evaluation time 5 cloud_only /home/robot/src/smt/sets/evaluation/simple`

### Q-Learning

1. Configure model
3. Set `decision.reinforcement-learning.solver.instances` on RaspberryPis and EV3
5. RaspberryPi's:
   * Set `smt.decision-mode` to `None`
   * Set `smt.decision-mode` to `q-learning`
   * Start: `python3.7 -m src.smt.smt_solver.native.main`
6. Start on Cloud-VMs: `sudo docker run <imagename>`
7.
   1. Goal time: Start on
      robot: `python3 -m src.evaluation.evaluation time <set repetition> q_learning <problem-directories>`
      *
      e.g. `python3 -m src.evaluation.evaluation /home/robot/src/smt/sets/evaluation/simple time 5 q_learning`

### Q-Learning (EV3) & DQN (RaspberryPis)

1. Define reward model `decision.reinforcement-learning.reward-modes`
2. Set `decision.reinforcement-learning.solver.insftances` on RaspberryPis and EV3
3. RaspberryPi's:
   * Set `smt.decision-mode` to `None`
   * Set `smt.decision-mode` to `deep_q_network`
   * Start: `python3.7 -m src.smt.smt_solver.native.main`
4. Start on Cloud-VMs: `sudo docker run <imagename>`
5.
   1. Goal time: Start on
      robot: `python3 -m src.evaluation.evaluation time <set repetition> q_learning <problem-directories>`
      *
      e.g. `python3 -m src.evaluation.evaluation time 5 q_learning /home/robot/src/smt/sets/evaluation/simple`

### Training Q-Learning

1. Define reward model `decision.reinforcement-learning.reward-modes`
2. Define hyper parameters `decision.reinforcement-learning.common-hyper-parameters`
3. Set training set: `decision.training-smt-problem-directory-edge` / `decision.training-smt-problem-directory-robot`
4.
   * On robot: `python3 -m src.decision.reinforcement_learning.q_learning.decision_making`
   * On RaspberryPi: `python3.7 -m src.decision.reinforcement_learning.q_learning.decision_making`

Printing Q-Table on EV3/RaspberryPi:

1. `python3` (EV3), `python3.7` (RaspberryPi)
2. `import numpy as np`
3. `print(np.load("src/decision/reinforcement_learning/q_learning/q_table.npy"))`

### Training DQN

1. Define reward model `decision.reinforcement-learning.reward-modes`
2. Define hyper parameters `decision.reinforcement-learning.common-hyper-parameters`
3. Define dqn specific hyper parameters `decision.reinforcement-learning.deep-q-network.hyper-parameters`
4. Set training set: `decision.training-smt-problem-directory-edge` / `decision.training-smt-problem-directory-robot`
5. On RaspberryPi: `python3.7 -m src.decision.reinforcement_learning.deep_q_network.decision_making` (DQN on EV3 not
   possible)

Printing DQN on EV3/RaspberryPi:

1. `python3.7` (RaspberryPi)
2. `import torch`
3. `print(torch.load("src/decision/reinforcement_learning/deep_q_network/neural_network"))`

## Simulation

#### Latency (application level) - recommended

We use the module simulation.py which is called in training and evaluation. The latency is randomly set and the
additional response time is calculated with additional_latency * 0.005

### Latency (netem level)

#### RPI's

The following latency simulation is based on netem

Add latency:
`sudo tc qdisc add dev eth0 root netem delay <additional latency>ms`
Delete latency:
`sudo tc qdisc delete dev eth0 root netem delay <additional latency>ms`
Delete all rules:
`sudo tc qdisc del dev eth0 root`

Add latency IP-specific:

1. `sudo tc qdisc add dev eth0 root handle 1: prio`
2. `sudo tc qdisc add dev eth0 parent 1:3 handle 30: netem delay <additional latency>ms`
3. `sudo tc filter add dev eth0 protocol ip parent 1:0 prio 3 u32 match ip dst <ip>/32 flowid 1:3`

Or call created script: `./change_latency.sh <latency>ms`

#### Cloud

Same as for RaspberryPi but use `eth0` as device for external VM and `ens3` for VM's Additional steps for VM's:

1. `sudo yum install iproute-tc`
2. `sudo yum install -y kernel-modules-extra` (not that easy, you need to download correct rpm file for used kernel
   version, see `uname -r` and install downloaded file with `sudo yum localinstall`)
3. `sudo modprobe sch_netem`

# Module Architecture

[pydeps](https://pydeps.readthedocs.io/en/latest/)  is a tool to visualize python module dependencies. The following
command can be used to show the dependencies of this project:
`pydeps --cluster --min-cluster-size=2 --max-cluster-size=3 --keep-target-cluster .\src\ -x src.slam --rmprefix src. --reverse --noise-level 1`
     