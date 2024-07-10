import threading
import time
import os
import datetime
import logging
import json
from telnet import Telnet
from IxiaApi import IxAPI
from readpcap import *
from docxpdfreporter import *
from loadcfg import *


##======================Переменные==========================================
#Сведения о тестируемой платформе
Platform = 'BS7510-48X6Q'

#Словарь для временных переменных результатов теста
results = {'Platform': Platform, 'TestNumber': 'IGMPv2 support'}

#Директории для результатов и логов теста, задание параметров логирования
cur_dir = os.path.realpath('').replace(os.path.sep, '/')
res_directory = "results"
log_directory = "debug"
cur_time = datetime.datetime.now().strftime("%d_%m_%y_%H_%M_%S")

if not os.path.exists(res_directory):
    os.makedirs(res_directory)
if not os.path.exists(log_directory):
    os.makedirs(log_directory)

#log_file = f"{log_directory}/{results['TestNumber']}_{cur_time}.log"

#logger = logging.getLogger("Debug")
#logger.setLevel(logging.DEBUG)
#logfile = logging.FileHandler(log_file)
#logfile.setLevel(logging.WARNING)
#formatter = logging.Formatter(
#    "{asctime} - {name} - {levelname} - {message}", datefmt="%H:%M:%S", style="{"
#)
#logfile.setFormatter(formatter)
#logger.addHandler(log_file)

#Словарь консольных портов и файлов конфигурации для Bulat
configs_bulat = {2039: 'Configs/TR2_IGMPv2_support.log',
          2040: 'Configs/TR4_IGMPv2_support.log',
          2041: 'Configs/TR3_IGMPv2_support.log',
          }

#Словарь консольных портов и файлов конфигурации для референсных устройств
config_cisco = {2028: 'Configs/ME3400_IGMPv2_support.log'}

#Данные консольного сервера, хостов
ip_cons = '10.27.193.2'
user_cons = 'admin'
pwd_cons = 'bulat'
user_bulat = 'admin'
pwd_bulat = 'bulat'
lines = [28, 39, 40, 41]

#Данные для подключения к IxAPI серверу
ixiaApiServer = "127.0.0.1"
ixiaApiPort = '11009'
ixiaChassis = "10.27.192.3"
#ixiaApiAuth = {"username": "admin",
#              "password": "admin"}


##=====================Последовательность теста====================
#1. Очистка консольных сессий, удаление и загрузка новых конфигураций устройств
print('1. Очистка консольных сессий, удаление и загрузка новых конфигураций устройств')
clear_tty = threading.Thread(target=clear_cons, args=(lines, ip_cons, user_cons, pwd_cons)) 
clear_tty.start()
clear_tty.join()


load_conf_bulat = threading.Thread(target=load_conf_bulat,
                                    args=(configs_bulat, ip_cons, user_bulat, pwd_bulat))
load_conf_bulat.start()
load_conf_bulat.join()

load_conf_cisco(config_cisco, ip_cons, user=user_cons, pwd=pwd_cons)

#2. Очистка консольных сессий и подключение к устройствам
print('2. Очистка консольных сессий и подключение к устройствам')
clear_tty = threading.Thread(target=clear_cons, args=(lines, ip_cons, user_cons, pwd_cons)) 
clear_tty.start()
clear_tty.join()
tr2 = connect_bulat(ip_cons, user_bulat, pwd_bulat, 2039)
tr3 = connect_bulat(ip_cons, user_bulat, pwd_bulat, 2041)
tr4 = connect_bulat(ip_cons, user_bulat, pwd_bulat, 2040)
me3400 = connect_cisco(ip_cons, None, None, 2028)

#3. Определение версии BulatOS для отчета
print('3. Определение версии BulatOS для отчета')
results.update({'TR2ShVersion': str(tr2.send_cmd('show version'))})

