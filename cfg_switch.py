"""Class for reset, cfg switch Trident."""

import time
import yaml
from ping3 import ping
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
# print(sys.path)
from constants_trident import (
    VALUE_CONS_CONNECT,
    CONSOLE,
)
from connect import Connect


class CfgTemplate(Connect):
    """Class for cfg trident from tamplate."""

    def cfg_template(self, commands_template):
        """
        Function for configuration of config from template
        with start control after reboot.
        """
        result = {}
        for command in commands_template:
            if "do reload" in command:
                output = self.ssh.send_command(
                    command, expect_string="reboot system",
                    read_timeout=.2)
                result_command = "- command is checked, wait, please."
                CONSOLE.print(command, result_command, style='success')
                result_command = self.ssh.send_command(
                    "y", expect_string="")
                CONSOLE.print(command, result_command, style='success')
                time.sleep(5)
                result = ping('10.27.192.48', timeout=2)
                while result is None:
                    result = ping('10.27.192.48', timeout=2)
                    CONSOLE.print(
                        "DUT is rebooting, please wait", style='fail')
                    time.sleep(5)
                else:
                    CONSOLE.print(
                        "\nDUT up after reboot, wait all protocols!",
                        style='success')
                    time.sleep(40)
                    CONSOLE.print("All up!", style='success')
                    self.ssh.send_command_timing(
                        'admin', read_timeout=2)
                    self.ssh.send_command_timing(
                        'bulat', read_timeout=5)
                    self.ssh.disconnect()
                    break
            output = self.ssh.send_command(
                command, expect_string="DUT", read_timeout=2)
            if "wr" or "write" in command:
                result_command = "- command is checked, wait, please."
                CONSOLE.print(
                    command, result_command, style='fail')
                time.sleep(3)
            if "No match input detected" in output:
                result_command = f"bad command! {output}"
                CONSOLE.print(
                    f'"{command}" -',
                    result_command, style='fail')
                result[command] = result_command
            else:
                result_command = "command passed!"
                result[command] = output
                CONSOLE.print(
                    f'"{command}" -',
                    result_command, style='success')
        return result


class TridentCfg(CfgTemplate):
    """Class for cfg trident."""

    def extended_reset_cfg(self):
        """
        Function for resetting the config to default settings
        with start control after a reboot.
        """
        self.check_connection(VALUE_CONS_CONNECT)
        self.ssh.enable()
        CONSOLE.print(
            "Do you realy want to reset config!?",
            style='fail')
        result_input = input("Input y/n:")
        if result_input == 'n':
            CONSOLE.print(
                "Configuration not reset, device name  and interface not configured",
                style="fail")
            self.ssh.exit_config_mode()
            exit
        if 'y' == result_input:
            temp = self.ssh.send_command(
                "copy empty-config startup-config")
            output = self.ssh.send_command(
                "reload", expect_string="reboot system",
                read_timeout=1)
            output = self.ssh.send_command("y", expect_string="")
            CONSOLE.print(
                output,
                "Swich rebooting! Wait, please +-70sec",
                style="success")
            time.sleep(75)
            self.ssh.send_command_timing('admin', read_timeout=2)
            self.ssh.send_command_timing('bulat', read_timeout=5)
            with open('../templates_cfg/cfg_hostnamAndint_eth0.yaml') as commands:
                commands_template = yaml.safe_load(commands)
                for command in commands_template:
                    output = self.ssh.send_command_timing(
                        command, read_timeout=0)
            result = ping('10.27.192.48', timeout=2)
            while result is None:
                result=ping('10.27.192.48', timeout=2)
                CONSOLE.print(
                    "DUT is rebooting, please wait", style='fail'
                    )
                time.sleep(5)
            else:
                CONSOLE.print(
                    "\nDUT up after reboot and int eth0(10.27.192.48) up!, wait all protocols!",
                    style='success')
                time.sleep(10)
                dev_name = self.ssh.find_prompt()
                CONSOLE.print(
                    f"All up!Config reset! New_name device: {dev_name} and interface eth0 configured",
                    style='success')
                exit
        else:
            CONSOLE.print("Wrong input", style="fail")
            self.ssh.exit_config_mode()
            exit

    def cfg_base(self, commands_template):
        """ФУНКЦИЯ-шаблон настройки базового конфига."""
        # self.check_connection(VALUE_CONS_CONNECT)
        CfgTemplate.cfg_template(self, commands_template)
        return


if __name__ == "__main__":
    tr1 = TridentCfg()
    tr1.check_connection(VALUE_CONS_CONNECT)
    tr1.ssh.enable()
    with open('./templates_cfg/cfg_current1.yaml') as commands:
        commands_template = yaml.safe_load(commands)
    print(tr1.cfg_base(commands_template))
