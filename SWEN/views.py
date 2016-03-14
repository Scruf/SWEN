
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login
import re
import uuid
from django.template.context import RequestContext
from django.core.mail import send_mail
import datetime
import pymongo



MONGODB_URI ='mongodb://ek5442:NokiaLumia920@ds033875.mlab.com:33875/movies'





def index(request):
    sign_up_template = loader.get_template('SWEN/index.html')
    context = {
        "Loading":"Sign Up"
    }
    return HttpResponse(sign_up_template.render(context,request))

def sign_up(request):
    if request.method=='POST':
        name = request.POST.get('name',None),
        user_name = request.POST.get('username',None)
        password = request.POST.get('password',None)
        args_to_push = {
            'name':str(name),
            'user_name':str(user_name),
            'password':str(password)
        }
        client = pymongo.MongoClient(MONGODB_URI)
        db = client.get_default_database()
        users = db['HealthNetUsers']
        users.insert(args_to_push)
        return HttpResponse("Succesfully pushed to momngo")
