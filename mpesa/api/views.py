from django.shortcuts import redirect,render
from rest_framework.generics import CreateAPIView

from rest_framework.permissions import AllowAny

from mpesa.models import Payment
from mpesa.api.serializers import MpesaSerializer
from ..email import send_payment_email
from Job_Seeking_App import views
from Job_Seeking_App.email import send_verification_email
from Job_Seeking_App.models import *
from django.contrib import messages




class CallBackApiView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = MpesaSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        print(request.data, "this is request.data")

        """
        {'Body': 
            {'stkCallback': 
             {
                'MerchantRequestID': '2012-9133539-1', 
                'CheckoutRequestID': 'ws_CO_110820210205212082', 
                'ResultCode': 0, 
                'ResultDesc': 'The service request is processed successfully.', 
                'CallbackMetadata': {
                                        'Item': [
                                                {'Name': 'Amount', 'Value': 1.0}, 
                                                {'Name': 'MpesaReceiptNumber', 'Value': 'PHB2GO0BYW'}, 
                                                {'Name': 'TransactionDate', 'Value': 20210811020535}, 
                                                {'Name': 'PhoneNumber', 'Value': 254725470732}
                                                ]
                                    }
                }
            }
        }
        """
        """
        {'Body':
            {'stkCallback':
                {
                    'MerchantRequestID': '92207-59467726-1',
                    'CheckoutRequestID': 'ws_CO_160820211325367182',
                    'ResultCode': 0,
                    'ResultDesc': 'The service request is processed successfully.',
                    'CallbackMetadata': {
                                            'Item': [
                                                    {'Name': 'Amount', 'Value': 1.0},
                                                    {'Name': 'MpesaReceiptNumber', 'Value': 'PHG2O85C7G'},
                                                    {'Name': 'Balance'},
                                                    {'Name': 'TransactionDate', 'Value': 20210816132545},
                                                    {'Name': 'PhoneNumber', 'Value': 254792625077}
                                                    ]
                                        }
                }
            }
        }
        """

        if request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][2]["Name"]=='TransactionDate':

            merchant_request_id = request.data["Body"]["stkCallback"]["MerchantRequestID"]
            checkout_request_id = request.data["Body"]["stkCallback"]["CheckoutRequestID"]
            result_code = request.data["Body"]["stkCallback"]["ResultCode"]
            result_description = request.data["Body"]["stkCallback"]["ResultDesc"]
            amount = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][0]["Value"]
            mpesa_receipt_number = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][1]["Value"]
            transaction_date = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][2]["Value"]
            phone_number = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][3]["Value"]

        else:
            merchant_request_id = request.data["Body"]["stkCallback"]["MerchantRequestID"]
            checkout_request_id = request.data["Body"]["stkCallback"]["CheckoutRequestID"]
            result_code = request.data["Body"]["stkCallback"]["ResultCode"]
            result_description = request.data["Body"]["stkCallback"]["ResultDesc"]
            amount = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][0]["Value"]
            mpesa_receipt_number = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][1]["Value"]
            transaction_date = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][3]["Value"]
            phone_number = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][4]["Value"]

        from datetime import datetime

        str_transaction_date = str(transaction_date)

        transaction_datetime = datetime.strptime(str_transaction_date, "%Y%m%d%H%M%S")

        import pytz
        aware_transaction_datetime = pytz.utc.localize(transaction_datetime)


        from mpesa.models import Payment

        new_transaction = Payment.objects.create(
            CheckoutRequestID=checkout_request_id,
            MerchantRequestID=merchant_request_id,
            Amount=amount,
            ResultCode=result_code,
            ResultDesc=result_description,
            MpesaReceiptNumber=mpesa_receipt_number,
            TransactionDate=aware_transaction_datetime,
            PhoneNumber=phone_number,
        )

        new_transaction.save()
        if result_code == 0:
            employer = User.objects.get(phone = phone_number)
            email = employer.email
            name = employer.first_name
            send_payment_email(name, email)
            employer.verified = True
            employer.save()

            return redirect('employerDash')

        elif result_code is not 0:
            return redirect('employerDash')


        return render(request,'employers/employer_dashboard.html')