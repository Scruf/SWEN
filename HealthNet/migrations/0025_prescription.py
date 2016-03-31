# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-31 22:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HealthNet', '0024_remove_scheduler_end_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prescription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('details', models.CharField(max_length=250)),
                ('dosage', models.CharField(max_length=250)),
            ],
        ),
    ]
