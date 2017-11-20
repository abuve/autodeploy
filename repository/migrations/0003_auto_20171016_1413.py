# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-16 06:13
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0002_remove_projectinfo_project_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appgroups',
            name='config_path',
        ),
        migrations.AddField(
            model_name='appgroups',
            name='yaml_path',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='YAML配置文件路径'),
        ),
    ]
