from django.contrib import admin
from django.http import HttpResponse

from HealthNet.models import *

admin.site.register(Logs)
