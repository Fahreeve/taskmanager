"""taskmanager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views
from django.views.generic import TemplateView

from board.forms import MyAuthenticationForm
from board.views import TaskListView

urlpatterns = [
    url(r'^$', TaskListView.as_view(), name='main'),
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.LoginView.as_view(template_name='login.html', form_class=MyAuthenticationForm), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(next_page='/login/'), name='logout'),
    url(r'^board/', include('board.urls')),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),
]
