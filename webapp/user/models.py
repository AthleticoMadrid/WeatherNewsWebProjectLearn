from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash   #функции шифрования пароля от пользователя

from webapp.db import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), index=True, unique=True)    #имя ограниченно по длине(50 символов)
    password = db.Column(db.String(128))        #пароль не более 128 символов
    role = db.Column(db.String(10), index=True)         #админ или пользователь
    email = db.Column(db.String(50))

    def set_password(self, password):
        self.password = generate_password_hash(password)    #шифрует текущий пароль и результат кладётся в password

    def check_password(self, password):
        return check_password_hash(self.password, password)     #возвращает зашифрованный пароль и пароль от пользователя
    
    @property                   #помогает методу вести себя как атрибут
    def is_admin(self):         #проверяет пользователя на админа
        return self.role == 'admin'

    def __repr__(self):
        return '<User name={} id={}>'.format(self.username, self.id)        #self.username - имя текущего юзера

