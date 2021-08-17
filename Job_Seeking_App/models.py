from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime as dt
from django.db import IntegrityError
from cloudinary.models import CloudinaryField
from django.core.validators import MaxLengthValidator,MinLengthValidator


class User(AbstractUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []#removes email from REQUIRED_FIELDS
    is_admin = models.BooleanField(default=False)
    is_employer = models.BooleanField(default=False)
    is_jobseeker = models.BooleanField(default=False)
    verified = models.BooleanField(default=False)
    email = models.EmailField(unique=True)
    first_name =models.CharField(max_length=144,null=True,blank=True)
    last_name = models.CharField(max_length=144,null=True,blank=True)
    profile_picture =CloudinaryField('image')
    location = models.CharField(max_length=144,null=True,blank=True)
    phone = models.CharField(unique=True,max_length=13, null=True,blank=True, validators=[MinLengthValidator(10),MaxLengthValidator(13)])

    def save_user(self):
        self.save()

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

    @classmethod
    def search_jobseekers_by_job_category(cls,job_category):
        jobseekers = JobSeeker.objects.filter(job_category__icontains=job_category)
        return jobseekers


class FileUpload(models.Model):
    name = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='documents/pdfs/')
    jobseeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name='documents')

    def save_upload(self):
        self.save()

    def delete_upload(self):
        self.delete()
    
    @classmethod
    def update_upload(cls, id ,name,pdf ,jobseeker):
        update = cls.objects.filter(id = id).update(name = name,pdf = pdf,jobseeker=jobseeker)
        return update

    @classmethod
    def get_all_uploads(cls):
        uploads = cls.objects.all()
        return uploads

    @classmethod
    def get_upload_id(cls,id):
        upload_id = cls.objects.filter(id= id).all()
        return upload_id

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
    mpesa_number = models.BigIntegerField('Mpesa Phone Number', validators=[MinLengthValidator(12),MaxLengthValidator(13)])

# previous projects
class Portfolio(models.Model):
    jobseeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name='portfolio')
    name = models.CharField(max_length=50)
    link=models.URLField(max_length=555)

    def __str__(self):
        return f"Portfolio {self.id}"
    def save(self, *args, **kwargs):
        super().save()

    class Meta:
        verbose_name = ("Portfolio")
        verbose_name_plural = ("Portfolio")

class Contact(models.Model):
    name = models.CharField(max_length = 30)
    email = models.EmailField()
    message = models.TextField()
    
    def __str__(self):
        return self.name
