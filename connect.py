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
    value_connect,
    CONSOLE,
)
class Connect():
    """
    Class represents connect and 
    disconnect actions for Node.
    """

    def __init__(self,
                 log=True
                 ):
        try:
            self.ssh = ConnectHandler(**value_connect)
        except ConnectionRefusedError as e:
            CONSOLE.print(
                    "*" * 5, "Error connection to:", 
                    value_connect['host'],'port:',value_connect['port'], "*" * 5,
                    "\nConnection refused - Console is busy!",
                    style='fail')
            exit()

    def send_command(self,command):
        self.check_connection(value_connect)
        self.ssh.enable()
        temp = self.ssh.send_command(command)
        return temp
    
    def check_connection(self,value_connect, log=True):
        if log:
            CONSOLE.print(
                'Try connect to', value_connect['host'],
                'port:',value_connect['port'], "...",
                style="info")
        try:
            CONSOLE.print(
                value_connect['host'],' port:',
                value_connect['port'], "connected!",
                style='success')
        except (NetmikoAuthenticationException, NetmikoTimeoutException) as error:
            CONSOLE.print(
                "*" * 5, "Error connection to:", 
                value_connect['host'],'port:',value_connect['port'], "*" * 5,
                style='fail')
        


if __name__=="__main__":
    tr1 = Connect()
    print(tr1.send_command("sh ip interface brief"))