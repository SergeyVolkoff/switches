"""Class for reset, cfg switch Trident."""

import time
import yaml
from ping3 import ping
import sys
import os
sys.path.insert(1, os.path.join(sys.path[0], '..'))
# print(sys.path)
from file_for_back.constants_trident import (
    CONSOLE,
)
from file_for_back.connect import Connect



class CfgTemplate(Connect):
    """Class for cfg trident from tamplate."""

    def cfg_template(self, commands_template):
        """
        Function for configuration DUT from template,
        with start control DUT after reboot.
        """
        self.check_mode()
        result = {}
        # в цикле проверяются команды и отправляются на исполнение
        for command in commands_template:
            if "do reload" in command:
                output = self.ssh.send_command(
                    command, expect_string="reboot system",
                    read_timeout=.45)
                result_command = "- команда проверяется, пожалуйста, подождите."
                CONSOLE.print(command, result_command, style='success')
                result_command = self.ssh.send_command(
                    "y", expect_string="")
                CONSOLE.print(command, result_command, style='success')
                time.sleep(5)

                #  читаем из файла присвоеный ip_eth0:
                with open("ip_eth0.txt", 'r') as file:
                    for line in file:
                        ip_eth0 = line
                # удаляем файл (будет мешать в след итерации):
                os.remove(path="ip_eth0.txt")
                # проверяем доступность eth0
                result = ping(ip_eth0, timeout=2)
                while result is None:
                    result = ping(ip_eth0, timeout=2)
                    CONSOLE.print(
                        "DUT перезагружается, пожалуйста, подождите!", style='fail')
                    time.sleep(5)
                else:
                    CONSOLE.print(
                        "\nDUT поднялся после перезагрузки, ждем поднятия сервисов и протоколов!",
                        style='success')
                    time.sleep(40)
                    CONSOLE.print("Коммутатор доступен!", style='success')
                    self.ssh.send_command_timing(
                        'admin', read_timeout=2)
                    self.ssh.send_command_timing(
                        'bulat', read_timeout=5)
                    self.ssh.disconnect()
                    break
            output = self.ssh.send_command(
                command, expect_string="DUT", read_timeout=2)
            if "wr" or "write" in command:
                result_command = "- команда проверяется, пожалуйста, подождите."
                CONSOLE.print(
                    command, result_command, style='fail')
                time.sleep(3)
            if "No match input detected" in output:
                result_command = f"Ошибочная или излишняя команда! {output}"
                CONSOLE.print(
                    f'"{command}" -',
                    result_command, style='fail')
                result[command] = result_command
            else:
                result_command = "команда выполнена!"
                result[command] = output
                CONSOLE.print(
                    f'"{command}" -',
                    result_command, style='success')
        return result


