# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-18 20:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20170618_2049'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tpost',
            old_name='user',
            new_name='author',
        ),
    ]
