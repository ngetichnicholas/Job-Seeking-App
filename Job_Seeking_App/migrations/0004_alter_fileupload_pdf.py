# Generated by Django 3.2.5 on 2021-08-19 23:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Job_Seeking_App', '0003_alter_fileupload_pdf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fileupload',
            name='pdf',
            field=models.FileField(upload_to='documents/pdfs/'),
        ),
    ]
