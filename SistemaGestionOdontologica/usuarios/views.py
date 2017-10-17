# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http.response import HttpResponse

def autenticar(request):
    if request.method == 'POST':
        usuario = request.POST.get('inputUsuario', None)
        contrasena = request.POST.get('inputContrasena', None)

        user = authenticate(username=usuario, password=contrasena)
        if user is not None:
            login(request, user)
            return HttpResponse('usuario logueado')
        else:
            return HttpResponse('usuario no existe')

    return render(request, 'login.html', {})

# Create your views here.
