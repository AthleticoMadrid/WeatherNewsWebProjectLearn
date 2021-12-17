#для кода который будет использоваться всеми парсерами
import requests

from webapp.db import db
from webapp.news.models import News

def get_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0'       #заголовки
    }
    try:
        result = requests.get(url, headers=headers)      #при каждом запросе будет отправляться User-Agent
        result.raise_for_status()       #чтобы не получить ошибку (невалидную страницу) при скачивании
        return result.text          # - если всё хорошо
    except(requests.RequestException, ValueError):
        print("Сетевая ошибка")
        return False

def save_news(title, url, published):
    news_exists = News.query.filter(News.url == url).count()       #возможность ограничить выборку(выполнив подсчёт объектов подходящих под условие)
    print(news_exists)
    if not news_exists:
        news_news = News(title=title, url=url, published=published)      #параметры новой новости
        db.session.add(news_news)    #добавление новости в бд
        db.session.commit()         #сохранение новости в бд
