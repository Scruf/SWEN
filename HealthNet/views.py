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
def success(request):
    if request.method == 'POST':
        search_user_name = request.POST.get('username',None)
        try:
            user = Patient.objects.get(user_name=search_user_name)
            html = ("<h3>You are who you are</h3>")
            return HttpResponse(html)
        except Patient.DoesNotExist:
            return HttpResponse("No such cunt")
    else:
        print "Hello"
