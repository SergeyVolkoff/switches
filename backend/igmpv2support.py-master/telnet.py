import telnetlib
import time

class Telnet:
    def __init__(self, ip, user, pwd, port=None):
        self.ip = ip
        self.user = user
        self.pwd = pwd
        self.port = port
        self.tn = telnetlib.Telnet(ip, port)
        
    def connect(self, userstr=None, pwdstr=None, expectstr=None):
        try:
            if userstr != None:
#                self.tn.open(self.ip, self.port)#, timeout=60)
                self.tn.write('\n'.encode("utf-8"))
                self.tn.read_until(userstr, timeout=10)
                self.tn.write(f'{self.user}\n'.encode("utf-8"))
                self.tn.read_until(pwdstr, timeout=10)
                self.tn.write(f'{self.pwd}\n'.encode("utf-8"))
                self.tn.write('\n'.encode("utf-8"))
                time.sleep(2)
                state = self.tn.read_very_eager().decode('utf-8')
            elif userstr == None:
#                self.tn.open(self.ip, self.port)#, timeout=60)
                self.tn.write('\n'.encode("utf-8"))
                if '#' in str(state):
                    if self.port == None:
                        print(f'You have successfully connected to {self.ip}')
                    if self.port != None:
                        print(f'You have successfully connected to {self.ip} port {self.port}')                    
                elif '>' in str(state):
                    if self.port == None:
                        print(f'You have successfully connected to {self.ip} but you need to switch to enable mode')
                    if self.port != None:
                        print(f'You have successfully connected to {self.ip} port {self.port} but you need to switch to enable mode')       
            else:
                if self.port == None:
                    print(f'Something is wrong with your connection to {self.ip}')
                if self.port != None:
                    print(f'Something is wrong with your connection to {self.ip} port {self.port}')                    
        except Exception as error:
            print(error)
    
    def send_cmd(self, cmd, expectstr=None):
        try:
            self.tn.write(f'{cmd}\n'.encode("utf-8"))
            time.sleep(2)
            if expectstr == None:
                return str(self.tn.read_very_eager().decode('utf-8'))
            if expectstr != None:
                return str(self.tn.read_until(expectstr, timeout=180))
        except Exception as error:
            print(error)
            
    def conn_close(self):
        self.tn.close()
        print(f'Connection to {self.ip} was closed')