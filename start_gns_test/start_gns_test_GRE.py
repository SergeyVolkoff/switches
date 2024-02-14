import time
import sys
import os
import pytest

import yaml
import json
import keyboard
sys.path.insert(1, os.path.join(sys.path[0],'..'))
# print(sys.path)
from constants_trident  import (
    VALUE_CONS_CONNECT,
    CONSOLE,
    NAME_DEV,
)
 

from base_gns3 import Base_gns
from connect import Connect
from cfg_switch import TridentCfg


CONSOLE.print(
    "Тест работает по ПМИ 'Проверка поддержки GRE'.",
    "Рекомендуется ознакомиться с описанием теста в ПМИ (Jira:TRIDENT2-1886).",
    "В ходе теста настройки устойства будут сброшены,",
    "будет запрошено название подключаемой схемы gns3 и предложены варианты ответа",
    style='info', sep='\n'
              )
time.sleep(10)
current_lab = Base_gns() # test wait this lab - SSV_auto_BM10_MWAN
print(current_lab.start_nodes_from_project())

CONSOLE.print("Стартует сброс настроек DUT на дефолтные",
              style='info', sep='\n')
time.sleep(5)
# Создание об-а для подключения по консоли
tr1 = TridentCfg()
# Сброс конфига
print(tr1.extended_reset_cfg())

CONSOLE.print(
       "Стартует настройка DUT под тест 'Проверка поддержки протокола GRE'",
       style='info', sep='\n')
time.sleep(5)
# команды настройки конфига 
with open("../templates_cfg/cfg_GRE.yaml") as commands:
        commands_template = yaml.safe_load(commands)
print(tr1.cfg_base(commands_template))

CONSOLE.print("Стартует настройка Pytests под тест 'Проверка поддержки протокола GRE'",
              style='info', sep='\n')
time.sleep(1)
pytest.main(["-v", "--html=BULAT_TEST_TRIDENT_GRE.html", "--alluredir=allure_report", "../tests/test_check_gre.py"])
