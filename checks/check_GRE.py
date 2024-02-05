import time

import sys
import os
sys.path.insert(1, os.path.join(sys.path[0],'..'))
print(sys.path)

import yaml
from constants_trident  import (
    VALUE_CONS_CONNECT,
    CONSOLE,
    NAME_DEV,
)


from cfg_switch import TridentCfg


tr1 = TridentCfg()

def check_status_interf_tunn():
    print("Test 1 \nПроверка ...")
    try:
        temp = tr1.send_command('sh ip interface Tunnel0')
        print(temp)
        if "Status: admin up" in temp:
            print("GRE - enable!")
            return True
        else:
            return False
    except ValueError as err:
        return False

def check_ip_interf_tunn():
    print("Test 1 \nПроверка ...")
    try:
        temp = tr1.send_command('sh ip interface Tunnel0')
        print(temp)
        if "IP address: 192.168.0.1" in temp:
            print("ip ok")
            return True
        else:
            return False
    except ValueError as err:
        return False   

def check_ip_interf_tunn(ip_for_ping):
    print("Test 1 \nПроверка ...")
    try:
        temp = tr1.ping_inet_extended(ip_for_ping=ip_for_ping)
        if "min/avg/max/mdev" in temp:
            CONSOLE.print("Interface availeble ",style="success")
            return True
        else:
            CONSOLE.print("Interface is not available ",style='fail')
            return False
    except ValueError as err:
        return False

if __name__ == "__main__":
    result = check_ip_interf_tunn(ip_for_ping="192.168.0.2")
    print(result)