from flask import Flask, render_template, Request

from webapp.python_org_news import get_python_news      #имя папки.имя файла
from webapp.weather import weather_by_city     

def create_app():      #функция создающая Flask app, инициализирующая и возвращающая объект app
    app = Flask(__name__)   #app - будет Flask-приложением, __name__ - имя текущего файла
    app.config.from_pyfile('config.py')

    @app.route('/')     #('/') - главная страница
    def index():    #функция-обработчик главной страницы
        title = "Новости Python"       #переменная с заголовком сайта
        weather = weather_by_city(app.config['WEATHER_DEFAULT_CITY'])    #получаем данные о погоде из config.py
        news_list = get_python_news()
        return render_template('index.html', page_title=title, weather=weather, news_list=news_list)  
        #возвращаем функцию с нашим HTML-шаблоном и переменными которые учавствуют в нём (по типу: переменная шаблона=переменная)

    return app

#запуск сервера на Windows:
#                           set FLASK_APP=webapp && set FLASK_ENV=development && set FLASK_DEBUG=1 && flask run