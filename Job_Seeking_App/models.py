from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
    is_jobseeker = models.BooleanField(default=False)

class JobSeeker(models.Model):
    first_name =models.CharField(max_length=144)
    last_name = models.CharField(max_length=144)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField(unique=True)
    phone = models.IntegerField()
    location = models.CharField(max_length=144)

    def __str__(self):
        return self.user.username

class Employer(models.Model):
    first_name =models.CharField(max_length=144)
    last_name = models.CharField(max_length=144)
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField(unique=True)
    phone = models.IntegerField()
    location = models.CharField(max_length=144)


    def __str__(self):
        return self.user.username
