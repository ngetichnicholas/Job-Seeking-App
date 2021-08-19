from django.http.response import Http404
from .email import *
from django.shortcuts import render,redirect, get_object_or_404
from .forms import *
from django.http import HttpResponse,HttpResponseRedirect,Http404,JsonResponse
import requests
from requests.auth import HTTPBasicAuth
import json
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
from .models import *
from mpesa.models import Payment as MpesaPayment
from django.http import FileResponse

import webbrowser
# Create your views here.

def index(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def services(request):
    return render(request,'services.html')

def contact(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    message = request.POST.get('message')
    if request.method == 'POST':
      contact_form = ContactForm(request.POST)
      if contact_form.is_valid():
        contact_form.save()
        send_contact_email(name, email)
        data = {'success': 'Your message has been reaceived. Thank you for contacting us, we will get back to you shortly'}
        messages.success(request, f"Message submitted successfully")
    else:
      contact_form = ContactForm()
    return render(request,'contact.html',{'contact_form':contact_form})

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
        return redirect('employerDash/')
    elif current.is_admin:
        return redirect('admin_dashboard')
    else: 
        return redirect('jobseekerDash/')


#jobseeker profile and profile update

@login_required
@allowed_users(allowed_roles=['admin','jobseeker'])
def jobseeker_profile(request):
  current_user = request.user
  documents = FileUpload.objects.filter(user_id = current_user.id).all()
  
  return render(request,'jobseekers/profile.html',{"documents":documents,"current_user":current_user})

@login_required
@allowed_users(allowed_roles=['admin','jobseeker'])
def update_jobseeker_profile(request):
  if request.method == 'POST':
    user_form = UpdateUserProfile(request.POST,request.FILES,instance=request.user)
    jobseeker_form = UpdateJobseekerProfile(request.POST,instance=request.user)
    if user_form.is_valid() and jobseeker_form.is_valid():
      user_form.save()
      jobseeker_form.save()
      messages.success(request,'Your Profile account has been updated successfully')
      return redirect('jobseekerDash')
  else:
    user_form = UpdateUserProfile(instance=request.user)
    jobseeker_form = UpdateJobseekerProfile(instance=request.user) 
  params = {
    'user_form':user_form,
    'jobseeker_form':jobseeker_form
  }
  return render(request,'jobseekers/update.html',params)

@login_required
@allowed_users(allowed_roles=['admin','jobseeker'])
def jobseekerDash(request):
    current_user = request.user
    documents = FileUpload.objects.filter(user_id = current_user.id).all()
    portfolios=Portfolio.objects.filter(user_id = current_user.id)
    return render(request,'jobseekers/jobseeker_dashboard.html',{"documents":documents,"portfolios":portfolios})


#jobseekers upload resumes

@login_required
@allowed_users(allowed_roles=['admin','jobseeker'])
def upload_file(request):
    if request.method == 'POST':
        upload_form = UploadFileForm(request.POST, request.FILES)
        if upload_form.is_valid():
            upload = upload_form.save(commit=False)
            upload.user = request.user
            upload.save()
            messages.success(request,"File uploaded successfully")
            return redirect('jobseekerDash')
    else:
        upload_form = UploadFileForm()
    return render(request, 'jobseekers/upload_file.html', {'upload_form': upload_form})

def pdf_view(request,file_id):
    file =get_object_or_404(FileUpload, pk = file_id)
    image_data = open(f"/home/moringa/Documents/Core-Django/Job-Seeking-App/media/{file.pdf}", "rb").read()
    return HttpResponse(image_data, content_type="application/pdf")


# jobseekers Add portfolio
@login_required
def add_portfolios(request):
  if request.method == 'POST':
    port_form=AddPortfolio(request.POST,request.FILES)
    if port_form.is_valid():
      portfolio = port_form.save(commit=False)
      portfolio.user = request.user
      portfolio.save()
      messages.success(request,'Your Portfolio has been added')
      print(port_form)
      return redirect('jobseekerDash')

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
    payment_form = PaymentForm(instance=request.user)
    job_seekers = User.objects.filter(verified = True,is_jobseeker = True).all()
    employer=User.objects.all()
    
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
    p_form = UpdateEmployerProfile(request.POST,instance=request.user)
    if u_form.is_valid() and p_form.is_valid():
      u_form.save()
      p_form.save()
      messages.success(request,'Your Profile account has been updated successfully')
      return redirect('employerDash')
  else:
    u_form = UpdateUserProfile(instance=request.user)
    p_form = UpdateEmployerProfile(instance=request.user) 
  context = {
    'u_form':u_form,
    'p_form':p_form
  }
  return render(request,'employers/update_employer.html',context)

  
#Employers view details of a specific_jobseeker


@login_required
@allowed_users(allowed_roles=['admin','employer'])
def single_jobseeker(request,user_id):
  try:
    jobseeker =get_object_or_404(User, pk = user_id)
    documents = FileUpload.objects.filter(user_id = user_id)
    portfolios=Portfolio.objects.filter(user_id = user_id)

  except ObjectDoesNotExist:
    raise Http404()

  return render(request,'employers/single_jobseeker.html',{'documents':documents, 'jobseeker':jobseeker,"portfolios":portfolios})


#Admin

#Admin view for all jobseekers and employers

@login_required
@admin_only
def adminDash(request):
    all_employers= User.objects.filter(is_employer=True).all()
    all_jobseekers = User.objects.filter(is_jobseeker=True).all()
    verified_jobseekers = User.objects.filter(verified=True,is_jobseeker = True).all()
    unverified_jobseekers = User.objects.filter(verified = False,is_jobseeker = True).all()
    verified_employers = User.objects.filter(verified=True,is_employer = True).all()
    unverified_employers = User.objects.filter(verified = False,is_employer = True).all()
    return render(request,'admin/admin_dashboard.html',{"unverified_employers":unverified_employers  ,"verified_employers":verified_employers  ,"all_employers":all_employers ,'verified_jobseekers':verified_jobseekers,'unverified_jobseekers':unverified_jobseekers,'all_jobseekers':all_jobseekers})

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
def verify_jobseeker(request, user_id):
  user = User.objects.get(pk=user_id)
  name = user.username
  email = user.email
  if request.method == 'POST':
    verify_jobseeker_form = AdminVerifyUserForm(request.POST,request.FILES, instance=user)
    if verify_jobseeker_form.is_valid():
      verify_jobseeker_form.save()
      send_verification_email(name, email)
      data = {'success': 'Verification email sent'}
      messages.success(request, f'jobseeker verified succesfully!')
      return redirect('admin_dashboard')
  else:
    verify_jobseeker_form = AdminVerifyUserForm(instance=user)

  return render(request, 'admin/jobseekers/verify_jobseeker.html', {"verify_jobseeker_form":verify_jobseeker_form})

@login_required
@allowed_users(allowed_roles=['admin'])
def delete_jobseeker(request,user_id):
  jobseeker = User.objects.get(pk=user_id)
  if jobseeker:
    jobseeker.delete_user()
    messages.success(request, f'User deleted successfully!')
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#Get single jobseeker
@login_required
@allowed_users(allowed_roles=['admin'])
def jobseeker_details(request,user_id):
  try:
    jobseeker =get_object_or_404(User, pk = user_id)
    documents = FileUpload.objects.filter(user_id = user_id).all()
    portfolios=Portfolio.objects.filter(user_id = user_id).all()

  except ObjectDoesNotExist:
    raise Http404()

  return render(request,'admin/jobseekers/jobseeker_details.html',{'jobseeker':jobseeker,'documents':documents,'portfolios':portfolios})


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
def verify_employer(request, user_id):
  employer = User.objects.get(pk=user_id)
  name = employer.username
  email = employer.email
  if request.method == 'POST':
    update_employer_form = AdminVerifyUserForm(request.POST,request.FILES, instance=employer)
    if update_employer_form.is_valid():
      update_employer_form.save()
      send_verification_email(name, email)
      data = {'success': 'Verification email sent'}
      messages.success(request, f'employer verified!')
      return redirect('admin_dashboard')
  else:
    update_employer_form = AdminVerifyUserForm(instance=employer)

  return render(request, 'admin/employers/update_employer.html', {"update_employer_form":update_employer_form})

@login_required
@allowed_users(allowed_roles=['admin'])
def delete_employer(request,user_id):
  employer = User.objects.get(pk=user_id)
  if employer:
    employer.delete_user()
    messages.success(request, f'User deleted successfully!')
  return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

#Get all payments
@login_required
@allowed_users(allowed_roles=['admin'])
def payments(request):
  payments = MpesaPayment.objects.all().order_by('-TransactionDate')
  
  return render(request, 'admin/employers/payments.html',{'payments':payments})

#Get single employer
@login_required
@allowed_users(allowed_roles=['admin'])
def employer_details(request,user_id):
  try:
    employer =get_object_or_404(User, pk = user_id)
    
  
  except ObjectDoesNotExist:
    raise Http404()

  return render(request,'admin/employers/employers_details.html',{'employer':employer})

#                           admin calender

def calender(request):
  return render(request,'admin/calender.html')


# Search View
def search_jobseekers(request):
  if 'job_category' in request.GET and request.GET["job_category"]:
    search_term = request.GET.get("job_category")
    searched_jobseekers = User.search_jobseekers_by_job_category(search_term)
    message = f"{search_term}"

    return render(request, 'employers/search.html', {"message":message,"jobseekers":searched_jobseekers})

  else:
    message = 'You have not searched for any term'
    return render(request, 'employers/search.html', {"message":message})
