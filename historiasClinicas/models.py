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

    tipo_examen = (
        ('Pre-ingreso','preingreso'),
        ('Periodico', 'periodico'),
        ('Egreso', 'egreso'),
        ('Cambio labor', 'cambio labor'),
        ('Reincorporacion laboral', 'reincorporacion'),
        ('Rev. Paraclinicos', 'rev paraclinicos'),
    )
    
    fecha_actualizacion = models.DateField(auto_now=True)
    #motivo_consulta = models.TextField(default=None)
    #tratamiento = models.TextField(default=None)
    cabecera = models.ForeignKey(Cabecera)
    
    #Nuevos
    empresa = models.CharField(max_length=100)
    cargo_aspirado = models.CharField(max_length=150)
    eps = models.CharField(max_length=100)
    arl = models.CharField(max_length=100)
    examen_actual = models.CharField(max_length=50, choices=tipo_examen)
    #preingreso = models.CharField(max_length=1, default='')
    #periodico=models.CharField(max_length=1, default='')
    #egreso=models.CharField(max_length=1,  default='')
    #cambio_labor=models.CharField(max_length=1, default='')
    #reincorp_labor=models.CharField(max_length=1, default='')
    #rev_paraclinicos=models.CharField(max_length=1, default='')
    
    #   Antecedentes
    ante_personales=models.CharField(max_length=1000)
    ante_laborales=models.CharField(max_length=1000)
    ante_familiares=models.CharField(max_length=1000)
    ante_ginecobstre=models.CharField(max_length=1000)

    #   Examen Fisico
    ta=models.CharField(max_length=15)
    fc=models.CharField(max_length=15)
    fr=models.CharField(max_length=15)
    peso=models.CharField(max_length=15)
    talla=models.CharField(max_length=15)
    imc=models.CharField(max_length=15)
    cabeza_cuello=models.CharField(max_length=500)
    sentidos=models.CharField(max_length=500)
    cardiopulmonar=models.CharField(max_length=500)
    abdomen=models.CharField(max_length=500)
    osteomuscular=models.CharField(max_length=500)
    neurologico=models.CharField(max_length=500)
    esfera_mental=models.CharField(max_length=500)

    #   Concepto de valoracion medica
    apto_sin_pato=models.CharField(max_length=2)
    apto_con_pato=models.CharField(max_length=2)
    apto_con_restri=models.CharField(max_length=2)
    aplazado=models.CharField(max_length=2)
    apto_alturas=models.CharField(max_length=2)
    apto_continuar_labor=models.CharField(max_length=2)
    examen_retiro=models.CharField(max_length=2)
    apto_alturas=models.CharField(max_length=2 )
    secuela_accidente_trabajo=models.CharField(max_length=2, choices=seleccion)
    #fecha_at = models.DateField(default=None)
    enfermedad_profesional=models.CharField(max_length=2, choices=seleccion)
    #fecha_dxco = models.DateField(default=None)
    efermedad_relTrabajo=models.CharField(max_length=2, choices=seleccion)
    #   Resultados de laboratorios
    resultados_laboratorio=models.CharField(max_length=5000)
    #   Recomendaciones
    #Restricciones laborales
    no_encuentra=models.CharField(max_length=2)
    transitorias=models.CharField(max_length=2)
    tiempo=models.CharField(max_length=10)
    permanentes=models.CharField(max_length=2)
    remite_eps=models.CharField(max_length=2)
    continuar_eps=models.CharField(max_length=2)
    remite_arl=models.CharField(max_length=2)
    otras=models.CharField(max_length=500)
    auditivo=models.CharField(max_length=2)
    visual=models.CharField(max_length=2)
    respiratorio=models.CharField(max_length=2)
    biologico=models.CharField(max_length=2)
    quimico=models.CharField(max_length=2)
    ergonomico=models.CharField(max_length=2)
    psicosocial=models.CharField(max_length=2)
    accidente_trabajo=models.CharField(max_length=2)
    otro=models.CharField(max_length=2)
    ninguno=models.CharField(max_length=2)

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
    actualizacion = Actualizacion.objects.create(cabecera=cabecera_usuario)
    actualizacion.save()