# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-05-06 23:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HealthNet', '0030_hospital_nurses'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='patient',
            name='diases_name',
        ),
        migrations.AddField(
            model_name='patient',
            name='appointments',
            field=models.ManyToManyField(to='HealthNet.Apoitment'),
        ),
        migrations.AddField(
            model_name='patient',
            name='prescriptions',
            field=models.ManyToManyField(to='HealthNet.Prescription'),
        ),
    ]
