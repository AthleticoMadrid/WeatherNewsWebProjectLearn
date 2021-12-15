from getpass import getpass         #для ввода пароля из командной строки пользователем
import sys

from webapp import create_app
from webapp.db import db
from webapp.user.models import User


app = create_app()

with app.app_context():         #доступ для работы с бд
    username = input('Введите имя пользователя: ')

    if User.query.filter(User.username == username).count():        #проверка пользователя
        print('Пользователь с таким именем уже существует')
        sys.exit(0)             #выходим из нашей программы

    password1 = getpass('Введите пароль')
    password2 = getpass('Повторите пароль')

    if not password1 == password2:
        print('Пароли не совпадают')
        sys.exit(0)

    #создание пользователя:
    new_user = User(username=username, role='admin')
    new_user.set_password(password1)

    db.session.add(new_user)    #добавляем пользователя в бд
    db.session.commit()         #сохраняем
    print('Создан пользователь с id={}'.format(new_user.id))

    