import time

import sys
import os
sys.path.insert(1, os.path.join(sys.path[0],'..'))
# print(sys.path)

import yaml
from constants_trident  import (
    VALUE_CONS_CONNECT,
    CONSOLE,
    NAME_DEV,
)


from cfg_switch import TridentCfg


tr1 = TridentCfg()

def check_ver_fw():
    print("Test 3 \nПроверка версии прошивки")
    try:
        temp = tr1.send_command('show version')
        if "2.5.0-rc0" in temp:
            CONSOLE.print("Version of FW 2.5 or higher",temp, style="success" )
            print("")
        else:
            CONSOLE.print("Firmware version lower than 2.5 ", temp, style='fail')
            return False
    except ValueError as err:
        return False


def check_status_interf_tunn():
    print("Test 1 \nПроверка ...")
    try:
        temp = tr1.send_command('sh ip interface Tunnel0')
        print(temp)
        if "Status: admin up" in temp:
            CONSOLE.print("GRE - enable!",style="success")
            return True
        else:
            CONSOLE.print("Interface is not available ",style='fail')
            return False
    except ValueError as err:
        return False

def check_ip_interf_tunn():
    print("Test 1 \nПроверка ...")
    try:
        temp = tr1.send_command('sh ip interface Tunnel0')
        print(temp)
        if "IP address: 192.168.0.1" in temp:
            CONSOLE.print("Ip ok",style="success")
            return True
        else:
            CONSOLE.print("Ip fail!",style="fail")
            return False
    except ValueError as err:
        return False   

def check_availebel_ip(ip_for_ping):
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
    result = check_ver_fw()
    print(result)