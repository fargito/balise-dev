# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-11-04 17:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compta', '0007_auto_20171104_1623'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lignecompta',
            name='reference',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
