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
from reportlab.lib.units import cm
from reportlab.lib.colors import black
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.rl_config import defaultPageSize


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
    
    PAGE_WIDTH  = defaultPageSize[0]

    margenIzq=30
    response = HttpResponse(content_type='applicatio/pdf')
    response['content-Disposition'] = 'attachment; filename= historia.pdf'
    buffer=BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    #HEADER
    c.setLineWidth(.3)
    c.setFont('Helvetica-Bold', 14)
    c.drawString(margenIzq+177,780, 'CONSULTORIOS MÉDICOS HERMANOS RODRÍGUEZ')
    c.setFont('Helvetica', 11)
    c.drawString(margenIzq+285,768, 'Consultorios ocupacionales y de medicina general.')
    c.drawString(margenIzq+324,756, 'Calle 4 #4 -97  Facatativá (Cundinamarca).')
    #c.setFont('Helvetica-Bold', 11)
    #text= 'EXAMENES REALIZADOS'
    #text_width = stringWidth(text,'Helvetica-Bold',11 )
    #c.line(margenIzq, 500, 560,500)
    #c.drawString((PAGE_WIDTH - text_width) / 2.0, 505, text)
    text='CERTIFICADO DE APTITUD LABORAL'
    text_width = stringWidth(text,'Helvetica-Bold',14)
    c.setFont('Helvetica-Bold', 14)
    c.drawString((PAGE_WIDTH - text_width) / 2.0,725, 'CERTIFICADO DE APTITUD LABORAL')

    #LOGOTIPO
    logo=os.path.join(os.path.dirname(os.path.abspath(__file__)), './Imagenes/logo.png')
    c.drawImage(logo,margenIzq,750,width=109, height=47)

    
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
    c.drawString(margenIzq,688, 'Fecha de consulta:')
    c.drawString(margenIzq,668, 'Nombre:')
    c.drawString(margenIzq,648, 'Identificación:')
    c.drawString(margenIzq+265, 628, 'Edad:')
    c.drawString(margenIzq+265, 648, 'Sexo:')
    c.drawString(margenIzq,628, 'Fecha de Nacimiento:')
    c.drawString(margenIzq, 608, 'EPS:')
    c.drawString(margenIzq, 588, 'ARL:')
    c.drawString(margenIzq, 568, 'Empresa:')
    c.drawString(margenIzq, 548, 'Cargo:')

    c.setFont('Helvetica', 9)
    c.drawString(margenIzq+63,648,paciente.cedula)
    c.drawString(75,668,paciente.primer_nombre+' '+paciente.segundo_nombre+' '
        +paciente.primer_apellido+' '+paciente.segundo_apellido)
    #c.drawString(margenIzq+190, 648, paciente.edad)
    c.drawString(margenIzq+292,648, paciente.sexo)
    #c.drawString(margenIzq+90, 628, 'F.Nacimiento')
    #c.drawString(margenIzq+30, 608, 'eps')
    #c.drawString(margenIzq+30, 588, 'ARL:')
    #c.drawString(margenIzq+50, 568, 'empresa')
    #c.drawString(margenIzq+50, 548, 'cargo')

    #Tabla examenes
    #   Header
    styles = getSampleStyleSheet()
    styleBH= styles["Normal"]
    styleBH.alignment = TA_CENTER
    styleBH.fontsize = 10
    styleBH.fontName = 'Helvetica-Bold'

    examenes=Paragraph('''EXAMENES REALIZADOS''', styleBH)
    dataTabla=[]
    dataTabla.append([examenes])

    #   Contenido
    styleN=styles["BodyText"]
    styleN.fontSize = 9
    styleN.fontName = 'Helvetica'

    high = 480
    cadena=[Paragraph('''Examen medico ocupacional básico.''', styleN)]
    dataTabla.append(cadena)

    width, height = A4
    tabla = Table(dataTabla, colWidths=[19*cm, 9.5*cm])
    tabla.setStyle(TableStyle([
        ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
        ('BOX', (0,0), (-1,-1), 1, colors.black),]))
    #c.drawString(margenIzq, 490, 'Examen medico ocupacional básico.')
    
    tabla.wrapOn(c,width, height)
    tabla.drawOn(c, margenIzq-2, high)
    c.showPage


    #Tabla Concepto
    #   Header
    concepto=Paragraph('''CONCEPTO''', styleBH)
    dataTablaConcepto=[]
    dataTablaConcepto.append([concepto])
    

    #   Contenido
    #high = 415
    #cadena=[Paragraph('''A''', styleN)]
    #dataTablaConcepto.append(cadena)

    width, height = A4
    tablaConcepto = Table(dataTablaConcepto, colWidths=[19*cm, 9.5*cm])
    tablaConcepto.setStyle(TableStyle([
        ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
        ('BOX', (0,0), (-1,-1), 1, colors.black),]))
    #c.drawString(margenIzq, 490, 'Examen medico ocupacional básico.')
    
    tablaConcepto.wrapOn(c,width, height)
    tablaConcepto.drawOn(c, margenIzq-2, high)
    c.showPage


    #Tabla observaciones
    #   Header
    observacion=Paragraph('''OBSERVACIONES''', styleBH)
    dataTablaObserv=[]
    dataTablaObserv.append([observacion])

    #   Contenido
    high = 50
    cadena=[Paragraph('''A''', styleN)]
    dataTablaObserv.append(cadena)

    width, height = A4
    tablaObserv = Table(dataTablaObserv, colWidths=[19*cm, 9.5*cm], rowHeights=(5*cm, 5*cm))
    tablaObserv.setStyle(TableStyle([
        ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
        ('BOX', (0,0), (-1,-1), 1, colors.black),]))
    #c.drawString(margenIzq, 490, 'Examen medico ocupacional básico.')
    
    tablaObserv.wrapOn(c,width, height)
    tablaObserv.drawOn(c, margenIzq-2, high)
    c.showPage

    c.setStrokeColor(black)
    c.setLineWidth(1)
    c.rect(margenIzq-2,540, 538,165, fill=0)

    
    c.save()
    pdf=buffer.getvalue();
    buffer.close()
    response.write(pdf)
    return response

