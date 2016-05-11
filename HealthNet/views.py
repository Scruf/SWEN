from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,HttpResponseServerError,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sessions.models import Session
from django.template import loader
from .models import Patient,Hospital,Logs,Doctor,Apoitment,Scheduler,Administration,Nurse,Prescription
import re
import uuid
from django.template.context import RequestContext
from django.core.mail import send_mail
import datetime
import json
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.utils import timezone

# Create your views here.
REDIRECT_URL="http://dogr.io/wow/suchservice/muchtextsplitting/verydirectcompose.png"
#begining of apis this method is for practice use only


def patient(request):
    patient = Patient.objects.all()
    patient_list = []
    for p in patient:
        data={
            'user_name':p.user_name,
            'first_name':p.first_name,
            'last_name':p.last_name
        }
        patient_list.append(data)
    if 'callback' in request.GET:
        data ='%s(%s)'%(request.GET['callback'],json.dumps(patient_list))
        return HttpResponse(data,'text/javascript')
    else:
        return render(request,'HealthNet/calendar.html',{'apointements':json.dumps(data)})
def doctor_names(request,doctor_name):
    try:
        doctor = Doctor.objects.get(username=doctor_name)
        print doctor.hospital_name
        hospital = Hospital.objects.get(hospital_name=doctor.hospital_name)
        doctor_list = []
        for hosp in hospital.doctors.all():
            name = hosp.first_name+" "+hosp.last_name
            names = {
                'name':name,
                'username':hosp.username
            }
            doctor_list.append(names)
        if request.is_ajax():
            data = json.dumps(doctor_list)
            return HttpResponse(data,'application/json')
    except Doctor.DoesNotExist:
        print("Some basd stuff")

#date must be submittied in a form YYYYMMDD
def check_fo_time(request,doctor_name,apoitment_date):
    try:
        doctor = Doctor.objects.get(username=doctor_name)
        doctor_apoitments = doctor.apoitment_list.all()
        year = int(apoitment_date[0:4])
        month = int(apoitment_date[4:6])
        day = int(apoitment_date[6:8])
        full_date = str(year)+"/"+str(month)+"/"+str(day)
        available_time_list = doctor.apoitment_list.all()

        current_date = datetime.datetime.now()
        date_to_compare = datetime.datetime(year,month,day)

        if year < current_date.year:
            error = {
                'error':True,
                'message':"You cannot schedule in the past"
            }
            if 'callback' in request.GET:
                data = '%s(%s)'%(request.GET['callback'],json.dumps(error))
                return HttpResponse(data,'text/javascript')
        if month <current_date.month:
            error = {
                'error':True,
                'message':"You cannot schedule apoitment in the past"
            }
            if 'callback' in request.GET:
                data ='%s(%s)'%(request.GET['callback'],json.dumps(error))
                return HttpResponse(data,'text/javascript')
        if month < current_date.month:
            error = {
                'error':True,
                'message':'You cannot schedule apoitment in the past'
            }
            if 'callback' in request.GET:
                data = '%s(%s)'%(request.GET['callback'],json.dumps(error))
                return HttpResponse (data,'text/javascript')
        apoitment_list = []
        for ap in doctor.apoitment_list.all():
            apoitment_list.append(ap)
        if date_to_compare in apoitment_list:
            error = {
                'error':True,
                'message':"Cannot schedule apoitment at this day"

            }
            if 'callback' in request.GET:
                data = '%s(%s)'%(request.GET['callback'], json.dumps(error))
                return HttpResponse(data,'text/javascript')
        if date_to_compare not in apoitment_list and date_to_compare>=current_date:
            date = {
                'error':False,
                'message':"Doctor is free at this day"
            }
            if 'callback' in request.GET:
                data ='%s(%s)'%(request.GET['callback'],json.dumps(date))
                return HttpResponse(data,'text/javascript')

    except Doctor.DoesNotExist:
        return HttpResponse("WOO")




def message(request,sender_name):
    message_template = loader.get_template('HealthNet/messages.html')
    context = {
        'message':'context',
        'sender':sender_name
    }
    return HttpResponse(message_template.render(context,request))
def apoitment_submit(request):
    if request.POST:
        patient_user_name = request.POST['patient_user_name']
        time = request.POST['time']
        date = request.POST['date']
        doctor_name =  request.POST['doctor_name']
        reason = request.POST['reason']
        doctor = Doctor.objects.get(username=doctor_name)
        year = int(date.split("-")[0])
        month = int(date.split("-")[1])
        day = int(date.split("-")[2])
        hours = int(time.split(':')[0])
        minute = int(time.split(':')[1])

        apoitment_date = datetime.datetime(year,month,day,hours,minute)
        doctor_apoitment = Apoitment(date=apoitment_date,name=patient_user_name,reason=reason)
        doctor_apoitment.save()
        doctor.apoitment_list.add(doctor_apoitment)
        doctor.save()
        patient_apoitment = Apoitment(date=apoitment_date,name=doctor_name,reason=reason)
        patient_apoitment.save()
        patient = Patient.objects.get(user_name=patient_user_name)
        patient.appointments.add(patient_apoitment)
        patient.save()
        # print request.POST['patient_user_name']
        # print "-------------------------------"
        # print request.POST['time']
        # print "-------------------------------"
        # print request.POST['date']
        # print "-------------------------------"
        # print request.POST['doctor_name']
        return redirect("/HealthNet/%s"%patient_user_name)
    if request.is_ajax():
        return HttpResponse('You got ajax request')
    else:
        return HttpResponse('It was not ajax')
    return HttpResponse("Data was submitted")
