from django.shortcuts import render,redirect
from .forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages

from .models import JobSeeker,Employer 
from .models import User

# Create your views here.

def index(request):
    return render(request,'index.html')

def register(request):
    return render(request,'register.html')

def registerJobseeker(request):
    registered=False
    if request.method=='POST':
        job_seeker_form=JobseekerSignUpForm(request.POST)
        if job_seeker_form.is_valid():
            user=job_seeker_form.save()
            user.refresh_from_db()
            user.profile.first_name = job_seeker_form.cleaned_data.get('first_name')
            user.profile.last_name = job_seeker_form.cleaned_data.get('last_name')
            user.profile.email = job_seeker_form.cleaned_data.get('email')
            user.profile.phone = job_seeker_form.cleaned_data.get('phone')
            user.is_jobseeker = True
            user.save()
            registered=True
    else:
        job_seeker_form=JobseekerSignUpForm()
    return render(request,'registration/registerJobseeker.html',{'job_seeker_form':job_seeker_form,'registered':registered})


def registerEmployer(request):
    registered=False
    if request.method=='POST':
        employer_form=EmployerSignUpForm(request.POST)
        if employer_form.is_valid():
            user=employer_form.save()
            user.refresh_from_db()
            user.employer.first_name = employer_form.cleaned_data.get('first_name')
            user.employer.last_name = employer_form.cleaned_data.get('last_name')
            user.employer.email = employer_form.cleaned_data.get('email')
            user.employer.phone = employer_form.cleaned_data.get('phone')
            user.is_employer = True
            user.save()
            registered=True
    else:
        employer_form=EmployerSignUpForm()
        
    return render(request,'registration/registerEmployer.html',{'employer_form':employer_form,'registered':registered})
    
def login(request):
  if request.method == 'POST':
    form = AuthenticationForm(request=request, data=request.POST)
    if form.is_valid():
      username = form.cleaned_data.get('username')
      email = form.cleaned_data.get('email')
      phone = form.cleaned_data.get('phone')
      password = form.cleaned_data.get('password')
      user = authenticate(username=username,email=email,phone=phone, password=password)
      if user is not None:
        auth_login(request, user)
        messages.info(request, f"You are now logged in as {username}")
        return redirect('index')
      else:
        messages.error(request, "Invalid username or password.")
    else:
      messages.error(request, "Invalid username or password.")
  form = AuthenticationForm()
  return render(request = request,template_name = "registration/login.html",context={"form":form})

@login_required
def dashboard(request):
    current = request.user
    if current.is_employer:
        return redirect('employerDash/')
    elif current.is_admin:
        return redirect('admin_dashboard')
    else: 
        return redirect('jobseekerDash/')
    return render(request,'dashboard.html')

@login_required
def jobseekerDash(request):
    return render(request,'jobseekerDash.html')


@login_required
def employerDash(request):
    
    job_seekers=JobSeeker.objects.all()
    context={
        "job_seekers":job_seekers,
    }
    return render(request,'employerDash.html',context)





@login_required
def adminDash(request):
    jobseekers = User.objects.filter(is_jobseeker=True).all()
    return render(request,'admin/admin_dashboard.html',{'jobseekers':jobseekers})

