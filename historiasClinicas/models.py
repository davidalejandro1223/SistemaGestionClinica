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
    

    seleccion = (
        ('Si','si'),
        ('No','no')        
    )
    
    fecha_actualizacion = models.DateField(auto_now=True)
    motivo_consulta = models.TextField(default=None)
    tratamiento = models.TextField(default=None)
    cabecera = models.ForeignKey(Cabecera)
    #Nuevos
    empresa=models.CharField(max_length=100, default='empresa')
    cargo_aspirado=models.CharField(max_length=100, default='cargo al que aspira')
    eps=models.CharField(max_length=50, default='nombre de la eps')
    arl=models.CharField(max_length=50, default='nombre de arl')
    preingreso=models.CharField(max_length=1, default='')
    periodico=models.CharField(max_length=1, default='')
    egreso=models.CharField(max_length=1,  default='')
    cambio_labor=models.CharField(max_length=1, default='')
    reincorp_labor=models.CharField(max_length=1, default='')
    #   Antecedentes
    rev_paraclinicos=models.CharField(max_length=1, default='')
    ante_personales=models.CharField(max_length=1000,default='Antecedentes personales')
    ante_laborales=models.CharField(max_length=1000,default='Antecedentes laborales')
    ante_familiares=models.CharField(max_length=1000,default='Antecedentes familiares')
    ante_ginecobstre=models.CharField(max_length=1000,default='Antecedentes ginecobstetricos')
    #   Examen Fisico
    ta=models.CharField(max_length=15,default='')
    fc=models.CharField(max_length=15,default='')
    fr=models.CharField(max_length=15,default='')
    peso=models.CharField(max_length=15,default='')
    talla=models.CharField(max_length=15,default='')
    imc=models.CharField(max_length=15,default='')
    cabeza_cuello=models.CharField(max_length=500,default='')
    sentidos=models.CharField(max_length=500,default='')
    cardiopulmonar=models.CharField(max_length=500,default='')
    abdomen=models.CharField(max_length=500,default='')
    osteomuscular=models.CharField(max_length=500,default='')
    neurologico=models.CharField(max_length=500,default='')
    esfera_mental=models.CharField(max_length=500,default='')
    #   Concepto de valoracion medica
    apto_sin_pato=models.CharField(max_length=2, default='x')
    apto_con_pato=models.CharField(max_length=2, default='')
    apto_con_restri=models.CharField(max_length=2, default='')
    aplazado=models.CharField(max_length=2, default='')
    apto_alturas=models.CharField(max_length=2, default='')
    apto_continuar_labor=models.CharField(max_length=2, default='')
    examen_retiro=models.CharField(max_length=2, default='')
    apto_alturas=models.CharField(max_length=2,  default='')
    secuela_accidente_trabajo=models.CharField(max_length=2, choices=seleccion ,default='No')
    #fecha_at = models.DateField(default=None)
    enfermedad_profesional=models.CharField(max_length=2, choices=seleccion ,default='No')
    #fecha_dxco = models.DateField(default=None)
    efermedad_relTrabajo=models.CharField(max_length=2, choices=seleccion ,default='No')
    #   Resultados de laboratorios
    resultados_laboratorio=models.CharField(max_length=5000,default='')
    #   Recomendaciones
    #Restricciones laborales
    no_encuentra=models.CharField(max_length=2, default='x')
    transitorias=models.CharField(max_length=2, default='')
    tiempo=models.CharField(max_length=10, default='')
    permanentes=models.CharField(max_length=2, default='')
    remite_eps=models.CharField(max_length=2, default='')
    continuar_eps=models.CharField(max_length=2, default='')
    remite_arl=models.CharField(max_length=2, default='')
    otras=models.CharField(max_length=500,default='')
    auditivo=models.CharField(max_length=2, default='')
    visual=models.CharField(max_length=2, default='')
    respiratorio=models.CharField(max_length=2, default='')
    biologico=models.CharField(max_length=2, default='')
    quimico=models.CharField(max_length=2, default='')
    ergonomico=models.CharField(max_length=2, default='')
    psicosocial=models.CharField(max_length=2, default='')
    accidente_trabajo=models.CharField(max_length=2, default='')
    otro=models.CharField(max_length=2, default='')
    ninguno=models.CharField(max_length=2, default='x')

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