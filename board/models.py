from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Task(models.Model):
    CLOSE = 'cl'
    CANCEL = 'ca'
    LATER = 'la'
    UNDEFINED = 'un'
    CHOICES = (
        (UNDEFINED, _("Неизвестно")),
        (CLOSE, _("Завершить")),
        (CANCEL, _("Отменить")),
        (LATER, _("Отложить")),
    )

    title = models.CharField(_("Заголовок"), max_length=50)
    description = models.TextField(_("Описание"))
    executor = models.ForeignKey(User, verbose_name=_("Исполнитель"), on_delete=models.CASCADE)
    status = models.CharField(_("Статус"), choices=CHOICES, default=UNDEFINED, max_length=2)
    deadline = models.DateTimeField(_("Дедлайн"))
    priority = models.IntegerField(_("Приоритет"), default=1, validators=[MinValueValidator(1), MaxValueValidator(3)])
    changed = models.DateTimeField(_("Дата последнего изменения"), auto_now=True)
    created = models.DateTimeField(_("Дата создания"), auto_now_add=True)

    @property
    def text_status(self):
        choices = dict(self.CHOICES)
        return choices[self.status]

    @property
    def text_deadline(self):
        return self.deadline.strftime("%d.%m.%Y %H:%M")


class Comment(models.Model):
    task = models.ForeignKey(Task, related_name="comments", on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    text = models.TextField(_('Комментарий'))
    created = models.DateTimeField(_("Дата создания"), auto_now_add=True)
