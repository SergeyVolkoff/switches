import time

import sys
import os
import yaml
sys.path.insert(1, os.path.join(sys.path[0],'..'))
# print(sys.path)


from constants_trident  import (
    VALUE_CONS_CONNECT,
    CONSOLE,
    NAME_DEV,
)
from cfg_switch import TridentCfg
from connect import Connect

tr1 = Connect()
tr1.check_connection(VALUE_CONS_CONNECT)
def check_ver_fw():
    print("Test 1 \nПроверка версии прошивки")
    try:
        temp = tr1.ssh.send_command('show version')
        if "2.5.0-rc0" in temp:
            CONSOLE.print("Version of FW 2.5 or higher",temp, style="success" )
            print("")
            return True
        else:
            CONSOLE.print("Firmware version lower than 2.5 ", temp, style='fail')
            return False
    except ValueError as err:
        return False


def check_status_interf_tunn():
    print("Test 2 \nПроверка статуса туннеля")
    try:
        temp = tr1.ssh.send_command('sh ip interface Tunnel0')
        print(temp)
        if "Interface Status: link up/admin up" in temp:
            CONSOLE.print("GRE - enable!",style="success")
            return True
        else:
            CONSOLE.print("Interface is not available ",style='fail')
            return False
    except ValueError as err:
        return False

def check_ip_interf_tunn():
    print("Test 3 \nПроверка назначенного ip-адреса на DUT туннелю")
    try:
        temp = tr1.ssh.send_command('sh ip interface Tunnel0')
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
    print("Test 4 \nПроверка доступности интерфейсов в схеме теста")
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