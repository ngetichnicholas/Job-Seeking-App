from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.forms import fields
from .models import User
from .models import *
from django.core.validators import MinLengthValidator


class UserSignUpForm(UserCreationForm):
    password1 = forms.CharField(label='Enter password', 
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', 
                                widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=("username","email","password1","password2")
        help_texts = {
            "username":None,
        }

class UpdateJobseekerProfile(forms.ModelForm):
  class Meta:
    model = User
    fields = ('job_category','availability', 'salary')

class UpdateUserProfile(forms.ModelForm):
  email = forms.EmailField()
  class Meta:
    model = User
    fields = ['username','first_name', 'last_name','email','phone','location', 'profile_picture','bio']

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
        model = User
        fields = ('company_name',  )

# update and add portfolio
class AddPortfolio(forms.ModelForm):
    class Meta:
        model = Portfolio
        fields = ('name','link',  )

class PaymentForm(forms.ModelForm):
  class Meta:
    model = User
    fields = ['first_name', 'last_name','phone']

class ContactForm(forms.ModelForm):
    class Meta:
      model = Contact
      fields = ['name','email','message']
