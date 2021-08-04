from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.dispatch import receiver
from django.db.models.signals import post_save

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
class Jobseeker_Profile(models.Model):
    is_jobseeker = models.BooleanField(default=True)
    jobseeker=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_photo = CloudinaryField('profile_photo',blank=True)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=60, blank=True)
    contact = models.CharField(max_length=60,blank=True)
    education = models.CharField(max_length=144,blank=True)
    create_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        Jobseeker_Profile.objects.create(user=instance)
    instance.profile.save()