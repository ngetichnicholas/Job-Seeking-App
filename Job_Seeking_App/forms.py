from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import fields
from .models import User
from .models import *

class UserSignUpForm(UserCreationForm):

  class Meta:
    model = User
    fields = ('username', 'email', 'password1', 'password2', )

class UpdateJobseekerProfile(forms.ModelForm):
  class Meta:
    model = JobSeeker
    fields = ('job_category','availability', 'salary','bio')

class UpdateUserProfile(forms.ModelForm):
  email = forms.EmailField()
  class Meta:
    model = User
    fields = ['username','first_name', 'last_name','email','phone','location', 'profile_picture']

class UploadFileForm(forms.ModelForm):
    class Meta:
        model = FileUpload
        fields = ('name','pdf')

class AdminVerifyUserForm(forms.ModelForm):
  verified = forms.BooleanField()

  class Meta:
    model = User

    fields = ('verified',)

class UpdateEmployerProfile(forms.ModelForm):
    class Meta:
        model = Employer
        fields = ('company_name',  )

# update and add portfolio
class AddPortfolio(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ('name','link',  )

class VerifyEmployer(forms.ModelForm):
  class Meta:
    model = Payments
    fields = ['first_name', 'last_name','mpesa_number']
