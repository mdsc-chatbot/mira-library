# Generated by Django 3.2 on 2021-09-20 13:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('resource', '0029_auto_20210920_0721'),
    ]

    operations = [
        migrations.RenameField(
            model_name='resource',
            old_name='definition',
            new_name='description',
        ),
    ]