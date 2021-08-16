import requests
from requests.auth import HTTPBasicAuth
from django.http import HttpResponse,HttpResponseRedirect,Http404,JsonResponse
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from Job_Seeking_App.forms import *
from Job_Seeking_App.views import *

from .access_token import generate_access_token
from .encode import create_password
from .utils import get_timestamp
from . import keys


def mpesa_payment(render_request):
    last_name = render_request.POST.get('last_name')
    first_name = render_request.POST.get('first_name')
    phone = render_request.POST.get('phone')
    phone_length = len(phone)
    if phone_length < 12:
        messages.error(render_request,'Phone number must be in format 254725470732')
        return redirect('employerDash')

    if render_request.method == 'POST':
        payment_form = PaymentForm(render_request.POST,instance=render_request.user)
        if payment_form.is_valid():
            payment_form.save()
            formatted_time = get_timestamp()
            decoded_password = create_password(formatted_time)
            access_token = generate_access_token()

            api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

            headers = {"Authorization": "Bearer %s" % access_token}

            request = {
                "BusinessShortCode": keys.business_shortCode,
                "Password": decoded_password,
                "Timestamp": formatted_time,
                "TransactionType": "CustomerPayBillOnline",
                "Amount": "1",
                "PartyA": phone,
                "PartyB": keys.business_shortCode,
                "PhoneNumber": phone,
                "CallBackURL": "https://job-seeking-app.herokuapp.com/api/payments/transaction/",
                "AccountReference": "Jobseeker Agency",
                "TransactionDesc": "This is for mpesa payment testing",
            }

            response = requests.post(api_url, json=request, headers=headers)
            print(response.text)

            return render(render_request,'mpesa/success.html',{'payment_form':payment_form,'phone':phone,'first_name':first_name,'last_name':last_name})
    else:
        payment_form = PaymentForm(instance=render_request.user)

    return render(render_request,'employers/employer_dashboard.html',{'payment_form':payment_form})


