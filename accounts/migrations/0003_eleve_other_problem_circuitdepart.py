# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-19 11:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_eleve_all_binets_passed'),
    ]

    operations = [
        migrations.AddField(
            model_name='eleve',
            name='other_problem_circuitdepart',
            field=models.BooleanField(default=False),
        ),
    ]
