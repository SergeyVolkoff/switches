import argparse
import fcntl
import logging
import pty
import select
import shlex
import sqlite3 as sq
import os
import sys
sys.path.insert(1, os.path.join(sys.path[0], '..'))
import struct
import subprocess
import termios
from flask import Flask, Response, abort, flash, make_response,render_template, redirect, url_for, request, g 

import sys
import os
from flask_socketio import SocketIO

import yaml
from cfg_switch import TridentCfg

from constants_trident import CONSOLE


sys.path.insert(1, os.path.join(sys.path[0], '..'))
from base_gns3 import Base_gns
from FDataBase import FDataBase
# from cfg_switch import TridentCfg

# from start_gns_test_GRE import StartGRE


# configuration
app = Flask(__name__)
SECRET_KEY = '*'
MAX_CONTENT_LEN=1024*1024
app.config.from_object(__name__)
app.config["child_pid"] = None
app.config["fd"] = None
socketio = SocketIO(app)
DATABASE = '/manage_app2/manage_app2.db'
DEBUG = True

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'manage_app2.db')))

def connect_db():
    conn = sq.connect(app.config['DATABASE']) # методу коннект передаем путь к базе
    conn.row_factory = sq.Row  # представит записи из базы в виде словаря
    return conn

def create_db():
    """Функция для создания таблиц БД"""
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f: # читаем скрипты sql для создания таблиц
        db.cursor().executescript(f.read())  # из установленного соединения db черезid класс cursor() запускаем выполнение скриптов sql
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

@app.route("/")
def index():
    return render_template(
        'index.html',menu = dbase.getMainmenu(),
        secondmenu = dbase.getSecondmenu(),
        constants = dbase.getConstants_trident())



@app.route("/reset",methods = ['POST', 'GET'])
def reset():
    result = ''
    if request.method == "POST":
        response = request.form['index'] # name="index" in reset.html
        print(response)
        flash("Warning! Switch settings will be reset to default settings!")
      
        result  = subprocess.run(["python3","/home/ssw/Documents/switches/reset_cfg.py"],stdout=subprocess.PIPE, text=True)
        # result  = result.returncode  
        result = result.stdout.split('\n')
        print(result)
        return render_template(
            'reset.html', 
            title = "Сброс конфига на дефолтные",
            menu = dbase.getMainmenu(),
            result = result)
    return render_template(
        'reset.html', title = "Сброс конфига на дефолтные",
        menu = dbase.getMainmenu(),
        constants = dbase.getConstants_trident())


@app.route("/add_constants", methods = ['POST', 'GET'])
def add_constants():
    if request.method == 'POST':
        res = dbase.addConstants_trident(request.form['port'])
      
        port_con = request.form.get('port')
        print(port_con)
        if not res:
            flash("Error changed value")
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


    
@app.route("/<int:id_post>",methods = ['POST', 'GET'])
def get_test(id_post):
    
    # img = FDataBase.readSchemaFromFile(id_post)
    # if not img:
    #     return "Err load img"
    # binary = sq.Binary(img)
    # cur = db.cursor()
    # if img:
    #     cur.execute("UPDATE posts SET schema= ? WHERE id = ?", (binary,id_post,))
    #     db.commit()
    # cur.execute("SELECT schema FROM posts WHERE id=?", (id_post,))
    # image_path = cur.fetchone()[0]
    id, schema, title, test_specification, test_progress,result = dbase.getPost(id_post)
    image_path=f'static/images/{id_post}.jpg'
    print(title)
    if request.method == "POST":
        # response = request.form['index']
        # print(response)
        flash("Button is pushed!")
        # from start_gns_test_GRE import StartGRE        
        # return response
        current_lab = Base_gns()
        print(current_lab.start_nodes_from_project())
        # REALIZOVAT!
        
    return render_template(
        'gre.html',  
        menu = dbase.getMainmenu(), secondmenu = dbase.getSecondmenu(),
        post=id,
        image_path=image_path,
        title=title,
        test_specification=test_specification,
        test_progress=test_progress,result=result,
        constants = dbase.getConstants_trident()
        )
@app.route("/cfg",methods = ['GET'])
def cfg():
    return render_template(
        'cfg.html', title = "Заливка конфига",
        menu = dbase.getMainmenu(),
        constants = dbase.getConstants_trident(),
        thirdmenu = dbase.getThirdmenu(),
        )

@app.route("/cfg/<int:id_post>",methods = ['POST', 'GET'])
def getCfgPage(id_post):
    result = ''
    if request.method == "POST":
        response = request.form['index'] # name="index" in reset.html
        print(response)
        result  = subprocess.run(["python3","/home/ssw/Documents/switches/cfg_gre.py"],stdout=subprocess.PIPE, text=True)
        # result  = result.returncode 
        if result:
            flash("Attention! The DUT configuration is in progress!",category='success')
        else:
            flash("Attention!configuration error send!",category='error')
        result = result.stdout.split('\n')
        # result = result.split('\n')
        # result = result.replace('\r\n', '<br>')
        print(result)
        return render_template(
            'cfg_gre.html', title = "настройка DUT под тест",
            menu = dbase.getMainmenu(),
            thirdmenu = dbase.getThirdmenu(),
            result = result)
    return render_template(
        'cfg_gre.html', title = "Заливка конфига",
        menu = dbase.getMainmenu(),
        constants = dbase.getConstants_trident(),
        thirdmenu = dbase.getThirdmenu(),
        )





