#файл задач (tasks) для Celery
from celery import Celery

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

#запуск Celery на Windows (после включения подсистемы Linux для Windows):
#            set FORKED_BY_MULTIPROCESSING=1 && celery -A tasks worker --loglevel=info

#в новом терминале активируем вирт.окружение и запускаем: python
#                                           далее:        from tasks import add     #где add - имя функции (напр.: habr_snippets, habr_content)
#чтобы начать работу с Celery (нужен delay):              add.delay(2, 2)
#                                                         <AsyncResult: 6af8eb86-d904-4251-9aa7-b8580ebfccdf>