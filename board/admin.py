from django.contrib import admin

from board.models import Task
from board.tasks import user_send_new_task_email


class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'executor', 'status', 'priority')
    list_filter = ('status', 'priority', 'created')

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if change and 'executor' in form.changed_data:
            user_send_new_task_email.delay(user_id=obj.executor.pk)
        elif not change:
            user_send_new_task_email.delay(user_id=obj.executor.pk)


admin.site.register(Task, TaskAdmin)
