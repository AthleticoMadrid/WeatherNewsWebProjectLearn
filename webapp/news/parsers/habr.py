#для уникального хода для Хабра
from datetime import datetime, timedelta
import locale                           #для выставления времени публикации
import platform

from bs4 import BeautifulSoup
from webapp.news.models import News

from webapp.db import db
from webapp.news.models import News
from webapp.news.parsers.utils import get_html, save_news

if platform.system() == 'Windows':
    locale.setlocale(locale.LC_ALL, "russian")
else:
    locale.setlocale(locale.LC_TIME, 'ru_RU')

def parse_habr_date(date_str):
    if 'сегодня' in date_str:
        today = datetime.now()
        date_str = date_str.replace('сегодня', today.strftime('%d %B %Y'))
    elif 'вчера' in date_str:
        yesterday = datetime.now() - timedelta(days=1)                      #нахождение вчерашней даты
        date_str = date_str.replace('вчера', yesterday.strftime('%d %B %Y'))
    try:
        return datetime.strptime(date_str, '%d %B %Y в %H:%M')      #если всё верно, то выдаёт дату в таком формате
    except ValueError:
        return datetime.now()

def get_news_snippets():
    html = get_html("https://habr.com/ru/search/?q=python&target_type=posts&order=date")    #наша функция идёт по ссылке и получает страницу с Хабра
    if html:
        soup = BeautifulSoup(html, 'html.parser')       #теперь soup - преобразованный html
        all_news = soup.find('div', class_='tm-articles-list').findAll('article', class_='tm-articles-list__item')      #ищем нужный нам класс со всеми новостями на странице ('div') и с каждой публикацией отдельно ('article')
        for news in all_news:
            title = news.find('a', class_='tm-article-snippet__title-link').text     #получаем заголовки статей
            url = news.find('a', class_='tm-article-snippet__title-link')['href']   #получаем ссылки у статей
            url = 'https://habr.com' + url
            published = news.find('span', class_='tm-article-snippet__datetime-published').text      #получаем дату публикации
            published = parse_habr_date(published)
            save_news(title, url, published)

def get_news_content():
    news_without_text = News.query.filter(News.text.is_(None))      #собирает новости без текста (is_ - сравнение на идентичность)
    for news in news_without_text:
        html = get_html(news.url)
        if html:
            soup = BeautifulSoup(html, 'html.parser')
            news_text = soup.find('div', class_='tm-articles-list__item').decode_contents()    #возьмём текст с новости
            if news_text:
                news.text = news_text
                db.session.add(news)
                db.session.commit()