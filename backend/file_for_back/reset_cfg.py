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
    NAME_DEV,
)
from ping3 import ping
from file_for_back.cfg_switch import  TridentCfg

if __name__ == "__main__":
    tr1 = TridentCfg()
    # tr1.check_connection()
    tr1.ssh.enable()
    print(tr1.reset_cfg_shot())