#end of apis


def administration(request):
    template = loader.get_template('HealthNet/administration_sign.html')
    return HttpResponse(template.render(None,request))

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
            log = Logs(date=timezone.now(),action="Admin signed in",who_did=email,what_happened="An Admin signed in")
            log.save()
            return redirect('/HealthNet/administration/%s'%admin_user_name)
        except Administration.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'Invalid login credentials for: %s'%email)
            return redirect('/HealthNet/administration',permenent=True)


def admin_profile(request,admin_name):

        context = {
            'admin':admin_name,
        }
        admin_profile_template = loader.get_template('HealthNet/admin.html')
        log = Logs(date=timezone.now(),action=admin_name + " loaded admin page",who_did=admin_name,what_happened="Admin loaded admin page")
        log.save()
        return HttpResponse(admin_profile_template.render(context,request))

#Creating a doctor
def admin_create(request,admin_name):
    admin_create_temlate = loader.get_template('HealthNet/admins/admin_create.html')
    return HttpResponse(admin_create_temlate.render(None,request))
#@controller admin  will create and verify  doctor profile
#in future this controller should create a username by itslf without
#requring admin entering it manually
def admin_create_verify(request,admin_name):
    if request.method == 'POST':
        user_name = request.POST.get('user_name',None)
        isdoctor = False
        print ("blah")
        #setting the boolean 'isDoctor' besed on whether the user is to be
        #a Doctor of a nurse
        #if request.POST.get('employeeType1',None).checked:
        #    print ("fuck you")
        #Checking length
        print request.POST.get('nurse',None)
        if request.POST.get('nurse',None):
            print "______________________"
            print "00000"
        if len(user_name)<3:
            messages.add_message(request, messages.ERROR, 'This username is too short')
            return redirect( '/HealthNet/administration/' + admin_name + '/create/',permanent=True)
        try:
            patient = Patient.objects.get(user_name=user_name)
        except Patient.MultipleObjectsReturned:
            print ("This %s is already taken "%user_name)
            messages.add_message(request, messages.ERROR, 'Username is already taken: %s'%user_name)
            return redirect( '/HealthNet/administration/' + admin_name + '/create/',permanent=True)
        except Patient.DoesNotExist:
            print("Ben Affleck was okay Batman")
        #checking the username in the system
        try:
            print("%s"%user_name)
            print Doctor.objects.get(username=user_name).password
            doctor = Doctor.objects.get(username=user_name)
        except Doctor.MultipleObjectsReturned:
            print ("%s with this username already exists"%user_name)
            messages.add_message(request, messages.ERROR, 'This username is already taken: %s'%user_name)
            return redirect( '/HealthNet/administration/' + admin_name + '/create/',permanent=True)
        except Doctor.DoesNotExist:
            print ("Join the darkside")
        try:
            print("%s"%user_name)
            nurse = Nurse.objects.get(username=user_name)
        except Nurse.MultipleObjectsReturned:
            print ("%s with this username already exists"%user_name)
            messages.add_message(request, messages.ERROR, 'This username is already taken: %s'%user_name)
            return redirect( '/HealthNet/administration/' + admin_name + '/create/',permanent=True)
        except Nurse.DoesNotExist:
            print ("Join the darkside")

        #checking first and last names
        first_name = request.POST.get('first_name',None)
        last_name = request.POST.get('last_name',None)
        if len(first_name)<2 or len(last_name)<2:
            messages.add_message(request, messages.ERROR, 'Either first name or last name is too short')
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
                messages.add_message(request, messages.ERROR, 'These first and last names are in the system already')
                return redirect( '/HealthNet/administration/' + admin_name + '/create/',permanent=True)
            except Doctor.DoesNotExist:
                print ("Join the darkside")
            try:
                nurse = Nurse.objects.get(first_name=first_name,last_name=last_name)
            except Nurse.MultipleObjectsReturned:
                print ("Doctor with this first name: %s and this last name: %s already exists"%(first_name,last_name))
                messages.add_message(request, messages.ERROR, 'These first and last names are in the system already')
                return redirect( '/HealthNet/administration/' + admin_name + '/create/',permanent=True)
            except Nurse.DoesNotExist:
                print ("Join the darkside")
        #checking email
        email = request.POST.get('email',None)
        if not re.match(r'(\w+[.|\w])*@(\w+[.])*\w+', str(email)):
            messages.add_message(request, messages.ERROR, 'Invalid email')
            return redirect( '/HealthNet/administration/' + admin_name + '/create/',permanent=True)
        try:
            patient = Patient.objects.get(email=email)
        except Patient.MultipleObjectsReturned:
            print("A patient with this email exists")
            messages.add_message(request, messages.ERROR, 'This email is already in use')
            return redirect( '/HealthNet/administration/' + admin_name + '/create/',permanent=True)
        except Patient.DoesNotExist:
            print ("Hooray to Satan")
        try:
            doctor = Doctor.objects.get(email=email)
        except Doctor.MultipleObjectsReturned:
            print ("A doctor with this email already exists")
            messages.add_message(request, messages.ERROR, 'This email is already in use')
            return redirect( '/HealthNet/administration/' + admin_name + '/create/',permanent=True)
        except Doctor.DoesNotExist:
            print ("Join the darkside")
        try:
            nurse = Nurse.objects.get(email=email)
        except Nurse.MultipleObjectsReturned:
            print ("A nurse with this email already exists")
            messages.add_message(request, messages.ERROR, 'This email is already in use')
            return redirect( '/HealthNet/administration/' + admin_name + '/create/',permanent=True)
        except Nurse.DoesNotExist:
            print ("Join the darkside")

        #saving everything at the end
        hospital = request.POST.get('hospital',None)
        password = "12345"
        try:
            hospital = Hospital.objects.get(hospital_name=hospital)
        except Hospital.DoesNotExist:
            messages.add_message(request, messages.ERROR,'There is no hospital with this name')
            return redirect('/HealthNet/administration/' + admin_name + '/create/',permenent=True)
        if isdoctor:
            doctor = Doctor(username=user_name,email=email,first_name=first_name,last_name=last_name,password=password,hospital_name=hospital)
            doctor.save()
            hospital.doctors.add(doctor)
            log = Logs(date=timezone.now(),action="New Doctor created",who_did=admin_name,what_happened="Doctor creation")
            log.save()
        elif not isdoctor:
            nurse = Nurse(username=user_name,email=email,first_name=first_name,last_name=last_name,password=password,hospital_name=hospital)
            nurse.save()
            hospital.nurses.add(nurse)
            log = Logs(date=timezone.now(),action="New Nurse created",who_did=admin_name,what_happened="Nurse creation")
            log.save()
        hospital.save()
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

