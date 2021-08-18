from django.contrib import admin
from django.urls import path, include

from mpesa.api.views import CallBackApiView

urlpatterns = [
    path("transaction/", CallBackApiView.as_view(), name="transaction-callbackurl"),
    ]

