# Generated by Django 5.0.6 on 2024-05-19 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analytics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookinganalytics',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
