from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.html import escape, mark_safe
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime as dt
from django.db import IntegrityError
from cloudinary.models import CloudinaryField
from django.core.validators import MaxLengthValidator,MinLengthValidator


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
    profile_picture =CloudinaryField('image',null=True,blank=True)
    location = models.CharField(max_length=144,null=True,blank=True)
    phone = models.CharField(unique=True,max_length=13, null=True,blank=True, validators=[MinLengthValidator(10),MaxLengthValidator(13)])
    company_name = models.CharField(max_length=144,null=True,blank=True)
    availability = models.CharField(null=True,blank=True,choices=JOBSEEKER_AVAILABILITY, max_length=20)
    salary = models.IntegerField(null=True,blank=True)
    job_category = models.CharField(null=True,blank=True,max_length=300,choices=JOb_CATEGORIES)
    bio =models.TextField(null=True,blank=True)


    def save_user(self):
        self.save()

    def delete_user(self):
        self.delete()

    @classmethod
    def update_user(cls, id ,username,first_name ,last_name,email,phone,location):
        update = cls.objects.filter(id = id).update(username = username,first_name = first_name,last_name=last_name,email=email,phone=phone,location=location)
        return update

    @classmethod
    def get_all_users(cls):
        users = cls.objects.all()
        return users

    @classmethod
    def get_user_id(cls,id):
        user_id = cls.objects.filter(id= id).all()
        return user_id

    @classmethod
    def search_jobseekers_by_job_category(cls,job_category):
        jobseekers = User.objects.filter(job_category__icontains=job_category)
        return jobseekers

    def __str__(self):
        return self.username

    @classmethod
    def search_by_category(cls,search_term):
        jobs = cls.objects.filter(job_category__name__icontains=search_term)
        return jobs


class FileUpload(models.Model):
    name = models.CharField(max_length=100)
    pdf = models.FileField(upload_to='documents/pdfs/')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')

    def save_upload(self):
        self.save()

    def delete_upload(self):
        self.delete()
    
    @classmethod
    def update_upload(cls, id ,name,pdf ,user):
        update = cls.objects.filter(id = id).update(name = name,pdf = pdf,user=user)
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


class Payments(models.Model):
    first_name =models.CharField(max_length=144,null=True,blank=True)
    last_name = models.CharField(max_length=144,null=True,blank=True)
    phone = models.CharField(max_length=144,null=True,blank=True)

# previous projects
class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='portfolio')
    name = models.CharField(max_length=50)
    link=models.URLField(max_length=555)

    def save_portfolio(self):
        self.save()

    def delete_portfolio(self):
        self.delete()
    
    @classmethod
    def update_portfolio(cls, id ,name,link ,user):
        update = cls.objects.filter(id = id).update(name = name,link = link,user=user)
        return update

    @classmethod
    def get_all_portfolios(cls):
        portfolios = cls.objects.all()
        return portfolios

    @classmethod
    def get_portfolio_id(cls,id):
        portfolio_id = cls.objects.filter(id= id).all()
        return portfolio_id

    def __str__(self):
        return self.name

class Contact(models.Model):
    name = models.CharField(max_length = 30)
    email = models.EmailField()
    message = models.TextField()

    def save_contact(self):
        self.save()

    def delete_contact(self):
        self.delete()
    
    @classmethod
    def update_contact(cls, id ,name,email ,message):
        update = cls.objects.filter(id = id).update(name = name,email = email,message=message)
        return update

    @classmethod
    def get_all_contacts(cls):
        contacts = cls.objects.all()
        return contacts

    @classmethod
    def get_contact_id(cls,id):
        contact_id = cls.objects.filter(id= id).all()
        return contact_id
    
    def __str__(self):
        return self.name
