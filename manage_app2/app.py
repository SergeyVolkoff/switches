"""Приложение для обработки страниц тестирования коммутатора."""
import sqlite3 as sq
import os
import sys
import subprocess
from threading import Thread
import time
import yaml
sys.path.insert(1, os.path.join(sys.path[0], '..'))
from flask import (abort,Flask, Response, 
                   flash, jsonify, make_response,
                   render_template, redirect, send_from_directory,
                   session, url_for, request, g)
from flask_login import (
    LoginManager, current_user, login_required, login_user,
    logout_user)

from wtforms import (DecimalField, Form,BooleanField, StringField,
                     PasswordField, ValidationError, validators)
from wtforms.validators import InputRequired, Regexp

from doc_reporter import report_doc

from flask_socketio import SocketIO
from werkzeug.security import generate_password_hash, check_password_hash
from base_gns3 import Base_gns
from manage_app2.FDataBase import FDataBase
from manage_app2.UserLogin import UserLogin
from werkzeug.utils import secure_filename




# configuration
app = Flask(__name__)
SECRET_KEY = '*'
MAX_CONTENT_LEN = 1024*1024

app.config.from_object(__name__)
app.config["child_pid"] = None
app.config["fd"] = None
socketio = SocketIO(app)
DATABASE = '/manage_app2/manage_app2.db'
DEBUG = True
UPLOAD_FOLDER = '../templates_cfg'
ALLOWED_EXTENSIONS = {'txt', 'yaml'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config.update(dict(DATABASE=os.path.join(app.root_path, 'manage_app2.db')))
login_manager = LoginManager(app)
"""перенаправлять пользователя на форму авторизации, атрибуту
login_view присваиваем имя функции представления для формы авторизации."""
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"


@login_manager.user_loader
def load_user(user_id):
    """объект UserLogin.

    Здесь будет создваться объект UserLogin
    при каждом запросе, если пользователь авторизован.
    """
    print('load_user')
    return UserLogin().fromDB(user_id, dbase)


def connect_db():
    """методу коннект передаем путь к базе."""
    conn = sq.connect(app.config['DATABASE'],check_same_thread=False)
    """представит записи из базы в виде словаря."""
    conn.row_factory = sq.Row
    return conn


def create_db():
    """Функция для создания таблиц БД."""
    db = connect_db()
    # читаем скрипты sql для создания таблиц
    with app.open_resource('sq_db.sql', mode='r') as f:
        # из установленного соединения db черезid класс cursor()
        # запускаем выполнение скриптов sql
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    """Соединение с БД, если оно еще не установлено."""
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.before_request
def before_request():
    """Установка соединения с БД перед выполнением запроса."""
    global dbase
    global db
    db = get_db()
    dbase = FDataBase(db)

# Мешает выводу консоли в html
# @app.teardown_appcontext
# def close_db(error):
#     """Закрываем соединение с БД, если оно установлено."""
#     if hasattr(g, 'link_db'):
#         g.link_db.close()



@app.route("/post/<alias>")
@login_required
def showPost(alias):
    """Пустая ф-я."""
    title, post = dbase.getPost(alias)
    if not title:
        abort(404)
    return render_template(
        'post.html', menu=dbase.getMenu(), title=title, post=post)


@app.route("/")
def index():
    """Обработчик index-страницы."""
    return render_template(
        'index.html', menu=dbase.getMainmenu(),
        secondmenu=dbase.getSecondmenu(),
        constants=dbase.getConstants_trident(),
        device = dbase.getDevice(),
        device_type = dbase.getDevice_type(),
        tests_category = dbase.getTests_category(),
        l2_test = dbase.getL2_test(),
        gns_test = dbase.getGNS_test(),
        )
@app.route("/bm10hp2xlte")
def bm10hp2xlte():
    return render_template(
        "bm10hp2xlte.html",
        menu=dbase.getMainmenu(),
        secondmenu=dbase.getSecondmenu(),
        constants=dbase.getConstants_trident(),
        tests_category = dbase.getTests_category(),

    )


@app.route("/base_tests")
def base_tests():
    """Обработчик base_tests-страницы."""
    return render_template(
        'base_tests.html', menu=dbase.getMainmenu(),
        secondmenu=dbase.getSecondmenu(),
        constants=dbase.getConstants_trident())


@app.route("/get_ver_sw", methods=['POST', 'GET'])
def get_ver_sw():
    "Обработчик выводит на страницу версию устр-ва"
    if request.method == "POST":
        response = request.form['index']  # name="index" in reset.html
        print(response)
        temp = os.system("python3 ../sh_ver.py")
        time.sleep(2)
        file_ver = '../process_temp.txt'
        for line in file_ver:
            with open(file_ver, 'r') as file:
                text = file.readlines()
        with open("../process_temp.txt", 'w') as file:
            file.write('')      
        return render_template('constants.html',
        title = "Настройки",
        menu = dbase.getMainmenu(),
        constants = dbase.getConstants_trident(),
        text=text
    )


@app.route("/add_constants", methods=['POST', 'GET'])
def add_constants():
    """Add in table constants.

    Обработчик ввода порта в табличку настройки устр-ва и возвращает
    страницу настроек."""
    if request.method == 'POST':
        res = dbase.addConstants_trident(request.form['port'])
        port_con = request.form.get('port')
        print(port_con)
        if not res:
            flash("Error changed port value")   
        else:
            flash("Настройки консольного порта сохранены в БД.")
       
    # return render_template(
    #     'add_constants.html',
    #     title = "Меню настройки console",
    #     menu = dbase.getMainmenu(),
    #     )
    return redirect(url_for("get_constants"))

class ValidValueConsolePort(Form):
    port = DecimalField('Port console',
                       [
                        validators.Length(min=4,max=4,
                        message='Длина port должна быть в диапазоне от 4 до 4.'),
                        # validators.Regexp(r'^\d+$', message='Номер порта - это только цифры.'),
                        validators.NumberRange(min=2000,max=2066,message='Номер порта консольного сервера в диапазоне 2003-2066.'),
                        validators.InputRequired(message='Это обязательное поле.')
                        ])
    # port = StringField('Port console', validators=[InputRequired(), Regexp(r'^\d+$', message='Please enter only digits')])


@app.route("/constants", methods=['POST', 'GET'])
def get_constants():
    """Обработчик выводит страницу настройки устр-ва."""
    form = ValidValueConsolePort(request.form)
    cur = db.cursor()  # Создаем курсор для выполнения SQL-запросов
    # Выполняем запрос для получения данных из таблицы constants_trident
    cur.execute("SELECT title, val FROM constants_trident")
    VALUE_CONS_CONNECT = cur.fetchall()
    # Открываем файл constants_trident1.yaml в режиме записи
    with open('../constants_trident1.yaml', 'w') as f:
        # Проходим по всем данным, полученным из БД
        for i in VALUE_CONS_CONNECT:
            # Создаем словарь с ключом "title" и значением "val"
            to_file = {i['title']: i['val']}
            print(to_file)
            for i in to_file:
                 # Записываем словарь to_file в файл f с использованием YAML
                yaml.dump(to_file, f)
    # Открываем файл constants_trident1.yaml в режиме чтения
    with open('../constants_trident1.yaml') as f:
        print(f.read())
    # global constants
    return render_template('constants.html',
        title = "Настройки",
        menu = dbase.getMainmenu(),
        constants = dbase.getConstants_trident(),
        form=form
        )

@app.route("/reset", methods=['POST', 'GET'])
def reset():
    """Обработчик страницы сброса конфига."""
    result = ''
    if request.method == "POST":
        
        response = request.form['index']  # name="index" in reset.html
        print(response)
        # result = subprocess.run(
        #     ["python3",
        #      "../reset_cfg.py"],
        #     stdout=subprocess.PIPE, text=True)
        # result = result.stdout.split('\n')

        args=["python3", "../reset_cfg.py"]
        process = subprocess.Popen(args, stdout=subprocess.PIPE) 
        for line in process.stdout:
            # print("stdout:", line.decode('utf-8'))
            with open("../process_temp.txt", 'a') as file:
                str_result = line.decode('utf-8')
                file.write(str_result) 

                    
        #     result = os.system("python3 ../reset_cfg.py")
           
        # if '' in result:
        #     flash('Сброс прошел успешно',category='success')
        # else:
        #     flash('Сброс прошел с ошибкой',category='error' )
        time.sleep(5)
        with open("../process_temp.txt", 'w'):
            pass  # не удальть - очищает файл
        flash(
            "Внимание! Коммутатор сброшен на заводские настройки",
            category='success')
        return render_template(
            'reset.html',
            title="Сброс конфига на дефолтные",
            menu=dbase.getMainmenu(),
            constants = dbase.getConstants_trident(),
            result=str_result
            )
    
    return render_template(
        'reset.html', title="Сброс конфига на дефолтные",
        menu=dbase.getMainmenu(),
        constants = dbase.getConstants_trident()
        )

@app.route("/gns_<int:id_post>",methods = ['POST', 'GET'])
def get_test(id_post):
    """Ф-я выводит в веб страницу тестов,кнопки старта и отчета
      и  текстовый результат тестов """
    id, schema, title, test_specification, test_progress,test_result = dbase.getPost(id_post)
    image_path=f'static/images/{id_post}.jpg'
    print(title)
    if request.method == "POST":
        flash("Button is pushed!")
        current_lab = Base_gns('SSV_auto_Tr_GRE')
        print(current_lab.start_nodes_from_project())
        response = request.form['in'] # name="index" in Vtest.html
        
        # result  = subprocess.run(["python3","../gre_test.py"],stdout=subprocess.PIPE, text=True)
        # if result:
        #     flash("Attention! The DUT test is in progress!",category='success')
        # else:
        #     flash("Attention!Start test error send!",category='error')
        # result = result.stdout.split('\n')
        # print(result)

        args=["python3", "../gre_test.py"]
        process = subprocess.Popen(args, stdout=subprocess.PIPE) 
        for line in process.stdout:
            # print("stdout:", line.decode('utf-8'))
            with open("../process_temp.txt", 'a') as file:
                str_result = line.decode('utf-8')
                file.write(str_result)
        with open("../process_temp.txt", 'w'):
            pass
        report_doc() # вызов ф-ии сздания ворд-отчета
        flash(
            "Внимание! Тесты выполнены, ознакомьтесь с результатами в отчетах.",
            category='error')
        return render_template(
            f'gns_{id_post}.html', title = "настройка DUT под тест",
            menu = dbase.getMainmenu(),
            thirdmenu = dbase.getThirdmenu(),
            result = str_result)
    
    return render_template(
        f'gns_1.html',  # Реализовать вызов универсальных стр(переделать HTML)
        menu = dbase.getMainmenu(), secondmenu = dbase.getSecondmenu(),
        post=id,
        image_path=image_path,
        title=title,
        test_specification=test_specification,
        test_progress=test_progress,
        constants = dbase.getConstants_trident()
        )

# переделать маршрут и запуск аллюре из места с тестами!!!
@app.route("/999",methods = ['GET','POST'])
def get_test_html():
    """Ф-я запускает сервер allure и открывает страницу с отчетом"""
    if request.method == "POST":
        flash("Button 'result HTML test' is pushed!")
        os.system("allure serve  -p 38671 allure_report")
    # print(temp)
    # temp1 = re.search(r'//\d+.\d+.\d+.\d+:(?P<servAllurePort>\d+)',temp)
    # print(temp1)
    # servAllurePort = temp1.group('servAllurePort')
    # print(servAllurePort)
    #     return f"""<a href='http://http://127.0.0.1:38671'</a>"""
    return render_template(
        'index.html',menu = dbase.getMainmenu(),
        secondmenu = dbase.getSecondmenu(),
        constants = dbase.getConstants_trident()
        )
        
@app.route("/cfg",methods = ['GET'])
def cfg():
    """Ф-я открывает страницу с заливкой конфига"""
    return render_template(
        'cfg.html', title = "Конфигурация устройства",
        menu = dbase.getMainmenu(),
        constants = dbase.getConstants_trident(),
        thirdmenu = dbase.getThirdmenu(),
        )

@app.route("/cfg/<int:id_post>",methods = ['POST', 'GET'])
def getCfgPage(id_post):
    """Ф-я запускает заливку конфига и возвращает страницу заливки"""
    
    if request.method == "POST":
        response = request.form['index1']# name="index" in ..html
        print(response)
        if "Настройка конфигурации" in response:
            # path_cfg="../cfg_gre.py"
            # result  = subprocess.run(["python3",path_cfg],stdout=subprocess.PIPE, text=True)
            # # result  = result.returncode 
            # result = result.stdout.split('\n')

            args=["python3", "../cfg_gre.py"]
            process = subprocess.Popen(args, stdout=subprocess.PIPE)
            
            for line in process.stdout:
                # print("stdout:", line.decode('utf-8'))
                with open("../process_temp.txt", 'a') as file:
                    str_result = line.decode('utf-8')
                    file.write(str_result)
            time.sleep(5)
            with open("../process_temp.txt", 'w'):
                pass
            flash("Устройство успешно сконфигурировано! ",category='success')
            return render_template(
                'cfg_gre.html', title = "Настройка устройства под тест",
                menu = dbase.getMainmenu(),
                thirdmenu = dbase.getThirdmenu(),
                constants = dbase.getConstants_trident()
                )
    
    return render_template(
        'cfg_gre.html', title = "Конфигурация устройства",
        menu = dbase.getMainmenu(),
        thirdmenu = dbase.getThirdmenu(),
        constants = dbase.getConstants_trident()
        )


@app.route('/get_content',methods = ['POST', 'GET'])
# Ф-я для получения вывода с консоли записаного в файл.
def get_content():
    with open('../process_temp.txt', 'r') as file:
        content = file.readlines()
    return jsonify({'content': content})


@app.errorhandler(404)
def pageNotFounretd(error):
    return render_template (
        'page404.html',
        title='Страница не найдена, но если она очень нужна - я ее сделаю.',
        menu=dbase.getMainmenu())

@app.route("/login", methods=["GET","POST"])
def login():
    """Обработчик для авторизации пользователя"""
    if current_user.is_authenticated:   # через прокси-юзер current_user проверяем: является ли пользователь авторизованным
        return redirect(url_for('profile')) 

    if request.method == 'POST':
        user= dbase.getUserByEmail(request.form['email']) # обращаемся к БД и считываем информацию о пользователе по email
        if user and check_password_hash(user['psw'],request.form['psw']): # Если верно введен пароль..
            userlogin = UserLogin().create(user) #..то формируется объект класса UserLogin
            rm = True if request.form.get('remainme') else False # проверка чек-бокс Запомнить меня
            login_user(userlogin, remember=rm)
            return redirect(request.args.get('next') or url_for('profile')) # перейдем либо на предыдущую страницу, либо в профайл
        flash('Неверная пара логин\пароль','error')
    return render_template('login.html',title="Авторизация", menu=dbase.getMainmenu())

class RegistrationForm(Form):
    """Класс для модуля WTForm - проверка данных в полях регистрации"""
    name = StringField('Имя пользователя',
                       [validators.Length(
                           min=4,max=10,
                           message='Длина имени должна быть в диапазоне от 4 до 25.')])
    email = StringField('Email-адрес',
                        [validators.Length(min=6, max=15,message='Длина email должна быть в диапазоне от 6 до 15.'),
                        #  validators.Regexp(r'^[-\w\.]+@([-\w]+\.)+[-\w]{2,4}$',message='Неправильный формат email.'),
                         validators.Email(message='Неправильный формат email.')
                         ])
    psw = PasswordField('Новый пароль', [
        validators.DataRequired(),          
        validators.EqualTo('psw2', message='Пароли должны совпадать')
    ])
    psw2 = PasswordField('Повторите пароль')

@app.route("/register", methods=["POST", "GET"])
def register():
    """Обработчик для регистрации пользователя"""
    form = RegistrationForm(request.form)    
    # если HTTP-метод GET, то просто отрисовываем форму
    if request.method == "POST" and form.validate():
        session.pop('_flashes', None)
        hash = generate_password_hash(request.form['psw'])
        res = dbase.addUser(request.form['name'], request.form['email'], hash)
        if res:
            flash("Вы успешно зарегистрированы", "success")
            return redirect(url_for('login'))
        else:
            flash("Ошибка при добавлении в БД", "error")
            return render_template("register.html",
                    menu=dbase.getMainmenu(),
                    title="Регистрация",
                    form=form,
                        ) 
    return render_template("register.html",
                           menu=dbase.getMainmenu(),
                           title="Регистрация",
                           form=form,
                           ) 

@app.route('/logout')
@login_required
def logout():
    """Обработчик для выхода пользователя"""
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    """Обработчик для профиля пользователя"""
    return render_template("profile.html", menu=dbase.getMainmenu(), title="Профиль пользователя") 


@app.route('/read_cfg',methods = ['POST', 'GET'])
# Ф-я для получения конфига cfg_GRE.yaml для просмотра
def read_cfg():
    id_cfg = request.form['index']# name="index" in ..html
    print(id_cfg)
    if id_cfg == 'Просмотр конфигурации':
        id_cfg="cfg_GRE.yaml"
        print(id_cfg)
        with open(f'../templates_cfg/{id_cfg}', 'r') as file:
            text = file.readlines()
        return render_template(
            f'/read_cfg.html',
            menu=dbase.getMainmenu(),
            constants = dbase.getConstants_trident(),
            title="Просмотр конфигурции",text=text)
    

def allowed_file_type(filename):
    """ Функция проверки расширения файла """
    # return '.' in filename and \
    #     filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS
    if '.' in filename and \
        filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS:
        name_cfg = filename.rsplit('.',1)[0].lower()
        return True
    else:
        return False
    
@app.route('/upload_file_cfg',methods=['GET', 'POST'])
def upload_file_cfg():
    """Обработчик загрузки файла """
    # читаем список файлов в директории
    listfile = os.listdir(UPLOAD_FOLDER)
    # path_name= os.path.join(UPLOAD_FOLDER)
    # print(path_name)
    # получаем объект со списком файлов
    # listfile = map(lambda name: os.path.join(UPLOAD_FOLDER, name), fileslist) 
    
    if request.method == 'POST':
        
        # проверим, передается ли в запросе файл
        if 'file' not in request.files:
            flash('Не могу прочитать файл', category='fail') 
            return redirect(request.url)
        file = request.files['file']
        # отправить пустой файл
        if file.filename == '':
            flash('Нет выбранного файла', category='fail')
            return redirect(request.url)
        if file and allowed_file_type(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('Файл загружен', category='success')
            return  render_template(
                'upload_file_cfg.html',
                constants = dbase.getConstants_trident(),
                items=listfile)
            # редирект на страницу с загруженным файлом
            # return redirect(url_for('shw_download_file', name=filename)) 
    return render_template(
            'upload_file_cfg.html',
            title="Загрузка файла конфигурации в БД",
            menu=dbase.getMainmenu(),
            constants = dbase.getConstants_trident(),
            items=listfile,
            )

@app.route('/view_cfg_table',methods=['GET'],)
def view_cfg_table():
    """Обработчик просмотра файла конфига из таблицы"""
    listfile = os.listdir(UPLOAD_FOLDER)

    return render_template(
        'cfg_from_table.html', title="Операции с файлом конфига",
        menu=dbase.getMainmenu(),
        constants = dbase.getConstants_trident(),
        items=listfile,
        )    



@app.route('/pull_cfg_sw/<filename>',methods=['GET','POST'],)
def pull_cfg_sw(filename):
    """Обработчик заливки конфига из таблицы"""
    filename = request.path.split('/')[-1]
    global path_name
    listfile = os.listdir(UPLOAD_FOLDER)
    path_name= os.path.join(UPLOAD_FOLDER, filename)
    with open("../path_name.txt", 'a') as file:
        file.write(path_name) 
    result =''
    str_result=''
    if request.method == "POST":
        response = request.form['index']  # name="index" in reset.html
        args=["python3", "../cfgFromFile.py"]
        process = subprocess.Popen(args, stdout=subprocess.PIPE) 
        for line in process.stdout:
            print(line)
            with open("../process_temp.txt", 'a') as file:
                str_result = line.decode('utf-8')
                file.write(str_result) 

        time.sleep(5)
        flash(
            f"Внимание! На коммутатор загружен конфиг из файла {filename}",
            category='success')
        with open("../path_name.txt", 'w') as file:
            pass
        with open("../process_temp.txt", 'w'):
            pass  # не удальть - очищает файл
        return render_template(
            'cfg_from_table.html',
            title="Добавить конфиг в коммутатор",
            menu=dbase.getMainmenu(),
            constants = dbase.getConstants_trident(),
            items=listfile,
            result=str_result,
            filename=filename,
            )    
    return render_template(
        'cfg_from_table.html', title="Операции с файлом конфига",
        menu=dbase.getMainmenu(),
        constants = dbase.getConstants_trident(),
        items=listfile,
        )  


@app.route('/get_file_cfg/<filename>')
def get_file_cfg(filename):
    """Обработчик просмотра конфига из папки по ссылке"""
    return send_from_directory(app.config['UPLOAD_FOLDER'],filename)


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
    app.run(debug=True)