#loading admin logs into admin_logs template
def admin_logs(request,admin_name):
    admin_logs_template = loader.get_template('HealthNet/admin_logs.html')
    log = Logs.objects.all();
    context = {
        'logs':log,
        'admin':admin_name
    }
    return HttpResponse(admin_logs_template.render(context,request))
#load the main page
def index(request):
    users = Patient.objects.all()
    template = loader.get_template('HealthNet/index.html')
    context = {
        'users':users,
    }
    return HttpResponse(template.render(context,request))

#Request will be submited to this controller which will generate the message
#on fail it will generate a fail message
#on success it will generate succes
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
            print ("found doctor")
            log = Logs(date=timezone.now(),action="Sign In",who_did=email,what_happened="Doctor logged in")
            log.save()
            return redirect('/HealthNet/doctor/%s'%doctor.username)
        except Doctor.DoesNotExist:
            try:
                print("opps")
                t = Patient.objects.get(email=email,password=password)
                context ={
                    'user_name':email,
                }
                user_name = Patient.objects.get(email=email,password=password).user_name
                log = Logs(date=timezone.now(),action="Sign In",who_did=user_name,what_happened="A user of the system logged in")
                log.save()
                user_context = {
                    'user_name':user_name,
                }
                log = Logs(date=timezone.now(),action="Doctor logged in",who_did=email,what_happened="Doctor logged into the system")
                log.save()
                return redirect('/HealthNet/%s'%user_name,None)
            except Patient.DoesNotExist:
                log = Logs(date=timezone.now(),action="A user failed to log in",who_did=email,what_happened="User attempted to log into the system")
                log.save()
                return redirect('/HealthNet/')

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
            print ("Eroor")
            messages.add_message(request, messages.ERROR, '%s too short'%username)
            return redirect( '/HealthNet/signup/',permanent=True)
        else:
            try:
                test_patient = Patient.objects.get(user_name=username)
            except Patient.DoesNotExist:
                print ("Robert")
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
                print ("Robert")
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
                print ("Robert")
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
                    print ("Robert")
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
            messages.add_message(request, messages.ERROR, 'Street Address too short')
            return redirect( '/HealthNet/signup/',permanent=True)
        addresstwo = request.POST.get('addresstwo',None)
        if addresstwo is None or len(addresstwo)<5:
            messages.add_message(request, messages.ERROR, 'City and State too short')
            return redirect( '/HealthNet/signup/',permentant=True)
        insuarance = request.POST.get('insuarance_number',None)
        if len(insuarance)<5:
            messages.add_message(request, messages.ERROR, 'Insurance Number is too short')
            return redirect( '/HealthNet/signup/',permanent=True)
        else:
            try:
                test_patient = Patient.objects.get(insuarance_number=insuarance)
            except Patient.DoesNotExist:
                print ("Robert")
            except Patient.MultipleObjectsReturned:
                messages.add_message(request, messages.ERROR, 'Insurance Number is already in use: %s'%insuarance)
                return redirect( '/HealthNet/signup/',permanent=True)
        hospital_val = request.POST.get("hospital",None)
        symptoms = ' '
        p = Patient(user_name=username,password=password,first_name=first_name,last_name=last_name,email=email,user_id=uuid.uuid1(),\
                     symptoms=symptoms,cell_phone=cell_phone,hospital_name=hospital_val,\
                      address = address,insuarance_number=insuarance)
        p.save()
        log = Logs(date=timezone.now(),action="Register",who_did=username,what_happened="Signing up to the system")
        log.save()

        h = Hospital.objects.get(hospital_name=hospital_val)
        h.patients_list.add(p)
        h.save()
        #DO NOT TOUCH
        logs1 = Logs(date=timezone.now(),who_did="%s saved a patient with a %s"%(hospital_name,username))
        logs1.save()
        return redirect('/HealthNet/%s'%username,None)

