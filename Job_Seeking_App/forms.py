from django import forms
from django.contrib.auth.models import User
from .models import JobSeeker,Employer
from django.contrib.auth.forms import UserCreationForm

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

class SignUpForm(UserCreationForm):

    username = forms.CharField( widget=forms.TextInput(attrs={"class":"form-control",
                                                               "placeholder":"Username"}))
    email = forms.CharField( widget=forms.TextInput(attrs={"class":"form-control",
                                                               "placeholder":"Email"}))
    phone = forms.CharField( widget=forms.TextInput(attrs={"class":"form-control",
                                                               "placeholder":"telephone number"}))

    password1 = forms.CharField(label='Password',  widget=forms.PasswordInput(attrs={"class":"form-control",
                                                               "placeholder":"Password"}))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={"class":"form-control",
                                                               "placeholder":"Confirm Password"}))
    class Meta:
        model = User
        fields = ('username','email', 'phone','password1', 'password2',)