from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from .models import *

class JobseekerSignUpForm(UserCreationForm):
  email = forms.EmailField(max_length=150, help_text='Email')


  class Meta:
    model = User
    fields = ('username', 'email', 'password1', 'password2', )

class UpdateJobseekerProfile(forms.ModelForm):
  class Meta:
    model = JobSeeker
    fields = ('phone', 'availability', 'salary','location', 'bio', 'profile_picture', )

class UpdateJobseeker(forms.ModelForm):
  email = forms.EmailField()
  class Meta:
    model = User
    fields = ['username','first_name', 'last_name','email']

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ('name','pdf')

class AdminVerifyUserForm(forms.ModelForm):
  verified = forms.BooleanField()

  class Meta:
    model = User

    fields = ('verified',)


class EmployerSignUpForm(UserCreationForm):
  email = forms.EmailField(max_length=150, help_text='Email')

  class Meta:
    model = User
    fields = ('username', 'email', 'password1', 'password2', )


class UpdateEmployerForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = Employer
        fields = ( 'first_name', 'last_name', 'email', 'phone',  'location', 'company_name', )

class UpdateEmployerProfile(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ('profile_picture', )
