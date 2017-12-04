from django.conf.urls import url
from .views import historia_paciente, HistoriaClinicaListView, ActualizacionCreateView

urlpatterns = [
    url(r'^historia-clinica$', HistoriaClinicaListView.as_view(), name='listar_historias'),
    url(r'^historia-clinica/(?P<pk>\d+)$', historia_paciente, name='historia_paciente'),
    url(r'^historia-clinica/(?P<pk>[0-9]+)/nueva-entrada$',
        ActualizacionCreateView.as_view(), name='crear_actualizacion'),
]
