"""Base class for switches Trident."""

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


class Connect():
    """Class represents connect and disconnect actions for Node."""

    def __init__(self, log=True):
        """Init Connect-class."""
        self.word_ping = "ping ",
        self.ip_inet = "8.8.8.8",
        with open("../constants_trident1.yaml") as f2:
                temp = yaml.safe_load(f2)
        self.VALUE_CONS_CONNECT = temp
        try:
            with open("../constants_trident1.yaml") as f2:
                self.VALUE_CONS_CONNECT = yaml.safe_load(f2)
            self.ssh = ConnectHandler(**self.VALUE_CONS_CONNECT)
        except ConnectionRefusedError:
            CONSOLE.print(
                    "*" * 5, "Error connection to:",
                    self.VALUE_CONS_CONNECT['host'],
                    'port:', self.VALUE_CONS_CONNECT['port'], "*" * 5,
                    "\nConnection refused - Console is busy!",
                    style='fail')
            exit()


    def sh_ver(self):
        ""
        self.check_connection(self.VALUE_CONS_CONNECT)
        self.ssh.enable()
        try:
            temp = self.ssh.send_command('show version',read_timeout=2)
            for i in temp:
                with open("../sh_ver.txt", 'a+') as file:
                     file.write(i)

        except FileNotFoundError:
            print('Файл отсутствует.')
        except ValueError as v_e:
            print(v_e)


    def send_command(self, command):
        """Redefinition send_command - no use."""
        self.check_connection(self.VALUE_CONS_CONNECT)
        self.ssh.enable()
        temp = self.ssh.send_command(command)
        return temp

    def check_connection(self, log=True):
        """Check connection to DUT."""
        if log:
            CONSOLE.print(
                'Пробую подключиться к', self.VALUE_CONS_CONNECT['host'],
                'порт:', self.VALUE_CONS_CONNECT['port'], "...",
                style="info")
        try:
            CONSOLE.print('Коммутатор',
                self.VALUE_CONS_CONNECT['host'], 'порт:',
                self.VALUE_CONS_CONNECT['port'], "подключен!",
                style='success')
        except (NetmikoAuthenticationException,
                NetmikoTimeoutException):
            CONSOLE.print(
                "*" * 5, "Ошибка подключения к:",
                self.VALUE_CONS_CONNECT['host'],
                'порт:', self.VALUE_CONS_CONNECT['port'], "*" * 5,
                style='fail')
            
    def check_eth0(self):
        
        temp = self.ssh.send_command('do sh ip interface eth0',read_timeout=5)
        temp1 = re.search(r'IP address\S\s+(?P<ip_eth0>\d+\S\d+\S\d+\S\d+)',temp)
        try:
            ip_eth0 = temp1.group('ip_eth0')
        except NetmikoTimeoutException as err:
            print("Не смог получить и обработать ip_eth0 error", err)
        return ip_eth0

    def ping_inet_izi(self, ip_for_ping):
        """Simple function ping."""
        result = ping(ip_for_ping)
        return result

    def ping_inet_extended(self, ip_for_ping):
        """Extended function ping."""
        self.ssh.enable()
        temp = self.ssh.send_command("ping",
                                     expect_string="Protocol",
                                     read_timeout=1)
        temp = self.ssh.send_command("ip",
                                     expect_string="Target IP address:",
                                     read_timeout=1)
        temp = self.ssh.send_command(ip_for_ping,
                                     expect_string="Name of the VRF",
                                     read_timeout=1)
        temp = self.ssh.send_command("",
                                     expect_string="Repeat count",
                                     read_timeout=1)
        temp = self.ssh.send_command("",
                                     expect_string="Datagram size",
                                     read_timeout=1)
        temp = self.ssh.send_command("",
                                     expect_string="Timeout in seconds",
                                     read_timeout=1)
        temp = self.ssh.send_command("",
                                     expect_string="Extended commands",
                                     read_timeout=1)
        temp = self.ssh.send_command("",
                                     expect_string="DUT",
                                     read_timeout=10)
        return temp

    def tracert_ip_izi(self, ip_dest):
        """Simple fuction traceroute."""
        # self.check_connection(VALUE_CONS_CONNECT)
        # ip_dest = input("Input ip destination: ")
        self.ssh.enable()
        output_tracert = self.ssh.send_command(f"traceroute {ip_dest}",
                                               read_timeout=40,
                                               auto_find_prompt=False)
        return output_tracert

    def tracert_ip_extended(self, ip_dest):
        """Extended fuction traceroute."""
        self.ssh.enable()
        temp = self.ssh.send_command("traceroute",
                                     expect_string="Protocol", read_timeout=1)
        temp = self.ssh.send_command("", expect_string="Target IP address:",
                                     read_timeout=1)
        temp = self.ssh.send_command(f'{ip_dest}',
                                     expect_string="Datagram size",
                                     read_timeout=1)
        temp = self.ssh.send_command("",
                                     expect_string="Set DF bit in IP header?",
                                     read_timeout=1)
        temp = self.ssh.send_command("",
                                     expect_string="Source-address/source-interface/skip parameter",
                                     read_timeout=1)
        temp = self.ssh.send_command("skip",
                                     expect_string="Name of the VRF",
                                     read_timeout=1)
        temp = self.ssh.send_command("",
                                     expect_string="Numeric display",
                                     read_timeout=1)
        temp = self.ssh.send_command("",
                                     expect_string="Timeout in seconds",
                                     read_timeout=1)
        temp = self.ssh.send_command("",
                                     expect_string="Probe count",
                                     read_timeout=1)
        temp = self.ssh.send_command("",
                                     expect_string="Maximum time to live",
                                     read_timeout=1)
        temp = self.ssh.send_command("5",
                                     expect_string="Port Number",
                                     read_timeout=1)
        temp = self.ssh.send_command("",
                                     expect_string="DUT",
                                     read_timeout=5)
        print(temp)

    def cfg_hostname(self):
        """Fuction re-name DUT."""
        temp = self.ssh.send_command('enable',
                                     read_timeout=4,
                                     expect_string="BS7510")
        temp = self.ssh.send_config_set([f"hostname {NAME_DEV}",
                                         "do write"],
                                         read_timeout=4)
        self.ssh.exit_config_mode()
        return temp

    def cfg_int_eth(self):
        """Fuction cfg interface ETH0."""
        temp = self.ssh.send_command('enable',
                                     read_timeout=4,
                                     expect_string="BS7510",)
        temp = self.ssh.send_config_from_file(
            './templates_cfg/cfg_int_eth0.txt'
            )
        self.ssh.exit_config_mode()
        return temp

    def izi_reset_cfg(self):
        """Simple fuction copy empty-config to startup cfg."""
        self.check_connection(self.VALUE_CONS_CONNECT)
        self.ssh.enable()
        CONSOLE.print("Do you realy want to reset config!?", style='fail')
        result_input = input("Input y/n:")
        if result_input == 'n':
            CONSOLE.print(
             "Configuration not reset, device name and interface not configured",
             style="fail")
            output_exit = self.ssh.exit_config_mode()
            exit
        if 'y' == result_input:
            self.ssh.send_command(
                "copy empty-config startup-config"
                )
            output = self.ssh.send_command(
                "reload",
                expect_string="reboot system", read_timeout=1)
            result_command = "Swich rebooting! Wait, please +-70sec"
            output = self.ssh.send_command("y", expect_string="")
            CONSOLE.print(output, result_command, style="success")
        else:
            CONSOLE.print("Wrong input", style="fail")
            self.ssh.exit_config_mode()
            exit


if __name__=="__main__":
    tr1 = Connect()
    print(tr1.send_command('sh run'))

