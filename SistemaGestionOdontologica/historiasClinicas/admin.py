# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Actualizacion, Cabecera
from django.contrib import admin

# Register your models here.
@admin.register(Actualizacion)
class AdminActualizacion(admin.ModelAdmin):
    list_display = ('id', 'fecha_actualizacion',)

@admin.register(Cabecera)
class AdminCabecera(admin.ModelAdmin):
    list_display = ('numero_historia', 'paciente')