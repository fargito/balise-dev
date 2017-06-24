# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-24 22:24
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('compta', '0004_auto_20170624_2200'),
    ]

    operations = [
        migrations.AddField(
            model_name='binet',
            name='current_president',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='president', to='compta.Eleve', verbose_name='Président'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='binet',
            name='current_promotion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compta.Promotion', verbose_name='Promotion'),
        ),
        migrations.AlterField(
            model_name='binet',
            name='current_tresorier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tresorier', to='compta.Eleve', verbose_name='Trésorier'),
        ),
        migrations.AlterField(
            model_name='binet',
            name='description',
            field=models.TextField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='binet',
            name='is_active',
            field=models.BooleanField(verbose_name='Actif'),
        ),
        migrations.AlterField(
            model_name='binet',
            name='remarques_admins',
            field=models.TextField(blank=True, default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='binet',
            name='type_binet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='compta.TypeBinet', verbose_name='chéquier'),
        ),
    ]
