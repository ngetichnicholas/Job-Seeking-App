from django.contrib import admin

# Register your models here.
from mpesa.models import Payment


class PaymentAdmin(admin.ModelAdmin):
    list_display = ("PhoneNumber", "Amount", "MpesaReceiptNumber", "TransactionDate")

admin.site.register(Payment,PaymentAdmin)