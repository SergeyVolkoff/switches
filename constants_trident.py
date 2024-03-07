import json
from rich import print
from rich.theme import Theme
from rich.console import Console
from pprint import pprint

import yaml

my_colors = Theme(
     #добавляет цветовую градацию для rich
    {
        "success":" bold green",
        "fail": "bold red",
        "info": "bold blue"
    }
)
CONSOLE = Console(theme=my_colors)

NAME_DEV = "DUT"
CONSOLE.print(
    "В форме ниже введите 4х значный порт",
    "консольного сервера за которым находится DUT.",
    style='info',
    sep='\n')
CONSOLE.print("ВНИМАНИЕ!", style='fail')
CONSOLE.print(
    "В ходе дальнейших операций устройство за этим портом может быть",
    "сброшено на заводские настройки и перезагружено!",
    style='info',
    sep='\n')
# input_console = input("УКАЖИТЕ ПОРТ КОНСОЛИ:")
# VALUE_CONS_CONNECT  = {
#     'device_type': 'cisco_ios_telnet',
#     'host': '10.27.193.2',
#     'username': 'admin',
#     'password': 'bulat',
#     'secret': 'enable',
#     'port': int(input_console),
# }
# with open("../constants_trident1.yaml") as f2:
#     VALUE_CONS_CONNECT = yaml.safe_load(f2)
    # print(temp)
    # for t in temp:
    #     print(t)
    #     VALUE_CONS_CONNECT = dict(t)
    # print(VALUE_CONS_CONNECT)
with open("../constants_trident1.yaml") as f2:
                VALUE_CONS_CONNECT = yaml.safe_load(f2)
                # for t in temp:
                #     VALUE_CONS_CONNECT = dict(t)
