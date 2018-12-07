#from django.conf.urls import url
from django.urls import re_path
from .views import historia_paciente, HistoriaClinicaListView, ActualizacionCreateView, report, ActualizacionDetailView

app_name = 'historias_clinicas'

urlpatterns = [
    re_path(r'^historia-clinica$', HistoriaClinicaListView.as_view(), name='listar_historias'),
    re_path(r'^historia-clinica/(?P<pk>\d+)$', historia_paciente, name='historia_paciente'),
    re_path(r'^historia-clinica/(?P<pk>[0-9]+)/(?P<pk_A>[0-9]+)$',ActualizacionDetailView.as_view(), name='detalle_actualizacion'),
    re_path(r'^historia-clinica/(?P<pk>[0-9]+)/(?P<pk_A>[0-9]+)/pdf$',report, name='reporte_pdf'),
    re_path(r'^historia-clinica/(?P<pk>[0-9]+)/nueva-entrada$',
        ActualizacionCreateView.as_view(), name='crear_actualizacion'),
]
