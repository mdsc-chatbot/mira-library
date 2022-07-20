# Generated by Django 2.2.6 on 2022-06-13 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resource', '0042_resource_chatbot_frontend_click_more_count'),
    ]

    def create_flags(apps, schema_editor):
        RF = apps.get_model('resource', 'ResourceFlags')
        RF.objects.create(description='Some information is incorrect')
        RF.objects.create(description='Resource is unavailable')
        RF.objects.create(description='This resource should not have been approved')
        RF.objects.create(description='Other Issue')

    operations = [
        migrations.CreateModel(
            name='ResourceFlags',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('description', models.CharField(max_length=100)),
            ],
        ),
        migrations.AddField(
            model_name='resource',
            name='visible',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='resource',
            name='flags',
            field=models.ManyToManyField(blank=True, to='resource.ResourceFlags'),
        ),
        migrations.RunPython(create_flags),
    ]