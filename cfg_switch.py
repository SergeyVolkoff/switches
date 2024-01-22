import time
import yaml
from ping3 import ping

from constants_trident import (
    VALUE_CONS_CONNECT,
    CONSOLE,
    NAME_DEV,
)
from connect import Connect


class CfgTemplate(Connect):

    def cfg_template(self,commands_template):

        """ФУНКЦИЯ управления  заливкой cfg_base"""
        result = {}
        for command in commands_template:
            output = self.ssh.send_command(command,expect_string="DUT",read_timeout=1)
            print(command ,output)
            if "reload" in command:
                time.sleep(5)
                result=ping('10.27.192.48',timeout=2)
                while result is None:
                    result=ping('10.27.192.48',timeout=2)
                    print("DUT is rebooting, wait")
                    time.sleep(5)
                else:
                    print("\nDUT up after reboot, wait all protocols!")
                    time.sleep(40)
                    print( "All up!")
        output_exit = self.ssh.exit_config_mode()
        print(output_exit)
        return result
    
class TridentCfg(CfgTemplate):

    def cfg_base(self,commands_template):

        """ФУНКЦИЯ-шаблон настройки базового конфига"""

        # self.check_connection(VALUE_CONS_CONNECT)
        CfgTemplate.cfg_template(self,commands_template)
        return 
        
    # def start_cfg():
    #     tr=CfgSwitch(VALUE_CONS_CONNECT)

if __name__=="__main__":
    tr1 = TridentCfg()
    tr1.check_connection(VALUE_CONS_CONNECT)
    output_enable=tr1.ssh.enable()
    print(output_enable)
    with open('./templates_cfg/cfg_current.yaml') as commands:                # команды настройки Ripv2
        commands_template = yaml.safe_load(commands)
        print(commands_template)
    print(tr1.cfg_base(commands_template))