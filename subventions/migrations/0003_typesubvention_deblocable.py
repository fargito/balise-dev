# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-17 12:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subventions', '0002_subvention_debloque'),
    ]

    operations = [
        migrations.AddField(
            model_name='typesubvention',
            name='deblocable',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]
