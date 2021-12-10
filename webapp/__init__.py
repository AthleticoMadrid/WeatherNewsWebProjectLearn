from flask import Flask, flash, render_template, redirect, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

from webapp.forms import LoginForm
from webapp.model import db, News, User     #связываем с файлом модели новостей и пользователем
from webapp.weather import weather_by_city     

def create_app():      #функция создающая Flask app, инициализирующая и возвращающая объект app
    app = Flask(__name__)   #app - будет Flask-приложением, __name__ - имя текущего файла
    app.config.from_pyfile('config.py')
    db.init_app(app)    #инициализация базы данных

    login_manager = LoginManager()              #создаём экземпляр ЛогинМенеджера
    login_manager.init_app(app)                 #инициализируем
    login_manager.login_view = 'login'          #даём название функции, которая занимается логином пользователя

    @login_manager.user_loader              #функция получающая при каждом входе id пользователя
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/')     #('/') - главная страница
    def index():    #функция-обработчик главной страницы
        title = "Новости Python"       #переменная с заголовком сайта
        weather = weather_by_city(app.config['WEATHER_DEFAULT_CITY'])    #получаем данные о погоде из config.py
        news_list = News.query.order_by(News.published.desc()).all()
        return render_template('index.html', page_title=title, weather=weather, news_list=news_list)  
        #возвращаем функцию с нашим HTML-шаблоном и переменными которые учавствуют в нём (по типу: переменная шаблона=переменная)

    @app.route('/login')
    def login():            #шаблон атворизации пользователя
        if current_user.is_authenticated:       #если пользователь уже авторизован то -> на главную
            return redirect(url_for('index'))
        title = "Авторизация"
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)

    @app.route('/process-login', methods=['POST'])      #реализация обработки формы логина
    def process_login():
        form = LoginForm()

        if form.validate_on_submit():       #если не возникли ошибки в ходе заполнения формы
            user = User.query.filter(User.username == form.username.data).first()   #пытаемся получить пользователя по имени из бд
            if user and user.check_password(form.password.data):            #если пользователь существует и проверка пароля прошла
                login_user(user)                #то пользователя запоминаем
                flash('Вы успешно вошли на сайт')
                return redirect(url_for('index'))       #перемещаем его на гл.страницу

        flash('Неправильные имя или пароль пользователя')
        return redirect(url_for('login'))               #перемещаем его на страницу логина

    @app.route('/logout')           #выход пользователя с сайта
    def logout():
        logout_user()
        flash('Вы успешно разлогинились')           #и перенаправляем пользователя на гл.страницу
        return redirect(url_for('index'))
    
    @app.route('/admin')        #функция только для зарегистрированных
    @login_required             #если пользователь не идентифицирован, то перебрасывается в логин
    def admin_index():
        if current_user.is_admin:
            return 'Привет, админ!'
        else:
            return 'Ты не админ!'

    return app

#запуск сервера на Windows:
#                           set FLASK_APP=webapp && set FLASK_ENV=development && set FLASK_DEBUG=1 && flask run