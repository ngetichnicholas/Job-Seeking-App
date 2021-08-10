from rest_framework import serializers

from mpesa.models import Payment


class MpesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("id",)

