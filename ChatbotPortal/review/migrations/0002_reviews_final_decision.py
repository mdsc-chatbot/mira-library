# Generated by Django 3.2 on 2021-08-17 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='final_decision',
            field=models.BooleanField(blank=True, default='False', null=True),
        ),
    ]
