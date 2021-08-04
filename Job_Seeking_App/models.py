from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe
import datetime as dt


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
        return self.employer.username

JOB_TYPE = (
    ('1', "Full time"),
    ('2', "Part time"),
    ('3', "Internship"),
)


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Jobs(models.Model):
    user = models.ForeignKey(User, related_name='User', on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    description = models.TextField(max_length=3000,null=True)
    tags = models.CharField(max_length=144,null=True)
    location = models.CharField(max_length=300)
    job_type = models.CharField(choices=JOB_TYPE, max_length=1)
    category = models.ForeignKey(Category, related_name='Category', on_delete=models.CASCADE)
    salary = models.CharField(max_length=30, blank=True)
    company_name = models.CharField(max_length=300)
    company_description = models.CharField(max_length=3000,null=True)
    published_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title




