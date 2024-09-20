# Generated by Django 5.0.6 on 2024-09-20 01:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('apartments', '0001_initial'),
        ('user_profile', '0002_userprofile_favorites_apartments_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='birth_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name=('birth date',)),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='favorites_apartments',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='favorites_apartments', to='apartments.apartment'),
        ),
    ]
