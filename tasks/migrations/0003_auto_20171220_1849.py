# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-20 18:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20171220_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Envoyé'),
        ),
    ]