#4. Подключение к IXIA. Загрузка конфигурационного файла (данные по API серверу указану в IxiaApi.py, файл ниже)
print('4. Подключение к IXIA. Загрузка конфигурационного файла')
conn = IxAPI(ixiaApiServer, ixiaApiPort)
conn.conn_srvr()
conn.verif_sessions()
file = f"{cur_dir}/Configs/IGMPv2_support.ixncfg"
conn.load_conf(file)

#5. Проверка состояния протоколов OSPF, PIM на всех устройствах с сохранением результатов 
print('5. Проверка состояния протоколов OSPF, PIM на всех устройствах')
tr2.send_cmd('terminal length 0')
tr3.send_cmd('terminal length 0')
tr4.send_cmd('terminal length 0')
me3400.send_cmd('terminal length 0')
results.update({'TR2OspfNeighbor_1_1': str(tr2.send_cmd('show ip ospf neighbor')).replace('\r', '')})
results.update({'TR2PimNeighbor_1_1': str(tr2.send_cmd('show ip pim neighbor')).replace('\r', '')})
results.update({'TR2PimMapping_1_1': str(tr2.send_cmd('show ip pim rp mapping')).replace('\r', '')})
#results.update({'TR2IgmpInterface_1': str(tr2.send_cmd('show ip igmp interface')).replace('\r', '')})
results.update({'TR3OspfNeighbor_1_1': str(tr3.send_cmd('show ip ospf neighbor')).replace('\r', '')})
results.update({'TR3PimNeighbor_1_1': str(tr3.send_cmd('show ip pim neighbor')).replace('\r', '')})
results.update({'TR3PimMapping_1_1': str(tr3.send_cmd('show ip pim rp mapping')).replace('\r', '')})
results.update({'TR4OspfNeighbor_1_1': str(tr4.send_cmd('show ip ospf neighbor')).replace('\r', '')})
results.update({'TR4PimNeighbor_1_1': str(tr4.send_cmd('show ip pim neighbor')).replace('\r', '')})
results.update({'TR4PimMapping_1_1': str(tr4.send_cmd('show ip pim rp mapping')).replace('\r', '')})
results.update({'ME3400OspfNeighbor_1_1': str(me3400.send_cmd('show ip ospf neighbor')).replace('\r', '')})
results.update({'ME3400PimNeighbor_1_1': str(me3400.send_cmd('show ip pim neighbor')).replace('\r', '')})
results.update({'ME3400PimMapping_1_1': str(me3400.send_cmd('show ip pim rp mapping')).replace('\r', '')})

#6. Проверки версии протокола IGMP на интерфейсах TR2
print('6. Проверки версии протокола IGMP на интерфейсах TR2')
results.update({'TR2IgmpInterface_1_2': str(tr2.send_cmd('show ip igmp interface xe1')).replace('\r', '')})

#7. Включение протоколов на NTG, запуск трафика
print('7. Включение NTG')
print('7.1. Формирование списка виртуальных и физических портов из файла конфигурации')
print(conn.get_vport())
vportList = conn.get_vport()[0]
portList = conn.get_vport()[1]

print('7.2. Переопределение портов IXIA')
conn.assign_port(vportList, portList)
time.sleep(60)

print('7.4. Включение протоколов на NTG, запуск трафика')
print(conn.start_proto())
time.sleep(60)
print(conn.apply_traffic())
time.sleep(60)
print(conn.start_traffic())

#8. Проверка счетчиков IGMP Report на TR2
print('8. Проверка счетчиков IGMP Report на TR2')
results.update({'TR2IgmpInterface_1_3': str(tr2.send_cmd('show ip igmp interface xe1')).replace('\r', '')})

#9. Проверка IGMP группы на TR2
print('9. Проверка IGMP группы на TR2')
results.update({'TR2ShIpIgmpGroups_1_4': str(tr2.send_cmd('show ip igmp groups')).replace('\r', '')})

