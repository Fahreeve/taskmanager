import datetime

from celery.schedules import crontab
from celery.task import periodic_task
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from celery import shared_task

from .models import Task


@shared_task()
def user_send_new_task_email(user_id):
    user = User.objects.get(pk=user_id)
    user.email_user(subject=_('Получено новое задание'), message=_('Вам назначено новое задание'))


@periodic_task(run_every=(crontab(minute='*/15')))  # run every 15 minutes
def deadline_notification():
    now = datetime.datetime.now()
    qs = Task.objects.filter(deadline__gte=now+datetime.timedelta(minutes=15),
                             deadline__lt=now+datetime.timedelta(minutes=30))
    for obj in qs:
        obj.executor.email_user(subject=_('Дедлайн близко'), message=obj.title)


