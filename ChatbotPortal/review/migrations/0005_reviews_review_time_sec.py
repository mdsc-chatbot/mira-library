# Generated by Django 3.2 on 2021-10-13 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0004_reviews_question_answers'),
    ]

    operations = [
        migrations.AddField(
            model_name='reviews',
            name='review_time_sec',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
