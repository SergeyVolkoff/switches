import time
import sys
import os

import yaml

sys.path.insert(1, os.path.join(sys.path[0],'..'))
print(sys.path)
from constants_trident  import (
    VALUE_CONS_CONNECT,
    CONSOLE,
    NAME_DEV,
)
 

from base_gns3 import Base_gns
from connect import Connect
from cfg_switch import TridentCfg

CONSOLE.print(
    "Тест работает по ПМИ 'Проверка поддержки GRE'(Jira:TRIDENT2-1886).",
    "\nРекомендуется ознакомиться с описанием теста.",
    "\nВ ходе теста настройки устойства будут сброшены,",
    "\nбудет запрошено название лабы gns3 и предложены варианты ответа",
    style='info'
              )
time.sleep(5)
current_lab = Base_gns() # test wait this lab - SSV_auto_BM10_MWAN
print(current_lab.start_nodes_from_project())

CONSOLE.print("Стартует сброс конфига DUT перед настройкой под тест\n",
              style='info')
time.sleep(5)
# Создание об-а для подключения по консоли
tr1 = TridentCfg()
# Сброс конфига
print(tr1.extended_reset_cfg())

CONSOLE.print(
       "Стартует настройка DUT под тест 'Проверка поддержки протокола GRE'\n",
       style='info')
time.sleep(5)
# команды настройки конфига 
with open("../templates_cfg/cfg_GRE.yaml") as commands:
        commands_template = yaml.safe_load(commands)
print(tr1.cfg_base(commands_template))