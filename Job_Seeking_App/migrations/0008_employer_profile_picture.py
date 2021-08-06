# Generated by Django 3.2.5 on 2021-08-06 14:09

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Job_Seeking_App', '0007_alter_fileupload_pdf'),
    ]

    operations = [
        migrations.AddField(
            model_name='employer',
            name='profile_picture',
            field=cloudinary.models.CloudinaryField(default='path', max_length=255, verbose_name='employer'),
            preserve_default=False,
        ),
    ]