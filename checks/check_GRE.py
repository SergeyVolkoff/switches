import allure
import re
import time
import sys
import os
import yaml
sys.path.insert(1, os.path.join(sys.path[0],'..'))
# print(sys.path)
from constants_trident  import (
    VALUE_CONS_CONNECT,
    NAME_DEV,
)
from cfg_switch import TridentCfg
from connect import Connect


tr1 = Connect()
tr1.check_connection(VALUE_CONS_CONNECT)

def check_ver_platform():
    print("Test 1", "Проверка платформы:", sep='\n')
    try:
        with allure.step('Отправка команды на просмотр версии платформы.'):
            temp = tr1.ssh.send_command('show version')
        temp1 =  re.search(r'Platform\s+:\s+(?P<ver_Platform>\S+)',temp)
        ver_Platform=temp1.group('ver_Platform')
        with allure.step('Сверка версии платформы - ожидается "BS7510-48".'):
            if "BS7510-48" in ver_Platform:
                print(f'Platform is {ver_Platform}, its - ok! ')
                print("")
                return True
            else:
                print(f"Version platform wrong - {ver_Platform}! ")
                return False
    except ValueError as err:
        return False

def check_ver_fw():
    print("Test 2", "Проверка версии прошивки:", sep='\n')
    try:
        with allure.step('Отправка команды на просмотр версии прошивки.'):
            temp = tr1.ssh.send_command('show version')
            temp1 = re.search(r'NOS version\s+:\s+(?P<ver_FW>\S+)',temp)
            ver_FW=temp1.group('ver_FW')
        with allure.step('Сверка версии прошивки - ожидается "2.5.0".'):
            if "2.5.0" in ver_FW:
                print(f'Version FW is {ver_FW}, its - ok. ')
                print("")
                return True
            else:
                print(f'Firmware version different from the test - {ver_FW}!')
                return False
    except ValueError as err:
        return False

def check_status_interf_tunn():
    print("Test 3", "Проверка статуса туннеля GRE:", sep='\n')
    try:
        with allure.step('Отправка команды на просмотр статуса туннеля GRE.'):
            temp = tr1.ssh.send_command('sh ip interface Tunnel0')
        temp1 = re.search(r'Interface Status:\s+link\s+(?P<link_stts>\S+)/admin\s+(?P<admin_stts>\S+)',temp)
        link_stts=temp1.group('link_stts')
        admin_stts=temp1.group('admin_stts')
        temp1 = re.search(r'Interface Status:\s+(?P<interface_stts>\S.*)',temp)
        interface_stts = temp1.group('interface_stts')
        with allure.step('Сверка состояния тоннеля - ожидается, что admin и link должны быть up.'):
            if admin_stts == 'up' and link_stts == 'up':
                print(f'Interface Tunnel0 status is: {interface_stts}, its - ok!')
                return True
            else:
                print(f'Interface Tunnel0 status wrong, is - {interface_stts}')
                return False
    except ValueError as err:
        return False

def check_ip_interf_tunn():
    print("Test 4", "Проверка назначенного ip-адреса туннелю на DUT :", sep='\n')
    try:
        with allure.step('Отправка команды на просмотр статуса туннеля GRE.'):
            temp = tr1.ssh.send_command('sh ip interface Tunnel0')
        temp1 = re.search(r'IP address\S\s+(?P<ip_tunn>\d+\S\d+\S\d+\S\d+)',temp)
        ip_tunn=temp1.group('ip_tunn')
        with allure.step('Сверка Ip address присвоенного интерфейсу тоннеля DUT - ожидается 192.168.0.1'):
            if ip_tunn == '192.168.0.1' in ip_tunn:
                print(f'Ip address tunn {ip_tunn}, its ok')
                return True
            else:
                print(f'Ip address tunn {ip_tunn}, fail!')
                return False
    except ValueError as err:
        return False  
        
def check_availebel_ip(ip_for_ping):
    print("Test 5", "Проверка доступности интерфейсов в схеме теста:", sep='\n')
    try:
        with allure.step(f'Отправка команды ping для проверки доступности интерфейса {ip_for_ping}'):
            temp = tr1.ping_inet_extended(ip_for_ping=ip_for_ping)
        with allure.step('Проверка, что есть обмен пакетами - ожидаем в ответе min/avg/max/mdev время отклика '):
            if "min/avg/max/mdev" in temp:
                print(f'Interface with ip {ip_for_ping} availeble now')
                return True
            else:
                print("Interface with ip {ip_for_ping } is not available now ")
                return False
    except ValueError as err:
        return False

def check_tracert_tunnUp(ip_dest):
    ip_for_check = '192.168.0.2'
    print("Test 6", "Проверка, что трассировка с DUT до хопа за тоннелем уходит в тоннель", sep='\n')
    with allure.step('Отправка команды tracert для проверки'):
        result_trcert = tr1.tracert_ip_izi(ip_dest)
    with allure.step(f'Проверка, что трасерт до {ip_dest} проходит через туннель - в выводе должен быть ip туннеля.'):
        if ip_dest in result_trcert and 'ms' in result_trcert :
            print (f'\nТрасерт до хопа {ip_dest} идет через тоннель: \n{result_trcert}')
            return True
        else:
            print(f'\nТрасерт FAIL : \n{result_trcert}')
            return False

if __name__ == "__main__":
    result = check_tracert_tunnUp(ip_dest='2.2.2.2')
    print(result)