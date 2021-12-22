from flask import abort, Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required

from webapp.db import db
from webapp.news.forms import CommentForm
from webapp.news.models import Comment, News
from webapp.weather import weather_by_city
from webapp.utils import get_redirect_target


blueprint = Blueprint('news', __name__)

@blueprint.route('/')     #('/') - главная страница
def index():    #функция-обработчик главной страницы
    title = "Новости Python"       #переменная с заголовком сайта
    weather = weather_by_city(current_app.config['WEATHER_DEFAULT_CITY'])    #получаем данные о погоде из config.py
    news_list = News.query.filter(News.text.isnot(None)).order_by(News.published.desc()).all()
    return render_template('news/index.html', page_title=title, weather=weather, news_list=news_list)  
    #возвращаем функцию с нашим HTML-шаблоном и переменными которые учавствуют в нём (по типу: переменная шаблона=переменная)

@blueprint.route('/news/<int:news_id>')         #страница с номером новости
def single_news(news_id):
    my_news = News.query.filter(News.id == news_id).first()

    if not my_news:
        abort(404)
    comment_form = CommentForm(news_id=my_news.id)
    return render_template('news/single_news.html', page_title=my_news.title, news=my_news, comment_form=comment_form)     # (page_title=my_news.title) - заголовок страницы = заголовку новости

@blueprint.route('/news/comment', methods=['POST'])         #обработчик комментария
@login_required                                             #защита от данных незалогиненных пользователей
def add_comment():
    form = CommentForm()
    if form.validate_on_submit():                                           #если форма провалидированна
        comment = Comment(text=form.comment_text.data, news_id=form.news_id.data, user_id=current_user.id)              #создаём новый комментарий, если новость = True
        db.session.add(comment)
        db.session.commit()
        flash('Комментарий успешно добавлен')
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле {}: {}'.format(
                    getattr(form, field).label.text,
                    error
                ))
    return redirect(get_redirect_target())       #иначе возвращаем пользователя на ту же страницу с которой он пришёл

