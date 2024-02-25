from flask import Flask,render_template, redirect, url_for, request
 
app = Flask(__name__)

secondmenu = [{"name": "Проверка поддержки GRE", "url": "/test1"},
              {"name": "Проверка поддержки test2", "url": "/test2"},
              {"name": "Проверка поддержки test3", "url": "/test3"}]

menu = [{"name": "Меню тестов", "url": "/"},
        {"name": "Меню конфигов", "url": "cfg"},
        {"name": "Меню сброса настроек", "url": "reset"}]

@app.route("/")
def index():
    return render_template('index.html', title="Основные тесты коммутатора Trident", menu = menu, secondmenu=secondmenu)

@app.route("/cfg")
def cfg():
    return render_template('cfg.html', title = "Заливка конфига", menu = menu)

@app.route("/reset")
def reset():
    return render_template('cfg.html', title = "Сброс конфига на деволтные", menu = menu)

if __name__ == "__main__":
    app.run(debug=True)