
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseServerError,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from django.contrib.auth.decorators import login_required
from django.template import loader
from .models import Patient,Hospital,Logs,Doctor,Apoitment,Scheduler,Administration
from django.contrib.auth import authenticate, login
import re
import uuid
from django.template.context import RequestContext
from django.core.mail import send_mail
import datetime
import redis
import json
from django.contrib import messages
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect


# Create your views here.
REDIRECT_URL="http://dogr.io/wow/suchservice/muchtextsplitting/verydirectcompose.png"
#Its not a full implementation of a fullcalendar
#I am just using it for testing (savages)
def message(request,sender_name):
    message_template = loader.get_template('HealthNet/messages.html')
    context = {
        'message':'context',
        'sender':sender_name
    }
    return HttpResponse(message_template.render(context,request))
def administration(request):
    template = loader.get_template('HealthNet/administration_sign.html')
    context ={
        "Some":"Wodo",
    }
    return HttpResponse(template.render(context,request))

def admin_verify(request):
    if request.method == 'POST':
        email = request.POST.get('email',None)
        password = request.POST.get('password',None)
        try:
            admin = Administration.objects.get(email=email,password=password)
            context = {
                "admin":admin,
            }
            admin_user_name = admin.user_name
            admin_template = loader.get_template('HealthNet/admin.html')
            return redirect('/HealthNet/administration/%s'%admin_user_name)
        except Administration.DoesNotExist:
            return HttpResponse("Invalid Credentails")


def admin_profile(request,admin_name):

        context = {
            'admin':admin_name,
        }
        admin_profile_template = loader.get_template('HealthNet/admin.html')
        return HttpResponse(admin_profile_template.render(context,request))


def admin_create(request,admin_name):
    admin_create_temlate = loader.get_template('HealthNet/admins/admin_create.html')
    context = {
        'create':'Doctors'
    }
    return HttpResponse(admin_create_temlate.render(context,request))
#@controller admin  will create and verify  doctor profile
#in future this controller should create a username by itslf without
#requring admin entering it manually
def admin_create_verify(request,admin_name):
    if request.method == 'POST':
        user_name = request.POST.get('user_name',None)
        if len(user_name)<3:
            messages.add_message(request, messages.ERROR, 'Username too short')
            return redirect( '/HealthNet/administration/' + admin_name + '/create/',permanent=True)
        try:
            patient = Patient.objects.get(user_name=user_name)
        except Patient.MultipleObjectsReturned:
            print ("This %s is already taken "%user_name)
            messages.add_message(request, messages.ERROR, 'Username is already taken: %s'%user_name)
            return redirect( '/HealthNet/administration/' + admin_name + '/create/',permanent=True)
        except Patient.DoesNotExist:
            print("Ben Affleck was okay Batman")
        try:
            print("%s"%user_name)
            print Doctor.objects.get(username=user_name).password
            doctor = Doctor.objects.get(username=user_name)
        except Doctor.MultipleObjectsReturned:
            print ("%s with this username already exists"%user_name)
            messages.add_message(request, messages.ERROR, 'Username is already taken: %s'%user_name)
            return redirect( '/HealthNet/administration/' + admin_name + '/create/',permanent=True)
        except Doctor.DoesNotExist:
            print ("Join the darkside")
        first_name = request.POST.get('first_name',None)
        last_name = request.POST.get('last_name',None)
        if len(first_name)<2 or len(last_name)<2:
            messages.add_message(request, messages.ERROR, 'Name too short')
            return redirect( '/HealthNet/administration/' + admin_name + '/create/',permanent=True)
        if first_name==user_name or last_name==user_name or (first_name + last_name)==user_name:
            messages.add_message(request, messages.ERROR, 'First or Last name cant be the username')
            return redirect( '/HealthNet/administration/' + admin_name + '/create/',permanent=True)
        if first_name==last_name:
            print("First name cannot be equals last name")
            messages.add_message(request, messages.ERROR, 'First and last name are equal')
            return redirect( '/HealthNet/administration/' + admin_name + '/create/',permanent=True)
        else:
            try:
                doctor = Doctor.objects.get(first_name=first_name,last_name=last_name)
            except Doctor.MultipleObjectsReturned:
                print ("Doctor with this first name: %s and this last name: %s already exists"%(first_name,last_name))
                messages.add_message(request, messages.ERROR, 'First and last names are in the system already')
                return redirect( '/HealthNet/administration/' + admin_name + '/create/',permanent=True)
            except Doctor.DoesNotExist:
                print ("Jointhe darkside")
        email = request.POST.get('email',None)
        if not re.match(r'(\w+[.|\w])*@(\w+[.])*\w+', str(email)):
            messages.add_message(request, messages.ERROR, 'Invalid email')
            return redirect( '/HealthNet/administration/' + admin_name + '/create/',permanent=True)
        try:
            patient = Patient.objects.get(email=email)
        except Patient.MultipleObjectsReturned:
            print("Patient with this email exists")
            messages.add_message(request, messages.ERROR, 'Email is already in use')
            return redirect( '/HealthNet/administration/' + admin_name + '/create/',permanent=True)
        except Patient.DoesNotExist:
            print "Hooray to Satan"
        try:
            doctor = Doctor.objects.get(email=email)
        except Doctor.MultipleObjectsReturned:
            print "Doctor with this email already exists"
            messages.add_message(request, messages.ERROR, 'Email is already in use')
            return redirect( '/HealthNet/administration/' + admin_name + '/create/',permanent=True)
        except Doctor.DoesNotExist:
            print "Join the darkside"
        hospital = request.POST.get('hospital',None)
        password = str(uuid.uuid1()).split("-")[0]
        doctor = Doctor(username=user_name,email=email,first_name=first_name,last_name=last_name,password=password,hospital_name=hospital)
        doctor.save()
        log = Logs(date=datetime.date.today(),action="New Doctor created",who_did="admin",what_happened="Doctor creation")

        log.save()
        return redirect('/HealthNet/administration/%s'%admin_name)
