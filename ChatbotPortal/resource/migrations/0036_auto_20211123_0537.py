# Generated by Django 3.2 on 2021-11-23 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resource', '0035_alter_resource_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='website_meta_data',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='resource',
            name='website_meta_data_updated_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
