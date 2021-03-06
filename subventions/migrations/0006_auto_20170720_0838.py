# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-20 08:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('compta', '0001_initial'),
        ('subventions', '0005_auto_20170717_1455'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deblocagesubvention',
            options={'ordering': ('subvention',)},
        ),
        migrations.AlterModelOptions(
            name='subvention',
            options={'ordering': ('-vague', 'mandat')},
        ),
        migrations.RemoveField(
            model_name='subvention',
            name='debloque',
        ),
        migrations.AlterUniqueTogether(
            name='deblocagesubvention',
            unique_together=set([('ligne_compta', 'subvention')]),
        ),
    ]
