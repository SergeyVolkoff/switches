import pytest
import pytest_html
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0],'..'))
# print(sys.path)
from checks.check_GRE import *


def test_check_ver_fw_on_DUT():
    assert check_ver_fw()==True, "Firmware version lower than 2.5!"

def test_check_ip_interf_tunn_on_DUT():
    assert check_ip_interf_tunn()==True, "Ip configured wrong!"

def test_check_status_interf_tunn_on_DUT():
    assert check_status_interf_tunn()==True, "Interface is not available "


"""
В блоке ниже используется параметризация 
"""
ip_for_check = (
    ('192.168.0.1'),
    ('192.168.0.2'),
    ('200.200.200.1'),
    ('200.200.200.2'),
    ('100.100.100.1'),
    ('100.100.100.2'),
    ('1.1.1.1'),
    ('2.2.2.2'),
)

task_ids = ['ip_test({})'.format(t)
             # определям параметр ids чтобы сделать идентификаторы для понимания вывода теста
            for t in ip_for_check
            ]
@pytest.mark.parametrize("ip_test",ip_for_check,ids=task_ids)
            #("ip_test",ip_for_check,ids=task_ids)
            # используем параметризацию,
            # передаем в нее первый аргумент parametrize() — это строка с разделенным
            # запятыми списком имен — "ip_test" в нашем случае,
            # переменную указывающую на данные для проверки (ip_for_check) и ids

def test_check_availebel_ip_from_DUT(ip_test,):
    assert check_availebel_ip(ip_for_ping=f"{ip_test}")==True, f"*** IP {ip_test} недоступен в данный момент ***"
