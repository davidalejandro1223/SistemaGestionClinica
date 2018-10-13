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
        ('si','Si'),
        ('no','No')        
    )

    tipo_examen = (
        ('preingreso','Pre-ingreso'),
        ('periodico','Periodico'),
        ('egreso','Egreso'),
        ('cambio labor','Cambio labor'),
        ('reincorporacion','Reincorporacion laboral'),
        ('rev paraclinicos','Rev. Paraclinicos'),
    )

    conceptos_valoracion_medica = (
        ('apto sin patologia','Apto para desempeñar el cargo sin patologia aparente'),
        ('apto con patologia','Apto para desempañar el cargo con patologia que no limita la labor'),
        ('apto con restricciones','Apto con restricciones o adaptaciones para la labor'),
        ('aplazado','Aplazado'),
        ('apto alturas','Apto para labor el alturas'),
        ('apto continuacion labor','Apto para continuar desempeñando su labor'),
        ('examen de retiro','Examen de retiro'),
    )

    restr_laborales = (
        ('no se encuentra','No se encuentra'),
        ('transitorias','Transitorias'),
        ('tiempo','Tiempo'),
        ('permanentes','Permanentes'),
    )

    remitenicia = (
        ('se remite EPS','Se remite a EPS'),
        ('continuar manejor medico EPS','Continuar manejo medio por EPS'),
        ('se remire ARL','Se remite a ARL'),
    )
    
    opciones_sistema_epidemiologico_ocupacional = (
        ('ergonomico','Ergonómico'),
        ('Psicosocial','Psicosocial'),
        ('auditivo','Autitivo'),
        ('visual','Visual'),
        ('respiratorio','Respitatorio'),
        ('biologico','Biológico'),
        ('quimico','Quimico'),
        ('accidente trabajo','Accidente de trabajo'),
        ('otro','Otro'),
        ('ninguno','Ninguno'),
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
    concepto_valoracion = models.CharField(max_length=50, choices=conceptos_valoracion_medica)
    #apto_sin_pato=models.CharField(max_length=2)
    #apto_con_pato=models.CharField(max_length=2)
    #apto_con_restri=models.CharField(max_length=2)
    #aplazado=models.CharField(max_length=2)
    #apto_alturas=models.CharField(max_length=2)
    #apto_continuar_labor=models.CharField(max_length=2)
    #examen_retiro=models.CharField(max_length=2)
    #apto_alturas=models.CharField(max_length=2 )
    secuela_accidente_trabajo=models.CharField(max_length=2, choices=seleccion)
    enfermedad_profesional=models.CharField(max_length=2, choices=seleccion)
    efermedad_relTrabajo=models.CharField(max_length=2, choices=seleccion)
    fecha_dxco = models.DateField()
    fecha_at = models.DateField()

    #   Resultados de laboratorios
    resultados_laboratorio=models.CharField(max_length=5000)
   
    #   Recomendaciones
    #Restricciones laborales
    restricciones_laborales = models.CharField(max_length=50, choices=restr_laborales)

    #Recomendaciones trabajador
    remite = models.CharField(max_length=50, choices=remitenicia)
    #no_encuentra=models.CharField(max_length=2)
    #transitorias=models.CharField(max_length=2)
    #tiempo=models.CharField(max_length=10)
    #permanentes=models.CharField(max_length=2)
    #remite_eps=models.CharField(max_length=2)
    #continuar_eps=models.CharField(max_length=2)
    #remite_arl=models.CharField(max_length=2)

    #recomendaciones empresa
    otras=models.CharField(max_length=1000)
    ingreso_sistema_epidemiologico_ocupacional = models.CharField(max_length=50, choices=opciones_sistema_epidemiologico_ocupacional)
    #auditivo=models.CharField(max_length=2)
    #visual=models.CharField(max_length=2)
    #respiratorio=models.CharField(max_length=2)
    #biologico=models.CharField(max_length=2)
    #quimico=models.CharField(max_length=2)
    #ergonomico=models.CharField(max_length=2)
    #psicosocial=models.CharField(max_length=2)
    #accidente_trabajo=models.CharField(max_length=2)
    #otro=models.CharField(max_length=2)
    #ninguno=models.CharField(max_length=2)

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