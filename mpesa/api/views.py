from rest_framework.generics import CreateAPIView

from rest_framework.permissions import AllowAny

from mpesa.models import Payment
from mpesa.api.serializers import MpesaSerializer
from ..email import send_payment_email
from Job_Seeking_App.models import *



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

        merchant_request_id = request.data["Body"]["stkCallback"]["MerchantRequestID"]
        checkout_request_id = request.data["Body"]["stkCallback"]["CheckoutRequestID"]
        result_code = request.data["Body"]["stkCallback"]["ResultCode"]
        result_description = request.data["Body"]["stkCallback"]["ResultDesc"]
        amount = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][0]["Value"]
        mpesa_receipt_number = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][1]["Value"]
        # transaction_date = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][2]["Value"]
        phone_number = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][3]["Value"]

        from datetime import datetime

        # # str_transaction_date = str(transaction_date)

        # # transaction_datetime = datetime.strptime(str_transaction_date, "%Y%m%d%H%M%S")

        # import pytz
        # aware_transaction_datetime = pytz.utc.localize(transaction_datetime)


        from mpesa.models import Payment

        new_transaction = Payment.objects.create(
            CheckoutRequestID=checkout_request_id,
            MerchantRequestID=merchant_request_id,
            Amount=amount,
            ResultCode=result_code,
            ResultDesc=result_description,
            MpesaReceiptNumber=mpesa_receipt_number,
            PhoneNumber=phone_number,
        )

        new_transaction.save()
        if mpesa_receipt_number:
            employer = User.objects.get(phone = phone_number)
            email = employer.email
            name = employer.username
            send_payment_email(name, email)
            employer.verified = True
            employer.save()


        from rest_framework.response import Response

        return Response({"Transaction saved to database"})