##10. Проверка прохождения multicast от источника к приемнику
print('10. Проверка прохождения multicast от источника к приемнику')
time.sleep(120)
stats = conn.get_stats(15)
dictStats = {}
capt = stats['columnCaptions']
val = stats['rowValues']['arg1'][0]

dictStats.update({capt[0]: val[0], capt[1]: val[1],
                  capt[2]: val[2], capt[3]: val[3]})
flowStats = str(dictStats)
results.update({'flowStats_1_5': flowStats})

#11. Остановка трафика и протоколов на NTG
print('11. Остановка трафика и протоколов на NTG')
conn.stop_traffic()
conn.stop_proto() 

#12. Включение на IXIA записи в pcap зеркалируемого трафика
print('12. Включение на IXIA записи в pcap зеркалируемого трафика')
conn.start_capt(3, "dataTraffic")

print(conn.start_proto())
time.sleep(30)
print(conn.start_traffic())

#13. Проверка формата и типов сообщений IGMPv2
print('13. Проверка формата и типов сообщений IGMPv2\n\n'
'Внимание!!! В связи с неполностью реализованной функциональностью IXIA Rest API по управлению IGMP (отправка сообщений leave и join), данную часть теста предполагается выполнять вручную, следуя подсказкам')

print('Покинуть группу 235.0.0.1 со стороны IGMP хоста')
act1 = input('Сообщение leave для группы 235.0.0.1 отправлено? Ответ y/Y/yes/Yes/YES:') 
time.sleep(3) 
if 'y' in str.lower(act1):
    print('Подписаться на группу 235.0.0.1 со стороны IGMP хоста')
    act2 = input('Сообщение join для группы 235.0.0.1 отправлено? Ответ y/Y/yes/Yes/YES:')  
    time.sleep(3) 
    if 'y' in str.lower(act2):
        time.sleep(180)
        print('Покинуть группу 235.0.0.1 со стороны IGMP хоста')
        act3 = input('Сообщение leave для группы 235.0.0.1 отправлено? Ответ y/Y/yes/Yes/YES:') 
        time.sleep(3) 
        if 'y' in str.lower(act3):
            time.sleep(10)  
            print('Подписаться на группу 235.0.0.1 со стороны IGMP хоста')
            act4 = input('Сообщение join для группы 235.0.0.1 отправлено? Ответ y/Y/yes/Yes/YES:')
            time.sleep(3) 
            if 'y' in str.lower(act4):
                time.sleep(180)
 
##12. Остановка записи зеркалируемого трафика, сохранение результатов, анализ
print('12. Остановка записи зеркалируемого трафика, сохранение результатов, анализ')
conn.stop_capt(3, "allTraffic")
conn.save_capt(f'{cur_dir}/{res_directory}/')
time.sleep(90)
results.update({'IGMPv2GenQuery_2_4': readpcap(f'{cur_dir}/{res_directory}/2-2_HW.cap', "b'\\x11d\\", "load")})
results.update({'IGMPv2SpecQuery_2_4': readpcap(f'{cur_dir}/{res_directory}/2-2_HW.cap', "b'\\x11\\", "load")})

##13. Создание отчетов о тестировании
print('13. Создание отчетов о тестировании')
#test_name = {results['TestNumber']}
try:
    gendocx('Templates/Template_IGMPv2_support.docx', results, f"{cur_dir}/{res_directory}/{results['TestNumber']}_{cur_time}.docx")
    docx2pdf(f"{cur_dir}/{res_directory}/{results['TestNumber']}_{cur_time}.docx", f"{cur_dir}/{res_directory}/{results['TestNumber']}_{cur_time}.pdf")
except Exception as err:
    print(err)

##14. Остановка трафика и выключение протоколов на NTG 
print('14. Остановка трафика и выключение протоколов на NTG')
conn.stop_traffic()
conn.stop_proto()
conn.close_conn()

with open(f"{cur_dir}/{res_directory}/{results['TestNumber']}_{cur_time}", 'w') as convert_file:
     convert_file.write(json.dumps(results))
