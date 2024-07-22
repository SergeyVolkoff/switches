import re
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException
)
import sys
import os
import time
sys.path.insert(1, os.path.join(sys.path[0], '..'))
# print(sys.path)
import yaml
from file_for_back.constants_trident import (
    CONSOLE,
)
from file_for_back.cfg_switch import  TridentCfg


if __name__ == "__main__":
    tr1 = TridentCfg()
    tr1.check_connection()
    tr1.check_mode()
    file =  open("file_for_back/path_name.txt", 'r')
    path_name = file.readline()
    # команды настройки конфига...
    with open(path_name) as commands:
        commands_template = yaml.safe_load(commands)
    # ...построчно передаются в cfg_base которая вызовет cfg_template
    print(tr1.cfg_base(commands_template))
   
