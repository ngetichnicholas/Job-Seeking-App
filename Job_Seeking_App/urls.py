from django.urls import path
from . import views as app_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',app_views.index,name='index'),
    path('register/',app_views.register,name='register'),
    path('registerJobseeker/',app_views.registerJobseeker,name='registerJobseeker'),
    path('registerEmployer/',app_views.registerEmployer,name='registerEmployer'),
    path('accounts/login/',app_views.login,name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name = 'registration/logout.html'),name='logout'),
    path('jobseekerDash/',app_views.jobseekerDash,name='jobseekerDash'),
    path('dashboard',app_views.dashboard,name='dashboard'),
    path('jobseekerDash/',app_views.jobseekerDash,name='jobseekerDash'),
    path('employerDash/',app_views.employerDash,name='employerDash'),

    path('admin_dashboard/',app_views.adminDash,name='admin_dashboard'),
    path('all_jobseekers',app_views.all_jobseekers,name='all_jobseekers'),
    path('verified_jobseekers',app_views.verified_jobseekers,name='verified_jobseekers'),
    path('unverified_jobseekers',app_views.unverified_jobseekers,name='unverified_jobseekers'),
    path('verify_jobseeker/<int:jobseeker_id>',app_views.verify_jobseeker,name='verify_jobseeker'),
    path('delete_jobseeker/<int:jobseeker_id>', app_views.delete_jobseeker,name='delete_jobseeker'),
    path('jobseeker_details/<int:jobseeker_id>', app_views.jobseeker_details,name='jobseeker_details'),
    
    path('employer_profile/<id>',app_views.employerProfile,name='employer_profile'),
]
