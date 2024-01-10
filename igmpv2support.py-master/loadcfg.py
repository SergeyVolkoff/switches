from telnet import Telnet
import time

def clear_cons(lines, ip, user, pwd):
    cons = Telnet(ip, user, pwd)
    cons.connect(b'Username', b'Password')
    cons.send_cmd('terminal length 0')
    for line in lines:
        print(cons.send_cmd(f'clear line tty {line}'))
        if 'OK' in cons.send_cmd(''):
            print(f'The line tty {line} was cleared')
    cons.conn_close()

def load_conf_bulat(configs_bulat, ip, user, pwd):
    for k1, v1 in configs_bulat.items():
        host = Telnet(ip, user, pwd, port=k1)
        print(host.connect(b'login', b'Password'))
        print(host.send_cmd('enable'))
        print(host.send_cmd('copy empty-config startup-config'))
        print(host.send_cmd('reload'))
        print(host.send_cmd('y', expectstr=b'login:'))
        print(host.connect(b'login', b'Password'))
        print(host.send_cmd('enable'))
        print(host.send_cmd('conf t'))
        conf = open(v1, 'r').read()
        time.sleep(2)
        print(host.send_cmd(conf))
        time.sleep(20)
        print(host.send_cmd('write'))
        host.conn_close()

def load_conf_cisco(config_cisco, ip, user=None, pwd=None):
    for k2, v2 in config_cisco.items():
        host = Telnet(ip, user, pwd, port=k2)
        print(host.send_cmd('\r\n'))
        host.connect(b'Username', b'Password')
        print(host.send_cmd('enable'))
        print(host.send_cmd('write erase'))
        time.sleep(5)
        print(host.send_cmd('\r'))
        print(host.send_cmd('reload', expectstr=b'[confirm]'))
        print(host.send_cmd('',  expectstr=b'(Timed out)'))        
        time.sleep(1)
        print(host.send_cmd(''))
        print(host.send_cmd('\r', expectstr=b'[yes/no]:'))
        print(host.send_cmd('no'))
        time.sleep(1)
        print(host.send_cmd('enable'))
        print(host.send_cmd('conf t'))
        conf = open(v2, 'r').read()
        time.sleep(2)     
        print(host.send_cmd(conf))
        time.sleep(40)
        print(host.send_cmd(''))
        print(host.send_cmd('write'))
        host.conn_close()  
        
def connect_bulat(ip, user, pwd, port):
    bulat = Telnet(ip, user, pwd, port=port)
    bulat.connect(b'login:', b'Password:')
    bulat.send_cmd('enable')
    return bulat

def connect_cisco(ip, user, pwd, port):
    cisco = Telnet(ip, user, pwd, port=port)
    cisco.connect(b'Username', b'Password')
    cisco.send_cmd('enable')
    return cisco