def load_profile(request,user_name):
    user = Patient.objects.get(user_name=user_name)
    hospital_name = user.hospital_name
    hospital = Hospital.objects.get(hospital_name=hospital_name)
    doctor_list = hospital.doctors.all()
    doctor_names = []
    try:
        doctor = Doctor.objects.get(username=user._doctor)
    except Doctor.DoesNotExist:
        print("bad call")
    apotiments = []
    for patient in user.appointments.all():
        month = str(patient.date.month)
        year = str(patient.date.year)
        day =  str(patient.date.day)
        hour = str(patient.date.hour)
        minute = str(patient.date.minute)
        apoitment_doctor = Doctor.objects.get(username=patient.name)
        day = {
            'title':str(apoitment_doctor.first_name)+" "+str(apoitment_doctor.last_name),
            'start':year+"-"+month+"-"+day+" "+hour+":"+minute,
            'url':str('/HealthNet/'+user.user_name+"/"+apoitment_doctor.username+"/"+str(patient.id)+"/"+"appoitment/views/")
        }

        apotiments.append(day)
    print apotiments
    for d in doctor_list:
        doctor_data  = {
            "first_name":d.first_name,
            "last_name":d.last_name
        }
        doctor_names.append(doctor_data)

    profile_template = loader.get_template('HealthNet/profile.html')
    context={
        'Patient':user,
        'hospital_name':hospital_name,
        'doctor_list':doctor_names,
        'apointments':apotiments
        }

    log = Logs(date=timezone.now(),action="Loaded profile",who_did=user_name,what_happened="User loaded profile")
    log.save()
    return HttpResponse(profile_template.render(context,request))

#start of apoitments
def apoitment_view(request,user_name,doctor_name,apoitment_id):

    apoitment = Apoitment.objects.get(id=apoitment_id)
    year = str(apoitment.date.year)
    month = str(apoitment.date.month)
    day = str(apoitment.date.day)
    hour = str(apoitment.date.hour)
    minute = str(apoitment.date.minute)
    full_date = month+"/"+day+"/"+year

    time = hour+":"+minute

    context = {
        'date':full_date,
        'time':time,
        'reason':apoitment.reason
    }
    apoitment_template = loader.get_template('HealthNet/appointment_details.html')
    return HttpResponse(apoitment_template.render(context,request))

def apoitment_view_edit(request,user_name,doctor_name,apoitment_id):
    apoitment = Apoitment.objects.get(id=apoitment_id)
    apoitment_edit_template = loader.get_template('HealthNet/apoitment_edit.html')
    year = str(apoitment.date.year)
    month = str(apoitment.date.month)
    if len(month)==1:
        month = '0'+month
    day = str(apoitment.date.day)
    if len(day)==1:
        day = '0'+day
    hour = str(apoitment.date.hour)
    minute = str(apoitment.date.minute)
    full_date = year+"-"+month+"-"+day

    time = hour+":"+minute

    context = {
        'date':full_date,
        'time':time,
        'reason':apoitment.reason
    }
    return HttpResponse(apoitment_edit_template.render(context,request))


def apoitment_view_edit_submit(request,user_name,doctor_name,apoitment_id):
    if request.method == 'POST':
        old_apoitment = Apoitment.objects.get(id=apoitment_id)
        current_date = datetime.datetime.now()
        submit_date = request.POST.get('date',None)
        year = int(submit_date.split("-")[0])
        month = int(submit_date.split("-")[1])
        day = int(submit_date.split("-")[2])
        date_to_compare = datetime.datetime(year,month,day)
        if date_to_compare<current_date:
            return HttpResponse("Cannot Schedule apoitment in past")
        if year>date_to_compare.year:
            return HttpResponse("Cannot schedule apoitent in the future")
        #update for doctor first
        time = request.POST.get('time',None)
        reason = request.POST.get('reason',None)
        hour = int(time.split(":")[0])
        minute = int(time.split(":")[1])
        date_to_compare = datetime.datetime(year,month,day,hour,minute)
        user_apoitment = Patient.objects.get(user_name=user_name)
        doctor = Doctor.objects.get(username=doctor_name)
