# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-07 21:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_auto_20170807_2127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='npc',
            name='picture',
            field=models.ImageField(default='NoImage.jpg', upload_to=''),
        ),
        migrations.AlterField(
            model_name='pc',
            name='picture',
            field=models.ImageField(default='NoImage.jpg', upload_to=''),
        ),
    ]