# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Cabecera, Actualizacion
from pacientes.models import Paciente

# Create your views here.

def historia_paciente(request, pk):
    cabecera = get_object_or_404(Cabecera, paciente=pk)
    paciente = get_object_or_404(Paciente, cedula=pk)
    actualizaciones = Actualizacion.objects.filter(cabecera=cabecera.numero_historia)
    context = {
        'cabecera': cabecera,
        'paciente': paciente,
        'actualizaciones':actualizaciones
    }
    return render(request, 'historiaClinica/historia_clinica.html', context)
