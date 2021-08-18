from django.core.mail import message
from Job_Seeking_App.views import *
from django.test import TestCase
from .models import *

# Create your tests here.

class PaymentTestClass(TestCase):
    # Set up Method
    def setUp(self):
        self.payment = Payment(id=1,CheckoutRequestID='ws_CO_160820211325367182',MerchantRequestID='92207-59467726-1',ResultCode=0,ResultDesc='The service request is processed successfully.',Amount=1.0,MpesaReceiptNumber='PHB2GO0BYW',Balance='',PhoneNumber='254725470732')
        self.payment.save()

    def test_instance(self):
        self.assertTrue(isinstance(self.payment, Payment))

    def tearDown(self):
        self.payment.delete_payment()

    def test_save_method(self):
        self.payment.save_payment()
        payments  = Payment.objects.all()
        self.assertTrue(len(payments)>0)

    def test_get_all_payments(self):
        payments = Payment.get_all_payments()
        self.assertTrue(len(payments)>0)

    def test_get_payment_id(self):
        payments= Payment.get_payment_id(self.payment.id)
        self.assertTrue(len(payments) == 1)



 
