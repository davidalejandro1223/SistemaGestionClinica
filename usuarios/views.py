# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, loader
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http.response import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

def autenticar(request):
    if request.method == 'POST':
        usuario = request.POST.get('inputUsuario', None)
        contrasena = request.POST.get('inputContrasena', None)

        user = authenticate(username=usuario, password=contrasena)
        if user is not None:
            login(request, user)
            return redirect('usuarios:inicio')
        else:
            return HttpResponse('usuario no existe')

    return render(request, 'login.html', {})

def desautenticar(request):
    logout(request)
    return redirect('usuarios:autenticar')

@login_required(login_url = '/')
def inicio(request):
    template = loader.get_template('inicio.html')
    context = {
        'active_inicio' : 'active',
    }
    return HttpResponse(template.render(context, request))
