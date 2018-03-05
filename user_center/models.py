# -*- coding: utf-8 -*-
# @Time    : 1/26/2018 10:18 AM
# @Author  : Abbott
# @Site    : 
# @File    : models.py
# @Software: PyCharm

from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """
    用户信息
    """
    phone = models.CharField(u'手机', max_length=32)
    department = models.CharField(blank=True, max_length=256, null=True, verbose_name='部门')
    roles = models.ManyToManyField('Roles', related_name='user_roles')

    class Meta:
        verbose_name_plural = "用户信息"

    def __str__(self):
        return self.username


class UserGroup(models.Model):
    """
    用户组
    """
    name = models.CharField(max_length=32, unique=True)
    users = models.ManyToManyField('UserProfile', related_name='user_groups')

    class Meta:
        verbose_name_plural = "用户组表"

    def __str__(self):
        return self.name


# 访问日志记录
class AccessLogs(models.Model):
    username = models.CharField(verbose_name=u'访问用户', max_length=35, blank=True, null=False)
    create_at = models.DateTimeField(verbose_name=u'访问时间', blank=True, auto_now_add=True, null=False)
    routing = models.CharField(verbose_name=u'访问地址', max_length=200, blank=True, null=False)
    ip_address = models.GenericIPAddressField(verbose_name=u'源地址')
    # 确定是否是同一次访问，只是刷新页面而已
    cookies = models.CharField(verbose_name=u'cookies值', max_length=300, blank=True, null=False)
    browser = models.CharField(verbose_name=u'浏览器信息', max_length=250, blank=True, null=True, default='')
    system = models.CharField(verbose_name=u'客户端系统信息', max_length=250, blank=True, null=True, default='')

    class Meta:
        verbose_name = "访问日志"
        verbose_name_plural = verbose_name
        ordering = ['-create_at']

    def __unicode__(self):
        return "{0},{1},{2},{3},{4},{5}".format(self.username, self.create_at, self.routing,
                                                self.ip_address, self.browser, self.system)

    __str__ = __unicode__


class Permission(models.Model):
    """
    权限配置管理
    """
    url_name = models.CharField(max_length=150)
    url_method_choice = (
        ('GET', 'GET'),
        ('POST', 'POST'),
        ('PUT', 'PUT'),
        ('DELETE', 'DELETE'),
    )
    url_method = models.CharField(u'url请求方法', max_length=10, choices=url_method_choice, default='GET')
    memo = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name_plural = "权限配置管理"

    def __str__(self):
        return self.url_name


class Roles(models.Model):
    """
    角色配置管理
    """
    name = models.CharField(u'角色名称', max_length=32)
    permissions = models.ManyToManyField('Permission', related_name='roles_permission')
    memo = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        verbose_name_plural = "角色配置管理"

    def __str__(self):
        return self.name