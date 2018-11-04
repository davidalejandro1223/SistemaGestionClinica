# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Paciente
from django.core.urlresolvers import reverse_lazy

# Create your views here.


class CrearPaciente(CreateView):
    model = Paciente
    fields = [
        'cedula',
        'primer_nombre',
        'segundo_nombre',
        'primer_apellido',
        'segundo_apellido',
        'direccion',
        'ciudad',
        'fecha_nacimiento',
        'estado_civil',
        'telefono',
        'sexo',
    ]


class DetallePaciente(DetailView):
    model = Paciente


class PacienteListView(ListView):
    model = Paciente
