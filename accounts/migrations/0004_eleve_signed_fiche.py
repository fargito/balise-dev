# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-19 12:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_eleve_other_problem_circuitdepart'),
    ]

    operations = [
        migrations.AddField(
            model_name='eleve',
            name='signed_fiche',
            field=models.BooleanField(default=False),
        ),
    ]
