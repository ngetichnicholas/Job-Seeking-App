from django import forms
from .models import Jobs, User
from .models import JobSeeker,Employer

class JobseekerForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model=User
        fields=['first_name','last_name','username','email','password']

class AddJobseekerForm(forms.ModelForm):
    class Meta():
        model=JobSeeker
        fields=['phone','location']

class employerForm(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model=User
        fields=['first_name','last_name','username','email','password']

class AddEmployerForm(forms.ModelForm):
    class Meta():
        model=Employer
        fields=['phone','location']

class JobsForm(forms.ModelForm):
    class Meta():
        model=Jobs
        fields= '__all__'

