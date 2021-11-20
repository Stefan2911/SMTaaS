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

`sudo apt install cvc4`
