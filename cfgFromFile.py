import re
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException
)
import sys
import os
# sys.path.insert(1, os.path.join(sys.path[0], '..'))
import yaml
from constants_trident import (
    CONSOLE,
)
from cfg_switch import  TridentCfg

# import importlib
# manage_app = importlib.import_module("manage-app")
# print(manage_app)
from switches.manage_app2 import app
# from manage_app.app import pull_cfg_sw

if __name__ == "__main__":
    tr1 = TridentCfg()
    tr1.check_connection()
    tr1.ssh.enable()
    # команды настройки конфига...
    print(path_name)
    with open(path_name) as commands:
        commands_template = yaml.safe_load(commands)
    # ...построчно передаются в cfg_base которая вызовет cfg_template
    print("This is tests print")
    print(tr1.cfg_base(commands_template))