#admin stuff goes on top
#whoever put not admin stuff in admin stuff will die horible and painful death
# def administration_save(request):
#     if request.method == 'POST':
#         username = request.POST.get('username',None)
#         password = request.POST.get('password',None)
#         email = request.POST.get('email',None)
#         admin = Administration(user_name=username,password=password,email=email)
#         admin.save()
#         return HttpResponse("Savage %s Saved"%username)
#     else:
#         return HttpResponse("Not Saved")
def admin_logs(request,admin_name):
    admin_logs_template = loader.get_template('HealthNet/admin_logs.html')
    log = Logs.objects.all();
    context = {
        'logs':log
    }
    return HttpResponse(admin_logs_template.render(context,request))
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
            doctor = Doctor.objects.get(email=email,password=password)
            return redirect('/HealthNet/doctor/%s'%doctor.username)
        except Doctor.DoesNotExist:
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
        if len(username)<5:
            print "Eroor"
            messages.add_message(request, messages.ERROR, '%s too short'%username)
            return redirect( '/HealthNet/signup/',permanent=True)
        else:
            try:
                test_patient = Patient.objects.get(user_name=username)
            except Patient.DoesNotExist:
                print "Robert"
            except Patient.MultipleObjectsReturned:
                messages.add_message(request, messages.ERROR, 'This username: %s already exists'%username)
                return redirect( '/HealthNet/signup/',permanent=True)
        password = request.POST.get('password',None)
        first_name = request.POST.get('first_name',None)
        last_name = request.POST.get('last_name',None)
        if first_name==last_name or len(first_name)<2 or len(last_name)<2:
            messages.add_message(request, messages.ERROR, 'These these first names and last names are too short')
            return redirect( '/HealthNet/signup/',permanent=True)
        else:
            try:
                test_patient = Patient.objects.get(first_name=first_name,last_name=last_name)
            except Patient.DoesNotExist:
                print "Robert"
            except Patient.MultipleObjectsReturned:
                fullname = first_name + " " + last_name,
                messages.add_message(request, messages.ERROR, 'First and last name already in the system: %s'%fullname)
                return redirect( '/HealthNet/signup/',permanent=True)
        email = request.POST.get('email',None)
        if not re.match(r'(\w+[.|\w])*@(\w+[.])*\w+', str(email)):
            messages.add_message(request, messages.ERROR, 'Invalid Email format')
            return redirect( '/HealthNet/signup/',permanent=True)
        else:
            try:
                test_patient = Patient.objects.get(email=email)
            except Patient.DoesNotExist:
                print "Robert"
            except Patient.MultipleObjectsReturned:
                messages.add_message(request, messages.ERROR, 'Email is already in use: %s'%email)
                return redirect( '/HealthNet/signup/',permanent=True)
        cell_phone = request.POST.get('cell_phone',None)
        if len(str(cell_phone.split("+")))<1 and str(cell_phone)[0] is not '1':
            cell_phone = '1'+cell_phone
            try:
                 float(str(cell_phone.split("+")[1]))
            except ValueError:
                 messages.add_message(request, messages.ERROR, 'Phone Number is invalid')
                 return redirect( '/HealthNet/signup/',permanent=True)
        elif cell_phone:
            if cell_phone[0] is '1':
                cell_phone = '+'+cell_phone
                try:
                    float(str(cell_phone.split("+")[1]))
                except ValueError:
                    messages.add_message(request, messages.ERROR, 'Phone Number is invalid')
                    return redirect( '/HealthNet/signup/',permanent=True)
            else:
                try:
                    cell_phone = request.POST.get('cell_phone',None)
                except Patient.DoesNotExist:
                    print "Robert"
                except Patient.MultipleObjectsReturned:
                    messages.add_message(request, messages.ERROR, 'Phone Number is ialready in use: %s'%cell_phone)
                    return redirect( '/HealthNet/signup/',permanent=True)
        else:
            messages.add_message(request, messages.ERROR, 'Phone Number is invalid')
            return redirect( '/HealthNet/signup/',permanent=True)
        hospital_name = request.POST.get('hospital',None)
        if not hospital_name  or len(hospital_name)<2:
            messages.add_message(request, messages.ERROR, 'Hospital Name too short')
            return redirect( '/HealthNet/signup/',permanent=True)
        address = request.POST.get('address',None)
        if address is None or len(address)<5:
            messages.add_message(request, messages.ERROR, 'Address too short')
            return redirect( '/HealthNet/signup/',permanent=True)
        insuarance = request.POST.get('insuarance_number',None)
        if len(insuarance)<5:
            messages.add_message(request, messages.ERROR, 'Insurance Number is too short')
            return redirect( '/HealthNet/signup/',permanent=True)
        else:
            try:
                test_patient = Patient.objects.get(insuarance_number=insuarance)
            except Patient.DoesNotExist:
                print "Robert"
            except Patient.MultipleObjectsReturned:
                messages.add_message(request, messages.ERROR, 'Insurance Number is already in use: %s'%insuarance)
                return redirect( '/HealthNet/signup/',permanent=True)
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
#