<<<<<<< HEAD
        patient_apoitment = None
        for patient_ap in user_apoitment.appointments.all():
            if patient_ap.date.year == year and patient_ap.date.month==month \
                and patient_ap.date.day==day and patient_ap.date.hour == hour and patient_ap.date.minute == minute:
                apoitment = patient_ap

        doctor_apoitment = None
        for patient_ap in doctor.apoitment_list.all():
            if patient_ap.date.year == year and patient_ap.date.month==month \
                and patient_ap.date.day==day and patient_ap.date.hour == hour and patient_ap.date.minute == minute:
                doctor_apoitment = patient_ap

    return HttpResponse("You edited")
=======
        patient_apoitment = Apoitment.objects.get(id=apoitment_id)
        doctor_apoitment_id = 0
        for doctor_ap in Doctor.objects.get(username=doctor_name).apoitment_list.all():
            if doctor_ap.date == patient_apoitment.date:
                doctor_apoitment_id = doctor_ap.id
        doctor_apoitment = Apoitment.objects.get(id=doctor_apoitment_id)
        patient_apoitment.delete()
        doctor_apoitment.delete()
        patient_apoitment.save()
        doctor_apoitment.save()
        doctor_new_apoitment = Apoitment(date=date_to_compare,name=user_name,reason=reason)
        doctor_new_apoitment.save()
        doctor = Doctor.objects.get(username=doctor_name)
        doctor.apoitment_list.add(doctor_new_apoitment)
        doctor.save()
        patient_new_apoitment = Apoitment(date=date_to_compare,name=doctor_name,reason=reason)
        patient_new_apoitment.save()
        patient = Patient.objects.get(user_name=user_name)
        patient.appointments.add(patient_new_apoitment)
        patient.save()
        return redirect('/HealthNet/%s'%user_name)
>>>>>>> 7df8dfee6e35ca3a9ffaeab65bb508f0e5b5425a
#end of appointments
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

            #setting the appropriate logs
            if user.user_name != user_name:
                print ("username is different")
                if user_name == first_name or user_name == last_name or user_name == user.first_name or user_name == user.last_name:
                    messages.add_message(request, messages.ERROR, 'Cannot set username to your first or last name')
                    return redirect( '/HealthNet/' + user.user_name + '/view/',permanent=True)
                if len(user_name)<5:
                    messages.add_message(request, messages.ERROR, 'Username is too short')
                    return redirect('/HealthNet/' + user.user_name + '/view/',permentant=True);
                try:
                    print ("trying to find patient")
                    test_patient = Patient.objects.get(user_name=user_name)
                    if test_patient is not None:
                        messages.add_message(request, messages.ERROR, 'Username is already in use')
                        return redirect( '/HealthNet/' + user.user_name + '/view/',permanent=True)
                except Patient.DoesNotExist:
                    print ("printing exception")
                log = Logs(date=timezone.now(),action="User edited profile",who_did=user.user_name,what_happened="User changed username from " + user.user_name + " to " + user_name)
                log.save()
            if user.first_name != first_name:
                if len(first_name) < 3:
                    messages.add_message(request, messages.ERROR, 'Invalid first name')
                    return redirect( '/HealthNet/' + user.user_name + '/view/',permanent=True)
                if first_name == last_name:
                    messages.add_message(request, messages.ERROR, 'First name cannot be equal to last name')
                    return redirect( '/HealthNet/' + user.user_name + '/view/',permanent=True)
                log = Logs(date=timezone.now(),action="User edited profile",who_did=user.user_name,what_happened="User changed first name from " + user.first_name + " to " + first_name)
                log.save()
            if user.last_name != last_name:
                if len(last_name) < 3:
                    messages.add_message(request, messages.ERROR, 'Invalid last name')
                    return redirect( '/HealthNet/' + user.user_name + '/view/',permanent=True)
                if last_name == first_name:
                    messages.add_message(request, messages.ERROR, 'Invalid first name')
                    return redirect( '/HealthNet/' + user.user_name + '/view/',permanent=True)
                log = Logs(date=timezone.now(),action="User edited profile",who_did=user.user_name,what_happened="User changed last name from " + user.last_name + " to " + last_name)
                log.save()
            if user.email != email:
                if not re.match(r'(\w+[.|\w])*@(\w+[.])*\w+', str(email)):
                    messages.add_message(request, messages.ERROR, 'Invalid email')
                    return redirect( '/HealthNet/' + user.user_name + '/view/',permanent=True)
                log = Logs(date=timezone.now(),action="User edited profile",who_did=user.user_name,what_happened="User changed email address from " + user.email + " to " + email)
                log.save()
            if user.cell_phone != cell_phone:
                if len(str(cell_phone.split("+")))<1 and str(cell_phone)[0] is not '1':
                    messages.add_message(request, messages.ERROR, 'Invalid cell phone number')
                    return redirect( '/HealthNet/' + user.user_name + '/view/',permanent=True)
                log = Logs(date=timezone.now(),action="User edited profile",who_did=user.user_name,what_happened="User changed cell phone number from " + user.cell_phone + " to " + cell_phone)
                log.save()
            if user.address != address:

                log = Logs(date=timezone.now(),action="User edited profile",who_did=user.user_name,what_happened="User changed address from " + user.adress + " to " + adress)
                log.save()
            if user.insuarance_number != insuarance_number:
                if len(insuarance_number) < 5:
                    messages.add_message(request, messages.ERROR, 'Invalid insurance number')
                    return redirect( '/HealthNet/' + user.user_name + '/view/',permanent=True)
                log = Logs(date=timezone.now(),action="User edited profile",who_did=user.user_name,what_happened="User changed insurance number from " + user.insuarance_number + " to " + insuarance_number)
                log.save()

            user.user_name = user_name
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.cell_phone = cell_phone
            user.address = address
            user.insuarance_number = insuarance_number
            user.save()
            return redirect('/HealthNet/%s'%user_name,None)
        except Patient.DoesNotExist:
            log = Logs(date=timezone.now(),action="Attempted User profile save",who_did=user_name,what_happened="User attempted to edit profile that doesn't exist")
            log.save()
            return HttpResponse("Could not save the user")




