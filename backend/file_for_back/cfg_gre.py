import re
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException
)
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import yaml
from file_for_back.constants_trident import (
    CONSOLE,
)
from file_for_back.cfg_switch import  TridentCfg

if __name__ == "__main__":
    tr1 = TridentCfg()
    tr1.check_connection()
    tr1.ssh.enable()
    # команды настройки конфига...
    path_cfg = "templates_cfg/cfg_GRE.yaml"
    with open(path_cfg) as commands:
        commands_template = yaml.safe_load(commands)
    # ...построчно передаются в cfg_base которая вызовет cfg_template
    # print("This is tests print")
    print(tr1.cfg_base(commands_template))
