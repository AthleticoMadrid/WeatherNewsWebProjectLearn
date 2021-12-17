from flask import abort, Blueprint, current_app, render_template

from webapp.news.models import News
from webapp.weather import weather_by_city


blueprint = Blueprint('news', __name__)

@blueprint.route('/')     #('/') - главная страница
def index():    #функция-обработчик главной страницы
    title = "Новости Python"       #переменная с заголовком сайта
    weather = weather_by_city(current_app.config['WEATHER_DEFAULT_CITY'])    #получаем данные о погоде из config.py
    news_list = News.query.order_by(News.published.desc()).all()
    return render_template('news/index.html', page_title=title, weather=weather, news_list=news_list)  
    #возвращаем функцию с нашим HTML-шаблоном и переменными которые учавствуют в нём (по типу: переменная шаблона=переменная)

@blueprint.route('/news/<int:news_id>')         #страница с номером новости
def single_news(news_id):
    my_news = News.query.filter(News.id == news_id).first()

    if not my_news:
        abort(404)
    
    return render_template('news/single_news.html', page_title=my_news.title, news=my_news)     # (page_title=my_news.title) - заголовок страницы = заголовку новости
    