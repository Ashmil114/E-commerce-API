# Generated by Django 4.2.15 on 2024-09-04 07:52

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_alter_tb_address_alt_phone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tb_customer',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, validators=[django.core.validators.EmailValidator(message='Enter a valid email address.')]),
        ),
    ]
