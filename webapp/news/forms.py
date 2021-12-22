#форма добавления комментариев к новостям
from flask_wtf import FlaskForm
from wtforms import HiddenField, SubmitField, StringField       #импорт скрытого, текстового поля и кнопки
from wtforms.validators import DataRequired, ValidationError

from webapp.news.models import News             #для проверки на существование news_id

class CommentForm(FlaskForm):
    news_id = HiddenField('ID новости', validators=[DataRequired()])
    comment_text = StringField('Ваш комментарий', validators=[DataRequired()], render_kw={"class": "form-control"})
    submit = SubmitField('Отправить', render_kw={"class": "btn btn-primary"})

    def validate_news_id(self, news_id):                #проверка от невалидного id новости
        if not News.query.get(news_id.data):
            raise ValidationError('Новости с таким id не существует')