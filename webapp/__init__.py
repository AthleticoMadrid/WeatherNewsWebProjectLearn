from flask import Flask, flash, render_template, redirect, url_for
from flask_login import LoginManager, current_user, login_required

from webapp.db import db         #связываем с файлом модели новостей и пользователем
from webapp.admin.views import blueprint as admin_blueprint     #импорт blueprint-а админа
from webapp.news.views import blueprint as news_blueprint       #импорт blueprint-а новостей
from webapp.user.models import User
from webapp.user.views import blueprint as user_blueprint       #импорт blueprint-а пользователя   


def create_app():      #функция создающая Flask app, инициализирующая и возвращающая объект app
    app = Flask(__name__)   #app - будет Flask-приложением, __name__ - имя текущего файла
    app.config.from_pyfile('config.py')
    db.init_app(app)    #инициализация базы данных

    login_manager = LoginManager()              #создаём экземпляр ЛогинМенеджера
    login_manager.init_app(app)                 #инициализируем
    login_manager.login_view = 'user.login'          #даём название функции, которая занимается логином пользователя
    
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(news_blueprint)
    app.register_blueprint(user_blueprint)
    

    @login_manager.user_loader              #функция получающая при каждом входе id пользователя
    def load_user(user_id):
        return User.query.get(user_id)

    return app

#запуск сервера на Windows:
#                           set FLASK_APP=webapp && set FLASK_ENV=development && set FLASK_DEBUG=1 && flask run