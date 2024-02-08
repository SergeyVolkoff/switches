"""base for switches Trident"""

import netmiko
import paramiko
from netmiko import (
    ConnectHandler,
    NetmikoTimeoutException,
    NetmikoAuthenticationException
)
import pexpect
import logging
import time
from constants_trident import (
    VALUE_CONS_CONNECT,
    CONSOLE,
    NAME_DEV,
)
from ping3 import ping, verbose_ping




class Connect():
    """
    Class represents connect and 
    disconnect actions for Node.
    """

    def __init__(self,
                 log=True
                 ):
        self.word_ping = "ping ",
        self.ip_inet = "8.8.8.8",
        try:
            self.ssh = ConnectHandler(**VALUE_CONS_CONNECT)
        except ConnectionRefusedError as e:
            CONSOLE.print(
                    "*" * 5, "Error connection to:", 
                    VALUE_CONS_CONNECT['host'],'port:', VALUE_CONS_CONNECT['port'], "*" * 5,
                    "\nConnection refused - Console is busy!",
                    style='fail')
            exit()

    def send_command(self,command):
        self.check_connection(VALUE_CONS_CONNECT)
        self.ssh.enable()
        temp = self.ssh.send_command(command)
        return temp
    
    def check_connection(self,VALUE_CONS_CONNECT, log=True):
        if log:
            CONSOLE.print(
                'Try connect to', VALUE_CONS_CONNECT['host'],
                'port:',VALUE_CONS_CONNECT['port'], "...",
                style="info")
        try:
            CONSOLE.print(
                VALUE_CONS_CONNECT['host'],' port:',
                VALUE_CONS_CONNECT['port'], "connected!",
                style='success')
        except (NetmikoAuthenticationException, NetmikoTimeoutException) as error:
            CONSOLE.print(
                "*" * 5, "Error connection to:", 
                VALUE_CONS_CONNECT['host'],'port:',VALUE_CONS_CONNECT['port'], "*" * 5,
                style='fail')
            
    def ping_inet_izi(self,ip_for_ping):
        # self.check_connection(VALUE_CONS_CONNECT)
        result=ping(ip_for_ping)
        # print(result)

    def ping_inet_extended(self, ip_for_ping):
        self.check_connection(VALUE_CONS_CONNECT)
        self.ssh.enable()
        temp = self.ssh.send_command("ping",expect_string="Protocol",read_timeout=1)
        temp = self.ssh.send_command("ip", expect_string="Target IP address:",read_timeout=1)
        temp = self.ssh.send_command(ip_for_ping, expect_string="Name of the VRF",read_timeout=1)
        temp = self.ssh.send_command("", expect_string="Repeat count",read_timeout=1)
        temp = self.ssh.send_command("", expect_string="Datagram size",read_timeout=1)
        temp = self.ssh.send_command("", expect_string="Timeout in seconds",read_timeout=1)
        temp = self.ssh.send_command("", expect_string="Extended commands", read_timeout=1 )
        temp = self.ssh.send_command("", expect_string="DUT", read_timeout=10)
        # result=verbose_ping('8.8.8.8',count=3)
        return temp
    
    def tracert_ip_izi(self):
        self.check_connection(VALUE_CONS_CONNECT)
        ip_dest = input("Input ip destination: ")
        output_tracert = self.ssh.send_command(f"traceroute {ip_dest}",read_timeout=40,auto_find_prompt=False)
        return output_tracert
    
    def tracert_ip_extended(self,ip_dest):
        # self.check_connection(VALUE_CONS_CONNECT)
        self.ssh.enable()
        # ip_dest = input("Input ip destination: ")
        temp = self.ssh.send_command("traceroute",expect_string="Protocol",read_timeout=1)
        temp = self.ssh.send_command("", expect_string="Target IP address:",read_timeout=1)
        temp = self.ssh.send_command(f'{ip_dest}', expect_string="Datagram size",read_timeout=1)
        temp = self.ssh.send_command("", expect_string="Set DF bit in IP header?",read_timeout=1)
        temp = self.ssh.send_command("", expect_string="Source-address/source-interface/skip parameter",read_timeout=1)
        temp = self.ssh.send_command("skip", expect_string="Name of the VRF",read_timeout=1)
        temp = self.ssh.send_command("", expect_string="Numeric display",read_timeout=1)
        temp = self.ssh.send_command("", expect_string="Timeout in seconds",read_timeout=1)
        temp = self.ssh.send_command("", expect_string="Probe count",read_timeout=1)
        temp = self.ssh.send_command("", expect_string="Maximum time to live",read_timeout=1)
        temp = self.ssh.send_command("5", expect_string="Port Number",read_timeout=1)
        temp = self.ssh.send_command("", expect_string="DUT", read_timeout=5)
        print(temp)
        

    def cfg_hostname(self):
        temp = self.ssh.send_command('enable',read_timeout=4,expect_string="BS7510")
        temp = self.ssh.send_config_set([f"hostname {NAME_DEV}","do write"], read_timeout=4)       
        output_exit = self.ssh.exit_config_mode()
        return temp
    
    def cfg_int_eth(self):
        # self.check_connection(VALUE_CONS_CONNECT)
        # self.ssh.enable()
        temp = self.ssh.send_command('enable',read_timeout=4,expect_string="BS7510",)
        temp = self.ssh.send_config_from_file('./templates_cfg/cfg_int_eth0.txt')
        output_exit = self.ssh.exit_config_mode()
        return temp
    
    def izi_reset_cfg(self):
        """Ф-я подкллючится по консоли к ,сбросит настрой"""

        self.check_connection(VALUE_CONS_CONNECT)
        self.ssh.enable()
        
        CONSOLE.print("Do you realy want to reset config!?", style='fail')
        result_input = input("Input y/n:")
        if result_input == 'n':
            CONSOLE.print(
            "Configuration not reset, device name  and interface not configured", 
            style="fail" )
            output_exit = self.ssh.exit_config_mode()
            exit
        if 'y' == result_input:
            temp = self.ssh.send_command("copy empty-config startup-config")
            output = self.ssh.send_command("reload",expect_string="reboot system" ,read_timeout=1,)
            result_command = "Swich rebooting! Wait, please +-70sec"
            output = self.ssh.send_command ("y",expect_string="")
            CONSOLE.print(output,result_command,style="success")
            
        else:
            CONSOLE.print(
            "Wrong input", 
            style="fail" )
            output_exit = self.ssh.exit_config_mode()
            exit
           
    
    
if __name__=="__main__":
    tr1 = Connect()
    print(tr1.send_command('sh run'))
