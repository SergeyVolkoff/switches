import time
import sys
import os
import pytest

import yaml

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

# CONSOLE.print(
#     "\nТест работает по ПМИ 'Проверка поддержки GRE'.",
#     "\nРекомендуется ознакомиться с описанием теста в ПМИ (Jira:TRIDENT2-1886).",
#     "\nВ ходе теста настройки устойства будут сброшены,",
#     "\nбудет запрошено название подключаемой схемы gns3 и предложены варианты ответа",
#     style='info'
#               )
# time.sleep(7)
# current_lab = Base_gns() # test wait this lab - SSV_auto_BM10_MWAN
# print(current_lab.start_nodes_from_project())

# CONSOLE.print("\nСтартует сброс настроек DUT на дефолтные\n",
#               style='info')
# time.sleep(5)
# # Создание об-а для подключения по консоли
tr1 = TridentCfg()
# Сброс конфига
# print(tr1.extended_reset_cfg())

CONSOLE.print(
       "\nСтартует настройка DUT под тест 'Проверка поддержки протокола GRE'\n",
       style='info')
time.sleep(5)
# команды настройки конфига 
with open("../templates_cfg/cfg_GRE.yaml") as commands:
        commands_template = yaml.safe_load(commands)
print(tr1.cfg_base(commands_template))

CONSOLE.print("\nСтартует настройка Pytests под тест 'Проверка поддержки протокола GRE'\n",
              style='info')
time.sleep(10)
pytest.main(["-v","--html=BULAT_TEST_TRIDENT_GRE.html","../tests/test_check_gre.py"])
