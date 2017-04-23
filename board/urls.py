from django.conf.urls import url
from board.views import TaskListView, TaskUpdateView, CreateCommentView

urlpatterns = [
    url(r'^$', TaskListView.as_view(), name='task-list'),
    url(r'^task/(?P<pk>\d+)/$', TaskUpdateView.as_view(), name='task-edit'),
    url(r'^task/(?P<pk>\d+)/comment/$', CreateCommentView.as_view(), name='comment'),
]
