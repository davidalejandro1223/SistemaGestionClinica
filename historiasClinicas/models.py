# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from pacientes.models import Paciente
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Cabecera(models.Model):

    numero_historia = models.CharField(primary_key=True, max_length=15)
    paciente = models.OneToOneField(Paciente)

    def __str__(self):
        return self.numero_historia

class Actualizacion(models.Model):

    fecha_actualizacion = models.DateField(auto_now=True)
    motivo_consulta = models.TextField(default=None)
    tratamiento = models.TextField(default=None)
    cabecera = models.ForeignKey(Cabecera)

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('historias_clinicas:historia_paciente', kwargs={'pk': self.cabecera.numero_historia})


@receiver(post_save, sender=Paciente)
def crearCabecera(sender, **kwargs):
    cabecera_usuario = Cabecera.objects.create(
        numero_historia=kwargs['instance'].cedula, paciente=kwargs['instance'])
    cabecera_usuario.save()
    actualizacion = Actualizacion.objects.create(
        motivo_consulta="Primer registro del Paciente", tratamiento="Primer registro del Paciente", cabecera=cabecera_usuario)
    actualizacion.save()
