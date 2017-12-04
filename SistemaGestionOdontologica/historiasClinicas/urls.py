from django.conf.urls import url
from .views import historia_paciente

urlpatterns = [
    #url(r'^historia-clinica$'),
    url(r'^historia-clinica/(?P<pk>\d+)', historia_paciente, name='historia_paciente'),
    
]
