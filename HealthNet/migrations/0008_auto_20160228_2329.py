# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-28 23:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HealthNet', '0007_auto_20160224_2021'),
    ]

    operations = [
        migrations.AddField(
            model_name='patient',
            name='address',
            field=models.CharField(default='', max_length=250),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='patient',
            name='insuarance_number',
            field=models.CharField(default='Hello', max_length=250),
            preserve_default=False,
        ),
    ]
