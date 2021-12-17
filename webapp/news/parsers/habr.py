#для уникального хода для Хабра
from datetime import datetime

from bs4 import BeautifulSoup

from webapp.news.parsers.utils import get_html, save_news

def get_habr_snippets():
    html = get_html("https://habr.com/ru/search/?q=python&target_type=posts&order=date")    #наша функция идёт по ссылке и получает страницу
    if html:
        soup = BeautifulSoup(html, 'html.parser')       #теперь soup - преобразованный html
        all_news = soup.find('div', class_='tm-articles-list').findAll('article', class_='tm-articles-list__item')      #ищем нужный нам класс со всеми новостями на странице ('div') и с каждой публикацией отдельно ('article')
        for news in all_news:
            title = news.find('a', class_='tm-article-snippet__title-link').text     #получаем заголовки статей
            url = news.find('a', class_='tm-article-snippet__title-link')['href']   #получаем ссылки у статей
            published = news.find('span', class_='tm-article-snippet__datetime-published').text      #получаем дату публикации
            print(title, url, published)
            """
            try:
                published = datetime.strptime(published, '%Y-%m-%d')     #strptime: парсит строку по заданому ей формату
            except ValueError:
                published = datetime.now()      #текущую дату и время
            save_news(title, url, published)
            """