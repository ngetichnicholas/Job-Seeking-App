from django import forms
from django.contrib.auth.models import User
from .models import JobSeeker,Employer
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm,
from django.forms.utils import ErrorList
from django.urls import reverse_lazy




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

class UsersLoginForm(ErrorListMixin, AuthenticationForm):
    def clean_username(self):
        username = self.cleaned_data.get('username')
        
        if username is not None:
            user = get_user_model().objects.filter(email=username).first()

            if user is None:
                return self.get_invalid_login_error()

            if not user.is_active:
                link = reverse_lazy('users:account_activation_request')
                error_message = f"Account has not been activated! <a href={link}>Click here to resend activation link</a>"
                raise ValidationError(mark_safe(error_message))
            
        return username
