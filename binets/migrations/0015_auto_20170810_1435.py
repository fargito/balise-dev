# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-10 14:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('binets', '0014_auto_20170810_1347'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mandat',
            old_name='is_displayed',
            new_name='is_last',
        ),
    ]