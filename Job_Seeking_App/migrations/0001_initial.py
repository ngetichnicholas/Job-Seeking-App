# Generated by Django 3.2.5 on 2021-08-08 17:38

import cloudinary.models
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobSeeker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=144, null=True)),
                ('last_name', models.CharField(blank=True, max_length=144, null=True)),
                ('availability', models.CharField(choices=[('Available', 'Available'), ('Not Available', 'Not Available')], default='Available', max_length=20)),
                ('salary', models.IntegerField(default=0)),
                ('job_category', models.CharField(choices=[('IT support technician', 'IT support technician'), ('Software developer', 'Software developer'), ('Systems analyst', 'Systems analyst'), ('Computer service and repair technician', 'Computer service and repair technician'), ('Solution architect', 'Solution architect'), ('Network manager', 'Network manager')], max_length=300)),
                ('phone', models.IntegerField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=144, null=True)),
                ('bio', models.TextField(blank=True, null=True)),
                ('profile_picture', cloudinary.models.CloudinaryField(max_length=255, verbose_name='image')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('is_admin', models.BooleanField(default=False)),
                ('is_employer', models.BooleanField(default=False)),
                ('is_jobseeker', models.BooleanField(default=False)),
                ('verified', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=254)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Portfolio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('link', models.URLField(max_length=555)),
                ('jobseeker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='portfolio', to='Job_Seeking_App.jobseeker')),
            ],
            options={
                'verbose_name': 'Portfolio',
                'verbose_name_plural': 'Portfolio',
            },
        ),
        migrations.AddField(
            model_name='jobseeker',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='FileUpload',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('pdf', models.FileField(upload_to='documents/pdfs/')),
                ('jobseeker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='documents', to='Job_Seeking_App.jobseeker')),
            ],
        ),
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=144, null=True)),
                ('last_name', models.CharField(blank=True, max_length=144, null=True)),
                ('profile_picture', cloudinary.models.CloudinaryField(max_length=255, verbose_name='employer')),
                ('phone', models.IntegerField(blank=True, null=True)),
                ('location', models.CharField(blank=True, max_length=144, null=True)),
                ('company_name', models.CharField(blank=True, max_length=144, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
