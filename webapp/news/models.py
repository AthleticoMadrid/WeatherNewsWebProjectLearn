from webapp.db import db

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)        #идентификатор новости
    title = db.Column(db.String, nullable=False)        #заголовок новости
    url = db.Column(db.String, unique=True, nullable=False)     #ссылка новости
    published = db.Column(db.DateTime, nullable=False)        #дата публикации новости
    text = db.Column(db.Text, nullable=True)        #текст новости

    def __repr__(self):
        return '<News {} {}>'.format(self.title, self.url)      #т.е.  'News {title} {url}'
