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
            if "No match input detected" in output:
                result_command = "bad command"
                CONSOLE.print(f'"{command}" -',result_command,style='fail')
                result[command] = result_command
                break
            if "" in output:
                result_command = "command passed"
                result[command]=output
                CONSOLE.print(f'"{command}" -',result_command,style='success')
            if "reload" in command:
                time.sleep(5)
                result=ping('10.27.192.48',timeout=2)
                while result is None:
                    result=ping('10.27.192.48',timeout=2)
                    CONSOLE.print("DUT is rebooting, please wait",style='success')
                    time.sleep(5)
                else:
                    CONSOLE.print("\nDUT up after reboot, wait all protocols!",style='success')
                    time.sleep(40)
                    CONSOLE.print( "All up!",style='success')
        output_exit = self.ssh.exit_config_mode()
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
    tr1.ssh.enable()
    with open('./templates_cfg/cfg_current.yaml') as commands:                # команды настройки Ripv2
        commands_template = yaml.safe_load(commands)
    print(tr1.cfg_base(commands_template))