"""socketio and PTY"""

# logging.getLogger("werkzeug").setLevel(logging.ERROR)
# __version__ = "0.5.0.2"

# def set_winsize(fd, row, col, xpix=0, ypix=0):
#     logging.debug("setting window size with termios")
#     winsize = struct.pack("HHHH", row, col, xpix, ypix)
#     fcntl.ioctl(fd, termios.TIOCSWINSZ, winsize)


# def read_and_forward_pty_output():
#     max_read_bytes = 1024 * 20
#     while True:
#         socketio.sleep(0.01)
#         if app.config["fd"]:
#             timeout_sec = 0
#             (data_ready, _, _) = select.select([app.config["fd"]], [], [], timeout_sec)
#             if data_ready:
#                 output = os.read(app.config["fd"], max_read_bytes).decode(
#                     errors="ignore"
#                 )
#                 socketio.emit("pty-output", {"output": output}, namespace="/pty")

# @socketio.on("pty-input", namespace="/pty")
# def pty_input(data):
#     """write to the child pty. The pty sees this as if you are typing in a real
#     terminal.
#     """
#     if app.config["fd"]:
#         logging.debug("received input from browser: %s" % data["input"])
#         os.write(app.config["fd"], data["input"].encode())


        

# @socketio.on("resize", namespace="/pty")
# def resize(data):
#     if app.config["fd"]:
#         logging.debug(f"Resizing window to {data['rows']}x{data['cols']}")
#         set_winsize(app.config["fd"], data["rows"], data["cols"])


# @socketio.on("connect", namespace="/pty")
# def connect():
#     """new client connected"""
#     logging.info("new client connected")
#     if app.config["child_pid"]:
#         # already started child process, don't start another
#         return

#     # create child process attached to a pty we can read from and write to
#     (child_pid, fd) = pty.fork()
#     if child_pid == 0:
#         # this is the child process fork.
#         # anything printed here will show up in the pty, including the output
#         # of this subprocess
#         subprocess.run(app.config["cmd"])
#     else:
#         # this is the parent process fork.
#         # store child fd and pid
#         app.config["fd"] = fd
#         app.config["child_pid"] = child_pid
#         set_winsize(fd, 50, 50)
#         cmd = " ".join(shlex.quote(c) for c in app.config["cmd"])
#         # logging/print statements must go after this because... I have no idea why
#         # but if they come before the background task never starts
#         socketio.start_background_task(target=read_and_forward_pty_output)

#         logging.info("child pid is " + child_pid)
#         logging.info(
#             f"starting background task with command `{cmd}` to continously read "
#             "and forward pty output to client"
#         )
#         logging.info("task started")


# def main():
#     parser = argparse.ArgumentParser(
#         description=(
#             "A fully functional terminal in your browser. "
#             "https://github.com/cs01/pyxterm.js"
#         ),
#         formatter_class=argparse.ArgumentDefaultsHelpFormatter,
#     )
#     parser.add_argument(
#         "-p", "--port", default=5000, help="port to run server on", type=int
#     )
#     parser.add_argument(
#         "--host",
#         default="127.0.0.1",
#         help="host to run server on (use 0.0.0.0 to allow access from other hosts)",
#     )
#     parser.add_argument("--debug", action="store_true", help="debug the server")
#     parser.add_argument("--version", action="store_true", help="print version and exit")
#     parser.add_argument(
#         "--command", default="bash", help="Command to run in the terminal"
#     )
#     parser.add_argument(
#         "--cmd-args",
#         default="",
#         help="arguments to pass to command (i.e. --cmd-args='arg1 arg2 --flag')",
#     )
#     args = parser.parse_args()
#     if args.version:
#         print(__version__)
#         exit(0)
#     app.config["cmd"] = [args.command] + shlex.split(args.cmd_args)
#     green = "\033[92m"
#     end = "\033[0m"
#     log_format = (
#         green
#         + "pyxtermjs > "
#         + end
#         + "%(levelname)s (%(funcName)s:%(lineno)s) %(message)s"
#     )
#     logging.basicConfig(
#         format=log_format,
#         stream=sys.stdout,
#         level=logging.DEBUG if args.debug else logging.INFO,
#     )
#     logging.info(f"serving on http://{args.host}:{args.port}")
#     socketio.run(app, debug=args.debug, port=args.port, host=args.host)


# if __name__ == "__main__":
#     main()




if __name__ == "__main__":
#     # socketio.run(app, debug=True)
    app.run()