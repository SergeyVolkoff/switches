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
        result=verbose_ping('8.8.8.8',count=3)
        print(result)

if __name__=="__main__":
    tr1 = Connect()
    print(tr1.extended_ping_inet())
