from __future__ import unicode_literals
import uuid
from django.db import models



class  Patient(models.Model):
    user_name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    user_id = models.UUIDField(primary_key=False,default=uuid.uuid1, editable=False)
    diases_name = models.CharField(max_length=60)
    symptoms = models.TextField(max_length=400)
    cell_phone = models.CharField(max_length=12)
    hospital_name = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    insuarance_number = models.CharField(max_length=250)
    gender = models.CharField(max_length=250)
    doctor = models.CharField(max_length=250)
    def __str__(self):
        return self.user_name+"-"+self.password


class Hospital(models.Model):
    hospital_name = models.CharField(max_length=20)
    patients =  models.TextField()
    doctors = models.TextField()
    stuff = models.TextField()

    def __str__(self):
        return self.hospital_name+"-"+self.patients

class Doctor(models.Model):
    username = models.CharField(max_length=250)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    cell_phone = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    hospital_name = models.CharField(max_length=250)
    patients = models.TextField(400)

    def __str__(self):
        return self.username+"-"+self.patients


class Apoitment(models.Model):
    date = models.DateTimeField()
    patients = models.CharField(max_length=250)
    doctor = models.CharField(max_length=250)
    reason = models.CharField(max_length=250)

    def __str__(self):
        return self.date+"-"+self.patients+"-"+self.doctor+"-"+self.reason

# Create your models here.
