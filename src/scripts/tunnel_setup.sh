#!/bin/bash
sudo pppd updetach noauth silent nodeflate pty "/usr/bin/ssh root@128.131.57.123 /usr/sbin/pppd nodetach notty noauth" ipparam vpn 10.10.10.1:10.10.20.1
sudo pppd updetach noauth silent nodeflate pty "/usr/bin/ssh root@128.131.57.122 /usr/sbin/pppd nodetach notty noauth" ipparam vpn 10.10.10.2:10.10.20.2
sudo pppd updetach noauth silent nodeflate pty "/usr/bin/ssh root@128.131.57.103 /usr/sbin/pppd nodetach notty noauth" ipparam vpn 10.10.10.3:10.10.20.3