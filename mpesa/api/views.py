from rest_framework.generics import CreateAPIView

from rest_framework.permissions import AllowAny

from mpesa.models import Payment
from mpesa.api.serializers import MpesaSerializer


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
                'CheckoutRequestID': 'ws_CO_DMZ_401669274_11032019190235305',
                'MerchantRequestID': '19927-3244045-1',
                'ResultCode': 0,
                'ResultDesc': 'The service request is processed successfully.',
                'CallbackMetadata': {
                                        'Item': [
                                                {'Name': 'Amount', 'Value': 1.0},
                                                {'Name': 'MpesaReceiptNumber', 'Value': 'NCB1FW1DFZ'},
                                                {'Name': 'Balance'},
                                                {'Name': 'TransactionDate', 'Value': 20190311190244},
                                                {'Name': 'PhoneNumber', 'Value': 254718821114}
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
        amount = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][0][
            "Value"
        ]
        mpesa_receipt_number = request.data["Body"]["stkCallback"]["CallbackMetadata"][
            "Item"
        ][1]["Value"]

        balance = ""
        transaction_date = request.data["Body"]["stkCallback"]["CallbackMetadata"][
            "Item"
        ][3]["Value"]

        phone_number = request.data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][
            4
        ]["Value"]

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
            Balance=balance,
            TransactionDate=aware_transaction_datetime,
            PhoneNumber=phone_number,
        )

        new_transaction.save()

        from rest_framework.response import Response

        return Response({"Transaction saved to database"})