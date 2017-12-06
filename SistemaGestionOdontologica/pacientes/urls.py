from django.conf.urls import url
from .views import CrearPaciente, DetallePaciente, PacienteListView

urlpatterns = [
	url(r'^nuevoPaciente$', CrearPaciente.as_view(), name='nuevo_paciente'),
    url(r'^pacientes$', PacienteListView.as_view(), name='listar_pacientes'),
    url(r'^pacientes/(?P<pk>\d+)$', DetallePaciente.as_view(), name='detalle_paciente'),
]