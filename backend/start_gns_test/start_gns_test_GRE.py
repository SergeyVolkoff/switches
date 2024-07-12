"""File for start test GRE where Dut - Trident."""
import time
import sys
import os
import pytest
import yaml
sys.path.insert(1, os.path.join(sys.path[0], '..'))
# print(sys.path)

from file_for_back.constants_trident import CONSOLE
from file_for_back.base_gns3 import Base_gns
from file_for_back.cfg_switch import TridentCfg


CONSOLE.print(
    "Тест работает по ПМИ 'Проверка поддержки GRE'.",
    "Рекомендуется ознакомиться с описанием теста в ПМИ (Jira:TRIDENT2-1886).",
    "В ходе теста настройки устойства будут сброшены,",
    "будет запрошено название подключаемой схемы gns3 - SSV_auto_Tr_GRE",
    "и предложены варианты ответа",
    style='info', sep='\n'
              )
# time.sleep(10)
# current_lab = Base_gns()  # test wait this lab: SSV_auto_Tr_GRE
# print(current_lab.start_nodes_from_project())

CONSOLE.print("Стартует сброс настроек DUT на дефолтные",
              style='info', sep='\n')
time.sleep(5)
# Создание объекта для подключения по консоли
tr1 = TridentCfg()
# Сброс конфига
print(tr1.extended_reset_cfg())
CONSOLE.print(
       "Стартует настройка DUT под тест 'Проверка поддержки протокола GRE'",
       style='info', sep='\n')
time.sleep(5)
# команды настройки конфига...
with open("templates_cfg/cfg_GRE.yaml") as commands:
    commands_template = yaml.safe_load(commands)
# ...построчно передаются в cfg_base которая вызовет cfg_template
print(tr1.cfg_base(commands_template))

CONSOLE.print("Стартует настройка Pytests под тест",
              "'Проверка поддержки протокола GRE'",
              style='info', sep='\n')
time.sleep(10)
"""
вызов pytest с созданием отчетов html и allure. Сервер allure
запускается из cli: allure serve allure_report
"""
pytest.main(
    [
        "-v", "--html=BULAT_TEST_TRIDENT_GRE.html",
        "--alluredir=allure_report",
        "tests/test_check_gre.py"
    ]
        )
