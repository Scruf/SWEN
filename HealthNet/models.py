from __future__ import unicode_literals
import uuid
from django.db import models



class  Patient(models.Model):
    user_name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    user_id = models.UUIDField(primary_key=False,default=uuid.uuid1, editable=False)

    def __str__(self):
        return self.user_name+"-"+self.password

# Create your models here.
