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

def check_enable_gre():
    try:
        temp = r1.send_command(device, 'uci show ripng.@rip[0].enabled')
        if "='1'" in temp:
            print("RIPng - enable!")
            return True
        else:
            return False
    except ValueError as err:
        return False