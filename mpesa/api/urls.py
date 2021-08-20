from django.contrib import admin
from django.urls import path, include

from mpesa.api.views import CallBackApiView
from Job_Seeking_App import views as app_views

urlpatterns = [
    path("transaction/", CallBackApiView.as_view(), name="transaction-callbackurl"),
    path('employerDash/',app_views.employerDash,name='employerDash'),

    ]

