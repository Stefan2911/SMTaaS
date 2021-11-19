# RaspberryPi Setup

processor name: ARMv7 Processor rev 3 (v7l)

Linux raspberrypi 5.10.63-v7l+ #1459 SMP Wed Oct 6 16:41:57 BST 2021 armv7l GNU/Linux

## Install Python 3.7

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

## Monitoring Change:

* There is an issue with root privileges: https://github.com/alessandromaggio/pythonping/issues/27. To solve the issue
  the following steps are necessary:
  * `sudo apt-get install libcap2-bin`
  * `sudo setcap cap_net_raw+ep $(which python3.7)` (depends on used python version)

## PyTorch Installation

`pip3.7 install torch-1.7.0a0-cp37-cp37m-linux_armv7l.whl.whl`

## SMT-Solver installation

1. switch to `src/smt/smt-solver`
2. `pip3.7 install -r requirements.txt`
3. `pysmt-install --cvc4`
4. rename file in `/home/pi/.smt_solvers/CVC5-391ab9df6c3fd9a3771864900c1718534c1e4666`
   to `/home/pi/.smt_solvers/cvc4/CVC4-391ab9df6c3fd9a3771864900c1718534c1e4666` (`mv cvc5-391ab9df6c3fd9a3771864900c1718534c1e4666 CVC4-391ab9df6c3fd9a3771864900c1718534c1e4666`)
5. rerun `pysmt-install --cvc4`
6. go to `~/.smt_solvers/cvc4/CVC4-391ab9df6c3fd9a3771864900c1718534c1e4666/antlr-3.4/src/libantlr3c-3.4`
7. `./configure --prefix=/home/pi/.smt_solvers/cvc4/CVC4-391ab9df6c3fd9a3771864900c1718534c1e4666/antlr-3.4`
8. remove `-m32` from CFLAGS in makefile
9. comment line 167: `/* #define size_t unsigned int */`
   in `/home/.smt_solvers/cvc4/CVC4-391ab9df6c3fd9a3771864900c1718534c1e4666/antlr-3.4/src/libantlr3c-3.4/antlr3config.h`
10. `make`
11. `make install`
12. `sudo apt-get install cmake libgmp3-dev default-jdk`
13. go to directory `~/.smt_solvers/cvc4/CVC4-391ab9df6c3fd9a3771864900c1718534c1e4666`
14. `./configure.sh --antlr-dir=/home/pi/.smt_solvers/cvc4/CVC4-391ab9df6c3fd9a3771864900c1718534c1e4666/antlr-3.4`
15. go to `build`
16. `make install`

