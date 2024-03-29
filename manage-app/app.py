from flask import Flask,render_template, redirect, url_for, request
from flask import render_template

app = Flask(__name__)

# @app.route("'/hello/<name>'")
# def hello_world():
#     return "<p>просто |КНОПКА| !!! </p>"

@app.route('/')
def hello():
  return render_template('landing.html' )

# страница формы логина в админ панель  
@app.route('/adm_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        # Здесь должна быть логика аутентификации
        # Если аутентификация прошла успешно, перенаправляем на /admin_panel
        return redirect(url_for('admin_panel'))
    # Если GET запрос, показываем форму входа
    return render_template('login_adm.html')

# страница админ панели
@app.route('/admin_panel')
def admin_panel():
    # Загрузка и отображение админ-панели
    return render_template('admin_panel.html')

if __name__ == 'main':
  app.run(debug=True)