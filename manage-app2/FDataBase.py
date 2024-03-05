import math
import sqlite3
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
            if res: return res
        except:
            print("Error read from DB")
        return[]
    
    def getSecondmenu(self):
        sql = '''SELECT * FROM secondmenu'''
        try:
            self.__cur.execute(sql) #
            res = self.__cur.fetchall() # вычитываем все записи
            if res: return res
        except:
            print("Error read from DB")
        return[]
    
    def getConstants_trident(self):
        sql = '''SELECT * FROM constants_trident'''
        try:
            self.__cur.execute(sql) #
            res = self.__cur.fetchall() # вычитываем все записи
            if res: return res
        except:
            print("Error read from DB")
        return res 
    
    def addConstants_trident(self,val):
        try:
            self.__cur.execute("UPDATE constants_trident SET val=(?) WHERE id = 6",(val,))
            self.__db.commit()
        except sqlite3.Error as err:
            print("Add port console error! "+ str(err))
            return False
        return True