# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-03 18:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('binets', '0019_auto_20171107_2005'),
        ('compta', '0018_evenement_code'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='evenement',
            unique_together=set([('nom', 'code', 'mandat')]),
        ),
    ]