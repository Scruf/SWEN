# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-07 21:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HealthNet', '0013_hospital_doctors'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hospital',
            name='patients',
        ),
        migrations.AddField(
            model_name='hospital',
            name='patients',
            field=models.ManyToManyField(to='HealthNet.Patient'),
        ),
    ]
