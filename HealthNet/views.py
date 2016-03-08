
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.template import loader
from .models import Patient,Hospital
from django.contrib.auth import authenticate, login
import re
import uuid


# Create your views here.

#Its is not index  I just created this controller to test sign in
def index(request):
    users = Patient.objects.all()
    template = loader.get_template('HealthNet/index.html')
    hospital_list = []
    context = {
        'users':users,
    }
    return HttpResponse(template.render(context,request))

#Request will be submited to this controller whoch will generate the message
#on fail it will gennerate fail message
#on succes it will generate succes
def sign_in(request):

    sign_in_template = loader.get_template('HealthNet/signin.html')
    return HttpResponse(sign_in_template.render(None,request))


#thank you controller will check if the user is valid
#In future it will alsoe validate if the login person is a doctor or a Patient
def thankyou(request):
    if request.method=='POST':
        email = request.POST.get('email',None)
        password = request.POST.get('password',None)
        try:
            t = Patient.objects.get(email=email,password=password)
            context ={
                'user_name':email,
            }
            success_template = loader.get_template('HealthNet/success.html')
            return HttpResponse(success_template.render(context,request))
        except Patient.DoesNotExist:
            return HttpResponse("Patient with this credentials does not exists")

#signup prompts the user to sign up with their name and contact information and to provide
#a unique username and password for their account
def signup(request):
    sign_up_template = loader.get_template('HealthNet/signup.html')
    hospital = Hospital.objects.all()
    context = {
        "hospitals":hospital,
    }
    return HttpResponse(sign_up_template.render(context,request))

#register takes in the user's information given in signup and creates a new user
#with the information provided
def register(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username',None)
            if len(username)<4:
                return HttpResponse("Length of the Username should be grater than 5")
            try:
                test_patient = Patient.objects.get(user_name=username)
            except Patient.DoesNotExist:
                print ("Good")
        except Patient.MultipleObjectsReturned:
            return HttpResponse("Patient with the %s exists"%username)
        password = request.POST.get('password',None)
        try:
            first_name = request.POST.get('first_name',None)
            last_name = request.POST.get('last_name',None)
            if first_name==last_name or len(first_name)<2 or len(last_name)<2:
                return HttpResponse("First or Last name of invalid length")
            try:
                test_patient = Patient.objects.get(first_name=first_name,last_name=last_name)
            except Patient.DoesNotExist:
                 print ("Good")
        except Patient.MultipleObjectsReturned:
            return HttpResponse("Patient with this %s and %s is already registered"%(first_name,last_name))
        try:
            email = request.POST.get('email',None)
            if not re.match(r'(\w+[.|\w])*@(\w+[.])*\w+', str(email)):
                return HttpResponse("Email format is invalid")
            try:
                test_patient = Patient.objects.get(email=email)
            except Patient.DoesNotExist:
                print ("Good")
        except Patient.MultipleObjectsReturned:
            return HttpResponse("User with thisn %s address is already in the system"%email)
        try:
            cell_phone = request.POST.get('cell_phone',None)
            try:
                float(str(cell_phone.split("+")[1]))
            except ValueError:
                return HttpResponse("Cell phone number of Invalid format")
            try:
                test_patient = Patient.objects.get(cell_phone=cell_phone)
            except Patient.DoesNotExist:
                print ("Good")
        except Patient.MultipleObjectsReturned:
            return HttpResponse("User with this cellphone %s number is registered in the system"%cell_phone)
        symptoms = request.POST.get('symptoms',None)
        hospital_name = request.POST.get('hospital',None)
        if len(hospital_name)<2 or hospital_name is None:
            return HttpResponse("Hospital field was left empty")
        address = request.POST.get('address',None)
        if address is None or len(address)<5:
            return HttpResponse("Address field was left empty")
        try:
            insuarance = request.POST.get('insuarance_number',None)
            if len(insuarance)<5:
                return HttpResponse("insuarance number is invalid")
            try:
                test_patient = Patient.objects.get(insuarance_number=insuarance)
            except Patient.DoesNotExist:
                 print ("Good")
        except Patient.MultipleObjectsReturned:
            return HttpResponse("User with this insuarance number %s is already registered in the system"%insuarance_number)
        hospital_val = request.POST.get("hospital",None)
        p = Patient(user_name=username,password=password,first_name=first_name,last_name=last_name,email=email,user_id=uuid.uuid1(),\
                    diases_name=" ",symptoms=symptoms,cell_phone=cell_phone,hospital_name=hospital_val,\
                    address = address,insuarance_number=insuarance)
        p.save()

        return redirect('/HealthNet/',None)
