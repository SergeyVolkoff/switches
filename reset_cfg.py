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
from constants_trident import (
    CONSOLE,
    NAME_DEV,
)
from ping3 import ping
from cfg_switch import  TridentCfg

if __name__ == "__main__":
    tr1 = TridentCfg()
    tr1.check_connection()
    tr1.ssh.enable()
    # with open('./templates_cfg/cfg_current1.yaml') as commands:
    #     commands_template = yaml.safe_load(commands)
    print(tr1.extended_reset_cfg1())
