# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-02 15:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0007_auto_20170902_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='learn_times',
            field=models.IntegerField(default=0, verbose_name='\u5b66\u4e60\u65f6\u957f'),
        ),
    ]