from __future__ import unicode_literals
import uuid
from django.db import models
from django.contrib.auth.models import User

#Patient is the model that holds all of a patient's information
class Administration(models.Model):
    user_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    email = models.CharField(max_length=255)

class Apoitment(models.Model):
    date = models.DateTimeField()
    name = models.CharField(max_length=250)
    reason = models.CharField(max_length=250)

    def __str__(self):
        return self.date+" "+self.name+" "+self.reason
#------------------------------------Logs----------------------------------
#@title = name of the drug to be given
#@details = the reason why this drug is being assigned_doctor
#@dosage = the amount of drug to be given
class Prescription(models.Model):
    title = models.CharField(max_length=250)
    details = models.CharField(max_length=250)
    dosage = models.CharField(max_length=250)

class Messages(models.Model):
    sender = models.CharField(max_length=250)
    receiver = models.CharField(max_length=250)
    text_body = models.CharField(max_length=500)
    time_stamp = models.CharField(max_length=250)

    def __str__(self):
        return self.sender+" "+self.receiver


class Comments(models.Model):
    user = models.ForeignKey(User)
    text = models.CharField(max_length=255)


class  Patient(models.Model):
    user_name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    user_id = models.UUIDField(primary_key=False,default=uuid.uuid1, editable=False)
    symptoms = models.TextField(max_length=400)
    cell_phone = models.CharField(max_length=12)
    hospital_name = models.CharField(max_length=250)
    address = models.CharField(max_length=250)
    insuarance_number = models.CharField(max_length=250)
    gender = models.CharField(max_length=250)
    _doctor = models.CharField(max_length=250)
    assigned_doctor = models.BooleanField(default=False)
    prescriptions = models.ManyToManyField(Prescription) # prescriptions
    appointments = models.ManyToManyField(Apoitment) #appointment lists

    def __str__(self):
        return self.user_name+"-"+self.password
#Doctor is a model where all doctors are
class Doctor(models.Model):
    username = models.CharField(max_length=250)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    cell_phone = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    hospital_name = models.CharField(max_length=250)
    patients = models.ManyToManyField(Patient)
    apoitment_list = models.ManyToManyField(Apoitment)

    def __str__(self):
        return self.username+"-"+self.patients

class Nurse(models.Model):
    username = models.CharField(max_length=250)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    cell_phone = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    hospital_name = models.CharField(max_length=250)
    patients = models.ManyToManyField(Patient)
    apoitment_list = models.ManyToManyField(Apoitment)

    def __str__(self):
        return self.username+"-"+self.patients

class Stuff(models.Model):
    hospital_name = models.CharField(max_length=250)
    username = models.CharField(max_length=250)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    cell_phone = models.CharField(max_length=250)
    password = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    hospital_name = models.CharField(max_length=250)
    patients_stuff_list = models.TextField(400)

    def __str__(self):
        return self.username+"-"+self.password
#Hospital is the class that holds all of the information about a hospital
class Hospital(models.Model):
    hospital_name = models.CharField(max_length=20)
    patients_list =  models.ManyToManyField(Patient)
    doctors = models.ManyToManyField(Doctor)
    stuff = models.ManyToManyField(Stuff)
    nurses = models.ManyToManyField(Nurse)


#Doctor is the class that holds all of the information about a doctor

#Apoitment is the class that holds all of the information about appointments
class Scheduler(models.Model):
    start_date = models.DateTimeField()
    # end_date = models.DateTimeField()
    title = models.CharField(max_length=250)
    doctor = models.CharField(max_length=250)
    patient = models.CharField(max_length=250)


class Logs(models.Model):
    date = models.DateTimeField()
    action = models.CharField(max_length=250)
    who_did = models.CharField(max_length=250)
    what_happened = models.CharField(max_length=250)
    def __str__(self):
        month = str(self.date.today().month)
        _date=str(self.date.today().date)
        year = str(self.date.today().year)
        _date_ = month+"/"+_date+"/"+year
        return _date_+" "+self.action+"-"+self.who_did+"-"+self.what_happened
# Create your models here.
