import requests
from requests.auth import HTTPBasicAuth
from django.http import HttpResponse,HttpResponseRedirect,Http404,JsonResponse


from .access_token import generate_access_token
from .encode import create_password
from .utils import get_timestamp
from . import keys


def mpesa_payment(request):
    user = request.user
    phone = request.POST.get('mpesa_number')
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
        "PartyA": 254725470732,
        "PartyB": keys.business_shortCode,
        "PhoneNumber": phone,
        "CallBackURL": "https://job-seeking-app.herokuapp.com/api/payments/transaction/",
        "AccountReference": "test aware",
        "TransactionDesc": "Pay School Fees",
    }

    response = requests.post(api_url, json=request, headers=headers)

    print(response.text)

    return HttpResponse('You will receive mpesa pop up, please enter your pin')


