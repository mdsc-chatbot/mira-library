# Generated by Django 2.2.6 on 2021-08-02 02:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviewer_user_email', models.IntegerField(default=-1)),
                ('approved', models.BooleanField()),
                ('resource_url', models.TextField(null=True)),
                ('resource_id', models.PositiveIntegerField()),
                ('review_comments', models.TextField(default='No Comment')),
                ('review_rating', models.IntegerField(validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
            ],
        ),
    ]