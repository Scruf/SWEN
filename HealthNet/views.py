
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.template import loader
from .models import Patient,Hospital,Logs,Doctor,Apoitment
from django.contrib.auth import authenticate, login
import re
import uuid
from django.template.context import RequestContext
from django.core.mail import send_mail
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
            multiple_object_template = loader.get_template('HealthNet/error/short_username.html')
            context = {
                "username":username,
            }
            return HttpResponse(multiple_object_template.render(context,request))
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
            multiple_object_template = loader.get_template('HealthNet/error/firstlastname_error.html')
            context = {
                "first":first_name,
                "last":last_name,
            }
            return HttpResponse(multiple_object_template.render(context,request))
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
            multiple_object_template = loader.get_template('HealthNet/error/email_format_error.html')
            context = {
                "mail":email,
            }
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
            multiple_object_template = loader.get_template('HealthNet/error/hospital_error.html')
            context = {
                "hospital":hospital_name,
            }

            return HttpResponse(multiple_object_template.render(context,request))
        address = request.POST.get('address',None)
        if address is None or len(address)<5:
            multiple_object_template = loader.get_template('HealthNet/error/address_error.html')

            context = {
                "addr":address,
            }

            return HttpResponse(multiple_object_template.render(context,request))
        insuarance = request.POST.get('insuarance_number',None)
        if len(insuarance)<5:
            multiple_object_template = loader.get_template('HealthNet/error/insurance_error.html')
            context = {
                "insuarance":insuarance,
            }
            return HttpResponse(multiple_object_template.render(context,render))
        else:
            try:
                test_patient = Patient.objects.get(insuarance_number=insuarance)
            except Patient.DoesNotExist:
                print "Robert"
            except Patient.MultipleObjectsReturned:
                multiple_object_template = loader.get_template('HealthNet/error/insurance_error.html')
                insur = request.POST.get('insuarance_number',None)

                context = {
                    "insuarance":insur,
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

        logs = Logs(date=datetime.date.today(),action="Registering",who_did="%s"%username)
        logs.save()
        h = Hospital.objects.get(hospital_name=hospital_val)
        h.patients_list.add(p)
        h.save()
        logs1 = Logs(date=datetime.date.today(),who_did="%s saved a patient with a %s"%(hospital_name,username))
        logs1.save()
        return redirect('/HealthNet/%s'%username,None)

def load_profile(request,user_name):
    user = Patient.objects.get(user_name=user_name)
    profile_template = loader.get_template('HealthNet/profile.html')
    context={
        'Patient':user,
    }
    return HttpResponse(profile_template.render(context,request))


def patient_pool(request,hospital_name,doctor_user_name):
    hospital = Hospital.objects.get(hospital_name=hospital_name)
    patient_list = []
    patient_info = {}
    for patient in hospital.patients_list.all():
        if not patient.assigned_doctor:
            patient_info={
                          'patient_user_name':patient.user_name,
                          'patient_first_name':patient.first_name,
                          'patient_last_name':patient.last_name,

                          }
            patient_list.append(patient_info)
    _hospital_name=hospital_name[0]
    for h in hospital_name[1:]:
        if h.isupper():
            _hospital_name = hospital_name + " "+h
        else:
            _hospital_name = hospital_name + h
    context ={
        'Patient':patient_list,
        "Hospital":hospital_name,
        "Normailized_Hospital_Name":_hospital_name,
    }
    logs = Logs(date=datetime.date.today(),action="Browsing list of patients",who_did="%s"%doctor_user_name)
    logs.save()
    pool_template = loader.get_template('HealthNet/free_pool.html')
    return HttpResponse(pool_template.render(context,request))

def patien_to_save(request,hospital_name,user_name,doctor_user_name):
    patient = Patient.objects.get(user_name=user_name)
    patient.assigned_doctor = True
    patient.save()
    doctor = Doctor.objects.get(username=doctor_user_name)
    doctor.patients.add(patient)
    patient._doctor = doctor.username
    patient.save()
    doctor.save()
    logs = Logs(date=datetime.date.today(),action="Assigning Patient",who_did="%s"%doctor_user_name)
    logs.save()
    return redirect("/HealthNet/%s/%s/pool"%(hospital_name,user_name))
#smpt fail
def send_message(request,user_name):
    if request.method == 'POST':
        doctor_user_name = request.POST.get("doctor_email",None)
        message = request.POST.get('message',None)
        #doctor_user_name = Doctor.objects.get(username=doctor_user_name).email
        email_m = doctor_user_name
        if send_mail("You've got a message from %s"%user_name,message,"healthnettesting@gmail.com",['%s'%email_m],fail_silently=False)==1:
            redirect('/HealthNet/%s'%user_name)
        else:
            print "Error in sending email"
    return HttpResponse("Message Was Send")


def doctor_sign(request,hospital_name):
    doctor_sign_template = loader.get_template("HealthNet/doctors_sign.html")
    context = {
        "Doctor":"Sign",
    }
    return HttpResponse(doctor_sign_template.render(context,request))


def doctor_verify(request,hospital_name):
    if request.method == 'POST':
        email = request.POST.get('email',None)
        password = request.POST.get('password',None)
        try:
            doctor = Doctor.objects.get(email=email,password=password)
            return redirect("/HealthNet/%s/doctor/profile/"%doctor.username)
            # return HttpResponse("HealthNet/%s/doctor/profile"%doctor.username)
        except Doctor.DoesNotExist:
            return HttpResponse("Hello")
    # else:
    #     return redirect(REDIRECT_URL)

def doctor_profile(request,user_name):
    try:
        doctor = Doctor.objects.get(username=user_name)
        doctor_template = loader.get_template('HealthNet/doctors.html')
        patients = doctor.patients.all()
        appoitment_list = Apoitment.objects.filter(doctor=user_name)
        context ={
            "doctor":doctor,
            "appoitment_list":appoitment_list,
            "patient_list":patients,
        }
        return HttpResponse(doctor_template.render(context,request))
    except Doctor,DoesNotExist:
        return redirect(REDIRECT_URL)


def appoitment(request,user_name):
    appoitment_template = loader.get_template('HealthNet/appointment.html')
    context = {
        'username':user_name,
    }
    return HttpResponse(appoitment_template.render(context,request))

def confirm_appoitment(request,user_name):
    if request.method == 'POST':
        patient = Patient.objects.get(user_name=user_name)
        doctor = Doctor.objects.get(patients=patient)
        appoitment_date = request.POST.get("date",None)
        reason_to = request.POST.get("reason",None)
        apoitment = Apoitment(date=appoitment_date,patients=patient.user_name,\
                                doctor=doctor.username,reason=reason_to)
        apoitment.save()
        logs = Logs(date=datetime.date.today(),action="Requestiong Appoitment",who_did=patient.user_name)
        logs.save()
        return redirect("/HealthNet/%s"%user_name)
    else:
        return HttpResponse("WWTF")
