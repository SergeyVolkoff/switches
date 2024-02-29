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