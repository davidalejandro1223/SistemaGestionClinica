#from django.conf.urls import url
from django.urls import re_path
from .views import CrearPaciente, DetallePaciente, PacienteListView
from django.views.decorators.csrf import csrf_exempt

app_name = 'pacientes'

urlpatterns = [
	re_path(r'^pacientes/nuevo', csrf_exempt(CrearPaciente.as_view()), name='nuevo_paciente'),
    re_path(r'^pacientes$', PacienteListView.as_view(), name='listar_pacientes'),
    re_path(r'^pacientes/(?P<pk>\d+)$', DetallePaciente.as_view(), name='detalle_paciente'),
]