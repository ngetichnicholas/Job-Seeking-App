# Generated by Django 3.2.5 on 2021-08-14 22:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Job_Seeking_App', '0010_alter_user_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
