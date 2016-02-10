from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Patient
# Create your views here.
def index(request):
    users = Patient.objects.all()
    template = loader.get_template('HealthNet/index.html')
    context = {
        'users':users,
    }
    return HttpResponse(template.render(context,request))
