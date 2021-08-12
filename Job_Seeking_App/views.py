from django.http.response import Http404
from .email import send_verification_email
from django.shortcuts import render,redirect, get_object_or_404
from .forms import *
from django.http import HttpResponse,HttpResponseRedirect,Http404,JsonResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from django.urls import reverse
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .decorators import unauthenticated_user,allowed_users,admin_only
import os
from .models import JobSeeker,Employer 
from .models import User

# from django_daraja.mpesa.core import MpesaClient

# Create your views here.

def index(request):
    return render(request,'index.html')

#signup and login
@unauthenticated_user
def register(request):
    return render(request,'registration/register.html')

#signup and jobseeker
@unauthenticated_user
def registerJobseeker(request):
    registered=False
    if request.method=='POST':
        job_seeker_form=UserSignUpForm(request.POST)
        if job_seeker_form.is_valid():
            user=job_seeker_form.save()
            user.refresh_from_db()
            user.email = job_seeker_form.cleaned_data.get('email')
            user.is_jobseeker = True
            group, created = Group.objects.get_or_create(name='jobseeker')
            group = Group.objects.get(name = 'jobseeker')
            user.groups.add(group)
            user.save()
            registered=True
            return redirect('login')
    else:
        job_seeker_form=UserSignUpForm()
    return render(request,'registration/registerJobseeker.html',{'job_seeker_form':job_seeker_form,'registered':registered})

#signup and employer

@unauthenticated_user
def registerEmployer(request):
    registered=False
    if request.method=='POST':
        employer_form=UserSignUpForm(request.POST)
        if employer_form.is_valid():
            user=employer_form.save()
            user.refresh_from_db()
            user.email = employer_form.cleaned_data.get('email')
            user.is_employer = True
            group, created = Group.objects.get_or_create(name='employer')
            group = Group.objects.get(name = 'employer')
            user.groups.add(group)
            user.save()
            registered=True
            return redirect('login')
    else:
        employer_form=UserSignUpForm()
        
    return render(request,'registration/registerEmployer.html',{'employer_form':employer_form,'registered':registered})


#Login users

@unauthenticated_user   
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


#Redirect users to their respective dashboards

@login_required
def dashboard(request):
    current = request.user
    if current.is_employer:
        return redirect('employer_profile/')
    elif current.is_admin:
        return redirect('admin_dashboard')
    else: 
        return redirect('jobseekerDash/')


#jobseeker profile and profile update

@login_required
@allowed_users(allowed_roles=['admin','jobseeker'])
def jobseeker_profile(request):
  current_user = request.user
  documents = FileUpload.objects.filter(jobseeker_id = current_user.id).all()
  
  return render(request,'jobseekers/profile.html',{"documents":documents,"current_user":current_user})

@login_required
@allowed_users(allowed_roles=['admin','jobseeker'])
def update_jobseeker_profile(request):
  if request.method == 'POST':
    user_form = UpdateUserProfile(request.POST,request.FILES,instance=request.user)
    jobseeker_form = UpdateJobseekerProfile(request.POST,instance=request.user.profile)
    if user_form.is_valid() and jobseeker_form.is_valid():
      user_form.save()
      jobseeker_form.save()
      messages.success(request,'Your Profile account has been updated successfully')
      return redirect('jobseeker_profile')
  else:
    user_form = UpdateUserProfile(instance=request.user)
    jobseeker_form = UpdateJobseekerProfile(instance=request.user.profile) 
  params = {
    'user_form':user_form,
    'jobseeker_form':jobseeker_form
  }
  return render(request,'jobseekers/update.html',params)

@login_required
@allowed_users(allowed_roles=['admin','jobseeker'])
def jobseekerDash(request):
    return render(request,'jobseekers/jobseeker_dashboard.html')


#jobseekers upload resumes

@login_required
@allowed_users(allowed_roles=['admin','jobseeker'])
def upload_file(request):
    if request.method == 'POST':
        upload_form = UploadFileForm(request.POST, request.FILES)
        if upload_form.is_valid():
            upload = upload_form.save(commit=False)
            upload.jobseeker = request.user.profile
            upload.save()
            return redirect('jobseeker_profile')
    else:
        upload_form = UploadFileForm()
    return render(request, 'jobseekers/upload_file.html', {'upload_form': upload_form})


