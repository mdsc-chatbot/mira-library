# Generated by Django 3.2 on 2021-09-14 06:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resource', '0026_alter_category_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='max_age',
            field=models.IntegerField(blank=True, default=120, null=True, validators=[django.core.validators.MaxValueValidator(120), django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AddField(
            model_name='resource',
            name='min_age',
            field=models.IntegerField(blank=True, default=0, null=True, validators=[django.core.validators.MaxValueValidator(120), django.core.validators.MinValueValidator(0)]),
        ),
    ]
