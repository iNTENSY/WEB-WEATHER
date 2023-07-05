# Generated by Django 4.2.3 on 2023-07-04 22:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=40, verbose_name='Название города')),
                ('total_searches', models.IntegerField(default=0, verbose_name='Количество поиска')),
                ('last_search', models.DateTimeField(auto_now=True, verbose_name='Дата последнего поиска')),
            ],
            options={
                'verbose_name': 'Город',
                'verbose_name_plural': 'Города',
            },
        ),
    ]