def profile_edit(request,user_name):
    try:
        patient = Patient.objects.get(user_name=user_name)
        template = loader.get_template('HealthNet/profile_details.html')
        context ={
            'patient':patient,
        }
        return HttpResponse(template.render(context,request))
    except Patient.DoesNotExist:
        return HttpResponse("Error")

def save_profile(request,user_name):
    if request.method=='POST':
        try:
            user = Patient.objects.get(user_name=user_name)
            user_name = request.POST.get("user_name",None)
            first_name = request.POST.get("first_name",None)
            last_name = request.POST.get("last_name",None)
            email = request.POST.get("email",None)
            cell_phone = request.POST.get("cell_phone",None)
            address = request.POST.get("address",None)
            insuarance_number = request.POST.get("insuarance",None)
            user.user_name=user_name
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.cell_phone = cell_phone
            user.address = address
            user.insuarance_number = insuarance_number
            user.save()
            logs1 = Logs(date=datetime.date.today(),who_did="%s edited profile "%user_name)
            logs1.save()
            return redirect('/HealthNet/%s'%user_name,None)
        except Patient.DoesNotExist:
            return HttpResponse("Could not save the user")





def patient_pool(request,hospital_name,doctor_user_name):
    temp_hospital_name= hospital_name
    hospital_name =' '.join(filter(None,re.split("([A-Z][^A-Z]*)",hospital_name)))
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


    context ={
        'Patient':patient_list,
        "Hospital":hospital_name,
        'hospital_name':temp_hospital_name,
        "doctor":doctor_user_name
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


def doctor_sign(request):
    doctor_sign_template = loader.get_template("HealthNet/doctors_sign.html")
    context = {
        "Doctor":"Sign",
    }
    return HttpResponse(doctor_sign_template.render(context,request))


def doctor_verify(request):
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

def doctor_profile(request,doctor_user_name):
    doctor_template = loader.get_template('HealthNet/doctors.html')
    doctor = Doctor.objects.get(username=doctor_user_name)
    hospital_name = ''.join(doctor.hospital_name.split(" "))
    context = {
        'doctor':doctor,
        'hospital_name':hospital_name
    }


    return HttpResponse(doctor_template.render(context,request))
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
        month = appoitment_date.split("/")[0]
        day = appoitment_date.split("/")[1]
        year = appoitment_date.split("/")[2]
        full_date = year+"-"+month+"-"+day
        reason_to = request.POST.get("reason",None)
        apoitment = Scheduler(start_date=full_date,patient=patient.user_name,\
                                doctor=doctor.username,title=reason_to)
        apoitment.save()
        logs = Logs(date=datetime.date.today(),action="Requestiong Appoitment",who_did=patient.user_name)
        logs.save()
        return redirect("/HealthNet/%s"%user_name)
    else:
        return HttpResponse("WWTF")


def edit_apoitment(request,user_name):
    try:
        apoitment_details = Scheduler.objects.get(patient=user_name)
    except Scheduler.DoesNotExist:
        calendar_template = loader.get_template('HealthNet/calendar.html')
        context = {
            "No Dteails":"Were Found"
        }
        return HttpResponse(calendar_template.render(context,request))
    calendar_template = loader.get_template('HealthNet/calendar.html')
    title=apoitment_details.title
    start=apoitment_details.start_date
    start_date=str(start.month)+"/"+str(start.day)+"/"+str(start.year)
    date_url = ''.join(start_date.split("/"))

    # end=apoitment_details.end_date
    data = {
        'title':title,
        'start':start_date,
        'url':'details/%s/%s'%(title,date_url),
        # 'end':end,
    }

    return render(request,'HealthNet/calendar.html',{'apointements':json.dumps(data)})

def view_appoitment(request,title,date_url):
    return HttpResponse("%s__%s__%s"%(user_name,title,date_url))


def edit_apoitment_(request,user_name,apoitment_id):
    appoitment_edit_template = loader.get_template("HealthNet/appoitment_edit_.html")
    appoitment_list = Apoitment.objects.filter(patients=user_name)
    context={
        "user_name":user_name,
        "Appoitment_prop":appoitment_list,
    }
    return HttpResponse(appoitment_edit_template.render(context,request))


def apoitment_save(request,apoitment_id):
    if request.method == 'POST':
        apoitment = Apoitment.objects.get(pk=apoitment_id)
        return HttpResponse("Something")
    # if request.method == 'POST':
    #     reason = request.POST.get("reason",None)
    #     return HttpResponse("%s"%reason)
    # else:
    #     return redirect(REDIRECT_URL)

def save(request):
    return HttpResponse("Saved")
#doctor edit will load the template with doctors details to be edited
def doctor_edit_profile(request,doctor_user_name):
    doctor_edit_template = loader.get_template('HealthNet/doctor_edit.html')
    try:
        doctor = Doctor.objects.get(username=doctor_user_name)
        context = {
            'doctor':doctor
        }
        return HttpResponse(doctor_edit_template.render(context,request))
    except Doctor.DoesNotExist:
        return HttpResponse("Doctor Does Not exists");

#doctor edit will validate and save doctor profile to database
def doctor_edit_profile_save(request,doctor_user_name):
    if request.method == 'POST':
        user_name = request.POST.get('user_name',None)
        first_name = request.POST.get('first_name',None)
        last_name = request.POST.get('last_name',None)
        email = request.POST.get('email',None)
        cell_phone = request.POST.get('cell_phone',None)
        password = request.POST.get('password',None)
        try:
            doctor = Doctor.objects.get(username=doctor_user_name)
            doctor.username = user_name
            doctor.first_name = first_name
            doctor.last_name = last_name
            doctor.email = email
            doctor.cell_phone=cell_phone
            doctor.password = password
            doctor.save()
            return redirect('/HealthNet/doctor/%s'%doctor.username)
        except Doctor.DoesNotExist:
            return HttpResponse("Could not find doctor")

#doctor apoitment will view all apoitments
#also doctor will have ability to views the details about apoitment
def doctor_apoitments_view(request,doctor_user_name):
    try:
        doctor = Doctor.objects.get(username=doctor_user_name)
        context = {
            'doctor':doctor
        }
        doctor_apoitment_template = loader.get_template('HealthNet/doctor_apoitment.html')
        return HttpResponse(doctor_apoitment_template.render(context,request))
    except Doctor.DoesNotExist:
        return HttpResponse("Viewing doctor apoitment")
#doctor_patient_pool will render a patient pool template
def patient_pool_view(request,hospital_name,doctor_user_name,patient_uesr_name):
    patient = Patient.objects.get(user_name=patient_uesr_name)
    context = {
        'patient':patient
    }
    patient_template = loader.get_template('HealthNet/patient_view.html')
    return HttpResponse(patient_template.render(context,request))
