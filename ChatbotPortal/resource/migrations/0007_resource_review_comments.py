# Generated by Django 2.2.7 on 2019-11-29 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resource', '0006_resource_public_view_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='resource',
            name='review_comments',
            field=models.TextField(default='No Comment'),
        ),
    ]
