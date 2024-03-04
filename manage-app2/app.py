import json
import sqlite3
import os
from flask import Flask, Response, flash,render_template, redirect, url_for, request, g 
import sys
import os

import yaml


sys.path.insert(1, os.path.join(sys.path[0], '..'))
from base_gns3 import Base_gns
from FDataBase import FDataBase
# from cfg_switch import TridentCfg

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
    global db
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


@app.route("/add_constants", methods = ['POST', 'GET'])
def add_constants():
    if request.method == 'POST':
        res = dbase.addConstants_trident(request.form['port'])
        port_con = request.form.get('port')
        print(port_con)
        if not res:
            flash("Error changed port console")
        else:
            flash("Settings changed and transferred to the database!")
        if res:
            flash("OK")
    # return render_template(
    #     'add_constants.html',
    #     title = "Меню настройки console",
    #     menu = dbase.getMainmenu(),
    #     )
    return redirect(url_for("get_constants"))

@app.route("/constants")
def get_constants():
    cur = db.cursor()
    cur.execute("SELECT title, val FROM constants_trident")
    VALUE_CONS_CONNECT = cur.fetchall()
    with open('../constants_trident1.yaml','w') as f:
        for i in VALUE_CONS_CONNECT:
            to_file = {i['title']:i['val']}
            print(to_file)
            for i in to_file:
                yaml.dump(to_file,f)
    with open('../constants_trident1.yaml') as f:
        print(f.read())

    return render_template('constants.html',
        title = "Constants",
        menu = dbase.getMainmenu(),
        constants = dbase.getConstants_trident(),
        )

    

@app.route("/test1")
def test1():
    return render_template('gre.html', title = "GRE", menu = dbase.getMainmenu(), secondmenu = dbase.getSecondmenu())

@app.route("/start_test_gre",methods = ['POST', 'GET'])
def start_test_gre():
    if request.method == "POST":
        flash("Button is pushed!")
        
    return render_template(
        'gre.html', title = "GRE",
        menu = dbase.getMainmenu(),
        secondmenu = dbase.getSecondmenu(),
        )  


if __name__ == "__main__":
    app.run(debug=True)