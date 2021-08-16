# Generated by Django 3.2.5 on 2021-08-14 11:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Job_Seeking_App', '0002_contact'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payments',
            name='mpesa_number',
            field=models.CharField(max_length=14, validators=[django.core.validators.MinLengthValidator(12)], verbose_name='Mpesa Phone Number'),
        ),
    ]
