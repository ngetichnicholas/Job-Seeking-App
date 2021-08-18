from django.urls import path

import mpesa
from . import views as app_views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from mpesa import payment

urlpatterns = [
    path('',app_views.index,name='index'),
    path('about',app_views.about,name='about'),
    path('contact',app_views.contact,name='contact'),
    path('services',app_views.services,name='services'),
    path('register/',app_views.register,name='register'),
    path('registerJobseeker/',app_views.registerJobseeker,name='registerJobseeker'),
    path('registerEmployer/',app_views.registerEmployer,name='registerEmployer'),
    path('accounts/login/',app_views.login,name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name = 'index.html'),name='logout'),
    
    path('jobseekerDash/',app_views.jobseekerDash,name='jobseekerDash'),
    path('dashboard',app_views.dashboard,name='dashboard'),
    path('upload_file',app_views.upload_file,name='upload_file'),
    path('accounts/profile/',app_views.jobseeker_profile,name='jobseeker_profile'),
    path('update_jobseeker_profile/',app_views.update_jobseeker_profile,name='update_jobseeker_profile'),

    path('admin_dashboard/',app_views.adminDash,name='admin_dashboard'),
    path('all_jobseekers',app_views.all_jobseekers,name='all_jobseekers'),
    path('verified_jobseekers',app_views.verified_jobseekers,name='verified_jobseekers'),
    path('unverified_jobseekers',app_views.unverified_jobseekers,name='unverified_jobseekers'),
    path('verify_jobseeker/<int:user_id>',app_views.verify_jobseeker,name='verify_jobseeker'),
    path('delete_jobseeker/<int:user_id>', app_views.delete_jobseeker,name='delete_jobseeker'),
    path('jobseeker_details/<int:user_id>', app_views.jobseeker_details,name='jobseeker_details'),

    path('all_employers',app_views.all_employers,name='all_employers'),
    path('verified_employers',app_views.verified_employers,name='verified_employers'),
    path('payments',app_views.payments,name='payments'),
    path('unverified_employers',app_views.unverified_employers,name='unverified_employers'),
    path('verify_employer/<int:user_id>',app_views.verify_employer,name='verify_employer'),
    path('delete_employer/<int:user_id>', app_views.delete_employer,name='delete_employer'),
    path('employer_details/<int:user_id>', app_views.employer_details,name='employer_details'),

    path('daraja/stk-push', app_views.stk_push_callback, name='mpesa_stk_push_callback'),
    path('access/token', app_views.getAccessToken, name='get_mpesa_access_token'),
    path('online/lipa', app_views.employerDash, name='mpesa_payment'),
    path('successful', app_views.success, name='success'),
    path('verify_employer',payment.mpesa_payment,name='verify_employer_payment'),

    path('all_employers',app_views.all_employers,name='all_employers'),
    path('verified_employers',app_views.verified_employers,name='verified_employers'),
    path('unverified_employers',app_views.unverified_employers,name='unverified_employers'),
    path('verify_employer/<int:employer_id>',app_views.verify_employer,name='verify_employer'),
    path('delete_employer/<int:employer_id>', app_views.delete_employer,name='delete_employer'),
    path('employer_details/<int:employer_id>', app_views.employer_details,name='employer_details'),

    path('daraja/stk-push', app_views.stk_push_callback, name='mpesa_stk_push_callback'),
    path('access/token', app_views.getAccessToken, name='get_mpesa_access_token'),
    path('online/lipa', app_views.employerDash, name='mpesa_payment'),
    path('successful', app_views.success, name='success'),
    path('verify_employer',payment.mpesa_payment,name='verify_employer_payment'),


    # get single jobseeker details from
    path('specific_jobseeker/<int:user_id>', app_views.single_jobseeker,name='specific_details'),
    path('employerDash/',app_views.employerDash,name='employerDash'),
    path('employer_profile/',app_views.employerProfile,name='employer_profile'),
    path('update_employer/',app_views.update_employer,name='update_employer'),
    path('portfolio/',app_views.add_portfolios,name='portfolio'),
    path('calender/',app_views.calender,name='calender'),
    path('search_jobseekers/', app_views.search_jobseekers, name='search_jobseekers'),
]
if settings.DEBUG:
  urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
