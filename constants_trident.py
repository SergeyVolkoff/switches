import json
from rich import print
from rich.theme import Theme
from rich.console import Console
from pprint import pprint

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
    "В форме ниже введите 4х значный порт консольного сервера за которым находится DUT.",
    "ВНИМАНИЕ!",
    "В ходе дальнейших операций устройство за этим портом будет",
    "сброшено на заводские настройки и перезагружено!",
    style='info',
    sep='\n')
input_console = input("Укажите порт консоли:")
VALUE_CONS_CONNECT  = {
    'device_type': 'cisco_ios_telnet',
    'host': '10.27.193.2',
    'username': 'admin',
    'password': 'bulat',
    'secret': 'enable',
    'port': int(input_console),
}
