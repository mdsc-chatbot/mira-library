# Generated by Django 3.2 on 2021-08-16 16:47

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resource', '0023_auto_20210816_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='is_free',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(1), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='resource',
            name='require_membership',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MaxValueValidator(1), django.core.validators.MinValueValidator(0)]),
        ),
    ]
