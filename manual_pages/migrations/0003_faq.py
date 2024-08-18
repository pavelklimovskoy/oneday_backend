# Generated by Django 5.0.6 on 2024-08-12 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manual_pages', '0002_alter_cleaningchecklistitem_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Faq',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('faq_name', models.CharField(default='Название по умолчанию', max_length=120, verbose_name='Название вопроса')),
                ('faq_text', models.TextField(default='Текст часто задаваемого вопроса', max_length=1000, verbose_name='Текст вопроса')),
                ('is_visible', models.BooleanField(default=True, verbose_name='Отображать в списке')),
                ('order', models.PositiveIntegerField(db_index=True, default=0, verbose_name='order')),
            ],
            options={
                'verbose_name': 'Часто задаваемый вопрос',
                'verbose_name_plural': 'Часто задаваемые вопросы',
                'ordering': ('order',),
            },
        ),
    ]
