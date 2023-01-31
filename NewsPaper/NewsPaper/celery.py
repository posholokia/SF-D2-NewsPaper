import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')

app = Celery('NewsPaper')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


app.conf.beat_schedule = {
    'email_to_subs_weekly': {
        'task': 'news.tasks.weekly_send_mail',
        'schedule': crontab(hour=8, minute=00, day_of_week='monday'),
    },
}