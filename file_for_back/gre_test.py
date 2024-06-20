import re
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException
)
import pytest
import time

import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from file_for_back.base_gns3 import Base_gns

import yaml
from file_for_back.constants_trident import (
    CONSOLE,
)
from file_for_back.cfg_switch import  TridentCfg

if __name__ == "__main__":
    # tr1 = TridentCfg()
    # tr1.check_connection()
    # tr1.ssh.enable()
    CONSOLE.print(
    "Тест работает по ПМИ 'Проверка поддержки GRE'.",
    "Рекомендуется ознакомиться с описанием теста в ПМИ (Jira:TRIDENT2-1886).",
    "В ходе теста настройки устойства будут сброшены,",
    "будет запрошено название подключаемой схемы gns3 - SSV_auto_Tr_GRE",
    "и предложены варианты ответа",
    style='info', sep='\n'
              )
    # time.sleep(10)
    # Base_gns.name_lab = 'SSV_auto_Tr_GRE'
    # current_lab = Base_gns()  # test wait this lab: SSV_auto_Tr_GRE
    # print(current_lab.start_nodes_from_project())
    CONSOLE.print("Стартует настройка Pytests под тест",
              "'Проверка поддержки протокола GRE'",
              style='info', sep='\n')
    # time.sleep(10)
    """
    вызов pytest с созданием отчетов html и allure. Сервер allure
    запускается из cli: allure serve allure_report
    """
    print (pytest.main(
        [
	    "-v", "--html=../report_doc/BULAT_TEST_TRIDENT_GRE.html",            
            "--alluredir=allure_report",
            "../tests/test_check_gre.py"
        ]
            ))
    # Вызов серевера allure с отчетом
    # os.system("allure serve allure_report")
