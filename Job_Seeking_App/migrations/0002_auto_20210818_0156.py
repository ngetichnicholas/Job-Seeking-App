# Generated by Django 3.2.5 on 2021-08-17 22:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Job_Seeking_App', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobseeker',
            name='user',
        ),
        migrations.AddField(
            model_name='user',
            name='availability',
            field=models.CharField(choices=[('Available', 'Available'), ('Not Available', 'Not Available'), ('Not Applicable', 'Not Applicable')], default='Available', max_length=20),
        ),
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='company_name',
            field=models.CharField(blank=True, max_length=144, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='job_category',
            field=models.CharField(choices=[('IT support technician', 'IT support technician'), ('Software developer', 'Software developer'), ('Systems analyst', 'Systems analyst'), ('Computer service and repair technician', 'Computer service and repair technician'), ('Solution architect', 'Solution architect'), ('Network manager', 'Network manager')], default='Software developer', max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='salary',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Employer',
        ),
        migrations.DeleteModel(
            name='JobSeeker',
        ),
    ]