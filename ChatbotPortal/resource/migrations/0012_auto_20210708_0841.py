# Generated by Django 2.2.6 on 2021-07-08 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resource', '0011_auto_20210707_1016'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='resource',
            name='general_url',
            field=models.TextField(blank=True, null=True),
        ),
    ]
