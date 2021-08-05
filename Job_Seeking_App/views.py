from django.http.response import Http404
from django.shortcuts import render,redirect, get_object_or_404
from .forms import *
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist


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
def jobseeker_profile(request):
  current_user = request.user
  documents = FileUpload.objects.filter(jobseeker_id = current_user.id).all()
  
  return render(request,'jobseekers/profile.html',{"documents":documents,"current_user":current_user})

@login_required
def update_jobseeker_profile(request):
  if request.method == 'POST':
    user_form = UpdateJobseeker(request.POST,instance=request.user)
    profile_form = UpdateJobseekerProfile(request.POST,request.FILES,instance=request.user.profile)
    if user_form.is_valid() and profile_form.is_valid():
      user_form.save()
      profile_form.save()
      messages.success(request,'Your Profile account has been updated successfully')
      return redirect('jobseeker_profile')
  else:
    user_form = UpdateJobseeker(instance=request.user)
    profile_form = UpdateJobseekerProfile(instance=request.user.profile) 
  params = {
    'user_form':user_form,
    'profile_form':profile_form
  }
  return render(request,'jobseekers/update.html',params)

@login_required
def jobseekerDash(request):
    return render(request,'jobseekerDash.html')

@login_required
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


@login_required
def employerDash(request):
    employer=Employer.objects.all()
    job_seekers=JobSeeker.objects.all()
    context={
        "job_seekers":job_seekers,
        "employer":employer
    }
    return render(request,'employerDash.html',context)

@login_required
def employerProfile(request,id):
    form=UpdateEmployerForm
    employer=Employer.objects.get(id=id)
    context={
        "employer":employer,
        "form":form
    }
    return render(request,'employer_profile.html',context)





@login_required
def adminDash(request):
    all_jobseekers = User.objects.filter(is_jobseeker=True).all()
    verified_jobseekers = JobSeeker.objects.filter(verified=True).all()
    unverified_jobseekers = JobSeeker.objects.filter(verified = False).all()
    return render(request,'admin/admin_dashboard.html',{'verified_jobseekers':verified_jobseekers,'unverified_jobseekers':unverified_jobseekers,'all_jobseekers':all_jobseekers})

# ADMIN VIEWS
# JobSeeker views
@login_required
def all_jobseekers(request):
    all_jobseekers = JobSeeker.objects.all()
    return render(request,'admin/jobseekers/all_jobseekers.html',{'all_jobseekers':all_jobseekers})

@login_required
def verified_jobseekers(request):
    verified_jobseekers = JobSeeker.objects.filter(verified = True).all()
    return render(request,'admin/jobseekers/verified_jobseekers.html',{'verified_jobseekers':verified_jobseekers})

@login_required
def unverified_jobseekers(request):
    unverified_jobseekers = JobSeeker.objects.filter(verified=False).all()
    return render(request,'admin/jobseekers/unverified_jobseekers.html',{'unverified_jobseekers':unverified_jobseekers})

@login_required
def verify_jobseeker(request, jobseeker_id):
  jobseeker = JobSeeker.objects.get(pk=jobseeker_id)
  if request.method == 'POST':
    update_jobseeker_form = AdminJobseekerVerifyForm(request.POST,request.FILES, instance=jobseeker)
    if update_jobseeker_form.is_valid():
      update_jobseeker_form.save()
      messages.success(request, f'jobseeker updated!')
      return redirect('admin_dashboard')
  else:
    update_jobseeker_form = AdminJobseekerVerifyForm(instance=jobseeker)

  return render(request, 'admin/jobseekers/update_jobseeker.html', {"update_jobseeker_form":update_jobseeker_form})

@login_required
def delete_jobseeker(request,jobseeker_id):
  jobseeker = JobSeeker.objects.get(pk=jobseeker_id)
  if jobseeker:
    jobseeker.delete_jobseeker()
  return redirect('admin_dashboard')

#Get single jobseeker
@login_required
def jobseeker_details(request,jobseeker_id):
  try:
    jobseeker =get_object_or_404(JobSeeker, pk = jobseeker_id)

  except ObjectDoesNotExist:
    raise Http404()

  return render(request,'admin/jobseekers/jobseeker_details.html',{'jobseeker':jobseeker})