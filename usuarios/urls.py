#from django.conf.urls import url
from django.urls import re_path
from . import views

app_name = 'usuarios'
urlpatterns = [
    re_path(r'^$', views.autenticar, name = 'autenticar'),
    re_path(r'^logout$', views.desautenticar, name = 'desautenticar'),
    re_path(r'^inicio$', views.inicio, name = 'inicio'),
]
