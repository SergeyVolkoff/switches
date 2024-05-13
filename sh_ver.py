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
from connect import Connect


if __name__ == "__main__":
    tr1 = TridentCfg()
    # tr1.check_connection()
    tr1.check_mode()
    tr1.ssh.enable()
    print(tr1.sh_ver())
