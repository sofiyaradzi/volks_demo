# Generated by Django 3.2.5 on 2021-10-28 12:32

import django.core.validators
from django.db import migrations, models
import staff.models


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='nric',
            field=models.CharField(max_length=12, validators=[django.core.validators.MinLengthValidator(12), staff.models.UserProfile.nric_check]),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(max_length=15, validators=[django.core.validators.MinLengthValidator(11), staff.models.UserProfile.phone_check]),
        ),
    ]
