# Generated by Django 3.2.5 on 2021-08-04 03:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='JobSeeker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_jobseeker', models.BooleanField(default=True)),
                ('phone', models.CharField(max_length=25)),
                ('location', models.CharField(max_length=25, null=True)),
                ('jobseeker', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Employer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_jobseeker', models.BooleanField(default=False)),
                ('phone', models.CharField(max_length=15)),
                ('location', models.CharField(max_length=25, null=True)),
                ('employer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
