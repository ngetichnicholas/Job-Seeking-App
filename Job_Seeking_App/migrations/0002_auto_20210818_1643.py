# Generated by Django 3.2.5 on 2021-08-18 13:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Job_Seeking_App', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='portfolio',
            options={},
        ),
        migrations.RemoveField(
            model_name='payments',
            name='mpesa_number',
        ),
    ]
