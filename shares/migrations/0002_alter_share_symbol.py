# Generated by Django 3.2.11 on 2022-01-22 23:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shares', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='share',
            name='symbol',
            field=models.CharField(max_length=3, validators=[django.core.validators.MinLengthValidator(3)]),
        ),
    ]
