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
        'ante_personales',
        'ante_laborales',
        'ante_familiares',
        'ante_ginecobstre',
        'ta',
        'fc',
        'fr',
        'peso',
        'talla',
        'imc',
        'cabeza_cuello',
        'sentidos',
        'cardiopulmonar',
        'abdomen',
        'osteomuscular',
        'neurologico',
        'esfera_mental',
        'concepto_valoracion',
        'secuela_accidente_trabajo',
        'enfermedad_profesional',
        'efermedad_relTrabajo',
        'fecha_dxco',
        'fecha_at',
        'resultados_laboratorio',
        'restricciones_laborales',
        'remite',
        'otras',
        'ingreso_sistema_epidemiologico_ocupacional',
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


