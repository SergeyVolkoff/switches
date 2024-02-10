import re
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

def check_ver_platform():
    print("Test 1 \nПроверка платформы:")
    try:
        temp = tr1.ssh.send_command('show version')
        temp1 = re.search(r'Platform\s+:\s+(?P<ver_Platform>\S+)',temp)
        ver_Platform=temp1.group('ver_Platform')
        if "BS7510-48" in ver_Platform:
            CONSOLE.print(f"Platform is {ver_Platform}, its - ok! ",style="success" )
            print("")
            return True
        else:
            CONSOLE.print(f"Version platform wrong - {ver_Platform}! ", temp, style='fail')
            return False
    except ValueError as err:
        return False

def check_ver_fw():
    print("Test 2 \nПроверка версии прошивки:")
    try:
        temp = tr1.ssh.send_command('show version')
        temp1 = re.search(r'NOS version\s+:\s+(?P<ver_FW>\S+)',temp)
        ver_FW=temp1.group('ver_FW')
        if "2.5.0" in ver_FW:
            CONSOLE.print(f"Version FW is {ver_FW}, its - ok ",style="success" )
            print("")
            return True
        else:
            CONSOLE.print(f"Firmware version different from the test - {ver_FW}!", temp, style='fail')
            return False
    except ValueError as err:
        return False

def check_status_interf_tunn():
    print("Test 3 \nПроверка статуса туннеля GRE:")
    try:
        temp = tr1.ssh.send_command('sh ip interface Tunnel0')
        temp1 = re.search(r'Interface Status:\s+link\s+(?P<link_stts>\S+)/admin\s+(?P<admin_stts>\S+)',temp)
        link_stts=temp1.group('link_stts')
        admin_stts=temp1.group('admin_stts')
        temp1 = re.search(r'Interface Status:\s+(?P<interface_stts>\S.*)',temp)
        interface_stts = temp1.group('interface_stts')
        if admin_stts == 'up' and link_stts == 'up':
            CONSOLE.print(f"Interface Tunnel0 status is: {interface_stts}, its - ok!",style="success")
            return True
        else:
            CONSOLE.print(f"Interface Tunnel0 status wrong, is - {interface_stts} ",style='fail')
            return False
    except ValueError as err:
        return False

def check_ip_interf_tunn():
    print("Test 4 \nПроверка назначенного ip-адреса туннелю на DUT :")
    try:
        temp = tr1.ssh.send_command('sh ip interface Tunnel0')
        temp1 = re.search(r'IP address\S\s+(?P<ip_tunn>\d+\S\d+\S\d+\S\d+)',temp)
        ip_tunn=temp1.group('ip_tunn')
        if ip_tunn == '192.168.0.1' in ip_tunn:
            CONSOLE.print(f"Ip address tunn {ip_tunn}, its ok",style="success")
            return True
        else:
            CONSOLE.print(f"Ip address tunn {ip_tunn}, fail!",style="fail")
            return False
    except ValueError as err:
        return False  
        
def check_availebel_ip(ip_for_ping):
    print("Test 5 \nПроверка доступности интерфейсов в схеме теста:")
    try:
        temp = tr1.ping_inet_extended(ip_for_ping=ip_for_ping)
        if "min/avg/max/mdev" in temp:
            CONSOLE.print(f"Interface with ip {ip_for_ping} availeble now",style="success")
            return True
        else:
            CONSOLE.print("Interface with ip {ip_for_ping } is not available now ",style='fail')
            return False
    except ValueError as err:
        return False

def check_tracert_tunnUp(ip_dest):
    # ip_dest = '192.168.0.2'
    print("Test 6 \nПроверка, что трассировка с DUT до хопа за тоннеленм уходит в тоннель") 
    result_trcert = tr1.tracert_ip_izi(ip_dest)
    if ip_dest in result_trcert and 'ms' in result_trcert :
        CONSOLE.print (f"\n Трасерт до хопа {ip_dest} идет через тоннель: \n{result_trcert}",style='success')
        return True
    else:
        CONSOLE.print(f'\nТрасерт FAIL : \n{result_trcert}',style='fail')
        return False

if __name__ == "__main__":
    result = check_tracert_tunnUp(ip_dest='2.2.2.2')
    print(result)