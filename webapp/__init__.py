from flask import Flask, render_template, Request

from webapp.model import db, News     #связываем с файлом модели новостей
from webapp.weather import weather_by_city     

def create_app():      #функция создающая Flask app, инициализирующая и возвращающая объект app
    app = Flask(__name__)   #app - будет Flask-приложением, __name__ - имя текущего файла
    app.config.from_pyfile('config.py')
    db.init_app(app)    #инициализация базы данных

    @app.route('/')     #('/') - главная страница
    def index():    #функция-обработчик главной страницы
        title = "Новости Python"       #переменная с заголовком сайта
        weather = weather_by_city(app.config['WEATHER_DEFAULT_CITY'])    #получаем данные о погоде из config.py
        news_list = News.query.order_by(News.published.desc()).all()
        return render_template('index.html', page_title=title, weather=weather, news_list=news_list)  
        #возвращаем функцию с нашим HTML-шаблоном и переменными которые учавствуют в нём (по типу: переменная шаблона=переменная)

    return app

#запуск сервера на Windows:
#                           set FLASK_APP=webapp && set FLASK_ENV=development && set FLASK_DEBUG=1 && flask run