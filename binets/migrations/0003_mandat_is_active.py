# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-31 08:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('binets', '0002_auto_20170715_0922'),
    ]

    operations = [
        migrations.AddField(
            model_name='mandat',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Actif'),
        ),
    ]