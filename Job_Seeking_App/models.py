from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class JobSeeker(models.Model):
    is_jobseeker = models.BooleanField(default=True)
    jobseeker=models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=25)
    location = models.CharField(max_length=25,null=True)

    def __str__(self):
        return self.jobseeker.username


class Employer(models.Model):
    is_jobseeker = models.BooleanField(default=False)
    employer=models.OneToOneField(User,on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    location = models.CharField(max_length=25,null=True)

    def __str__(self):
        return self.employer.username