#This is loading the patient pool template into the system
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
    logs = Logs(date=timezone.now(),action=doctor_user_name + " is Browsing list of patients at : " + hospital_name,who_did="%s"%doctor_user_name)
    logs.save()
    pool_template = loader.get_template('HealthNet/free_pool.html')
    return HttpResponse(pool_template.render(context,request))

#doctor is choosing which patient to take
def patien_to_save(request,hospital_name,user_name,doctor_user_name):
    patient = Patient.objects.get(user_name=user_name)
    patient.assigned_doctor = True
    patient.save()
    doctor = Doctor.objects.get(username=doctor_user_name)
    doctor.patients.add(patient)
    patient._doctor = doctor.username
    patient.save()
    doctor.save()
    logs = Logs(date=timezone.now(),action="Assigning Patient",who_did="%s"%doctor_user_name)
    logs.save()
    return redirect("/HealthNet/%s/%s/pool"%(hospital_name,doctor_user_name))

#loading doctor profile
def doctor_profile(request,doctor_user_name):
    doctor_template = loader.get_template('HealthNet/doctors.html')
    doctor = Doctor.objects.get(username=doctor_user_name)
    hospital_name = ''.join(doctor.hospital_name.split(" "))
    patients=[]
    apoitment_list = []
    apoitments = doctor.apoitment_list.all()

    for patient in apoitments:
        print patient.name
        month = str(patient.date.month)
        year = str(patient.date.year)
        day = str(patient.date.day)
        hour = str(patient.date.hour)
        minute = str(patient.date.minute)
        user = Patient.objects.get(user_name=patient.name)
        day = {
            'title':str(user.first_name)+" "+str(user.last_name),
            'start':year+"-"+month+"-"+day+" "+hour+":"+minute
        }
        patients.append(user)
        apoitment_list.append(day)

    #getting all free patients
    count = -1
    for free_patiens in Patient.objects.all():
        if not free_patiens.assigned_doctor:
            count = count + 1
    print (count)

    context = {
        'doctor':doctor,
        'hospital_name':hospital_name,
        'patient_list':patients,
        'apoitments':apoitment_list,
        'count':count
    }
    logs = Logs(date=timezone.now(),action=doctor_user_name + " loaded profile",who_did="%s"%doctor_user_name)
    logs.save()

    return HttpResponse(doctor_template.render(context,request))

#loading appointment page
def appoitment(request,user_name):

    appoitment_template = loader.get_template('HealthNet/appointment.html')
    patient  = Patient.objects.get(user_name=user_name)
    try:
        doctor = Doctor.objects.get(username=patient._doctor)
    except Doctor.DoesNotExist:
        return redirect("/HealthNet/"+user_name+"/",permentant=True)    
    hospital = Hospital.objects.get(hospital_name=doctor.hospital_name)
    hospitl_list = []
    for hosp in hospital.doctors.all():
        names = {
            'first_name':hosp.first_name,
            'last_name':hosp.last_name
        }
        hospitl_list.append(names)
    context = {
        'username':user_name,
        'doctor':doctor,
        'hospital_list':hospitl_list
    }
    return HttpResponse(appoitment_template.render(context,request))




def confirm_appoitment_dates(request,user_name,dates):
    doctor_user_name = Patient.objects.get(user_name=user_name)._doctor
    try:
        doctor = Doctor.objects.get(username=doctor_user_name)
        available_time = doctor.apoitment_list.all()
        year = int(dates.split("/")[0])
        month = int(dates.split("/")[1])
        return HttpResponse("The dates are %s"%dates)

    except Doctor.DoesNotExist:
        #must prompt a user to submit a ticket to a hospital administration so that issue can be resolved
        return HttpResponse("You do not have a doctor assigned to you")
    return HttpResponse("dates %s "%doctor_user_name)

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
    log = Logs(date=timezone.now(),action="Appointment was edited",who_did=user_name,what_happened="Appointment edited")
    log.save()
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

