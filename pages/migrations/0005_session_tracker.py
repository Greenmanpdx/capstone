# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-04 22:58
from __future__ import unicode_literals

from django.db import migrations
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0004_auto_20170804_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='session',
            name='tracker',
            field=picklefield.fields.PickledObjectField(editable=False, null=True),
        ),
    ]