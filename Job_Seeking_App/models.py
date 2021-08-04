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
    tags = models.CharField()
    location = models.CharField(max_length=300)
    job_type = models.CharField(choices=JOB_TYPE, max_length=1)
    category = models.ForeignKey(Category, related_name='Category', on_delete=models.CASCADE)
    salary = models.CharField(max_length=30, blank=True)
    company_name = models.CharField(max_length=300)
    company_description = models.CharField(blank=True, null=True)
    published_date = models.DateTimeField(auto_now_add=True)(default=False)


    def __str__(self):
        return self.title




