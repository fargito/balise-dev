# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-29 20:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compta', '0023_auto_20171229_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lignecompta',
            name='poste_depense',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='compta.PosteDepense'),
        ),
    ]