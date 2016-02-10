from __future__ import unicode_literals

from django.db import models



class  Patient(models.Model):
    user_name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)


    def __str__(self):
        return self.user_name+"-"+self.password

# Create your models here.
