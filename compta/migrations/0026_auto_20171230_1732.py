# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-30 17:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compta', '0025_auto_20171230_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hiddenoperation',
            name='operation_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compta.HiddenOperationType', verbose_name='Type'),
        ),
        migrations.AlterField(
            model_name='hiddenoperation',
            name='title',
            field=models.CharField(max_length=30, verbose_name='Nom'),
        ),
    ]
