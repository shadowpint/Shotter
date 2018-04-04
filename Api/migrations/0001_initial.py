# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-03-17 05:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Urls',
            fields=[
                ('short_id', models.SlugField(max_length=6, primary_key=True, serialize=False)),
                ('httpurl', models.URLField()),
                ('pub_date', models.DateTimeField(auto_now=True)),
                ('count', models.IntegerField(default=0)),
            ],
        ),
    ]
