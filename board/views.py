import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, UpdateView, CreateView

from board.forms import ChangeTaskForm, AddCommentForm
from board.models import Task, Comment


class TaskListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Task
    template_name = 'tasks.html'
    paginate_by = 10

    def get_queryset(self):
        qs = super().get_queryset()
        filter = self.request.GET.get('filter')
        if filter == 'p1':
            return qs.filter(priority=1)
        if filter == 'p2':
            return qs.filter(priority=2)
        if filter == 'p3':
            return qs.filter(priority=3)
        if filter == 'today':
            return qs.filter(deadline__date=datetime.datetime.today())
        if filter == 'tomorrow':
            return qs.filter(deadline__date=datetime.datetime.today() + datetime.timedelta(days=1))
        if filter == 'week':
            today = datetime.datetime.today()
            return qs.filter(deadline__date__gte=today, deadline__date__lte=today+datetime.timedelta(days=7))
        return qs.order_by('-priority')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = self.request.GET.get('filter', '')
        return context


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Task
    template_name = 'task.html'
    form_class = ChangeTaskForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(task=self.object).order_by('created')
        context['comment_form'] = AddCommentForm(initial={'task': self.object})
        return context


class CreateCommentView(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    form_class = AddCommentForm

    def get(self, request, *args, **kwargs):
        return self.http_method_not_allowed(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.task = get_object_or_404(Task, pk=self.kwargs['pk'])
        if self.task.executor != request.user:
            raise PermissionDenied
        return super().post(request, *args, **kwargs)

    def get_initial(self):
        initial = super().get_initial()
        initial['creator'] = self.request.user
        initial['task'] = self.task
        return initial

    def get_success_url(self):
        return reverse('task-edit', kwargs={'pk': self.kwargs['pk']})