class TridentCfg(CfgTemplate):
    """Class for cfg trident."""

    def extended_reset_cfg(self):
        """
        Function for resetting the config DUT to default settings,
        with control start DUT after a reboot.
        """
        self.check_connection(self.VALUE_CONS_CONNECT)
        self.check_mode()
        self.ssh.enable()
        CONSOLE.print(
            "Do you realy want to reset config!?",
            style='fail')
        result_input = input("Input y/n:")
        if result_input == 'n':
            CONSOLE.print(
                "Configuration not reset!",
                "Device name  and interface not configured!",
                style="fail")
            self.ssh.exit_config_mode()
            exit
        if 'y' == result_input:
            self.ssh.send_command("copy empty-config startup-config")
            output = self.ssh.send_command(
                "reload", expect_string="reboot system",
                read_timeout=1)
            output = self.ssh.send_command("y", expect_string="")
            CONSOLE.print(
                output,
                "Swich rebooting! Wait, please +-70sec",
                style="success")
            time.sleep(70)
            self.ssh.send_command_timing('admin', read_timeout=2)
            self.ssh.send_command_timing('bulat', read_timeout=5)
            with open('templates_cfg/cfg_hostnamAndint_eth0.yaml') as commands:
                commands_template = yaml.safe_load(commands)
                for command in commands_template:
                    output = self.ssh.send_command_timing(
                        command, read_timeout=0)
            # определяем ip на eth0:
            ip_eth0 = Connect.check_eth0(self)
            # формируем строку ip_eth0:
            ip_eth0 = str(ip_eth0)
            # пишем строку с ip_eth0 в файл ip_eth0.txt:
            with open("ip_eth0.txt", 'w') as file:
                file.write(ip_eth0)
            # проверяем доступность eth0:
            result = ping(ip_eth0, timeout=2)
            print(result)
            while result is None:
                result = ping(ip_eth0, timeout=2)
                CONSOLE.print(
                    "DUT is rebooting, please wait", style='fail'
                    )
                time.sleep(5)
            else:
                CONSOLE.print(
                    f"\nDUT up after reboot and int eth0 ({ip_eth0}) up!",
                    "Wait up protocols!",
                    style='success')
                time.sleep(10)
                dev_name = self.ssh.find_prompt()
                CONSOLE.print(
                    f"All up! Config reset!",
                    f"New_name device: {dev_name}.",
                    f"interface eth0 ({ip_eth0}) configured",
                    style='success')
                exit
        else:
            CONSOLE.print("Wrong input", style="fail")
            self.ssh.exit_config_mode()
            exit
    
    def extended_reset_cfg1(self):
        """
        replica
        """
        # self.check_connection(self.VALUE_CONS_CONNECT)
        self.check_mode()
        self.ssh.enable()
        
        # CONSOLE.print(
        #     "Do you realy want to reset config!?",
        #     style='fail')
        # result_input = input("Input y/n:")
        # if result_input == 'n':
        #     CONSOLE.print(
        #         "Configuration not reset!",
        #         "Device name  and interface not configured!",
        #         style="fail")
        #     self.ssh.exit_config_mode()
        #     exit
        # if 'y' == result_input:
        self.ssh.send_command("copy empty-config startup-config")
        CONSOLE.print(
            "В коммутатор записан базовый конфиг.",
            style="success")
        output = self.ssh.send_command(
            "reload", expect_string="reboot system",
            read_timeout=1)
        
        output = self.ssh.send_command("y", expect_string="")
        CONSOLE.print(
            output,
            "Коммутатор перезагружается, время ожидания около 70 сек.",
            style="success")
            
        time.sleep(75)
        self.ssh.send_command_timing('admin', read_timeout=2)
        self.ssh.send_command_timing('bulat', read_timeout=5)
        with open('templates_cfg/cfg_hostnamAndint_eth0.yaml') as commands:
            commands_template = yaml.safe_load(commands)
            for command in commands_template:
                output = self.ssh.send_command_timing(
                    command, read_timeout=0)
        time.sleep(20)
        # определяем ip на eth0:
        ip_eth0 = Connect.check_eth0(self)
        print(ip_eth0)
        # формируем строку ip_eth0:
        ip_eth0 = str(ip_eth0)
        # пишем строку с ip_eth0 в файл ip_eth0.txt:
        with open("ip_eth0.txt", 'w') as file:
            file.write(ip_eth0)
        # проверяем доступность eth0:
        result = ping(ip_eth0, timeout=2)
        print(result)
        while result is None:
            result = ping(ip_eth0, timeout=2)
            CONSOLE.print(
                "Коммутатор перезагружается, время ожидания около 70 сек.", style='fail'
                )
            time.sleep(5)
        else:
            
            CONSOLE.print(
                f"\nDUT поднялся после перезагрузки и интерфейс eth0 ({ip_eth0}) поднялся!",
                "Ждем поднятия всех протоколов.",
                style='success')
            time.sleep(10)
            dev_name = self.ssh.find_prompt()
            CONSOLE.print(
                f"Устройство доступно! Конфиг сброшен!",
                f"Новое имя устр-ва: {dev_name}.",
                f"интерфейс {ip_eth0} настроен по dhcp.",
                style='success')
            exit
	
        return "Коммутатор сброшен на заводские настройки успешно."
        # else:
        #     CONSOLE.print("Wrong input", style="fail")
        #     self.ssh.exit_config_mode()
        #     exit


    def cfg_base(self, commands_template):
        """ФУНКЦИЯ-шаблон настройки базового конфига."""
        # self.check_connection(self.VALUE_CONS_CONNECT)
        CfgTemplate.cfg_template(self, commands_template)
        return


# if __name__ == "__main__":
#     tr1 = TridentCfg()
#     tr1.check_connection()
#     tr1.ssh.enable()
#     # with open('./templates_cfg/cfg_current1.yaml') as commands:
#     #     commands_template = yaml.safe_load(commands)
#     print(tr1.extended_reset_cfg1())
