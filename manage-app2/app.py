import sqlite3
import os
from flask import Flask, flash,render_template, redirect, url_for, request, g 
import sys
import os


sys.path.insert(1, os.path.join(sys.path[0], '..'))
from base_gns3 import Base_gns
from FDataBase import FDataBase
# from start_gns_test_GRE import StartGRE


# configuration
DATABASE = '/manage_app2/manage_app2.db'
DEBUG = True
SECRET_KEY = 'qwerty12345'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'manage_app2.db')))

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE']) # методу коннект передаем путь к базе
    conn.row_factory = sqlite3.Row  # представит записи из базы в виде словаря
    return conn

def create_db():
    """Функция для создания таблиц БД"""
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f: # читаем скрипты sql для создания таблиц
        db.cursor().executescript(f.read())  # из установленного соединения db через класс cursor() запускаем выполнение скриптов sql
    db.commit()
    db.close()

def get_db():
    """Соединение с БД, если оно еще не установлено"""
    if not hasattr(g,'link_db'):
        g.link_db = connect_db()
    return g.link_db

@app.before_request
def before_request():
    """Установка соединения с БД перед выполнением запроса"""
    global dbase
    db = get_db()
    dbase = FDataBase(db)

@app.teardown_appcontext
def close_db(error):
    """Закрываем соединение с БД, если оно установлено"""
    if hasattr(g,'link_db'):
        g.link_db.close()


# @app.route("/")
# def index():
#     db = get_db()
#     return render_template(
#         'index.html',
#         menu =[{"name": "Меню тестов", "url": "/"},
#         {"name": "Меню конфигов", "url": "cfg"},
#         {"name": "Меню сброса настроек", "url": "reset"}]
#         )


# @app.route("/")
# def index():
#     return render_template('index.html', title="Основные тесты коммутатора Trident", menu = menu, secondmenu=secondmenu)

@app.route("/")
def index():
    return render_template('index.html',menu = dbase.getMainmenu(),secondmenu = dbase.getSecondmenu())

@app.route("/cfg")
def cfg():
    return render_template('cfg.html', title = "Заливка конфига", menu = dbase.getMainmenu())

@app.route("/reset")
def reset():
    return render_template('cfg.html', title = "Сброс конфига на деволтные", menu = dbase.getMainmenu())

@app.route("/constants", methods = ['POST', 'GET'])
def constants():
    if request.method == 'POST':
        print(type(int(request.form["port"])))
    return render_template('constants.html',title = "Меню настройки подключения и тестов", menu = dbase.getMainmenu())

@app.route("/test1")
def test1():
    return render_template('gre.html', title = "GRE", menu = dbase.getMainmenu(), secondmenu = dbase.getSecondmenu())

@app.route("/start_test_gre",methods = ['POST', 'GET'])
def start_test_gre():
    if request.method == "POST":
        print("Button is pushed!")
        flash("Button is pushed!")
        current_lab = Base_gns()  # test wait this lab: SSV_auto_Tr_GRE
        print(current_lab.start_nodes_from_project())
    return render_template('gre.html', title = "GRE", menu = dbase.getMainmenu(), secondmenu = dbase.getSecondmenu())  


if __name__ == "__main__":
    app.run(debug=True)