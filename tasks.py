#файл задач (tasks) для Celery
from celery import Celery
from celery.schedules import crontab                #модуль ищущий новости по заданным временным промежуткам

from webapp import create_app
from webapp.news.parsers import habr

flask_app = create_app()
celery_app = Celery('tasks', broker='redis://localhost:6379/0')

@celery_app.task
def habr_snippets():                                        #ссылки и заголовки новостей
    with flask_app.app_context():
        habr.get_news_snippets()

@celery_app.task
def habr_content():                                         #статьи новостей
    with flask_app.app_context():
        habr.get_news_content()

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute='*/1'), habr_snippets.s())
    sender.add_periodic_task(crontab(minute='*/2'), habr_content.s())