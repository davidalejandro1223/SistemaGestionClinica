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
    response = HttpResponse(content_type='applicatio/pdf')
    response['content-Disposition'] = 'attachment; filename= historia.pdf'
    buffer=BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    
    #HEADER
    c.setLineWidth(.3)
    c.setFont('Helvetica', 14)
    c.drawString(30,780, 'CONSULTORIOS MEDICOS HERMANOS RODRIGUEZ')
    c.setFont('Helvetica', 11)
    c.drawString(30,768, 'Consultorios ocupacionales y de medicina general.')
    c.drawString(30,756, 'Calle 4 #4 -97  Facatativá (Cundinamarca).')
    
    logo=os.path.join(os.path.dirname(os.path.abspath(__file__)), './Imagenes/logo.png')
    c.drawImage(logo,410,740,width=156, height=68)

    c.setFont('Helvetica', 14)
    c.drawString(168,705, 'HISTORIA CLINICA OCUPACIONAL')

    c.save()
    pdf=buffer.getvalue();
    buffer.close()
    response.write(pdf)
    return response

   
