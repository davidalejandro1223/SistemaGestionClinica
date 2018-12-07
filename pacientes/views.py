# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import Paciente
from .forms import PacienteForm
from django.http.response import HttpResponse

# Create your views here.


class CrearPaciente(CreateView):
    model = Paciente
    #form_class = PacienteForm
    #template_name = 'pacientes/paciente_form.html'
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

    def post(self, request, *args, **kwargs):
        form = PacienteForm(request.POST, request.FILES)
        if form.is_valid():
            print(request.FILES)
            form.save()
            return HttpResponse('Formulario valido')
        print('no es valido')
        print(request.FILES)
        return HttpResponse('Formulario no valido')

class DetallePaciente(DetailView):
    model = Paciente


class PacienteListView(ListView):
    model = Paciente
