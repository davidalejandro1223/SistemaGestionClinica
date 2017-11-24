# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class cabecera(models.Model):
    numero_historia = models.CharField(primary_key=True, max_length=15)
