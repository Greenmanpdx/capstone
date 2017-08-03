# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-01 23:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_monster_number'),
    ]

    operations = [
        migrations.CreateModel(
            name='Session',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('encounter', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='pages.Encouter')),
                ('players', models.ManyToManyField(blank=True, to='pages.Character')),
            ],
        ),
    ]
