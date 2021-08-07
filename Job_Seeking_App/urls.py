from django.urls import path
from . import views as app_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static

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
    path('upload_file',app_views.upload_file,name='upload_file'),
    path('accounts/profile/',app_views.jobseeker_profile,name='jobseeker_profile'),
    path('update_jobseeker_profile/',app_views.update_jobseeker_profile,name='update_jobseeker_profile'),

    path('admin_dashboard/',app_views.adminDash,name='admin_dashboard'),
    path('all_jobseekers',app_views.all_jobseekers,name='all_jobseekers'),
    path('verified_jobseekers',app_views.verified_jobseekers,name='verified_jobseekers'),
    path('unverified_jobseekers',app_views.unverified_jobseekers,name='unverified_jobseekers'),
    path('verify_jobseeker/<int:jobseeker_id>',app_views.verify_jobseeker,name='verify_jobseeker'),
    path('delete_jobseeker/<int:jobseeker_id>', app_views.delete_jobseeker,name='delete_jobseeker'),
    path('jobseeker_details/<int:jobseeker_id>', app_views.jobseeker_details,name='jobseeker_details'),

    path('all_employers',app_views.all_employers,name='all_employers'),
    path('verified_employers',app_views.verified_employers,name='verified_employers'),
    path('unverified_employers',app_views.unverified_employers,name='unverified_employers'),
    path('verify_employer/<int:employer_id>',app_views.verify_employer,name='verify_employer'),
    path('delete_employer/<int:employer_id>', app_views.delete_employer,name='delete_employer'),
    path('employer_details/<int:employer_id>', app_views.employer_details,name='employer_details'),


    # get single jobseeker details from

    path('specific_jobseeker/<int:jobseeker_id>', app_views.single_jobseeker,name='specific_details'),
    path('employerDash/',app_views.employerDash,name='employerDash'),
    path('employer_profile/<id>',app_views.employerProfile,name='employer_profile'),
    path('update_employer/',app_views.update_employer,name='update_employer'),
    # hire
    path('hireJobseeker/',app_views.hireJobseeker,name='hireJobseeker'),
]
if settings.DEBUG:
  urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)