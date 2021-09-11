# Monitoring EV3

In the following there is a short description about system states, which act as parameters for our decision making
algorithm.

## Installation steps:

* `pip3 install -r requirements.txt`
* There is an issue with root privileges: https://github.com/alessandromaggio/pythonping/issues/27. To solve the issue
  the following steps are necessary:
  * `sudo apt-get install libcap2-bin`
  * `sudo setcap cap_net_raw+ep $(which python3.5)`

## Battery Level

To get the information about the battery level, we use the generic interface PowerSupply.
See: https://ev3dev-lang.readthedocs.io/projects/python-ev3dev/en/stable/power-supply.html

The `psutil` module also provides a possibility to get information about the battery level. But these functions are not
supported by the EV3 system.

## Connectivity

## speedtest

The `speedtest` module provides methods to get information about the upload and download speed. Due to the limited EV3
system the following error occurs and `pythonping` is the way to go.

Error: `speedtest.SpeedtestCLIError: Insufficient memory to pre-allocate upload data. Please use --no-pre-allocate`

## pythonping (the way to go)

There are two additional installation steps necessary (see installation steps above). The function delivers the average
roundtrip time (rtt).

## System Utilization

The `psutil` module provides information about CPU usage etc. See: https://psutil.readthedocs.io/en/latest/
