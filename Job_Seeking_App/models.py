from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime as dt
from django.db import IntegrityError


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
    is_jobseeker = models.BooleanField(default=False)

JOBSEEKER_AVAILABILITY = (
    ('Available', "Available"),
    ('Not Available', "Not Available"),
)

JOb_CATEGORIES = (
    ('IT support technician', "IT support technician"),
    ('Software developer', "Software developer"),
    ('Systems analyst', "Systems analyst"),
    ('Computer service and repair technician', "Computer service and repair technician"),
    ('Solution architect', "Solution architect"),
    ('Network manager', "Network manager"),
)

class JobSeeker(models.Model):
    first_name =models.CharField(max_length=144)
    last_name = models.CharField(max_length=144)
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    availability = models.CharField(choices=JOBSEEKER_AVAILABILITY, default="Available", max_length=20)
    salary = models.IntegerField(default=0)
    job_category = models.CharField(max_length=300,choices=JOb_CATEGORIES)
    email = models.EmailField()
    phone = models.IntegerField(null=True,blank=True)
    location = models.CharField(max_length=144,null=True,blank=True)
    bio =models.TextField(null=True,blank=True)
    profile_picture =models.ImageField(upload_to='profiles')
    verified = models.BooleanField(default=False)


    @receiver(post_save, sender=User)
    def update_jobseeker_signal(sender, instance, created, **kwargs):
        if created:
            JobSeeker.objects.create(user=instance)
        instance.profile.save()

    def __str__(self):
        return self.user.username

class Employer(models.Model):
    first_name =models.CharField(max_length=144)
    last_name = models.CharField(max_length=144)
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="employer")
    email = models.EmailField()
    phone = models.IntegerField(null=True,blank=True)
    location = models.CharField(max_length=144,null=True,blank=True)
    company_name = models.CharField(max_length=144,null=True,blank=True)


    @receiver(post_save, sender=User)
    def update_employer_signal(sender, instance, created, **kwargs):
        if created:
            Employer.objects.create(user=instance)
        instance.employer.save()


    def __str__(self):
        return self.user.username

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
    company_description = models.TextField(max_length=3000,null=True)
    published_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title




