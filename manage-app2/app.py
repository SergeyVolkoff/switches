import sqlite3
import os
from flask import Flask,render_template, redirect, url_for, request, g 

# configuration
DATABASE = '/tmp/manage_app.db'
DEBUG = True
SECRET_KET = 'qwerty12345'

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'manage_app.db')))

def connect_db():
    conn = sqlite3.connect(app.config['DATABASE']) # методу коннект передаем путь к базе
    conn.row_factory = sqlite3.Row  # представит записи из базы в виде словаря
    return conn

def create_db():
    """Функция для создания таблиц БД"""
    db = connect_db()
    with app.open_resource('sq_db.sql',mode='r') as f: # читаем скрипты sql для создания таблиц
        db.cursor().executescript(f.read())  # из установленного соединения db через класс cursor() запускаем выполнение скриптов sql
    db.commit()
    db.close()


secondmenu = [{"name": "Проверка поддержки GRE", "url": "/test1"},
              {"name": "Проверка поддержки test2", "url": "/test2"},
              {"name": "Проверка поддержки test3", "url": "/test3"}]

menu = [{"name": "Меню тестов", "url": "/"},
        {"name": "Меню конфигов", "url": "cfg"},
        {"name": "Меню сброса настроек", "url": "reset"}]

def get_db():
    """Соединение с БД, если оно еще не установлено"""
    if not hasattr(g,'link_db'):
        g.link_db = connect_db()
    return g.link_db

@app.route("/")
def index():
    db = get_db()
    return render_template(
        'index.html',
        menu =[{"name": "Меню тестов", "url": "/"},
        {"name": "Меню конфигов", "url": "cfg"},
        {"name": "Меню сброса настроек", "url": "reset"}]
        )

@app.teardown_appcontext
def close_db(error):
    """Закрываем соединение с БД, если оно установлено"""
    if hasattr(g,'link_db'):
        g.link_db.close()

# @app.route("/")
# def index():
#     return render_template('index.html', title="Основные тесты коммутатора Trident", menu = menu, secondmenu=secondmenu)

@app.route("/cfg")
def cfg():
    return render_template('cfg.html', title = "Заливка конфига", menu = menu)

@app.route("/reset")
def reset():
    return render_template('cfg.html', title = "Сброс конфига на деволтные", menu = menu)

@app.route("/test1")
def test1():
    return render_template('gre.html', title = "GRE", menu = menu)

if __name__ == "__main__":
    app.run(debug=True)