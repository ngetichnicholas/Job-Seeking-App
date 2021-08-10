from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime as dt
from django.db import IntegrityError
from cloudinary.models import CloudinaryField


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
    is_jobseeker = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    email = models.EmailField()
    first_name =models.CharField(max_length=144,null=True,blank=True)
    last_name = models.CharField(max_length=144,null=True,blank=True)
    profile_picture =CloudinaryField('image')
    location = models.CharField(max_length=144,null=True,blank=True)
    phone = models.IntegerField(null=True,blank=True)


    def delete_user(self):
        self.delete()

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
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='profile')
    availability = models.CharField(choices=JOBSEEKER_AVAILABILITY, default="Available", max_length=20)
    salary = models.IntegerField(default=0)
    job_category = models.CharField(max_length=300,choices=JOb_CATEGORIES)
    bio =models.TextField(null=True,blank=True)

    @receiver(post_save, sender=User)
    def update_jobseeker_signal(sender, instance, created, **kwargs):
        if created:
            JobSeeker.objects.create(user=instance)
        instance.profile.save()

    def save_jobseeker(self):
        self.save()

    def delete_jobseeker(self):
        self.delete()

    def __str__(self):
        return self.user.username


class FileUpload(models.Model):
    name = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='documents/pdfs/')
    jobseeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name='documents')

    def __str__(self):
        return self.name

class Employer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="employer")
    company_name = models.CharField(max_length=144,null=True,blank=True)

    @receiver(post_save, sender=User)
    def update_employer_signal(sender, instance, created, **kwargs):
        if created:
            Employer.objects.create(user=instance)
        instance.employer.save()

    def save_employer(self):
        self.save()

    def delete_employer(self):
        self.delete()

    def __str__(self):
        return self.user.username

class Payments(models.Model):
    first_name =models.CharField(max_length=144,null=True,blank=True)
    last_name = models.CharField(max_length=144,null=True,blank=True)
    phone = models.CharField(max_length=144,null=True,blank=True)

# previous projects
class Portfolio(models.Model):
    jobseeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name='portfolio')
    name = models.CharField(max_length=50)
    link=models.URLField(max_length=555)

    def __str__(self):
        return f"Portfolio {self.id}"

    class Meta:
        verbose_name = ("Portfolio")
        verbose_name_plural = ("Portfolio")


# JOB_TYPE = (
#     ('1', "Full time"),
#     ('2', "Part time"),
#     ('3', "Internship"),
# )

# class Category(models.Model):
#     name = models.CharField(max_length=200)

#     def __str__(self):
#         return self.name

# class Jobs(models.Model):
#     user = models.ForeignKey(User, related_name='User', on_delete=models.CASCADE)
#     title = models.CharField(max_length=300)
#     description = models.TextField(max_length=3000,null=True)
#     tags = models.CharField(max_length=144,null=True)
#     location = models.CharField(max_length=300)
#     job_type = models.CharField(choices=JOB_TYPE, max_length=1)
#     category = models.ForeignKey(Category, related_name='Category', on_delete=models.CASCADE)
#     salary = models.CharField(max_length=30, blank=True)
#     company_name = models.CharField(max_length=300)
#     company_description = models.TextField(max_length=3000,null=True)
#     published_date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return self.title