# jobseekers Add portfolio
@login_required
def add_portfolios(request):
  if request.method == 'POST':
    port_form=AddPortfolio(request.POST,request.FILES)
    if port_form.is_valid():
      portfolio = port_form.save(commit=False)
      portfolio.jobseeker = request.user.profile
      portfolio.save()
      messages.success(request,'Your Portfolio has been added')
      print(port_form)
      return redirect('jobseeker_profile')

  else:
    port_form = AddPortfolio()
  context = {
    'port_form': port_form,
    }
  return render(request,"jobseekers/portfolio.html",context)


#Employers dashboard to view all available jobseekers

# Mpesa payment
def getAccessToken(request):
    consumer_key = os.environ.get("CONSUMER_KEY")
    consumer_secret = os.environ.get("CONSUMER_SECRET")
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return HttpResponse(validated_mpesa_access_token)

def success(request):
  return render('mpesa/success.html')

def stk_push_callback(request):
  data = request.body
  # You can do whatever you want with the notification received from MPESA here.

# employers and misc
@login_required
@allowed_users(allowed_roles=['admin','employer'])
def employerDash(request):
    user = request.user
    payment_form = PaymentForm()
    job_seekers = User.objects.filter(verified = True,is_jobseeker = True).all()
    employer=Employer.objects.all()
    
    context={
        "job_seekers":job_seekers,
        "employer":employer,
        "payment_form":payment_form
    }
    return render(request,'employers/employer_dashboard.html',context)


#Employers profile and update profile

@login_required
@allowed_users(allowed_roles=['admin','employer'])
def employerProfile(request):
    employer=request.user
    available=User.objects.filter(is_jobseeker= True,verified=True).all() # notifications on avialable jobseeker
    context={
        "employer":employer,
        "available":available,
    }
    return render(request,'employers/employer_profile.html',context)


@login_required
@allowed_users(allowed_roles=['admin','employer'])
def update_employer(request):
  if request.method == 'POST':
    u_form = UpdateUserProfile(request.POST,request.FILES,instance=request.user)
    p_form = UpdateEmployerProfile(request.POST,instance=request.user.employer)
    if u_form.is_valid() and p_form.is_valid():
      u_form.save()
      p_form.save()
      messages.success(request,'Your Profile account has been updated successfully')
      return redirect('employer_profile')
  else:
    u_form = UpdateUserProfile(instance=request.user)
    p_form = UpdateEmployerProfile(instance=request.user.employer) 
  context = {
    'u_form':u_form,
    'p_form':p_form
  }
  return render(request,'employers/update_employer.html',context)

  
#Employers view details of a specific_jobseeker


@login_required
@allowed_users(allowed_roles=['admin','employer'])
def single_jobseeker(request,jobseeker_id):
  try:
    jobseeker =get_object_or_404(JobSeeker, pk = jobseeker_id)
    documents = FileUpload.objects.filter(jobseeker_id = jobseeker_id)
    portfolios=Portfolio.objects.filter(jobseeker_id = jobseeker_id)

  except ObjectDoesNotExist:
    raise Http404()

  return render(request,'employers/single_jobseeker.html',{'documents':documents, 'jobseeker':jobseeker,"portfolios":portfolios})


#Admin

#Admin view for all jobseekers and employers

@login_required
@admin_only
def adminDash(request):
    jobseekers=JobSeeker.objects.all()
    employers=Employer.objects.all()
    all_employers= User.objects.filter(is_employer=True).all()
    all_jobseekers = User.objects.filter(is_jobseeker=True).all()
    verified_jobseekers = User.objects.filter(verified=True,is_jobseeker = True).all()
    unverified_jobseekers = User.objects.filter(verified = False,is_jobseeker = True).all()
    verified_employers = User.objects.filter(verified=True,is_employer = True).all()
    unverified_employers = User.objects.filter(verified = False,is_employer = True).all()
    return render(request,'admin/admin_dashboard.html',{"unverified_employers":unverified_employers  ,"verified_employers":verified_employers  ,"all_employers":all_employers ,"employers":employers ,"jobseekers":jobseekers,'verified_jobseekers':verified_jobseekers,'unverified_jobseekers':unverified_jobseekers,'all_jobseekers':all_jobseekers})

# ADMIN VIEWS
# JobSeeker views
@allowed_users(allowed_roles=['admin'])
@login_required
def all_jobseekers(request):
    all_jobseekers = User.objects.filter(is_jobseeker=True).all()
    return render(request,'admin/jobseekers/all_jobseekers.html',{'all_jobseekers':all_jobseekers})

@login_required
@allowed_users(allowed_roles=['admin'])
def verified_jobseekers(request):
    verified_jobseekers = User.objects.filter(verified=True,is_jobseeker = True).all()
    return render(request,'admin/jobseekers/verified_jobseekers.html',{'verified_jobseekers':verified_jobseekers})

