# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from pacientes.models import Paciente
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.


class Cabecera(models.Model):

    numero_historia = models.CharField(primary_key=True, max_length=15)
    paciente = models.OneToOneField(
        Paciente,
        on_delete=models.CASCADE,
    )

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
        ('manipulacion de alimentos','Manipulacion de alimentos'),
    )

    conceptos_valoracion_medica = (
        ('apto sin patologia','Apto para desempeñar el cargo sin patologia aparente'),
        ('apto con patologia','Apto para desempañar el cargo con patologia que no limita la labor'),
        ('apto con restricciones','Apto con restricciones o adaptaciones para la labor'),
        ('aplazado','Aplazado'),
        ('apto alturas','Apto para labor el alturas'),
        ('apto continuacion labor','Apto para continuar desempeñando su labor'),
        ('examen de retiro','Examen de retiro'),
        ('apto para manipulación de alimentos','Apto para manipulación de alimentos'),
    )

    restr_laborales = (
        ('no se encuentra','No se encuentra'),
        ('transitorias','Transitorias'),
        ('tiempo','Tiempo'),
        ('permanentes','Permanentes'),
    )

    remitenicia = (
        ('ninguno', 'Ninguno'),
        ('se remite EPS','Se remite a EPS'),
        ('continuar manejo medico EPS','Continuar manejo medico por EPS'),
        ('se remite ARL','Se remite a ARL'),
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
    cabecera = models.ForeignKey(
        Cabecera,
        on_delete=models.CASCADE,
    )
    
    #Nuevos
    empresa = models.CharField(max_length=100)
    cargo_aspirado = models.CharField(max_length=150)
    eps = models.CharField(max_length=100, verbose_name='EPS')
    arl = models.CharField(max_length=100, verbose_name='ARL')
    examen_actual = models.CharField(max_length=50, choices=tipo_examen, verbose_name='Examen')
    #preingreso = models.CharField(max_length=1, default='')
    #periodico=models.CharField(max_length=1, default='')
    #egreso=models.CharField(max_length=1,  default='')
    #cambio_labor=models.CharField(max_length=1, default='')
    #reincorp_labor=models.CharField(max_length=1, default='')
    #rev_paraclinicos=models.CharField(max_length=1, default='')
    
    #   Antecedentes
    antecedentes_personales=models.TextField()
    antecedentes_laborales=models.TextField()
    antecedentes_familiares=models.TextField()
    antecedentes_ginecobstetricos=models.TextField()

    #   Examen Fisico
    ta=models.CharField(max_length=9, verbose_name='TA')
    fc=models.IntegerField(verbose_name='FC')
    fr=models.IntegerField(verbose_name='FR')
    peso=models.DecimalField(max_digits=5,decimal_places=2)
    talla=models.DecimalField(max_digits=5,decimal_places=2)
    imc=models.DecimalField(max_digits=60,decimal_places=2,verbose_name='IMC')
    cabeza_y_cuello=models.CharField(max_length=500)
    sentidos=models.CharField(max_length=500)
    cardiopulmonar=models.CharField(max_length=500)
    abdomen=models.CharField(max_length=500)
    osteomuscular=models.CharField(max_length=500)
    neurologico=models.CharField(max_length=500)
    esfera_mental=models.CharField(max_length=500)

    #   Concepto de valoracion medica
    valoracion_medica= models.CharField(
        max_length=50,
        choices=conceptos_valoracion_medica,
        verbose_name='Concepto de valoracion medica',
    )
    #apto_sin_pato=models.CharField(max_length=2)
    #apto_con_pato=models.CharField(max_length=2)
    #apto_con_restri=models.CharField(max_length=2)
    #aplazado=models.CharField(max_length=2)
    #apto_alturas=models.CharField(max_length=2)
    #apto_continuar_labor=models.CharField(max_length=2)
    #examen_retiro=models.CharField(max_length=2)
    #apto_alturas=models.CharField(max_length=2 )
    secuela_acci_trab=models.CharField(
        max_length=2, 
        choices=seleccion, 
        verbose_name='Secuela accidente de trabajo'
    )
    enfer_pro=models.CharField(
        max_length=2, 
        choices=seleccion, 
        verbose_name='Enfermedad profesional'
    )
    enfer_rel_trabajo=models.CharField(
        max_length=2, 
        choices=seleccion, 
        verbose_name='Enfermedad relacionada con el trabajo'
    )

    #reemplazar textfield por datepicker con bootstrap
    fecha_dxco = models.DateField(blank=True,null=True, verbose_name='Fecha del diagnostico')
    fecha_at = models.DateField(blank=True,null=True, verbose_name='Fecha accidente de trabajo')

    #   Resultados de laboratorios
    resultados_laboratorio=models.TextField(verbose_name='Resultados de laboratorio')
   
    #   Recomendaciones
    #Restricciones laborales
    restricciones_laborales = models.CharField(max_length=50, choices=restr_laborales)

    #Recomendaciones trabajador
    remite = models.CharField(max_length=50, choices=remitenicia, verbose_name='Se remite a')
    #no_encuentra=models.CharField(max_length=2)
    #transitorias=models.CharField(max_length=2)
    #tiempo=models.CharField(max_length=10)
    #permanentes=models.CharField(max_length=2)
    #remite_eps=models.CharField(max_length=2)
    #continuar_eps=models.CharField(max_length=2)
    #remite_arl=models.CharField(max_length=2)

    #recomendaciones empresa
    otras=models.TextField(verbose_name='Recomendaciones para la empresa')
    observaciones=models.TextField(verbose_name='Observaciones')

    ingreso_sis_epidem_ocup = models.CharField(
        max_length=50, 
        choices=opciones_sistema_epidemiologico_ocupacional, 
        verbose_name='Ingresar al trabajador examinado al Sistema de Vigilancia Epidemiológica Ocupacional'
    )
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
        from django.urls import reverse
        return reverse('historias_clinicas:historia_paciente', kwargs={'pk': self.cabecera.numero_historia})


@receiver(post_save, sender=Paciente)
def crearCabecera(sender, **kwargs):
    cabecera_usuario = Cabecera.objects.create(
        numero_historia=kwargs['instance'].cedula, paciente=kwargs['instance'])
    cabecera_usuario.save()