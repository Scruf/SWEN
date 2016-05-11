
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse
from django.template import loader
from django.contrib.auth import authenticate, login
import re
import uuid
from django.template.context import RequestContext
from django.core.mail import send_mail
import datetime



MONGODB_URI ='mongodb://ek5442:NokiaLumia920@ds033875.mlab.com:33875/movies'





def index(request):
    sign_up_template = loader.get_template('SWEN/index.html')
    context = {
        "Loading":"Sign Up"
    }
    return redirect('/HealthNet/')

def sign_up(request):
    return HttpResponse("Succesfully pushed to momngo")
