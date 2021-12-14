from flask import Blueprint, render_template

from webapp.user.decorators import admin_required

blueprint = Blueprint('admin', __name__, url_prefix='/admin')

@blueprint.route('/')        #функция только для зарегистрированных
@admin_required             #если пользователь прошёл проверку @admin_required, то он точно - админ!
def admin_index():
    title = "Панель управления"
    return render_template('admin/index.html', page_title=title)