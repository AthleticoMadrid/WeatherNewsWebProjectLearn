from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField     #импорт типов полей (строковых, для ввода пароля и кнопку)
from wtforms.validators import DataRequired     #импорт класса проверки данных от пользователя

class LoginForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()], render_kw={"class": "form-control"})     #строка с именем пользователя (render_kw = html(class="form-control"))
    remember_me = BooleanField('Запомнить меня', default=True, render_kw={"class": "form-check-input"})     #функция запоминания пользователя
    password = PasswordField('Пароль', validators=[DataRequired()], render_kw={"class": "form-control"})     #пароль (render_kw = html(class="form-control"))
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary"})      #кнопка 'отправить' (render_kw = html(class="btn btn-primary")) - класс кнопки
    