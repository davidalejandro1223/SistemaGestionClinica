# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Cabecera, Actualizacion
from pacientes.models import Paciente
from django.views.generic.list import ListView
from django.views.generic import CreateView, DetailView

#Librerias para la generación del PDF
import datetime
import os
import os.path
from io import BytesIO
import xlwt
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
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


class ActualizacionDetailView(DetailView):
    model = Actualizacion
    pk_url_kwarg = 'pk_A'
    
    def get_queryset(self):
        queryset = Actualizacion.objects.filter(id=self.kwargs.get('pk_A'))
        print(queryset.values())
        return queryset
    
    
    def get_context_data(self, **kwargs):
        context = super(ActualizacionDetailView, self).get_context_data(**kwargs)
        context['paciente'] = Paciente.objects.get(cedula=self.kwargs['pk'])
        return context
    
    

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

def report(request, pk, pk_A):
    margenIzq=30;
    PAGE_WIDTH  = defaultPageSize[0]
    response = HttpResponse(content_type='applicatio/pdf')
    response['content-Disposition'] = 'attachment; filename= historia.pdf'
    buffer=BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)


    cabecera = get_object_or_404(Cabecera, paciente=pk)
    paciente = get_object_or_404(Paciente, cedula=pk)
    actualizacion = Actualizacion.objects.get(id=pk_A)
    context = {
        'cabecera': cabecera,
        'paciente': paciente,
        'actualizacion':actualizacion
    }

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
    text='Motivo: '+actualizacion.examen_actual
    text_width = stringWidth(text,'Helvetica-Bold',14)
    c.drawString((PAGE_WIDTH - text_width) / 2.0,710, text)


    #LOGOTIPO
    logo=os.path.join(os.path.dirname(os.path.abspath(__file__)), './Imagenes/logo.png')
    c.drawImage(logo,margenIzq,750,width=109, height=47)

    
    #DATOS DEL PACIENTE
    c.setFont('Helvetica-Bold', 9)
    c.drawString(margenIzq,688, 'Fecha de consulta:')
    c.drawString(margenIzq,668, 'Nombre:')
    c.drawString(margenIzq,648, 'Identificación:')
    c.drawString(margenIzq+255, 628, 'Edad:')
    c.drawString(margenIzq+255, 648, 'Sexo:')
    c.drawString(margenIzq,628, 'Fecha de Nacimiento:')
    c.drawString(margenIzq, 608, 'EPS:')
    c.drawString(margenIzq, 588, 'ARL:')
    c.drawString(margenIzq, 568, 'Empresa:')
    c.drawString(margenIzq, 548, 'Cargo:')

    c.setFont('Helvetica', 9)
    c.drawString(margenIzq+85, 688, actualizacion.fecha_actualizacion.strftime('%m/%d/%Y'))
    c.drawString(margenIzq+64,648,paciente.cedula)
    c.drawString(75,668,paciente.primer_nombre+' '+paciente.segundo_nombre+' '
        +paciente.primer_apellido+' '+paciente.segundo_apellido)
    #c.drawString(margenIzq+190, 648, paciente.edad)
    c.drawString(margenIzq+282,648, paciente.sexo)
    c.drawString(margenIzq+98, 628, paciente.fecha_nacimiento.strftime('%m/%d/%Y'))
    c.drawString(margenIzq+28, 608, actualizacion.eps)
    c.drawString(margenIzq+28, 588, actualizacion.arl)
    c.drawString(margenIzq+48, 568, actualizacion.empresa)
    c.drawString(margenIzq+38, 548, actualizacion.cargo_aspirado)

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
    valoracion=actualizacion.valoracion_medica
    high = 415
    cadena=[Paragraph(valoracion, styleN)]
    dataTablaConcepto.append(cadena)

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
    styleN.alignment = TA_JUSTIFY
    observacion=Paragraph('''OBSERVACIONES''', styleBH)
    dataTablaEncab=[]
    dataTablaObserv=[]
    dataTablaEncab.append([observacion])

    #   Contenido
    high = 280
    
    cadena=[Paragraph('''''', styleN)]
    dataTablaObserv.append(cadena)

    width, height = A4
    tablaEncab = Table(dataTablaEncab, colWidths=[19*cm, 9.5*cm])
    tablaEncab.setStyle(TableStyle([
        ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
        ('BOX', (0,0), (-1,1), 1, colors.black),]))


    tablaObserv = Table(dataTablaObserv, colWidths=[19*cm, 9.5*cm], rowHeights=(3*cm))
    tablaObserv.setStyle(TableStyle([
        ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
        ('BOX', (0,0), (-1,-1), 1, colors.black),]))
    #c.drawString(margenIzq, 490, 'Examen medico ocupacional básico.')
    
    tablaEncab.wrapOn(c,width, height)
    tablaEncab.drawOn(c, margenIzq-2, high+83)
    c.showPage

    tablaObserv.wrapOn(c,width, height)
    tablaObserv.drawOn(c, margenIzq-2, high)
    c.showPage

    #   Parte final - consideraciones
    high = 218
    consideracion=[Paragraph('''IMPORTANTE: 1) El trabajador recibió orientación medica sobre las recomendaciones necesarias para 
    prevenir posibles efectos en la salud relacionados o asociados con los riesgos ocupacionales propios en su cargo. 
     2) Señor(a) trabajador(a): a partir de la fecha, usted cuenta con 30 días para seguir y realizar las indicaciones del 
     medico especialista en salud ocupacional registradas en este documento.''', styleN)]
    dataTablaConsideracion=[]
    dataTablaConsideracion.append([consideracion])
    tablaConsideracion = Table(dataTablaConsideracion, colWidths=[19*cm, 9.5*cm], rowHeights=(2*cm))
    tablaConsideracion.setStyle(TableStyle([
        ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
        ('BOX', (1,1), (-1,-1), 1, colors.black),]))
    tablaConsideracion.wrapOn(c,width, height)
    tablaConsideracion.drawOn(c, margenIzq-2, high)
    c.showPage

    high = 188
    declaracion=[Paragraph('''DECLARACIÓN DEL ASPIRANTE: Manifiesto con mi firma o huella que no omití datos relevantes 
    en mis antecedentes que pudieran influir sobre la evaluación de mi estado actual de salud.''', styleN)]
    dataDeclaracion=[]
    dataDeclaracion.append([declaracion])
    tablaDeclaracion = Table(dataDeclaracion, colWidths=[19*cm, 9.5*cm], rowHeights=(1*cm))
    tablaDeclaracion.setStyle(TableStyle([
        ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
        ('BOX', (1,1), (-1,-1), 1, colors.black),]))
    tablaDeclaracion.wrapOn(c,width, height)
    tablaDeclaracion.drawOn(c, margenIzq-2, high)
    c.showPage

    high = 108
    resolucion=[Paragraph('''El contenido de la historia clínica, tiene carácter confidencial y su custodia está regulada 
    por la resolución 1918 del 5 de junio de 2009, del cual se transcribe a continuación algunos apartes. La custodia de la 
    evaluación medica y de la historia clínica ocupacional, está a cargo del prestador del servicio de salud ocupacional, que 
    le generó en el curso de la atención, cumpliendo los requisitos y procedimientos de archivo conforme a las normas legales 
    vigentes para la historia clínica. En ningún caso los empleadores podán tener, conservar o anexar copia de las evaluaciones 
    medicas ocupacionales y de la historia clínica ocupacional a la hoja del vida del trabajador.''', styleN)]
    dataResolucion=[]
    dataResolucion.append([resolucion])
    tablaResolucion = Table(dataResolucion, colWidths=[19*cm, 9.5*cm], rowHeights=(2.75*cm))
    tablaResolucion.setStyle(TableStyle([
        ('INNERGRID', (0,0), (-1,-1), 1, colors.black),
        ('BOX', (1,1), (-1,-1), 1, colors.black),]))
    tablaResolucion.wrapOn(c,width, height)
    tablaResolucion.drawOn(c, margenIzq-2, high)
    c.showPage


    c.line(margenIzq+60,50,margenIzq+230,50)
    c.line(margenIzq+300,50,margenIzq+470,50)
    c.drawString(margenIzq+62,40, 'Profesional')
    c.drawString(margenIzq+62,30, 'Lic. Ocupacional')
    c.drawString(margenIzq+302,40,paciente.primer_nombre+' '+paciente.segundo_nombre+' '
        +paciente.primer_apellido+' '+paciente.segundo_apellido)
    c.drawString(margenIzq+302,30, 'Identificación: ')
    c.drawString(margenIzq+362,30,paciente.cedula)


    c.setStrokeColor(black)
    c.setLineWidth(1)
    c.rect(margenIzq-2,540, 538,165, fill=0)

    
    c.save()
    pdf=buffer.getvalue();
    buffer.close()
    response.write(pdf)
    return response

