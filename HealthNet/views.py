
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.template import loader
from .models import Patient,Hospital
from django.contrib.auth import authenticate, login
import random
import uuid
import json

# Create your views here.

#Its is not index  I just created this controller to test sign in
def index(request):
    users = Patient.objects.all()

    hospitals = Hospital.objects.all()
    hospital_list = []
    for h in hospitals:
        hospital_list.append(h.hospital_name)

    for patient in users:
        random_hospital = random.randint(0,len(hospital_list)-1)
        if patient.hospital_name not in hospital_list:
            patient = Patient(user_name = patient.user_name, \
                              password = patient.password, \
                              first_name = patient.first_name, \
                              last_name = patient.last_name, \
                              email = patient.email, \
                              user_id = patient.user_id, \
                              diases_name = patient.diases_name, \
                              symptoms = patient.symptoms, \
                              cell_phone = patient.cell_phone, \
                              hospital_name = hospital_list[random_hospital])
            patient.save()

    template = loader.get_template('HealthNet/index.html')
    context = {
        'users':users,
    }
    return HttpResponse(template.render(context,request))

#Request will be submited to this controller whoch will generate the message
#on fail it will gennerate fail message
#on succes it will generate succes
def sign_in(request):

    sign_in_template = loader.get_template('HealthNet/signin.html')
    users = Patient.objects.all()
    context={
        'users':users,
    }
    return HttpResponse(sign_in_template.render(context,request))


#thank you controller will check if the user is valid
#In future it will alsoe validate if the login person is a doctor or a Patient
def thankyou(request):
    if request.method=='POST':
        user_name = request.POST.get('username',None)
        password = request.POST.get('password',None)
        hospital_data = []
        try:
            t = Patient.objects.get(user_name=user_name,password=password)
            context ={
                'user_name':user_name,
            }
            success_template = loader.get_template('HealthNet/success.html')
            return HttpResponse(success_template.render(context,request))
        except Patient.DoesNotExist:
            context = {
                'user_name':user_name,
            }
            failure_template = loader.get_template('HealthNet/failure.html')
            return HttpResponse(failure_template.render(context,request))

def signup(request):
    sign_up_template = loader.get_template('HealthNet/SignUp/signup.html')
    hospital = Hospital.objects.all()
    context = {
        "hospitals":hospital,
    }
    return HttpResponse(sign_up_template.render(context,request))

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username',None)
        password = request.POST.get('password',None)
        first_name = request.POST.get('first_name',None)
        last_name = request.POST.get('last_name',None)
        email = request.POST.get('email',None)
        cell_phone = request.POST.get('cell_phone',None)
        symptoms = request.POST.get('symptoms',None)
        hospital_name = request.POST.get('hospital',None)
        p = Patient(user_name=username,password=password,first_name=first_name,last_name=last_name,email=email,user_id=uuid.uuid1(),diases_name=" ",symptoms=symptoms,cell_phone=cell_phone,hospital_name=hospital_name)
        p.save()
        return redirect('/HealthNet/',None)
