# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-16 16:17
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_tuserprofile_address'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tuserprofile',
            name='address',
        ),
    ]