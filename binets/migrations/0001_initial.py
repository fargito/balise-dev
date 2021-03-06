# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-07-12 18:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Binet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('remarques_admins', models.TextField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='Actif')),
                ('current_president', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='current_president', to=settings.AUTH_USER_MODEL, verbose_name='Président')),
                ('current_promotion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Promotion', verbose_name='Promo')),
                ('current_tresorier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='current_tresorier', to=settings.AUTH_USER_MODEL, verbose_name='Trésorier')),
            ],
            options={
                'ordering': ('current_promotion', 'nom'),
            },
        ),
        migrations.CreateModel(
            name='Mandat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('binet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='binets.Binet')),
                ('president', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='president', to=settings.AUTH_USER_MODEL)),
                ('promotion', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.Promotion', verbose_name='Promo')),
                ('tresorier', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tresorier', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('binet', 'promotion'),
            },
        ),
        migrations.CreateModel(
            name='TypeBinet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=30)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='typebinet',
            unique_together=set([('nom',)]),
        ),
        migrations.AddField(
            model_name='mandat',
            name='type_binet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='binets.TypeBinet', verbose_name='Type du binet'),
        ),
        migrations.AddField(
            model_name='binet',
            name='type_binet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='binets.TypeBinet', verbose_name='Type du binet'),
        ),
        migrations.AlterUniqueTogether(
            name='mandat',
            unique_together=set([('binet', 'promotion')]),
        ),
        migrations.AlterUniqueTogether(
            name='binet',
            unique_together=set([('nom',)]),
        ),
    ]
