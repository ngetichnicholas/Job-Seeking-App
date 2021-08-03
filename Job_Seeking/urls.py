"""Job_Seeking URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include, path

from Job_Seeking_App.views import jobseeking, jobseeker, employer

urlpatterns = [
    path('', include('Job_Seeking_App.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/',jobseeking.SignUpView.as_view(), name='signup'),
    path('accounts/signup/jobseeker/', jobseeker.JobseekerSignUpView.as_view(), name='jobseeker_signup'),
    path('accounts/signup/employer/', employer.EmployerSignUpView.as_view(), name='employer_signup'),
]