from django.db import models

# Create your models here.


class Payment(models.Model):
    CheckoutRequestID = models.CharField(max_length=50, blank=True, null=True)
    MerchantRequestID = models.CharField(max_length=20, blank=True, null=True)
    ResultCode = models.IntegerField(blank=True, null=True)
    ResultDesc = models.CharField(max_length=120, blank=True, null=True)
    Amount = models.FloatField(blank=True, null=True)
    MpesaReceiptNumber = models.CharField(max_length=15, blank=True, null=True)
    Balance = models.CharField(max_length=12, blank=True, null=True)
    TransactionDate = models.DateTimeField(blank=True, null=True)
    PhoneNumber = models.CharField(max_length=13, blank=True, null=True)

    def save_payment(self):
        self.save()

    def delete_payment(self):
        self.delete()

    @classmethod
    def get_all_payments(cls):
        payments = cls.objects.all()
        return payments

    @classmethod
    def get_payment_id(cls,id):
        payment_id = cls.objects.filter(id= id).all()
        return payment_id

    def __str__(self):
        return f"{self.PhoneNumber} has sent {self.Amount} >> {self.MpesaReceiptNumber}"
