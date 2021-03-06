# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-03 12:59
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('binets', '0004_auto_20170731_0904'),
        ('compta', '0003_auto_20170802_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postedepense',
            name='mandat',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='binets.Mandat'),
        ),
        migrations.AlterUniqueTogether(
            name='postedepense',
            unique_together=set([('nom', 'mandat')]),
        ),
    ]
