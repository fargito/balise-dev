# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-24 22:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compta', '0005_auto_20170624_2224'),
    ]

    operations = [
        migrations.AddField(
            model_name='mandat',
            name='president',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='president', to='compta.Eleve'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='binet',
            name='current_president',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='current_president', to='compta.Eleve', verbose_name='Président'),
        ),
        migrations.AlterField(
            model_name='binet',
            name='current_tresorier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='current_tresorier', to='compta.Eleve', verbose_name='Trésorier'),
        ),
        migrations.AlterField(
            model_name='mandat',
            name='tresorier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tresorier', to='compta.Eleve'),
        ),
    ]