@login_required
@allowed_users(allowed_roles=['admin'])
def unverified_jobseekers(request):
    unverified_jobseekers = User.objects.filter(verified = False,is_jobseeker = True).all()
    return render(request,'admin/jobseekers/unverified_jobseekers.html',{'unverified_jobseekers':unverified_jobseekers})

@login_required
@allowed_users(allowed_roles=['admin'])
def verify_jobseeker(request, jobseeker_id):
  user = User.objects.get(pk=jobseeker_id)
  name = user.username
  email = user.email
  if request.method == 'POST':
    verify_jobseeker_form = AdminVerifyUserForm(request.POST,request.FILES, instance=user)
    if verify_jobseeker_form.is_valid():
      verify_jobseeker_form.save()
      send_verification_email(name, email)
      data = {'success': 'Verification sent'}
      messages.success(request, f'jobseeker updated!')
      return redirect('admin_dashboard')
  else:
    verify_jobseeker_form = AdminVerifyUserForm(instance=user)

  return render(request, 'admin/jobseekers/verify_jobseeker.html', {"verify_jobseeker_form":verify_jobseeker_form})

@login_required
@allowed_users(allowed_roles=['admin'])
def delete_jobseeker(request,jobseeker_id):
  jobseeker = User.objects.get(pk=jobseeker_id)
  if jobseeker:
    jobseeker.delete_user()
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#Get single jobseeker
@login_required
@allowed_users(allowed_roles=['admin'])
def jobseeker_details(request,jobseeker_id):
  try:
    jobseeker =get_object_or_404(JobSeeker, pk = jobseeker_id)

  except ObjectDoesNotExist:
    raise Http404()

  return render(request,'admin/jobseekers/jobseeker_details.html',{'jobseeker':jobseeker})


  #Admin Employer views
@login_required
@allowed_users(allowed_roles=['admin'])
def all_employers(request):
    all_employers = User.objects.filter(is_employer=True).all()
    return render(request,'admin/employers/all_employers.html',{'all_employers':all_employers})

@login_required
@allowed_users(allowed_roles=['admin'])
def verified_employers(request):
    verified_employers = User.objects.filter(verified = True,is_employer = True).all()
    return render(request,'admin/employers/verified_employers.html',{'verified_employers':verified_employers})

@login_required
@allowed_users(allowed_roles=['admin'])
def unverified_employers(request):
    unverified_employers = User.objects.filter(verified = False,is_employer=True).all()
    return render(request,'admin/employers/unverified_employers.html',{'unverified_employers':unverified_employers})

@login_required
@allowed_users(allowed_roles=['admin'])
def verify_employer(request, employer_id):
  employer = User.objects.get(pk=employer_id)
  if request.method == 'POST':
    update_employer_form = AdminVerifyUserForm(request.POST,request.FILES, instance=employer)
    if update_employer_form.is_valid():
      update_employer_form.save()
      messages.success(request, f'employer verified!')
      return redirect('admin_dashboard')
  else:
    update_employer_form = AdminVerifyUserForm(instance=employer)

  return render(request, 'admin/employers/update_employer.html', {"update_employer_form":update_employer_form})

@login_required
@allowed_users(allowed_roles=['admin'])
def delete_employer(request,employer_id):
  employer = User.objects.get(pk=employer_id)
  if employer:
    employer.delete_user()
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#Get single employer
@login_required
@allowed_users(allowed_roles=['admin'])
def employer_details(request,employer_id):
  try:
    employer =get_object_or_404(Employer, pk = employer_id)
    
  
  except ObjectDoesNotExist:
    raise Http404()

  return render(request,'admin/employers/employers_details.html',{'employer':employer})

#                           admin calender

def calender(request):
  return render(request,'admin/calender.html')


# Search View

def search_results(request):

    if 'jobseeker' in request.GET and request.GET["jobseeker"]:
        search_term = request.GET.get("jobseeker")
        searched_jobseekers_by_category = JobSeeker.search_by_category(search_term)
        results = [*searched_jobseekers_by_category]
        message = f"{search_term}"

        return render(request, 'employers/search.html',{"message":message,"jobseekers": results})

    else:
        message = "You haven't searched for any term"
        return render(request, 'employers/search.html',{"message":message})

def jobseeker(request):
    jobseekers = JobSeeker.objects.all()
    
    return render(request,"jobseeker.html", {"jobseekers":jobseekers})
