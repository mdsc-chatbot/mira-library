# Generated by Django 3.2 on 2021-09-29 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resource', '0032_alter_resource_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='time_zone',
            field=models.CharField(default='-6 UTC', max_length=10),
        ),
        migrations.AlterField(
            model_name='resource',
            name='phone_numbers',
            field=models.TextField(blank=True, null=True),
        ),
    ]
