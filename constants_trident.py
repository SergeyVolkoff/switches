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

value_connect = {
    'device_type': 'cisco_ios_telnet',
    'host': '10.27.193.2',
    'username': 'admin',
    'password': 'bulat',
    'secret': 'enable',
    'port': 2046,
}