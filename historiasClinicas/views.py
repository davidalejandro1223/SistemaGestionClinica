# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Cabecera, Actualizacion
from pacientes.models import Paciente
from django.views.generic.list import ListView
from django.views.generic import CreateView

# Create your views here.
class ActualizacionCreateView(CreateView):
    model = Actualizacion
    fields = [
        'empresa',
        'cargo_aspirado',
        'eps',
        'arl',
        'examen_actual',
        'antecedentes_personales',
        'antecedentes_laborales',
        'antecedentes_familiares',
        'antecedentes_ginecobstetricos',
        'ta',
        'fc',
        'fr',
        'peso',
        'talla',
        'imc',
        'cabeza_y_cuello',
        'sentidos',
        'cardiopulmonar',
        'abdomen',
        'osteomuscular',
        'neurologico',
        'esfera_mental',
        'valoracion_medica',
        'secuela_acci_trab',
        'enfer_pro',
        'enfer_rel_trabajo',
        'fecha_dxco',
        'fecha_at',
        'resultados_laboratorio',
        'restricciones_laborales',
        'remite',
        'otras',
        'ingreso_sis_epidem_ocup',
    ]

    def form_valid(self, form):
        form.instance.cabecera = Cabecera.objects.get(numero_historia=self.kwargs.get('pk'))
        return super(ActualizacionCreateView, self).form_valid(form)

def historia_paciente(request, pk):
    cabecera = get_object_or_404(Cabecera, paciente=pk)
    paciente = get_object_or_404(Paciente, cedula=pk)
    actualizaciones = Actualizacion.objects.filter(cabecera=cabecera.numero_historia)
    context = {
        'cabecera': cabecera,
        'paciente': paciente,
        'actualizaciones':actualizaciones
    }
    return render(request, 'historiasClinicas/historia_clinica.html', context)


class HistoriaClinicaListView(ListView):
    model = Cabecera


