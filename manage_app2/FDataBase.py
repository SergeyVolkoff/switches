import math
import sqlite3
import psycopg
import time

class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def getMainmenu(self):
        sql = '''SELECT * FROM mainmenu'''
        try:
            self.__cur.execute(sql) #
            res = self.__cur.fetchall() # вычитываем все записи
            print(res)
            if res: return res
        except:
            print("Error read mainmenu from DB")
        return[]
    
    def getSecondmenu(self):
        sql = '''SELECT * FROM secondmenu'''
        try:
            self.__cur.execute(sql) #
            res = self.__cur.fetchall() # вычитываем все записи
            if res: return res
        except:
            print("Error read secondmenu from DB")
        return[]
    
    def getThirdmenu(self):
        sql = '''SELECT * FROM thirdmenu'''
        try:
            self.__cur.execute(sql) #
            res = self.__cur.fetchall() # вычитываем все записи
            if res: return res
        except:
            print("Error read thirdmenu from DB")
        return[]
    
    def getConstants_trident(self):
        sql = '''SELECT * FROM constants_trident'''
        try:
            self.__cur.execute(sql) #
            res = self.__cur.fetchall() # вычитываем все записи
            if res: return res
        except:
            print("Error read constants_trident from DB")
        return res 
    
    def getTests_category(self):
        sql = '''SELECT * FROM tests_category'''
        try:
            self.__cur.execute(sql) #
            res = self.__cur.fetchall() # вычитываем все записи
            if res: return res
        except:
            print("Error read tests_category from DB")
        return res 
    
    def getDevice_type(self):
        sql = '''SELECT * FROM device_type'''
        try:
            self.__cur.execute(sql) #
            res = self.__cur.fetchall() # вычитываем все записи
            if res: return res
        except:
            print("Error read device_type from DB")
        return res 
    
    def getDevice(self):
        sql = '''SELECT * FROM device'''
        try:
            self.__cur.execute(sql) #
            res = self.__cur.fetchall() # вычитываем все записи
            if res: return res
        except:
            print("Error read device from DB")
        return res
    

    def getL2_test(self):
        sql = '''SELECT * FROM tests_all'''
        try:
            self.__cur.execute(sql) #
            res = self.__cur.fetchall() # вычитываем все записи
            if res: return res
        except:
            print("Error read tests_all from DB")
        return res
    

    # def getGNS_test(self):
    #     sql = '''SELECT * FROM gns_test'''
    #     try:
    #         self.__cur.execute(sql) #
    #         res = self.__cur.fetchall() # вычитываем все записи
    #         if res: return res
    #     except:
    #         print("Error read from DB")
    #     return res
    

    def getIDtemplate_testPage(self,cat, postId):
        try:
            self.__cur.execute(f"SELECT id,tag, name, path_schema, path_descr FROM tests_all WHERE tag = '{cat}' AND id = {postId} ")  #
            res = self.__cur.fetchone() # вычитываем  запис
            if res: return res
        except:
            print("Error read id,tag, name, path_schema, path_descr FROM tests_all from DB")
        return False 
    

    def getTemplate_testPage(self):
        sql = '''SELECT * FROM tests_all'''
        try:
            self.__cur.execute(sql) #
            res = self.__cur.fetchall() # вычитываем все записи
            if res: return res
        except:
            print("Error read tests_all from DB")
        return res


    def addConstants_trident(self,val):
        try:
            self.__cur.execute("UPDATE constants_trident SET val=(?) WHERE id = 6",(val,))
            self.__db.commit()
        except sqlite3.Error as err:
            print("Add port console error! "+ str(err))
            return False
        return True
    
    
    # def addPost(self,title,schema, test_specification, test_progress,result):
        # try:
        #     self.__cur.execute("INSERT INTO posts VALUES (NULL,?,?,?,?,?)", (title,schema, test_specification, test_progress,result,))
        #     self.__db.commit()
        # except sqlite3.Error as err:
        #     print("Add posts  error! "+ str(err))
        #     return False
        
    def getPost(self, postId):
        try:
            self.__cur.execute(f"SELECT id, schema, title, test_specification, test_progress,test_result FROM posts WHERE id = {postId}") #
            res = self.__cur.fetchone() # вычитываем  запис
            if res: return res
        except:
            print("Error read id, schema, title, test_specification, test_progress,test_result FROM posts from DB")
        return False 
    
    def readSchemaFromFile(n):
        try:
            with open(f"media/schema/{n}.jpg", "rb") as f:
                return f.read()
        except IOError as e:
            print(e)
            return False
        
    def addUser(self, name, email, hpsw):
        """Добавления юзера в БД с проверкой мыла на повтор"""
        try:
            self.__cur.execute(f"SELECT COUNT() as 'count' FROM users WHERE email LIKE '{email}'") # проверям мыло на существование в БД
            res = self.__cur.fetchone() # вычитываем  запис
            if res['count'] > 0:
                print('Пользователь с таким email уже есть в БД')
                return False
            tm = math.floor(time.time())
            self.__cur.execute("INSERT INTO users VALUES (NULL, ?, ?, ?, ?)", (name, email, hpsw, tm))
            self.__db.commit()
        except sqlite3.Error as er:
            print("Error add user into DB"+str(er))
            return False
        return True 
    
    def getUser(self, user_id):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE id ='{user_id}' LIMIT 1")  # проверям мыло на существование в БД
            res = self.__cur.fetchone() # вычитываем  запис
            if not res:
                print('Пользователь с таким email no')
                return False
            return res
        except sqlite3.Error as er:
            print("Error get user  WHERE id ='{user_id}' from DB"+str(er))
        return False
        
    def getUserByEmail(self, email):
        try:
            self.__cur.execute(f"SELECT * FROM users WHERE email='{email}' LIMIT 1")  # проверям мыло на существование в БД
            res = self.__cur.fetchone() # вычитываем  запис
            if not res:
                print('Пользователь с таким email no')
                return False
            return res
        except sqlite3.Error as er:
            print("Error get user from DB"+str(er))
        return False
