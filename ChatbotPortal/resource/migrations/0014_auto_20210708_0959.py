# Generated by Django 2.2.6 on 2021-07-08 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resource', '0013_auto_20210708_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resource',
            name='url',
            field=models.TextField(blank=True, null=True),
        ),
    ]
