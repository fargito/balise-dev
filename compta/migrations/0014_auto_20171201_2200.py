# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-01 22:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compta', '0013_auto_20171201_2200'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postedepense',
            old_name='pervisionnel_credit',
            new_name='previsionnel_credit',
        ),
    ]
