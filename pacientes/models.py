# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.urls import reverse

# Create your models here.

class Paciente(models.Model):
    estados_civiles = (
        ('soltero', 'Soltero/a'),
        ('casado', 'Casado/a'),
        ('union libre', 'Union libre'),
        ('viudo', 'Viudo/a'),
        ('divorciado', 'Divorciado/a'),
        ('comprometido', 'Comprometido/a')
    )
    cedula = models.CharField(primary_key=True, max_length=11)
    primer_nombre = models.CharField(max_length=15)
    segundo_nombre = models.CharField(max_length=15, blank=True)
    primer_apellido = models.CharField(max_length=15)
    segundo_apellido = models.CharField(max_length=15)
    direccion = models.CharField(max_length=100)
    ciudad = models.CharField(max_length=50)
    fecha_nacimiento = models.DateField()
    estado_civil = models.CharField(max_length=50, choices=estados_civiles)
    telefono = models.CharField(max_length=10)

    def __str__(self):
        return self.cedula

    def get_absolute_url(self):
        return reverse('pacientes:detalle_paciente', kwargs={"pk": self.cedula})

