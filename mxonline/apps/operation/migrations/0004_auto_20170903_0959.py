# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-09-03 09:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0003_userfavorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermessage',
            name='message',
            field=models.CharField(max_length=500, verbose_name='\u6d88\u606f\u5185\u5bb9'),
        ),
    ]