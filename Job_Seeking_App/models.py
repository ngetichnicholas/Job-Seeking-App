from django.db import models
from django.contrib.auth.models import (AbstractUser)

# Create your models here.
class User(AbstractUser):
    is_jobseeker = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=50,null=True)


class JobSeeker(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    phone = models.CharField(max_length=25)
    location = models.CharField(max_length=25,null=True)


class Employer(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=25,null=True)
