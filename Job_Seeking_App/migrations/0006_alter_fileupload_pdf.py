# Generated by Django 3.2.5 on 2021-08-05 18:52

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Job_Seeking_App', '0005_fileupload'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileupload',
            name='pdf',
            field=cloudinary.models.CloudinaryField(max_length=255, null=True),
        ),
    ]