# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-12-25 12:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('help', '0003_auto_20171225_1221'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='helparticle',
            unique_together=set([('title',)]),
        ),
    ]