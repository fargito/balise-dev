# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-10 13:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('binets', '0013_auto_20170810_1343'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mandat',
            options={'ordering': ('binet', 'promotion')},
        ),
    ]
