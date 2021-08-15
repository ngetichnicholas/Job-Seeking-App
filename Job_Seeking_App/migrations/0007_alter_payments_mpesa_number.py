# Generated by Django 3.2.5 on 2021-08-14 11:55

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Job_Seeking_App', '0006_alter_payments_mpesa_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='mpesa_number',
            field=models.BigIntegerField(validators=[django.core.validators.MinLengthValidator(12), django.core.validators.MaxLengthValidator(13)], verbose_name='Mpesa Phone Number'),
        ),
    ]
