# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from pacientes.models import Paciente
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Actualizacion(models.Model):

    fecha_actualizacion = models.DateField(auto_now=True)
    motivo_consulta = models.TextField(default=None)
    tratamiento = models.TextField(default=None)

    def __str__(self):
        return str(self.id)


class Cabecera(models.Model):

    numero_historia = models.CharField(primary_key=True, max_length=15)
    antecedentes = models.ForeignKey(Actualizacion, on_delete=models.CASCADE)
    paciente = models.OneToOneField(Paciente)

    def __str__(self):
        return self.numero_historia


@receiver(post_save, sender=Paciente)
def crearCabecera(sender, **kwargs):
    actualizacion = Actualizacion.objects.create(
        motivo_consulta="Primer registro del Paciente", tratamiento="Primer registro del Paciente")
    actualizacion.save()
    cabecera_usuario = Cabecera.objects.create(
        numero_historia=kwargs['instance'].cedula, paciente=kwargs['instance'], antecedentes = actualizacion)
    cabecera_usuario.save()
