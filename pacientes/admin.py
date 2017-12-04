# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Paciente
from django.contrib import admin

# Register your models here.
@admin.register(Paciente)
class AdminPaciente(admin.ModelAdmin):
    list_display = ('primer_nombre', 'segundo_nombre', 'cedula' ,)
