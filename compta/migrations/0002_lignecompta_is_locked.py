# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-02 18:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compta', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lignecompta',
            name='is_locked',
            field=models.BooleanField(default=False),
        ),
    ]