#doctor edit will load the template with doctors details to be edited
def doctor_edit_profile(request,doctor_user_name):
    doctor_edit_template = loader.get_template('HealthNet/doctor_edit.html')
    try:
        doctor = Doctor.objects.get(username=doctor_user_name)
        context = {
            'doctor':doctor
        }
        log = Logs(date=timezone.now(),action="Doctor editing profile",who_did=doctor_user_name,what_happened="Doctor editing his profile")
        log.save()
        return HttpResponse(doctor_edit_template.render(context,request))
    except Doctor.DoesNotExist:
        return HttpResponse("Doctor Does Not exists");

#doctor edit will validate and save doctor profile to database
def doctor_edit_profile_save(request,doctor_user_name):
    if request.method == 'POST':
        user_name = request.POST.get('user_name',None)
        if len(user_name ) < 4:
            messages.add_message(request, messages.ERROR, 'Username too short')
            return redirect( '/HealthNet/doctor/' + doctor_user_name + '/edit/',permanent=True)
        try:
            doctor = Doctor.objects.get(username=user_name)
        except Doctor.DoesNotExist:
            print ("good job")
        except Doctor.MultipleObjectsReturned:
            messages.add_message(request, messages.ERROR, 'Username is in use by someone else')
            return redirect( '/HealthNet/doctor/' + doctor_user_name + '/edit/',permanent=True)
        first_name = request.POST.get('first_name',None)
        if len(first_name ) < 3:
            messages.add_message(request, messages.ERROR, 'First name too short')
            return redirect( '/HealthNet/doctor/' + doctor_user_name + '/edit/',permanent=True)
        last_name = request.POST.get('last_name',None)
        if len(last_name) < 3:
            messages.add_message(request, messages.ERROR, 'Last name too short')
            return redirect( '/HealthNet/doctor/' + doctor_user_name + '/edit/',permanent=True)
        if first_name == last_name:
            messages.add_message(request, messages.ERROR, 'First and last names cannot be equal')
            return redirect( '/HealthNet/doctor/' + doctor_user_name + '/edit/',permanent=True)
        if first_name == user_name or last_name == user_name:
            messages.add_message(request, messages.ERROR, 'Username cannot be first or last name')
            return redirect( '/HealthNet/doctor/' + doctor_user_name + '/edit/',permanent=True)
        email = request.POST.get('email',None)
        if not re.match(r'(\w+[.|\w])*@(\w+[.])*\w+', str(email)):
            messages.add_message(request, messages.ERROR, 'Email is of invalid format')
            return redirect( '/HealthNet/doctor/' + doctor_user_name + '/edit/',permanent=True)
        cell_phone = request.POST.get('cell_phone',None)
        if len(str(cell_phone.split("+")))<1 and str(cell_phone)[0] is not '1':
            cell_phone = '1'+cell_phone
            try:
                 float(str(cell_phone.split("+")[1]))
            except ValueError:
                 messages.add_message(request, messages.ERROR, 'Phone number is of invalid format')
                 return redirect( '/HealthNet/doctor/' + doctor_user_name + '/edit/',permanent=True)
        elif cell_phone and len(cell_phone ) > 5:
            if cell_phone[0] is '1':
                cell_phone = '+'+cell_phone
                try:
                    float(str(cell_phone.split("+")[1]))
                except ValueError:
                    messages.add_message(request, messages.ERROR, 'Phone number is of invalid format')
                    return redirect( '/HealthNet/doctor/' + doctor_user_name + '/edit/',permanent=True)
            else:
                try:
                    cell_phone = request.POST.get('cell_phone',None)
                except Patient.DoesNotExist:
                    print ("Robert")
                except Patient.MultipleObjectsReturned:
                    messages.add_message(request, messages.ERROR, 'Phone number is of invalid format')
                    return redirect( '/HealthNet/doctor/' + doctor_user_name + '/edit/',permanent=True)
        else:
            messages.add_message(request, messages.ERROR, 'Phone number is of invalid format')
            return redirect( '/HealthNet/doctor/' + doctor_user_name + '/edit/',permanent=True)
        password = request.POST.get('password',None)
        passwordTryTwo = request.POST.get('confirm_password',None)
        if password != passwordTryTwo:
            messages.add_message(request, messages.ERROR, 'Passwords do not match')
            return redirect( '/HealthNet/doctor/' + doctor_user_name + '/edit/',permanent=True)
        try:
            doctor = Doctor.objects.get(username=doctor_user_name)
            doctor.username = user_name
            doctor.first_name = first_name
            doctor.last_name = last_name
            doctor.email = email
            doctor.cell_phone=cell_phone
            doctor.password = password
            doctor.save()
            log = Logs(date=timezone.now(),action="Doctor edited his profile",who_did=user_name,what_happened="Doctor edited profile")
            log.save()
            return redirect('/HealthNet/doctor/%s'%doctor.username)
        except Doctor.DoesNotExist:
            log = Logs(date=timezone.now(),action="Doctor attempted to edit profile and failed",who_did=user_name,what_happened="Doctor failed in profile edit")
            log.save()
            return HttpResponse("Could not find doctor")

