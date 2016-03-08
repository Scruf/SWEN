
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.template import loader
from .models import Patient,Hospital,Logs
from django.contrib.auth import authenticate, login
import re
import uuid
import datetime


# Create your views here.
REDIRECT_URL="http://dogr.io/wow/suchservice/muchtextsplitting/verydirectcompose.png"
#Its is not index  I just created this controller to test sign in
def index(request):
    users = Patient.objects.all()
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
            user_name = Patient.objects.get(email=email,password=password).user_name
            log = Logs(date=datetime.date.today(),action="Sign In",who_did=user_name,what_happened="Log In the System")
            log.save()
            user_context = {
                'user_name':user_name,
            }
            success_template = loader.get_template('HealthNet/profile.html')
            return redirect('/HealthNet/%s'%user_name,None)
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
        username = request.POST.get('username',None)
        if len(username)<4:
            return HttpResponse("Length of the Username should be grater than 5")
        else:
            try:
                test_patient = Patient.objects.get(user_name=username)
            except Patient.DoesNotExist:
                print "Robert"
            except Patient.MultipleObjectsReturned:
                multiple_object_template = loader.get_template('HealthNet/error/username_error.html')
                username = request.POST.get('username',None)
                context = {
                    "user_name":username,
                }
                return HttpResponse(multiple_object_template.render(context,request))

        password = request.POST.get('password',None)
        first_name = request.POST.get('first_name',None)
        last_name = request.POST.get('last_name',None)
        if first_name==last_name or len(first_name)<2 or len(last_name)<2:
            return HttpResponse("First or Last name of invalid length")
        else:
            try:
                test_patient = Patient.objects.get(first_name=first_name,last_name=last_name)
            except Patient.DoesNotExist:
                print "Robert"
            except Patient.MultipleObjectsReturned:
                 multiple_object_template = loader.get_template('HealthNet/error/firstlastname_error.html')
                 first_name = request.POST.get('first_name',None)
                 last_name = request.POST.get('last_name',None)
                 context = {
                    "first_name":first_name,
                    "last_name":last_name,
                 }
                 return HttpResponse(multiple_object_template.render(context,request))

        email = request.POST.get('email',None)
        if not re.match(r'(\w+[.|\w])*@(\w+[.])*\w+', str(email)):
            return HttpResponse("Email format is invalid")
        else:
            try:
                test_patient = Patient.objects.get(email=email)
            except Patient.DoesNotExist:
                print "Robert"
            except Patient.MultipleObjectsReturned:
                multiple_object_template = loader.get_template('HealthNet/error/email_error.html')
                email = request.POST.get('first_name',None)

                context = {
                    "email":email,
                }

                return HttpResponse(multiple_object_template.render(context,request))

        cell_phone = request.POST.get('cell_phone',None)
        if len(str(cell_phone.split("+")))<1 and str(cell_phone)[0] is not '1':
            cell_phone = '1'+cell_phone
            try:
                 float(str(cell_phone.split("+")[1]))
            except ValueError:
                 return HttpResponse("Cell phone number of Invalid format")
        elif cell_phone[0] is '1':
            cell_phone = '+'+cell_phone
            try:
                float(str(cell_phone.split("+")[1]))
            except ValueError:
                return redirect(REDIRECT_URL)
        else:
            try:
                cell_phone = request.POST.get('cell_phone',None)
            except Patient.DoesNotExist:
                print "Robert"
            except Patient.MultipleObjectsReturned:
                multiple_object_template = loader.get_template('HealthNet/error/phone_error.html')
                phone = request.POST.get('cell_phone',None)

                context = {
                    "cell_phone":phone,
                }


                return HttpResponse(multiple_object_template.render(context,request))

        hospital_name = request.POST.get('hospital',None)
        if len(hospital_name)<2:
            return HttpResponse("Hospital field was left empty")
        address = request.POST.get('address',None)
        if address is None or len(address)<5:
            return HttpResponse("Address field was left empty")
        insuarance = request.POST.get('insuarance_number',None)
        if len(insuarance)<5:
             return HttpResponse("insuarance number is invalid")
        else:
            try:
                test_patient = Patient.objects.get(insuarance_number=insuarance)
            except Patient.DoesNotExist:
                print "Robert"
            except Patient.MultipleObjectsReturned:
                multiple_object_template = loader.get_template('HealthNet/error/insurance_error.html')
                insur = request.POST.get('insuarance_number',None)

                context = {
                    "insuarance":insur
                }

                return HttpResponse(multiple_object_template.render(context,request))

        hospital_val = request.POST.get("hospital",None)
        symptoms = ' '
        p = Patient(user_name=username,password=password,first_name=first_name,last_name=last_name,email=email,user_id=uuid.uuid1(),\
                     diases_name=" ",symptoms=symptoms,cell_phone=cell_phone,hospital_name=hospital_val,\
                      address = address,insuarance_number=insuarance)
        p.save()
        log = Logs(date=datetime.date.today(),action="Register",who_did=username,what_happened="Signing up to the system")
        log.save()
        user_profile = loader.get_template('/HealthNet/profile.html')
        h = Hospital.objects.get(hospital_name=hospital_val)
        return redirect('/HealthNet/%s'%username,None)

def load_profile(request,user_name):
    user = Patient.objects.get(user_name=user_name)
    return HttpResponse("Hello %s profiles"%user_name)
