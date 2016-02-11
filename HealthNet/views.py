from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Patient
from django.contrib.auth import authenticate, login

# Create your views here.

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
    search_id=request.POST.get('username',None)
    succes_template = loader.get_template('HealthNet/success.html')
    failure_template = loader.get_template('HealthNet/failure.html')
    try:
        user_name = Patient.objects.get(user_name=search_id)
        return HttpResponse(succes_template.render({"Hello":user_name},request))
    except Patient.DoesNotExist:
        return HttpResponse(failure_template.render({"No such":"cunt"},request))
