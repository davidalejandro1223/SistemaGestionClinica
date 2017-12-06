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
    fields = '__all__'


class DetallePaciente(DetailView):
    model = Paciente


class PacienteListView(ListView):
    model = Paciente
