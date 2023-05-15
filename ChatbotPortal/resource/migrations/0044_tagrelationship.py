# Generated by Django 2.2.6 on 2022-07-18 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('resource', '0043_auto_20220613_0934'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagRelationship',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('parent', models.IntegerField()),
                ('tag_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='resource.Tag')),
            ],
        ),
    ]
