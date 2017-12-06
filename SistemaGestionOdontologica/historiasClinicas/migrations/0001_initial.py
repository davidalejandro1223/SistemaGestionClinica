# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-02 03:26
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pacientes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Actualizacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_actualizacion', models.DateField(auto_now=True)),
                ('motivo_consulta', models.TextField()),
                ('tratamiento', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Cabecera',
            fields=[
                ('numero_historia', models.CharField(max_length=15, primary_key=True, serialize=False)),
                ('antecedentes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='historiasClinicas.Actualizacion')),
                ('paciente', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='pacientes.Paciente')),
            ],
        ),
    ]
