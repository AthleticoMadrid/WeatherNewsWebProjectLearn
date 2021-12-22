from flask import Blueprint, flash, render_template, redirect, url_for
from flask_login import current_user, login_user, logout_user

from webapp.db import db
from webapp.user.forms import LoginForm, RegistrationForm
from webapp.user.models import User
from webapp.utils import get_redirect_target

blueprint = Blueprint('user', __name__, url_prefix='/users')        #'user' - имя декоратора Blueprint, '/users' - начальный url для всех route('/') в этом файле  

@blueprint.route('/login')
def login():            #шаблон атворизации пользователя
    if current_user.is_authenticated:       #если пользователь уже авторизован то -> на главную
        return redirect(get_redirect_target())
    title = "Авторизация"
    login_form = LoginForm()
    return render_template('user/login.html', page_title=title, form=login_form)

@blueprint.route('/process-login', methods=['POST'])      #реализация обработки формы логина
def process_login():
    form = LoginForm()

    if form.validate_on_submit():       #если не возникли ошибки в ходе заполнения формы
        user = User.query.filter(User.username == form.username.data).first()   #пытаемся получить пользователя по имени из бд
        if user and user.check_password(form.password.data):            #если пользователь существует и проверка пароля прошла
            login_user(user, remember=form.remember_me.data)                #то пользователя запоминаем
            flash('Вы успешно вошли на сайт')
            return redirect(get_redirect_target())       #перемещаем его на гл.страницу

    flash('Неправильные имя или пароль пользователя')
    return redirect(url_for('user.login'))               #перемещаем его на страницу логина

@blueprint.route('/logout')           #выход пользователя с сайта
def logout():
    logout_user()
    flash('Вы успешно разлогинились')           #и перенаправляем пользователя на гл.страницу
    return redirect(url_for('news.index'))

@blueprint.route('/register')               #страница с регистрацией
def register():
    if current_user.is_authenticated:
        return redirect(url_for('news.index'))
    title = "Регистрация"
    form = RegistrationForm()
    return render_template('user/registration.html', page_title=title, form=form)

@blueprint.route('/process-reg', methods=['POST'])      #регистрация пользователей (только users)
def process_reg():
    form = RegistrationForm()
    if form.validate_on_submit():               #если при проверки формы нет ошибок, то:
        new_user = User(username=form.username.data, email=form.email.data, role='user')
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash('Вы успешно зарегистрировались!')
        return redirect(url_for('user.login'))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash('Ошибка в поле {}: {}'.format(
                    getattr(form, field).label.text,        #getattr - взять атрибут
                    error
                ))
    return redirect(url_for('user.register'))