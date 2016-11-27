# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-04 10:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scrumdea', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='assignedUser',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL, verbose_name='User'),
        ),
    ]