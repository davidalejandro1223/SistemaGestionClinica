# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Cabecera, Actualizacion
from pacientes.models import Paciente
from django.views.generic.list import ListView
from django.views.generic import CreateView
#Librerias para la generación del PDF
import os
import os.path
from io import BytesIO
import xlwt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER
from reportlab.lib import colors
from django.http import HttpResponse
from reportlab.lib.utils import ImageReader



# Create your views here.
class ActualizacionCreateView(CreateView):
    model = Actualizacion
    fields = [
        'empresa',
        'cargo_aspirado',
        'eps',
        'arl',
        'examen_actual',
        'antecedentes_personales',
        'antecedentes_laborales',
        'antecedentes_familiares',
        'antecedentes_ginecobstetricos',
        'ta',
        'fc',
        'fr',
        'peso',
        'talla',
        'imc',
        'cabeza_y_cuello',
        'sentidos',
        'cardiopulmonar',
        'abdomen',
        'osteomuscular',
        'neurologico',
        'esfera_mental',
        'valoracion_medica',
        'secuela_acci_trab',
        'enfer_pro',
        'enfer_rel_trabajo',
        'fecha_dxco',
        'fecha_at',
        'resultados_laboratorio',
        'restricciones_laborales',
        'remite',
        'otras',
        'ingreso_sis_epidem_ocup',
    ]

    def form_valid(self, form):
        form.instance.cabecera = Cabecera.objects.get(numero_historia=self.kwargs.get('pk'))
        return super(ActualizacionCreateView, self).form_valid(form)

def historia_paciente(request, pk):
    cabecera = get_object_or_404(Cabecera, paciente=pk)
    paciente = get_object_or_404(Paciente, cedula=pk)
    actualizaciones = Actualizacion.objects.filter(cabecera=cabecera.numero_historia)
    context = {
        'cabecera': cabecera,
        'paciente': paciente,
        'actualizaciones':actualizaciones
    }
    return render(request, 'historiasClinicas/historia_clinica.html', context)


class HistoriaClinicaListView(ListView):
    model = Cabecera

def report(request, pk):
    margenIzq=30;
    response = HttpResponse(content_type='applicatio/pdf')
    response['content-Disposition'] = 'attachment; filename= historia.pdf'
    buffer=BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    
    #HEADER
    c.setLineWidth(.3)
    c.setFont('Helvetica-Bold', 14)
    c.drawString(margenIzq,780, 'CONSULTORIOS MÉDICOS HERMANOS RODRÍGUEZ')
    c.setFont('Helvetica', 11)
    c.drawString(margenIzq,768, 'Consultorios ocupacionales y de medicina general.')
    c.drawString(margenIzq,756, 'Calle 4 #4 -97  Facatativá (Cundinamarca).')
    c.setFont('Helvetica-Bold', 14)
    c.drawString(173,715, 'HISTORIA CLÍNICA OCUPACIONAL')

    #LOGOTIPO
    logo=os.path.join(os.path.dirname(os.path.abspath(__file__)), './Imagenes/logo.png')
    c.drawImage(logo,440,750,width=109, height=47)

    
    cabecera = get_object_or_404(Cabecera, paciente=pk)
    paciente = get_object_or_404(Paciente, cedula=pk)
    actualizaciones = Actualizacion.objects.filter(cabecera=cabecera.numero_historia)
    context = {
        'cabecera': cabecera,
        'paciente': paciente,
        'actualizaciones':actualizaciones
    }
    
    #DATOS DEL PACIENTE
    c.setFont('Helvetica-Bold', 9)
    
    c.drawString(margenIzq,688, 'Paciente:')
    c.drawString(margenIzq,678, 'Identificación:')
    c.drawString(margenIzq+60, 678, '')
    c.setFont('Helvetica', 9)
    c.drawString(margenIzq+63,678,paciente.cedula)
    c.drawString(75,688,paciente.primer_nombre+' '+paciente.segundo_nombre+' '+paciente.primer_apellido+' '+paciente.segundo_apellido)


    c.save()
    pdf=buffer.getvalue();
    buffer.close()
    response.write(pdf)
    return response

   
