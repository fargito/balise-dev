# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-02 22:09
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('binets', '0004_auto_20170731_0904'),
        ('compta', '0002_lignecompta_is_locked'),
    ]

    operations = [
        migrations.CreateModel(
            name='PosteDepense',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=10)),
                ('mandat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='binets.Mandat')),
            ],
            options={
                'ordering': ('nom',),
            },
        ),
        migrations.AddField(
            model_name='lignecompta',
            name='poste_depense',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='compta.PosteDepense'),
        ),
    ]