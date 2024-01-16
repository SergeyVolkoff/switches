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
    VALUE_CONNECT,
    CONSOLE,
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
            self.ssh = ConnectHandler(**VALUE_CONNECT)
        except ConnectionRefusedError as e:
            CONSOLE.print(
                    "*" * 5, "Error connection to:", 
                    VALUE_CONNECT['host'],'port:',VALUE_CONNECT['port'], "*" * 5,
                    "\nConnection refused - Console is busy!",
                    style='fail')
            exit()

    def send_command(self,command):
        self.check_connection(VALUE_CONNECT)
        self.ssh.enable()
        temp = self.ssh.send_command(command)
        return temp
    
    def check_connection(self,VALUE_CONNECT, log=True):
        if log:
            CONSOLE.print(
                'Try connect to', VALUE_CONNECT['host'],
                'port:',VALUE_CONNECT['port'], "...",
                style="info")
        try:
            CONSOLE.print(
                VALUE_CONNECT['host'],' port:',
                VALUE_CONNECT['port'], "connected!",
                style='success')
        except (NetmikoAuthenticationException, NetmikoTimeoutException) as error:
            CONSOLE.print(
                "*" * 5, "Error connection to:", 
                VALUE_CONNECT['host'],'port:',VALUE_CONNECT['port'], "*" * 5,
                style='fail')
            
    def izi_ping_inet(self):
        self.check_connection(VALUE_CONNECT)
        result=ping('8.8.8.8')
        print(result)

    def extended_ping_inet(self):
        self.check_connection(VALUE_CONNECT)
        self.ssh.enable()
        temp = self.ssh.send_command("ping",expect_string="Protocol",read_timeout=1)
        temp = self.ssh.send_command("ip", expect_string="Target IP address:",read_timeout=1)
        temp = self.ssh.send_command("8.8.8.8", expect_string="Name of the VRF",read_timeout=1)
        temp = self.ssh.send_command("", expect_string="Repeat count",read_timeout=1)
        temp = self.ssh.send_command("", expect_string="Datagram size",read_timeout=1)
        temp = self.ssh.send_command("", expect_string="Timeout in seconds",read_timeout=1)
        temp = self.ssh.send_command("", expect_string="Extended commands", read_timeout=1 )
        print("ping",temp)
        temp = self.ssh.send_command("", expect_string="DUT", read_timeout=10)
        # result=verbose_ping('8.8.8.8',count=3)
        print(temp)

if __name__=="__main__":
    tr1 = Connect()
    print(tr1.extended_ping_inet())
