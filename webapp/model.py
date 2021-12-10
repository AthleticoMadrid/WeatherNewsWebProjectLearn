from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash   #функции шифрования пароля от пользователя

db = SQLAlchemy()       #инициализация базы данных

class News(db.Model):
    id = db.Column(db.Integer, primary_key=True)        #идентификатор новости
    title = db.Column(db.String, nullable=False)        #заголовок новости
    url = db.Column(db.String, unique=True, nullable=False)     #ссылка новости
    published = db.Column(db.DateTime, nullable=False)        #дата публикации новости
    text = db.Column(db.Text, nullable=True)        #текст новости

    def __repr__(self):
        return '<News {} {}>'.format(self.title, self.url)      #т.е.  'News {title} {url}'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)    #имя ограниченно по длине(50 символов)
    password = db.Column(db.String(128))        #пароль не более 128 символов
    role = db.Column(db.String(10), index=True)         #админ или пользователь

    def set_password(self, password):
        self.password = generate_password_hash(password)    #шифрует текущий пароль и результат кладётся в password

    def check_password(self, password):
        return check_password_hash(self.password, password)     #возвращает зашифрованный пароль и пароль от пользователя
    
    @property                   #помогает методу вести себя как атрибут
    def is_admin(self):         #проверяет пользователя на админа
        return self.role == 'admin'

    def __repr__(self):
        return '<User name={} id={}>'.format(self.username, self.id)        #self.username - имя текущего юзера


