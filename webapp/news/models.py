from datetime import datetime

from sqlalchemy.orm import relationship
from webapp.db import db

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)        #идентификатор новости
    title = db.Column(db.String, nullable=False)        #заголовок новости
    url = db.Column(db.String, unique=True, nullable=False)     #ссылка новости
    published = db.Column(db.DateTime, nullable=False)        #дата публикации новости
    text = db.Column(db.Text, nullable=True)        #текст новости

    def comments_count(self):                           #метод подсчёта комментариев
        return Comment.query.filter(Comment.news_id == self.id).count()

    def __repr__(self):
        return '<News {} {}>'.format(self.title, self.url)      #т.е.  'News {title} {url}'

class Comment(db.Model):                                #класс с комментариями пользователей
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now())       #время создания комментария
    news_id = db.Column(
        db.Integer,
        db.ForeignKey('news.id', ondelete='CASCADE'),       #внешний ключ ссылается на 'news.id', onedelete - поведение этого поля при удалении (удаляя новость все комментарии удаляются автоматически)
        index=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey('user.id', ondelete='CASCADE'),
        index=True
    )
    news = relationship('News', backref='comments')         #виртуальное поле 'comments' у модели News
    user = relationship('User', backref='comments')         #виртуальное поле 'comments' у модели User

    def __repr__(self):
        return '<Comment {}>'.format(self.id)

    #после создания новой модели сделаем миграцию в cmd:  set FLASK_APP=webapp && flask db migrate -m "Comments model added"
    #                                       и затем уже:  flask db upgrade