# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-06 22:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('binets', '0008_auto_20170806_1355'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='binet',
            name='current_mandat',
        ),
    ]