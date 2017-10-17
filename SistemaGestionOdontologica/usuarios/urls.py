from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.autenticar, name = 'autenticar')
]
