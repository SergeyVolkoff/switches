import time
import sys
import os

sys.path.insert(1, os.path.join(sys.path[0],'..'))
from constants_trident  import (
    VALUE_CONS_CONNECT,
    CONSOLE,
    NAME_DEV,
)

from base_gns3 import Base_gns

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