#doctor apoitment will view all apoitmentsf
#also doctor will have ability to views the details about apoitment
def doctor_apoitments_view(request,doctor_user_name):
    try:
        doctor = Doctor.objects.get(username=doctor_user_name)



        context = {
            'doctor':doctor

        }
        doctor_apoitment_template = loader.get_template('HealthNet/doctor_apoitment.html')
        log = Logs(date=timezone.now(),action="Doctor viewing appointments",who_did=doctor_user_name,what_happened="Doctor viewed appointments")
        log.save()
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
    log = Logs(date=timezone.now(),action="Doctor viewed a patient in the patient pool",who_did=doctor_user_name,what_happened=doctor_user_name + " viewed " + patient_user_name + " at " + hospital_name)
    log.save()
    return HttpResponse(patient_template.render(context,request))

def loadaddprescription(request,doctor_user_name,patient_uesr_name):
    template = loader.get_template('HealthNet/addprescription.html')
    context = {
        'patient':patient_uesr_name,
        'doctor':doctor_user_name
    }

    return HttpResponse(template.render(context,request))

def viewPrescriptions(request,doctor_user_name,patient_uesr_name):
    template = loader.get_template('HealthNet/viewprescriptions.html')

    patient = Patient.objects.get(user_name=patient_uesr_name)
    pres = patient.prescriptions.all()

    doctor = Doctor.objects.get(username=doctor_user_name)
    print(doctor.username)
    context = {
        'prescriptions':pres,
        'patient':patient,
        'doctor':doctor.username
    }

    return HttpResponse(template.render(context,request))

#adding a prescription
def addPrescription(request,patient_uesr_name,doctor_user_name):#the context here is is just for doctor and patient
    if request.method == 'POST':
        patient = Patient.objects.get(user_name=patient_uesr_name)

        doctor = patient._doctor

        medicine = request.POST.get('medication',None)
        description = request.POST.get('description',None)
        dosage = request.POST.get('dosage',None)
        print (medicine)
        print(dosage)
        print(description)

        #error checking
        #redirect needs to be changed
        if medicine is None or len(medicine)<3:
            messages.add_message(request, messages.ERROR, 'Medicine name is too short: %s'%medicine)
            return redirect('/HealthNet/doctor/'+doctor_user_name+'/patients/'+patient_uesr_name+'/add/',permenent=True)
        if description is None or len(description)<3:
            messages.add_message(request, messages.ERROR, 'Description is too short: %s'%description)
            return redirect('/HealthNet/doctor/'+doctor_user_name+'/patients/'+patient_uesr_name+'/add/',permenent=True)
        if dosage is None or len(dosage)<3:
            messages.add_message(request, messages.ERROR, 'Dosage message too short: %s'%dosage)
            return redirect('/HealthNet/doctor/'+doctor_user_name+'/patients/'+patient_uesr_name+'/add/',permenent=True)

        #saving the prescription
        prescription = Prescription(title=medicine,details=description,dosage=dosage)
        prescription.save()

        #adding to patient
        patient.prescriptions.add(prescription)

        #setting logs
        log = Logs(date=timezone.now(),action="A doctor added a new prescription to "+ patient_uesr_name + " of " + medicine,who_did=doctor,what_happened="A doctor added a new prescription to "+ patient_uesr_name + " of " + medicine)
        log.save()

        return redirect('/HealthNet/doctor/'+ doctor_user_name +'/patients/',permenent=True) #redirecting back to doctor page
    else:
        print "NOt POST"
#deleting a prescription
def deletePrescription(request,patient_uesr_name,doctor_user_name,medicine_id):
    #getting the prescription to be deleted

    patient = Patient.objects.get(user_name = patient_uesr_name)
    doctor = Doctor.objects.get(username= doctor_user_name)
    prescript = Prescription.objects.get(id=medicine_id)

    log = Logs(date=timezone.now(),action=doctor_user_name + " deleted prescription of " + prescript.title + " from " + patient_uesr_name,who_did=doctor_user_name,what_happened="A doctor deleted a prescription")
    log.save()

    prescript.delete()
    prescript.save()

    return redirect('/HealthNet/doctor/'+ doctor_user_name +'/patients/',permentent=True)

#loading the patient view page
def patients(request,doctor_user_name):
    doctor = Doctor.objects.get(username=doctor_user_name)
    patients = doctor.patients.all()
    context = {
        'patient':patients,
        'doctor':doctor
    }
    patient_template = loader.get_template('HealthNet/prescription.html')#loading the patient page

    return HttpResponse(patient_template.render(context,request))

def statistics(request,admin_name):



    context = {

    }
    template = loader.get_template('HealthNet/statistics.html')#this doesn't exist yet

    return HttpResponse(template.render(context,request))
