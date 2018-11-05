from django.conf.urls import url
from .views import CrearPaciente, DetallePaciente, PacienteListView
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
	url(r'^pacientes/nuevo', csrf_exempt(CrearPaciente.as_view()), name='nuevo_paciente'),
    url(r'^pacientes$', PacienteListView.as_view(), name='listar_pacientes'),
    url(r'^pacientes/(?P<pk>\d+)$', DetallePaciente.as_view(), name='detalle_paciente'),
]