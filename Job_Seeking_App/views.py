from django.shortcuts import render,redirect
from .forms import JobseekerForm,AddJobseekerForm,employerForm,AddEmployerForm
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
        job_seeker_form=JobseekerForm(request.POST)
        add_jobseeker_form=AddJobseekerForm(request.POST)
        if job_seeker_form.is_valid() and add_jobseeker_form.is_valid():
            jobseeker=job_seeker_form.save()
            jobseeker.set_password(jobseeker.password)
            jobseeker.save()
            add_jobseeker=add_jobseeker_form.save(commit=False)
            add_jobseeker.is_jobseeker = True
            add_jobseeker.user=jobseeker
            add_jobseeker.save()
            registered=True
    else:
        job_seeker_form=JobseekerForm()
        add_jobseeker_form=AddJobseekerForm()
    return render(request,'registerJobseeker.html',{'job_seeker_form':job_seeker_form,'add_jobseeker_form':add_jobseeker_form,'registered':registered})


def registerEmployer(request):
    registered=False
    if request.method=='POST':
        employer_form=employerForm(request.POST)
        add_employer_form=AddEmployerForm(request.POST)
        if employer_form.is_valid() and add_employer_form.is_valid():
            employer=employer_form.save()
            employer.set_password(employer.password)
            employer.save()
            add_emplyer=add_employer_form.save(commit=False)
            add_emplyer.is_employer = True
            add_emplyer.user=employer
            add_emplyer.save()
            registered=True
    else:
        employer_form=employerForm()
        add_employer_form=AddEmployerForm()
        
    return render(request,'registerEmployer.html',{'employer_form':employer_form,'add_employer_form':add_employer_form,'registered':registered})
    
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
    if current.is_jobseeker:
        return redirect('jobseekerDash/')
    else:
        return redirect('employerDash/')
    return render(request,'dashboard.html')

    
def jobseekerDash(request):
    return render(request,'jobseekerDash.html')

def employerDash(request):
    return render(request,'employerDash.html')