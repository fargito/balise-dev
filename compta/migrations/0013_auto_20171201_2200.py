# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-01 22:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('compta', '0012_postedepense_previsionnel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='postedepense',
            old_name='previsionnel',
            new_name='pervisionnel_credit',
        ),
        migrations.AddField(
            model_name='postedepense',
            name='previsionnel_debit',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
        migrations.AddField(
            model_name='postedepense',
            name='previsionnel_deblocages',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=9),
        ),
    ]