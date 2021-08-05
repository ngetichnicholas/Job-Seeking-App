from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User
from .models import JobSeeker,Employer

class JobseekerSignUpForm(UserCreationForm):
  first_name = forms.CharField(max_length=100, help_text='Last Name')
  last_name = forms.CharField(max_length=100, help_text='Last Name')
  email = forms.EmailField(max_length=150, help_text='Email')
  phone = forms.CharField(max_length=10, help_text='Phone Number')


  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email','phone', 'password1', 'password2', )

class EmployerSignUpForm(UserCreationForm):
  first_name = forms.CharField(max_length=100, help_text='Last Name')
  last_name = forms.CharField(max_length=100, help_text='Last Name')
  email = forms.EmailField(max_length=150, help_text='Email')
  phone = forms.CharField(max_length=10, help_text='Phone Number')


  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name', 'email','phone', 'password1', 'password2', )


class UpdateEmployerForm(forms.ModelForm):
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = Employer
        fields = ('first_name', 'last_name', 'email','phone', )

