# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-08-09 21:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('binets', '0011_mandat_being_checked'),
    ]

    operations = [
        migrations.AddField(
            model_name='mandat',
            name='passator',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='passator', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='mandat',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator', to=settings.AUTH_USER_MODEL),
        ),
    ]
