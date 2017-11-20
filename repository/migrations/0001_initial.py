# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-10-16 03:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppGroups',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='分组名称')),
                ('app_path', models.CharField(blank=True, max_length=200, null=True, verbose_name='应用路径')),
                ('config_path', models.CharField(blank=True, max_length=200, null=True, verbose_name='配置文件路径')),
            ],
            options={
                'verbose_name_plural': '应用分组表',
            },
        ),
        migrations.CreateModel(
            name='AppInstances',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP地址')),
                ('port', models.SmallIntegerField(blank=True, null=True, verbose_name='实例端口')),
                ('asset_number', models.CharField(blank=True, max_length=20, null=True, verbose_name='资产编号(CMDB)')),
                ('group_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='instances', to='repository.AppGroups')),
            ],
            options={
                'verbose_name_plural': '应用实例表',
            },
        ),
        migrations.CreateModel(
            name='Applications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('app_type', models.CharField(choices=[('java', 'java'), ('php', 'php'), ('python', 'python'), ('worker', 'worker'), ('static', 'static')], default='java', max_length=10)),
                ('leader', models.CharField(blank=True, max_length=40, null=True, verbose_name='开发leader')),
                ('members', models.CharField(blank=True, max_length=40, null=True, verbose_name='开发成员')),
            ],
            options={
                'verbose_name_plural': '应用信息表',
            },
        ),
        migrations.CreateModel(
            name='Mission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('mission_type', models.SmallIntegerField(choices=[(1, 'Update'), (2, 'Restart'), (3, 'Rollback'), (4, 'Stop')], default=1)),
                ('app_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='missions', to='repository.Applications')),
            ],
            options={
                'verbose_name_plural': '任务管理表',
            },
        ),
        migrations.CreateModel(
            name='ProjectInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('project_path', models.CharField(max_length=200, unique=True, verbose_name='系统目录')),
            ],
            options={
                'verbose_name_plural': '项目信息表',
            },
        ),
        migrations.AddField(
            model_name='applications',
            name='project_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='repository.ProjectInfo'),
        ),
        migrations.AddField(
            model_name='appgroups',
            name='app_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='repository.Applications'),
        ),
    ]
