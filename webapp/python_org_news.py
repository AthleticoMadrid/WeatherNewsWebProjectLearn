from datetime import datetime

import requests
from bs4 import BeautifulSoup   #библиотека для парсинга

from webapp.db import db
from webapp.news.models import News

def get_html(url):
    try:
        result = requests.get(url)      #с помощью request берутся данные из url-а
        result.raise_for_status()       #чтобы не получить ошибку (невалидную страницу) при скачивании
        return result.text          # - если всё хорошо
    except(requests.RequestException, ValueError):
        print("Сетевая ошибка")
        return False

def get_python_news():
    html = get_html("https://www.python.org/blogs/")    #наша функция идёт по ссылке и получает страницу
    if html:
        #with open("python.org.html", "w", encoding="utf-8") as f:    #результат скачивания запишем в файл python.org.html
            #f.write(html)
        soup = BeautifulSoup(html, 'html.parser')       #теперь soup - преобразованный html
        all_news = soup.find('ul', class_='list-recent-posts menu').findAll('li')      #ищем нужный нам класс (<ul class="list-recent-posts menu">) с новостями
#.findAll('li') - выделяет отдельно каждый <li>
        result_news = []
        for news in all_news:
            title = news.find('a').text     #получаем тексты новостей
            url = news.find('a')['href']   #получаем ссылки новостей
            published = news.find('time').text      #получаем дату публикации
            try:
                published = datetime.strptime(published, '%Y-%m-%d')     #strptime: парсит строку по заданому ей формату
            except ValueError:
                published = datetime.now()      #текущую дату и время
            save_news(title, url, published)

def save_news(title, url, published):
    news_exists = News.query.filter(News.url == url).count()       #возможность ограничить выборку(выполнив подсчёт объектов подходящих под условие)
    print(news_exists)
    if not news_exists:
        news_news = News(title=title, url=url, published=published)      #параметры новой новости
        db.session.add(news_news)    #добавление новости в бд
        db.session.commit()         #сохранение новости в бд
