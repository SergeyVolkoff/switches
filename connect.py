"""base for switches Trident"""
import netmiko
import paramiko
from netmiko import ConnectHandler
import pexpect
import logging
import time
from constants import trident

class Connect():
    """
    Class represents connect and 
    disconnect actions for Node.
    """

    def __init__(self,
                 ):
        self.ssh = ConnectHandler(**trident)
    
    def send_command(self,command):
        self.ssh.enable()
        temp = self.ssh.send_command(command)
        print(temp)
        return temp

if __name__=="__main__":
    tr1 = Connect()
    print(tr1)
    print(tr1.send_command("show running-config"))