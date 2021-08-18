import requests
from requests.auth import HTTPBasicAuth



def generate_access_token():

    consumer_key = 'RzeH7NKGIqJQFo2GhnOYTiW2FIvIWxA2'
    consumer_secret = 'DeGC9Ecimu5xB5Rw'
    api_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"

    try:
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    except:
        r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret), verify=False)
        
    print(r.text)

    json_response = (
        r.json()
    )  

    my_access_token = json_response["access_token"]

    return my_access_token


generate_access_token()